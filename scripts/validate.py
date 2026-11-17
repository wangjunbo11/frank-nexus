import pathlib,json,urllib.parse
root=pathlib.Path(__file__).resolve().parents[1]/'dist'
a=json.loads((root/'catalog.json').read_text()); assert len({x['id'] for x in a})==len(a)
for x in a:
    assert all(k in x for k in ['title','url','summary','tags','categories','status']),x
    assert urllib.parse.urlsplit(x['url']).scheme in ['http','https']
    assert x['summary'] and x['categories'] and x['tags']
for f in ['index.html','style.css','app.js','reviews.json','candidates.json']:assert (root/f).is_file()
print('PASS:',len(a),'catalog records; required assets and source links valid in structure.')

from html.parser import HTMLParser
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)
html_files=list(root.rglob('*.html'))
for path in html_files:
    text=path.read_text();parser=Links();parser.feed(text)
    assert '待核验' not in text,path
    for href in parser.links:
        link=urllib.parse.urlsplit(href)
        if link.scheme or link.netloc or not link.path:continue
        target=(path.parent/urllib.parse.unquote(link.path)).resolve()
        assert target.is_relative_to(root.resolve()),(path,href)
        assert target.exists(),(path,href)
for x in a:
    if x['id'].startswith('L'):
        assert x.get('abstract',{}).get('text') and x['abstract'].get('kind') and x['abstract'].get('source'),x['id']
        assert all(x.get('analysis',{}).get(k) for k in ('background','methods','conclusions','implications')),x['id']
    if '政策报告' in x['categories']:assert x.get('scope') in ('全球政策','国内政策'),x['id']
print('PASS:',len(html_files),'HTML pages with valid local links; literature analyses and policy scopes present.')

references=json.loads((root/'references.json').read_text());refmap={r['id']:r for r in references}
reviews=json.loads((root/'reviews.json').read_text())
sections={s['id']:s for p in reviews for c in p['chapters'] for s in c['sections']}
for sid,section in sections.items():
    assert all(r in refmap for r in section.get('referenceIds',[])),sid
    for block in section['blocks']:
        if block['type']=='paragraph':
            for r in references:assert r['text']!=block['text'],('Bibliography leaked into body',sid)
            for c in block.get('citations',[]):
                assert c['referenceId'] in section['referenceIds']
                assert sid in refmap[c['referenceId']]['usedIn']
                assert 0<=c['start']<c['end']<=len(block['text'])
for r in references:
    for sid in r['usedIn']:assert r['id'] in sections[sid]['referenceIds']
print('PASS: separated bibliography and bidirectional section citation associations.')
