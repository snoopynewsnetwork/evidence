#!/usr/bin/env python3
"""One-time catalog use: individual exact receipts and content-addressed references, not numeric inputs."""
import json,hashlib,gzip,subprocess,tempfile,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; STATE=ROOT.parents[1]
ledger=json.loads((STATE/'data/news/manifest.json').read_text())
selected=[r for r in ledger if r['id'].startswith(('sbe-','jefferson-2020','state-'))]
refs={}
for r in selected:
 p=STATE/'data/news'/r['asset']; stored=p.read_bytes(); raw=gzip.decompress(stored)
 assert hashlib.sha256(stored).hexdigest()==r['stored_sha256']
 assert hashlib.sha256(raw).hexdigest()==r['raw_sha256']
 (ROOT/'source/receipts'/f"{r['id']}.json").write_text(json.dumps(r,indent=2)+'\n')
 h=r['raw_sha256']
 refs.setdefault(h,dict(raw_sha256=h,raw_bytes=len(raw),stored_sha256=r['stored_sha256'],stored_bytes=len(stored),path=str(p.relative_to(STATE)),source_ids=[],magic=raw[:16].hex()))['source_ids'].append(r['id'])
 if raw.startswith(b'%PDF') and not (ROOT/'extracts'/f'{h}.layout.txt').exists():
  with tempfile.TemporaryDirectory(dir=ROOT) as td:
   q=Path(td)/'original.pdf';q.write_bytes(raw)
   result=subprocess.run(['pdftotext','-layout',str(q),'-'],capture_output=True,check=True)
   (ROOT/'extracts'/f'{h}.layout.txt').write_bytes(result.stdout)
   result=subprocess.run(['pdfinfo',str(q)],capture_output=True,check=True)
   (ROOT/'extracts'/f'{h}.pdfinfo.txt').write_bytes(result.stdout)
 (ROOT/'source/refs.json').write_text(json.dumps(list(refs.values()),indent=2)+'\n')
print('Pinned',len(selected),'individual receipts;',len(refs),'unique raw entities')
