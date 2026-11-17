"""Fail publication if private artifacts or recognizable credentials are exposed.
This guard supplements GitHub secret scanning; it cannot prove all data is safe.
"""
from pathlib import Path
import re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
PRIVATE={'notes.json','source-state.json','citation-audit.json'}
PATTERNS={
 'GitHub credential':re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,})'),
 'private key':re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),
 'cloud access ID':re.compile(r'\b(?:AKIA[A-Z0-9]{16}|AKID[A-Za-z0-9]{20,})\b')}
def problems(path,content):
 hits=[];p=Path(path)
 if p.name in PRIVATE or '.local' in p.parts:hits.append('private artifact')
 text=content.decode('utf-8','ignore')
 for label,pattern in PATTERNS.items():
  if pattern.search(text):hits.append(label)
 if ('/'+'Users'+'/') in text:hits.append('absolute local user path')
 return hits

def main():
 failures=[]
 if '--staged' in sys.argv:
  names=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR','-z'],cwd=ROOT).split(b'\0')
  for raw in names:
   if not raw:continue
   name=raw.decode();content=subprocess.check_output(['git','show',':'+name],cwd=ROOT)
   for problem in problems(name,content):failures.append((name,problem))
 else:
  names=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).split(b'\0')
  for raw in names:
   if not raw:continue
   name=raw.decode();p=ROOT/name
   if not p.is_file():continue
   for problem in problems(name,p.read_bytes()):failures.append((name,problem))
  for p in (ROOT/'dist').rglob('*'):
   if p.is_symlink():failures.append((str(p.relative_to(ROOT)),'symlink in publication files'))
   if p.is_file():
    for problem in problems(str(p.relative_to(ROOT)),p.read_bytes()):failures.append((str(p.relative_to(ROOT)),problem))
 if failures:
  for name,problem in sorted(set(failures)):print('BLOCKED:',name,'-',problem)
  raise SystemExit(1)
 print('PASS: no private artifacts, local user paths or recognized credentials in publication inputs.')
if __name__=='__main__':main()
