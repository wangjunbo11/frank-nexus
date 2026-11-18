"""Discover Crossref candidates. Never overwrite curated summaries."""
import json, pathlib, urllib.request, urllib.parse, datetime, hashlib, time
ROOT=pathlib.Path(__file__).resolve().parents[1]/'dist'
def publication_date(work):
    for key in ['published-online','published','published-print']:
        parts=work.get(key,{}).get('date-parts',[[]])[0]
        try:
            if parts:return datetime.date(parts[0],parts[1] if len(parts)>1 else 1,parts[2] if len(parts)>2 else 1)
        except (ValueError,TypeError):continue
    return None

def relevant_title(title):
    t=title.casefold()
    if 'nexus' in t and any(w in t for w in ['water','energy','food','climate','carbon','ecosystem','biodiversity','resource','land']):return True
    if any(w in t for w in ['climate','warming','drought']) and any(w in t for w in ['crop','agri','food','water']):return True
    return 'food security' in t or 'agrifood' in t or 'agri-food' in t

def run():
    curated=json.loads((ROOT/'catalog.json').read_text())
    candidates=json.loads((ROOT/'candidates.json').read_text())
    known={x['url'].lower().rstrip('/') for x in curated+candidates}
    today=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date()
    since_date=today-datetime.timedelta(days=45)
    since=since_date.isoformat()
    errors=[]
    journal_config=json.loads((ROOT.parent/'config/journals.json').read_text())
    priority={name.casefold() for name in journal_config['priority']}
    for query in ['water energy food nexus','climate change food security agrifood systems']:
        params=urllib.parse.urlencode({'query':query,'filter':'from-pub-date:'+since+',until-pub-date:'+today.isoformat()+',type:journal-article','sort':'published','order':'desc','rows':15})
        try:
            req=urllib.request.Request('https://api.crossref.org/works?'+params,headers={'User-Agent':'FrankNexusLibrary/1.0 (research catalog discovery)'})
            with urllib.request.urlopen(req, timeout=60) as r: works=json.load(r)['message']['items']
            for w in works:
                doi=w.get('DOI'); title=' '.join(w.get('title',[]))
                published=publication_date(w)
                if not doi or not title or not relevant_title(title) or published is None or not since_date<=published<=today: continue
                url='https://doi.org/'+doi
                if url.lower().rstrip('/') in known: continue
                known.add(url.lower().rstrip('/'))
                journal='; '.join(w.get('container-title',[]))
                candidates.append({'journalPriority':any(t.casefold() in priority for t in w.get('container-title',[])),'id':'A'+hashlib.sha256(doi.encode()).hexdigest()[:12],'title':title,'url':url,'journal':'; '.join(w.get('container-title',[])),'year':published.year,'publishedDate':published.isoformat(),'discovered':today.isoformat(),'status':'Crossref检索候选·待相关性与官网核验'})
            time.sleep(1)
        except Exception as exc: errors.append(query+': '+str(exc))
    candidates.sort(key=lambda x:(x.get('discovered',''),x.get('journalPriority',False)),reverse=True)
    (ROOT/'candidates.json').write_text(json.dumps(candidates[:300],ensure_ascii=False,indent=2)+'\n')
    (ROOT/'discovery-status.json').write_text(json.dumps({'lastAttempt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':errors,'candidateCount':len(candidates)},ensure_ascii=False,indent=2)+'\n')
    if errors: raise SystemExit('\n'.join(errors))
if __name__=='__main__':run()
