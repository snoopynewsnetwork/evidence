import gzip,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
x=json.loads(gzip.decompress((D/'full-orders.json.gz').read_bytes()));out={}
for y,s in x.items():
 out[y]={}
 for level,a in [('parish',s['order']),('native',s['native_order'])]:
  total=sum(r['votes'] for r in a);cum=0;rows=[];cut=None
  for i,r in enumerate(a,1):
   before=cum;cum+=r['votes'];rows.append(dict(r,rank=i,cumulative=cum))
   if cut is None and 5*cum>=4*total:cut=i;prior=before;cross=cum
  out[y][level]=dict(total=total,threshold=(4*total+4)//5,count=cut,previous=prior,crossing=cross,top15=sum(r['votes'] for r in a[:15]),priority_keys=[r.get('key',r.get('code')) for r in a[:cut]],full_order=rows)
out['current_canonical_dispatch']=None;out['current_canonical_units']=[];out['qualification']='Historical source-native disjoint selected-contest rows only. No November2026 identity/geometry closure or coordinator acceptance.'
p=D/'historical-priority-contract.json.gz';b=(json.dumps(out,separators=(',',':'))+'\n').encode();p.write_bytes(gzip.compress(b,mtime=0))
f=D/'priority-original-freeze.json';assert not f.exists();f.write_text(json.dumps({'scope':'Independent original-derived historical priority, before peer derivative read','source_freeze_sha256':hashlib.sha256((D/'original-freeze.json').read_bytes()).hexdigest(),'priority_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'priority_bytes':p.stat().st_size},indent=2)+'\n')
