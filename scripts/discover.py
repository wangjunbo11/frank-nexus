"""Discover Crossref candidates. Never overwrite curated summaries."""
import json, pathlib, urllib.request, urllib.parse, datetime, hashlib, time
ROOT=pathlib.Path(__file__).resolve().parents[1]/'dist'
def run():
    curated=json.loads((ROOT/'catalog.json').read_text())
    candidates=json.loads((ROOT/'candidates.json').read_text())
    known={x['url'].lower().rstrip('/') for x in curated+candidates}
    since=(datetime.date.today()-datetime.timedelta(days=45)).isoformat()
    errors=[]
    journal_config=json.loads((ROOT.parent/'config/journals.json').read_text())
    priority={name.casefold() for name in journal_config['priority']}
    for query in ['water energy food nexus','climate change food security agrifood systems']:
        params=urllib.parse.urlencode({'query':query,'filter':'from-pub-date:'+since+',type:journal-article','sort':'published','order':'desc','rows':15})
        try:
            req=urllib.request.Request('https://api.crossref.org/works?'+params,headers={'User-Agent':'FrankNexusLibrary/1.0 (research catalog discovery)'})
            with urllib.request.urlopen(req, timeout=60) as r: works=json.load(r)['message']['items']
            for w in works:
                doi=w.get('DOI'); title=' '.join(w.get('title',[]))
                if not doi or not title: continue
                url='https://doi.org/'+doi
                if url.lower().rstrip('/') in known: continue
                known.add(url.lower().rstrip('/'))
                journal='; '.join(w.get('container-title',[]))
                candidates.append({'journalPriority':any(t.casefold() in priority for t in w.get('container-title',[])),'id':'A'+hashlib.sha256(doi.encode()).hexdigest()[:12],'title':title,'url':url,'journal':'; '.join(w.get('container-title',[])),'year':w.get('published',{}).get('date-parts',[[0]])[0][0],'discovered':datetime.date.today().isoformat(),'status':'Crossref检索候选·待相关性与官网核验'})
            time.sleep(1)
        except Exception as exc: errors.append(query+': '+str(exc))
    candidates.sort(key=lambda x:(x.get('discovered',''),x.get('journalPriority',False)),reverse=True)
    (ROOT/'candidates.json').write_text(json.dumps(candidates[:300],ensure_ascii=False,indent=2)+'\n')
    (ROOT/'discovery-status.json').write_text(json.dumps({'lastAttempt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':errors,'candidateCount':len(candidates)},ensure_ascii=False,indent=2)+'\n')
    if errors: raise SystemExit('\n'.join(errors))
if __name__=='__main__':run()
