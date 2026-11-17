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
parts=json.loads((ROOT/'reviews.json').read_text()); toc='<a href="index.html">全部综述</a>'+''.join('<a href="'+p['id']+'.html">'+e(p['title'])+'</a>' for p in parts)
page(Path('reviews/index.html'),'Nexus综述', '<p class="lead">沿着理论基础、资源系统与跨系统研究，逐章建立 Nexus 分析框架。</p>'+cards(parts,'PART'),toc=toc)
for p in parts:
 page(Path('reviews/'+p['id']+'.html'),p['title'],cards(p['chapters'],'CHAPTER'),toc=toc)
 for c in p['chapters']:
  ctoc=toc+'<hr>'+''.join('<a href="'+s['id']+'.html">'+e(s['title'])+'</a>' for s in c['sections'])
  page(Path('reviews/'+c['id']+'.html'),'第'+str(c['number'])+'章 · '+c['title'],'<p class="lead">'+e(p['title'])+'</p>'+cards(c['sections'],'SECTION'),toc=ctoc)
  for i,s in enumerate(c['sections']):
   blocks=[]
   for b in s['blocks']:
    if b['type']=='paragraph':blocks.append('<p>'+e(b['text'])+'</p>')
    elif b['type']=='table':blocks.append('<div class="table-scroll"><table>'+''.join('<tr>'+''.join(('<th>' if k==0 else '<td>')+e(v)+('</th>' if k==0 else '</td>') for v in row)+'</tr>' for k,row in enumerate(b['rows']))+'</table></div>')
   page(Path('reviews/'+s['id']+'.html'),s['title'],'<a class="parent-link" href="'+c['id']+'.html">第'+str(c['number'])+'章 · '+e(c['title'])+'</a>'+''.join(blocks),toc=ctoc,prev=(c['sections'][i-1]['id']+'.html' if i else c['id']+'.html'),next=(c['sections'][i+1]['id']+'.html' if i+1<len(c['sections']) else c['id']+'.html'))
records=json.loads((ROOT/'catalog.json').read_text());literature=[x for x in records if x['id'].startswith('L')]
page(Path('literature/index.html'),'文献精读',cards(literature,'LITERATURE'),crumb='文献精读',toc='<a href="../index.html">返回资料库</a>')
for x in literature:
 analysis=x.get('analysis',{}); body='<p class="lead">'+e(x.get('journal',''))+' · '+str(x.get('year',''))+'</p>'
 for key,title in [('background','研究背景'),('methods','研究方法'),('conclusions','主要结论'),('implications','研究启示')]:body+='<section id="'+key+'"><h2>'+title+'</h2><p>'+e(analysis.get(key,''))+'</p></section>'
 body+='<p class="source-note">中文导读依据课题组研究材料整理。</p><a class="primary" href="'+e(x['url'])+'" target="_blank" rel="noopener noreferrer">阅读官方原文 ↗</a>'
 page(Path('literature/'+x['id']+'.html'),x['title'],body,crumb='文献精读',toc='<a href="../index.html">返回资料库</a>'+''.join('<a href="#'+k+'">'+t+'</a>' for k,t in [('background','研究背景'),('methods','研究方法'),('conclusions','主要结论'),('implications','研究启示')]))
print('Built',len(list((ROOT/'reviews').glob('*.html'))),'review pages and',len(literature),'literature pages')
