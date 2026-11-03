"""Bounded stable witness-body capture AFTER owned original-first freezes."""
from pathlib import Path
import json,gzip,hashlib,datetime
ROOT=Path(__file__).resolve().parents[3];B=ROOT/'data/baselines';P=ROOT/'data/turnout'
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
 assert (B/'proof/original-first-freeze-v2.json').exists()
 out=B/'peer';out.mkdir(exist_ok=True);(out/'bodies').mkdir(exist_ok=True)
 if (out/'capture.json').exists():raise SystemExit('Already captured. No live peer dependency permitted.')
 captures=[]
 for version in ['original-first','original-first-v2']:
  wp=P/'history'/version/'witness.json';wb=wp.read_bytes();w=json.loads(wb)
  if version=='original-first':assert sha(wb)=='a101f4693c6cbf1ab0f1f0a5872a26037bbe24eb43f2d30760f3861d63afdafe'
  (out/(version+'-witness.json')).write_bytes(wb)
  for r in w['bodies']:
   path=r['path']
   # Complete selected numeric/header/schema/receipt/source-role bodies only.
   selected=(path.startswith('extracts/') and not any(s in path for s in ['.layout.txt','.pdfinfo.txt','.ocr.txt'])) or path.startswith('source/receipts/') or path in ['source/refs.json','source/SCHEMA.md']
   if not selected:continue
   stored=(P/r['immutable_body']).read_bytes();raw=gzip.decompress(stored)
   assert sha(raw)==r['sha256'] and len(raw)==r['bytes']
   if 'immutable_stored_sha256' in r:assert sha(stored)==r['immutable_stored_sha256']
   assert len(stored)<40000000
   dest=out/'bodies'/(sha(raw)+'.gz')
   if not dest.exists():dest.write_bytes(stored)
   captures.append(dict(version=version,peer_path=path,raw_sha256=sha(raw),raw_bytes=len(raw),stored_sha256=sha(stored),body=str(dest.relative_to(B))))
 (out/'capture.json').write_text(json.dumps(dict(captured_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),own_gate='proof/original-first-freeze-v2.json',scope='Complete individually hashed witness bodies only; no future peer outputs or model adopted',bodies=captures),indent=2)+'\n')
 print('captured',len(captures),'stable roles')
if __name__=='__main__':main()
