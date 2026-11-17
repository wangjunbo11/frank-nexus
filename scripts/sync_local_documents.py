"""Track local source changes and import review structure and citation links.
Reads originals without modifying them. No network calls or guessed references.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,re,unicodedata,zipfile
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};W='{'+NS['w']+'}'
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(c))
def text_of(el):return ''.join(t.text or '' for t in el.findall('.//w:t',NS)).strip()
def year_of(text):
 m=re.search(r'\((\d{4}[a-z]?|n\.\s*d\.)\)\.',text)
 return m.group(1) if m else None

def is_reference(text):
 return bool(year_of(text) and (re.match(r'^[A-ZÀ-Ž][^,\n]{1,65},\s*[A-ZÀ-Ž]\.',text) or re.match(r'^Food and Agriculture Organization',text)))

def import_review(path):
 body=E.fromstring(zipfile.ZipFile(path).read('word/document.xml')).find('w:body',NS);els=list(body);texts=[text_of(e) for e in els]
 start=next((i for i,t in enumerate(texts) if re.fullmatch(r'(参考文献|References|Bibliography)',t,re.I)),None)
 if start is None:
  # Only classify a continuous bibliography suffix, not citation-bearing prose.
  tail=[i for i,t in enumerate(texts) if t]
  suffix=[]
  for i in reversed(tail):
   if is_reference(texts[i]):suffix.append(i)
   else:break
  if len(suffix)>=3:start=min(suffix)
 refs=[]
 if start is not None:
  for t in texts[start:]:
   if not is_reference(t):continue
   # Some Word paragraphs contain two references with no separating space.
   t=re.sub(r'(https?://\S+?)(?=[A-Z][a-z]+,\s*[A-Z]\.)',r'\1\n',t)
   for entry in t.split('\n'):
    year=year_of(entry)
    if not year:continue
    urlmatch=re.search(r'https?://\S+',entry);url=urlmatch.group().rstrip(' .') if urlmatch else ''
    author=entry.split('(')[0].strip().rstrip('.');surname=author.split(',')[0]
    aliases=[surname]
    if author.startswith('Food and Agriculture Organization'):aliases+=['FAO']
    key=url.lower() if url else norm(entry)
    refs.append({'id':'ref-'+hashlib.sha256(key.encode()).hexdigest()[:12],'text':entry.strip(),'author':surname,'year':year,'aliases':aliases,'url':url,'usedIn':[]})
 # De-duplicate by stable DOI/URL or complete bibliographic entry.
 refs=list({r['id']:r for r in refs}.values());parts=[];part=chapter=section=None;n=0
 for idx,el in enumerate(els[:start] if start is not None else els):
  t=text_of(el)
  if not t:continue
  if el.tag==W+'p' and re.match(r'^Part\s+[IVX\d]+\b',t,re.I):
   part={'id':'part-'+str(len(parts)+1),'title':t,'chapters':[]};parts.append(part);chapter=section=None;continue
  if part is None:continue
  style=el.find('w:pPr/w:pStyle',NS);level=el.find('w:pPr/w:numPr/w:ilvl',NS)
  is_heading=style is not None and (style.get(W+'val')=='aa' or 'heading' in style.get(W+'val','').lower())
  if is_heading and ((level is not None and level.get(W+'val')=='0') or style.get(W+'val','').lower()=='heading1'):
   n+=1;chapter={'id':'chapter-'+str(n),'title':t,'number':n,'sections':[]};part['chapters'].append(chapter);section=None;continue
  if chapter is None:continue
  if is_heading:
   section={'id':chapter['id']+'-section-'+str(len(chapter['sections'])+1),'title':t,'blocks':[]};chapter['sections'].append(section);continue
  if section is None:
   section={'id':chapter['id']+'-intro','title':'章节导读','blocks':[]};chapter['sections'].append(section)
  if el.tag==W+'tbl':section['blocks'].append({'type':'table','rows':[[''.join(x.text or '' for x in cell.findall('.//w:t',NS)) for cell in row.findall('w:tc',NS)] for row in el.findall('w:tr',NS)]})
  else:section['blocks'].append({'type':'paragraph','text':t})
 ambiguous=[];unmatched=[]
 for p in parts:
  for c in p['chapters']:
   for s in c['sections']:
    used=[]
    for block in s['blocks']:
     if block['type']!='paragraph':continue
     text=block['text'];normalized=norm(text);matches={}
     for ref in refs:
      for alias in ref['aliases']:
       pattern=r'(?<![a-zA-Z])'+re.escape(alias)+r'(?![a-zA-Z])[^。；;\n]{0,65}?[（(]\s*'+re.escape(ref['year'])+r'\s*[)）]'
       for m in re.finditer(pattern,text,re.I):matches.setdefault((m.start(),m.end()),[]).append(ref)
     citations=[]
     for (a,b),options in sorted(matches.items()):
      options=list({r['id']:r for r in options}.values())
      # Distinguish the two Wang (2026) studies using explicitly named study objects.
      if len(options)>1:
       context=norm(text)
       if '额尔齐斯' in context or 'irtysh' in context:options=[r for r in options if 'irtysh' in norm(r['text'])]
       elif any(word in context for word in ['最适温度','温度最适','适宜光合温度','光合温度最优','thermal','temperature optima']):options=[r for r in options if 'temperature optima' in norm(r['text'])]
      if len(options)!=1:
       ambiguous.append({'section':s['id'],'citation':normalized[a:b],'options':[r['id'] for r in options]});continue
      ref=options[0]
      original_match=(a,b)
      if original_match:
       citations.append({'start':original_match[0],'end':original_match[1],'referenceId':ref['id']})
       if ref['id'] not in used:used.append(ref['id'])
       if s['id'] not in ref['usedIn']:ref['usedIn'].append(s['id'])
     block['citations']=list({(v['start'],v['end'],v['referenceId']):v for v in citations}.values())
     for m in re.finditer(r'([A-ZÀ-Ž][A-Za-zÀ-žšŠćĆ-]+)(?:等|\s+et al\.?|和[^（(]{1,25})?\s*[（(](\d{4}[a-z]?)[)）]',text):
      if not any(v['start']<=m.start()<v['end'] for v in citations):unmatched.append({'section':s['id'],'citation':m.group()})
    s['referenceIds']=used
 audit={'source':path.name,'referenceCount':len(refs),'linkedReferences':sum(bool(r['usedIn']) for r in refs),'ambiguous':ambiguous,'unmatched':unmatched,'unlinkedReferenceIds':[r['id'] for r in refs if not r['usedIn']]}
 return parts,refs,audit

def sync(source_root,force=False):
 state_path=ROOT/'source-state.json';old=json.loads(state_path.read_text()) if state_path.exists() else {'files':{}}
 files={}
 for p in sorted(source_root.rglob('*')):
  if not p.is_file() or ROOT in p.parents or p.name.startswith('~$') or p.suffix.lower() not in ['.docx','.xlsx','.pdf','.csv','.dta','.do']:continue
  st=p.stat();files[str(p.relative_to(source_root))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':st.st_size,'mtimeNs':st.st_mtime_ns}
 changed=[k for k,v in files.items() if old.get('files',{}).get(k,{}).get('sha256')!=v['sha256']]
 removed=[k for k in old.get('files',{}) if k not in files]
 name='Nexus研究.docx'
 if name in files and (force or name in changed):
  parts,refs,audit=import_review(source_root/name)
  for filename,obj in [('reviews.json',parts),('references.json',refs),('citation-audit.json',audit)]:
   (DIST/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 # Keep non-review changes pending until the scheduled agent has reconciled them.
 pending=sorted(set(old.get('pendingFiles',[])+[k for k in changed if k!=name]))
 state={'sourceRootLabel':source_root.name,'files':files,'pendingFiles':pending,'removedFiles':removed}
 state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'changed':changed,'pending':pending,'removed':removed},ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,default=ROOT.parent);p.add_argument('--force',action='store_true');a=p.parse_args();sync(a.source_root.resolve(),a.force)
