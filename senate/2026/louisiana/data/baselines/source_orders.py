"""Full historical source orders from own frozen extracts only, no peer files."""
import csv,gzip,json
from pathlib import Path
D=Path(__file__).resolve().parent;C=json.load(open(D/'controls.json'));P=list(csv.DictReader((D/'parish-controls.csv').open()));N=json.loads(gzip.decompress((D/'native-results.json.gz').read_bytes()));out={}
for y in C:
 n=[r for r in N if r['year']==y];p=[r for r in P if r['year']==y]
 fields={'votes':'all_candidate_votes','qualified':'stats_qualified','voted':'stats_voted','race_qualified':'qualified','race_voted':'voted'}
 for field in [*fields,'early_votes','ordinary_votes','provisional_votes']:
  rows=[]
  for a in p:
   if field in fields:v=int(a[fields[field]])
   else:v=sum(r['all_candidate_votes'] for r in n if r['parish_code']==a['parish_code'] and r['type']=={'early_votes':'early-aggregate','ordinary_votes':'ward-precinct','provisional_votes':'provisional-aggregate'}[field])
   rows.append(dict(key='LA:'+a['parish_code'],parish=a['parish'],votes=v))
  out[y+'-parish-'+field]=rows
 out[y+'-native-votes']=[dict(key=json.dumps([y,C[y]['race_id'],a['parish_code'],a['ward'],a['precinct']],separators=(',',':')),own_key=a['key'],parish=a['parish'],votes=a['all_candidate_votes']) for a in n]
for k,rows in list(out.items()):
 rows.sort(key=lambda a:(-a['votes'],a['key']));T=sum(a['votes'] for a in rows);cum=0;cut=None
 for i,a in enumerate(rows,1):
  prev=cum;cum+=a['votes'];a.update(rank=i,cumulative_votes=cum,share_numerator=a['votes'],share_denominator=T)
  if cut is None and 5*cum>=4*T:cut=i;prior=prev;cross=cum
 out[k]=dict(total=T,minimum80_count=cut,threshold=(4*T+4)//5,previous=prior,crossing=cross,full_order=rows)
(D/'all-source-orders.json.gz').write_bytes(gzip.compress((json.dumps(out,separators=(',',':'))+'\n').encode(),mtime=0));print('Full orders',len(out))
