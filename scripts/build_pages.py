"""Build independently linkable review and literature pages from curated JSON."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]/'dist'
def e(s):return html.escape(str(s or ''))
def page(path,title,body,crumb='Nexus综述',toc='',prev='',next=''):
 path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
 nav=('<a href="'+prev+'">← 上一篇</a>' if prev else '<span></span>')+('<a href="'+next+'">下一篇 →</a>' if next else '<a href="index.html">返回目录 ↑</a>')
 path.write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+' · Frank Nexus资料库</title><link rel="stylesheet" href="../style.css"></head><body class="document-page"><header class="doc-header"><a href="../index.html">Frank Nexus资料库</a><a href="index.html">'+e(crumb)+'</a></header><div class="document-layout"><nav class="document-toc" aria-label="本页目录">'+toc+'</nav><article class="document"><p class="eyebrow">FRANK NEXUS / '+e(crumb)+'</p><h1>'+e(title)+'</h1>'+body+'<div class="page-neighbors">'+nav+'</div></article></div></body></html>')
def cards(nodes,caption):return '<div class="review-links">'+''.join('<a href="'+e(n['id'])+'.html"><small>'+e(caption)+'</small><strong>'+e(n['title'])+'</strong><span>进入阅读 ↗</span></a>' for n in nodes)+'</div>'
references=json.loads((ROOT/'references.json').read_text()) if (ROOT/'references.json').exists() else []
refmap={r['id']:r for r in references}
def reference_html(r,backlinks=False):
 text=e(r['text'])
 if r.get('url'):text+=' <a href="'+e(r['url'])+'" target="_blank" rel="noopener noreferrer">官方来源 ↗</a>'
 if backlinks and r.get('usedIn'):text+='<div class="reference-backlinks">引用位置：'+''.join('<a href="'+sid+'.html#'+r['id']+'">'+e(section_titles.get(sid,sid))+'</a> ' for sid in r['usedIn'])+'</div>'
 return '<li id="'+r['id']+'">'+text+'</li>'
def paragraph_html(block):
 text=block['text'];output=[];cursor=0
 for citation in sorted(block.get('citations',[]),key=lambda c:c['start']):
  a,b=citation['start'],citation['end']
  if a<cursor or citation['referenceId'] not in refmap:continue
  output.append(e(text[cursor:a]));output.append('<a class="citation" href="#'+citation['referenceId']+'">'+e(text[a:b])+'</a>');cursor=b
 output.append(e(text[cursor:]));return '<p>'+''.join(output)+'</p>'
parts=json.loads((ROOT/'reviews.json').read_text()); toc='<a href="index.html">全部综述</a>'+''.join('<a href="'+p['id']+'.html">'+e(p['title'])+'</a>' for p in parts)+'<a href="references.html">参考文献总表</a>'
page(Path('reviews/index.html'),'Nexus综述', '<p class="lead">沿着理论基础、资源系统与跨系统研究，逐章建立 Nexus 分析框架。</p>'+cards(parts,'PART')+'<p><a href="references.html">查看参考文献总表 ↗</a></p>',toc=toc)
section_titles={s['id']:s['title'] for p in parts for c in p['chapters'] for s in c['sections']}
page(Path('reviews/references.html'),'参考文献', '<p class="lead">综述文末书目集中展示；点击引用位置返回对应小节。</p><ol class="reference-list">'+''.join(reference_html(r,True) for r in references)+'</ol>',toc=toc)
for p in parts:
 page(Path('reviews/'+p['id']+'.html'),p['title'],cards(p['chapters'],'CHAPTER'),toc=toc)
 for c in p['chapters']:
  ctoc=toc+'<hr>'+''.join('<a href="'+s['id']+'.html">'+e(s['title'])+'</a>' for s in c['sections'])
  page(Path('reviews/'+c['id']+'.html'),'第'+str(c['number'])+'章 · '+c['title'],'<p class="lead">'+e(p['title'])+'</p>'+cards(c['sections'],'SECTION'),toc=ctoc)
  for i,s in enumerate(c['sections']):
   blocks=[]
   for b in s['blocks']:
    if b['type']=='paragraph':blocks.append(paragraph_html(b))
    elif b['type']=='table':blocks.append('<div class="table-scroll"><table>'+''.join('<tr>'+''.join(('<th>' if k==0 else '<td>')+e(v)+('</th>' if k==0 else '</td>') for v in row)+'</tr>' for k,row in enumerate(b['rows']))+'</table></div>')
   if s.get('referenceIds'):blocks.append('<section class="section-references"><h2>本节参考文献</h2><ol class="reference-list">'+''.join(reference_html(refmap[r]) for r in s['referenceIds'] if r in refmap)+'</ol><a href="references.html">查看全部参考文献 ↗</a></section>')
   page(Path('reviews/'+s['id']+'.html'),s['title'],'<a class="parent-link" href="'+c['id']+'.html">第'+str(c['number'])+'章 · '+e(c['title'])+'</a>'+''.join(blocks),toc=ctoc,prev=(c['sections'][i-1]['id']+'.html' if i else c['id']+'.html'),next=(c['sections'][i+1]['id']+'.html' if i+1<len(c['sections']) else c['id']+'.html'))
records=json.loads((ROOT/'catalog.json').read_text());literature=[x for x in records if x['id'].startswith('L')]
page(Path('literature/index.html'),'文献精读',cards(literature,'LITERATURE'),crumb='文献精读',toc='<a href="../index.html">返回资料库</a>')
for x in literature:
 analysis=x.get('analysis',{}); body='<p class="lead">'+e(x.get('journal',''))+' · '+str(x.get('year',''))+'</p>'
 if x.get('abstract',{}).get('text'):body+='<section id="abstract"><h2>摘要 · '+e(x['abstract'].get('kind','中文概述'))+'</h2><p>'+e(x['abstract']['text'])+'</p></section>'
 for key,title in [('background','研究背景'),('methods','研究方法'),('conclusions','主要结论'),('implications','研究启示')]:body+='<section id="'+key+'"><h2>'+title+'</h2><p>'+e(analysis.get(key,''))+'</p></section>'
 body+='<p class="source-note">中文导读依据研究材料整理。</p><a class="primary" href="'+e(x['url'])+'" target="_blank" rel="noopener noreferrer">阅读官方原文 ↗</a>'
 page(Path('literature/'+x['id']+'.html'),x['title'],body,crumb='文献精读',toc='<a href="../index.html">返回资料库</a>'+''.join('<a href="#'+k+'">'+t+'</a>' for k,t in [('background','研究背景'),('methods','研究方法'),('conclusions','主要结论'),('implications','研究启示')]))
print('Built',len(list((ROOT/'reviews').glob('*.html'))),'review pages and',len(literature),'literature pages')
