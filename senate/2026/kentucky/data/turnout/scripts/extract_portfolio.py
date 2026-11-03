#!/usr/bin/env python3
"""Full original PDF text bodies and source metadata, no numerical derivatives."""
import json,gzip,subprocess,tempfile,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
summary=[]
for f in sorted((ROOT/'source/receipts').glob('*.json')):
 r=json.loads(f.read_text())
 if not r.get('hops'):continue
 hop=r['hops'][-1];p=ROOT/hop['body'];b=gzip.decompress(p.read_bytes());assert hashlib.sha256(b).hexdigest()==hop['raw_sha256']
 if not b.startswith(b'%PDF'):continue
 h=hop['raw_sha256'];out=ROOT/'extracts'/f'{h}.layout.txt';info=ROOT/'extracts'/f'{h}.pdfinfo.txt'
 if not out.exists():
  with tempfile.TemporaryDirectory(dir=ROOT) as td:
   q=Path(td)/'original.pdf';q.write_bytes(b)
   z=subprocess.run(['pdftotext','-layout',str(q),'-'],capture_output=True)
   if z.returncode: (ROOT/'history'/f'{h}.pdftotext-error.txt').write_bytes(z.stderr);continue
   out.write_bytes(z.stdout)
   z=subprocess.run(['pdfinfo',str(q)],capture_output=True);info.write_bytes(z.stdout)
 t=out.read_text();summary.append({'receipt':f.name,'role':r['role'],'source_sha256':h,'pages':t.count('\f'),'text_bytes':out.stat().st_size,'text_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'has_choice': 'Choice' in t,'has_summary':'Precinct Summary Results Report' in t,'text_excerpt':t[:100]})
(ROOT/'extracts/portfolio.json').write_text(json.dumps(summary,indent=2)+'\n')
for x in summary:print(x['role'],x['pages'],x['text_bytes'],flush=True)
