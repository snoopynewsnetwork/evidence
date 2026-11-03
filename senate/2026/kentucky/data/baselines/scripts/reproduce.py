"""Read-only production inputs, isolated temporary replay, no retained dependency/cache tree."""
from pathlib import Path
import json,gzip,hashlib,subprocess,tempfile,shutil,sys,os
B=Path(__file__).resolve().parents[1];ROOT=B.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 pins=json.loads((B/'source/pins.json').read_text())['pins'];checks=[]
 with tempfile.TemporaryDirectory(prefix='ky-partisanship-replay-') as td:
  root=Path(td)/'kentucky';out=root/'data/baselines'
  for d in ['source','extracted','proof','scripts','fixtures']: (out/d).mkdir(parents=True,exist_ok=True)
  for f in (B/'scripts').glob('*.py'):shutil.copyfile(f,out/'scripts'/f.name)
  for name in ['source/pins.json','extracted/document-inventory.json','extracted/elliott-manual.json']:shutil.copyfile(B/name,out/name)
  done=set()
  print('Verifying individual original pins and extracting all133PDFs',flush=True)
  for p in pins:
   stored=(ROOT/p['path']).read_bytes();raw=gzip.decompress(stored)
   assert sha(stored)==p['stored_sha256'] and sha(raw)==p['raw_sha256'] and len(raw)==p['raw_bytes']
   if p['raw_sha256'] in done:continue
   done.add(p['raw_sha256'])
   # Only this exact body/hash is read. Full source text freshly extracted.
   if raw.startswith(b'%PDF'):
    result=subprocess.run(['pdftotext','-layout','-','-'],input=raw,capture_output=True,check=True)
    target=out/'extracted'/f"{p['raw_sha256']}.layout.txt.gz";target.write_bytes(gzip.compress(result.stdout,mtime=0))
    assert gzip.decompress((B/'extracted'/target.name).read_bytes())==result.stdout
    checks.append(dict(source_sha256=p['raw_sha256'],fresh_full_layout_sha256=sha(result.stdout),passed=True))
   if p['role']=='2024 Census county FIPS identity only':
    dest=root/p['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.symlink_to((ROOT/p['path']).resolve())
  for year in [2024,2022,2020]:
   p=next(p for p in pins if p['role'] and p['role'].startswith(f'sbe-{year}-archive-'))
   shutil.copyfile(out/'extracted'/f"{p['raw_sha256']}.layout.txt.gz",out/'extracted'/f'{year}-full-layout.txt.gz')
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  for name in ['extract_certificates.py','extract_native.py','native_quantities.py','extract_admin.py','build.py','source_reconciliation.py','validate_calculator.py']:
   print('Isolated replay:',name,flush=True)
   r=subprocess.run([sys.executable,str(out/'scripts'/name)],capture_output=True,text=True,env=env)
   assert r.returncode==0,(name,r.stdout,r.stderr)
  names=['certificate-fields.csv','certificate-headers.json','candidates.json','certificate-controls.json','native-observations.jsonl.gz','native-page-contexts.jsonl.gz','native-coverage.json','native-positional-fields.jsonl.gz','native-known-pair-units.json','native-unresolved-pair-contexts.json','county-admin-turnout.csv','county-registration.csv','admin-controls.json','turnout-registration-positioned-controls.jsonl.gz']
  outputs=[Path('extracted')/n for n in names]+[Path(n) for n in ['county-order.csv','priority.json','state-scenarios.json','county-targets.csv','native-known-subset-targets.csv','native-subset-scope.json','source-reconciliation.csv']]+[p.relative_to(B) for p in (B/'scenarios').glob('*.json')]
  outputs.append(Path('../county-baselines.csv'))
  for rel in outputs:
   a=(B/rel).read_bytes();z=(out/rel).read_bytes();assert a==z,rel
   checks.append(dict(output=str(rel),sha256=sha(a),bytes=len(a),passed=True))
 result=dict(status='passed',method='All individually pinned original hashes verified;133fresh whole-PDF positioned-layout extracts equal retained text; isolated replay of own extraction/build/CLI checks; exact output-byte comparisons; temp tree removed',checks=checks)
 (B/'proof/reproduction.json').write_text(json.dumps(result,indent=2)+'\n');print('reproduction passed',len(checks),'source/output checks')
if __name__=='__main__':main()
