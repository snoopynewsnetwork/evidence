"""Offline replay in isolated temporary mirror; final owned artifacts remain read-only."""
import gzip,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[4];H=lambda b:hashlib.sha256(b).hexdigest();freeze=json.load(open(D/'original-freeze.json'));results=[]
with tempfile.TemporaryDirectory(prefix='la-baselines-replay-') as t:
 root=Path(t);dest=root/'senate/2026/louisiana/data/baselines';dest.mkdir(parents=True)
 for a in freeze['assets']:
  src=D/a['path'];b=src.read_bytes();assert H(b)==a['sha256'] and len(b)==a['bytes'];p=dest/a['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 for r in json.load(open(D/'source/receipts.json')):
  src=ROOT/r['reference_path'];b=src.read_bytes();assert H(b)==r['stored_sha256'];p=root/r['reference_path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 r=subprocess.run([sys.executable,'-B',str(dest/'extract.py')],capture_output=True,text=True);assert r.returncode==0,r.stderr
 for name in ['controls.json','candidates.csv','parish-controls.csv','native-results.json.gz','native-coverage.json','full-orders.json.gz','source/json-position-witness.json.gz','source/workbook-position-witness.json.gz',*[f'source/{y}-{k}-csv-positions.json.gz' for y in ['2024','2022','2020'] for k in ['parish','precinct']]]:
  a=(D/name).read_bytes();b=(dest/name).read_bytes();assert a==b,name;results.append(dict(path=name,bytes=len(b),sha256=H(b)))
 # Rebuild whole-state scenarios from replayed originals, independently of peer/news ledger.
 for name in ['build.py','calculator.py']:shutil.copyfile(D/name,dest/name)
 r=subprocess.run([sys.executable,'-B',str(dest/'build.py')],capture_output=True,text=True);assert r.returncode==0,r.stderr
 for p in [D.parent/'county-baselines.csv',D/'state-scenarios.csv',D/'all-unit-scenarios.json.gz',D/'native-baselines.json.gz',*sorted((D/'scenarios').glob('*'))]:
  rel=p.relative_to(D.parent);replayed=dest.parent/rel;assert p.read_bytes()==replayed.read_bytes(),str(rel);results.append(dict(path=str(rel),bytes=p.stat().st_size,sha256=H(p.read_bytes())))
print(json.dumps({'passed':True,'offline_exact_reproductions':len(results),'results':results},indent=2))
