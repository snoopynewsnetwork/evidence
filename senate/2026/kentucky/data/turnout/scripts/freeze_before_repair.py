#!/usr/bin/env python3
"""Preserve every current owned body before narrow repairs, referencing original byhash bodies/history without duplicate originals."""
import json,gzip,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R.parents[1];D=R/'history'/sys.argv[1];D.mkdir(exist_ok=False);(D/'bodies').mkdir();out=[]
files=sorted([S/'turnout.md',S/'data/county-turnout.csv']+[p for p in R.rglob('*') if p.is_file() and D not in p.parents])
for p in files:
 b=p.read_bytes();h=hashlib.sha256(b).hexdigest();rel=p.relative_to(S);entry={'path':str(rel),'bytes':len(b),'sha256':h}
 if ('source/bodies/' in str(rel) or 'history/' in str(rel)):
  entry['immutable_existing_body_reference']=str(rel)
 else:
  q=D/'bodies'/f'{h}.gz'
  if not q.exists():q.write_bytes(gzip.compress(b,mtime=0))
  entry['frozen_body']=str(q.relative_to(S));entry['frozen_sha256']=hashlib.sha256(q.read_bytes()).hexdigest();assert q.stat().st_size<40000000
 out.append(entry)
(D/'witness.json').write_text(json.dumps({'reason':sys.argv[2] if len(sys.argv)>2 else None,'files':out,'original_source_bytes_modified':False,'peer_numerical_inputs':False},indent=2)+'\n');print('full prior owned membership/body freeze',len(out))
