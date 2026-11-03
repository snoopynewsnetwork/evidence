#!/usr/bin/env python3
"""Immutable body witness before opening any peer/coordinator numerical derivative."""
import json,gzip,hashlib,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'history/original-first-v3';D.mkdir(parents=True,exist_ok=False);(D/'bodies').mkdir()
rows=[]
for folder in ['scripts','extracts','source/receipts']:
 for p in sorted((R/folder).rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts:continue
  b=p.read_bytes();h=hashlib.sha256(b).hexdigest();q=D/'bodies'/f'{h}.gz'
  if not q.exists():q.write_bytes(gzip.compress(b,mtime=0))
  assert q.stat().st_size<40000000
  rows.append({'path':str(p.relative_to(R)),'sha256':h,'bytes':len(b),'immutable_body':str(q.relative_to(R)),'immutable_stored_sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
for p in [R/'source/SCHEMA.md',R/'source/refs.json',R/'source/acquisition-plan.json']:
 b=p.read_bytes();h=hashlib.sha256(b).hexdigest();q=D/'bodies'/f'{h}.gz';q.write_bytes(gzip.compress(b,mtime=0));rows.append({'path':str(p.relative_to(R)),'sha256':h,'bytes':len(b),'immutable_body':str(q.relative_to(R))})
# Acquired full raw sources are already byhash immutable; reference without duplicating huge originals.
sources=[]
for p in sorted((R/'source/bodies').glob('*.gz')):
 b=p.read_bytes();raw=gzip.decompress(b);sources.append({'path':str(p.relative_to(R)),'stored_sha256':hashlib.sha256(b).hexdigest(),'stored_bytes':len(b),'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw)})
w={'freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gate':'Independent originals only; no coordinator numerical JSON/table/parser or peer derivatives opened','peer_agent_id':'ce1620b8-8df0-406b-bdb1-a8522aeea2f4','peer_existence_evidence':'user coordinator informational message in this session; agreement unknown','bodies':rows,'owned_originals':sources,'shared_original_pins':json.load(open(R/'source/refs.json')),'native_limitations':['Scott county cumulative only; exact archive same source scope','Magoffin Mail In only','source candidate/write-in universe differences and small Fayette/Whitley certificate discrepancies retained'],'reconciliation_source':'own original certificate/footer/native positional scripts only'}
p=D/'witness.json';p.write_text(json.dumps(w,indent=2)+'\n');print(p,hashlib.sha256(p.read_bytes()).hexdigest(),len(rows),len(sources))
