"""Independent source-weight audit and exact-rational affine clipping roots."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as Q
import csv,gzip,json,math,re,sys
S=Path(__file__).resolve().parents[1];B=S/'data/baselines';N=0;maxdiff=0.;maxres=0.
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
def load(p):return json.loads(p.read_bytes())
def close(a,b,tol=2e-6):ck(a is not None and math.isfinite(float(a)) and abs(float(a)-float(b))<=tol,('numeric',a,float(b),tol))
def f(x):return Q(str(x))
def root(units,goal):
 events=defaultdict(Q);pool=Q(0)
 for w,q in units:
  pool+=w
  if w:events[-q]+=2*w;events[1-q]-=2*w
 last=Q(-1);net=-pool;slope=Q(0)
 for x in sorted(events):
  at=net+slope*(x-last)
  if slope and net<=goal<=at:return last+(goal-net)/slope
  last=x;net=at;slope+=events[x]
 if goal==pool:return Q(1)
 raise AssertionError('no feasible exact affine segment')
original=load(S/'data/coordinator-first-pair-original-review.json');ck(original['status']=='pass' and original['checks']==1358198)
fields=list(csv.DictReader((B/'extracted/certificate-fields.csv').open()));vectors=defaultdict(dict)
for r in fields:
 if r['scope']=='county':vectors[int(r['year']),r['county_literal']][int(r['column'])]=int(r['votes'])
county={};allcounty=list(csv.DictReader((S/'data/county-baselines.csv').open()))
for r in allcounty:
 v=vectors[int(r['year']),r['county_literal']];cv=[v[i] for i in range(1,len(v)+1)]
 ck(json.loads(r['candidate_vector'])==cv and int(r['A'])==cv[1] and int(r['B'])==cv[0] and int(r['pair'])==sum(cv[:2]) and int(r['all'])==sum(cv) and int(r['other'])==sum(cv[2:]))
 ck(r['registration']==r['ballots_cast']=='');county[int(r['year']),r['fips']]={**r,'vector':cv}
ck(len(county)==360 and all(sum(int(r['all']) for (y,k),r in county.items() if y==yr)==total for yr,total in [(2024,2074530),(2022,1477830),(2020,2135057)]))
known=load(B/'extracted/native-known-pair-units.json')+load(B/'extracted/elliott-manual.json');positive={r['key']:r for r in known if r['pair']>0};zero=[r for r in known if r['pair']==0]
ck(len(known)==3150 and len(positive)==3127 and len(zero)==23 and all(r['A_pair_share'] is None for r in zero))
for r in known:
 ck(r['pair']==r['A']+r['B']<=r['all_candidate_printed_total'] and r['full_named_field_closure'] is False and r['native_geographic_equivalence_2026'] is None)
source_rows={r['observation_key']:r for r in [json.loads(v) for v in gzip.decompress((B/'extracted/native-observations.jsonl.gz').read_bytes()).splitlines()]}
for r in known:
 if 'A_row' not in r:continue
 for candidate,key in [('A','A_row'),('B','B_row')]:
  row=source_rows[r[key]];ck(row['source_sha256']==r['source_sha256'] and row['county']==r['county'] and row['unit_literal']==r['unit_literal'])
  # Source TOTAL is last in literal Choice headers; first in summary tables.
  text=gzip.decompress((B/'extracted'/f"{r['source_sha256']}.layout.txt.gz").read_bytes()).decode().split('\f')[row['page']-1]
  tokens=[int(m.group().replace(',','')) for m in re.finditer(r'(?<!\S)\d[\d,]*(?!\S)',row['raw'])]
  value=tokens[-1] if re.search(r'^\s*Choice\s',text,re.M) else tokens[0]
  ck(value==r[candidate],('native source TOTAL position',r['key'],candidate))
proofs=[];target_rows=0
for p in sorted((B/'scenarios').glob('*.input.json')):
 x=load(p);o=load(p.with_name(p.name.replace('.input.','.result.')));native=p.name.startswith('native-known-subset');source={};m=re.fullmatch(r'county-anchor(2020|2022|2024)-mix(2020|2022|2024)-margin(0|0\.01)\.input\.json',p.name)
 if native:
  ck({r['key'] for r in x['units']}==set(positive) and x['other_scope']=='unresolved')
  for k,r in positive.items():source[k]={'A':r['A'],'B':r['B'],'full':r['all_candidate_printed_total'],'volume':r['all_candidate_printed_total'],'others':None}
 else:
  ck(m is not None);anchor,mix=int(m[1]),int(m[2]);ck(len(x['units'])==120 and {u['key'] for u in x['units']}=={k for y,k in county if y==anchor})
  for (yr,k),r in county.items():
   if yr==anchor:source[k]={'A':r['vector'][1],'B':r['vector'][0],'full':sum(r['vector']),'volume':int(county[mix,k]['all']),'others':r['vector'][2:]}
  sample=next(r for (yr,k),r in county.items() if yr==anchor);ck(x['pair']==[sample['A_identity'],sample['B_identity']] and x['other_scope']=='named')
 tuples=[]
 for u in x['units']:
  r=source[u['key']];a,b,full=r['A'],r['B'],r['full'];pair=a+b;ck(u['remaining']==r['volume'] and u['counted']=={'A':0,'B':0,'other':{c:0 for c in x['others']}})
  close(u['participation'],Q(pair,full),1e-12);close(u['share'],Q(a,pair),1e-12);ck(set(u['other_allocation'])==set(x['others']))
  if r['others'] is not None:
   ck(len(r['others'])==len(x['others']))
   if full>pair:
    for c,v in zip(x['others'],r['others']):close(u['other_allocation'][c],Q(v,full-pair),1e-12)
  pool=f(u['remaining'])*f(u['participation']);tuples.append((f(u['remaining']),pool,f(u['share'])))
 F=sum(w for v,w,q in tuples);full=sum(v for v,w,q in tuples);net=sum(w*(2*q-1) for v,w,q in tuples);goal=f(x['target'])*F;d=root([(w,q) for v,w,q in tuples],goal);unbounded=(goal-net)/(2*F)
 ck(o['status']=='ok' and [u['key'] for u in x['units']]==[u['key'] for u in o['units']]);close(o['final_pair_denominator'],F);close(o['final_all_candidate_denominator'],full);close(o['baseline_final_pair_net'],net);close(o['uniform']['clipped_share_shift'],d,1e-12);close(o['uniform']['unbounded_share_shift'],unbounded,1e-12)
 achieved=Q(0)
 for u,z,(v,w,q) in zip(x['units'],o['units'],tuples):
  share=max(Q(0),min(Q(1),q+d));old=w*(2*q-1);new=w*(2*share-1);achieved+=new
  close(z['pair_weight'],w/F,1e-12);close(z['target_A_share'],share,1e-12);close(z['target_pair_net_contribution'],new);close(z['baseline_pair_net_contribution'],old);close(z['net_gain'],new-old);close(z['one_A_share_point_net_votes'],w/50)
 ck(achieved==goal,'exact-rational affine root residual zero')
 target_file=B/('native-known-subset-targets.csv' if native else 'county-targets.csv');csvrows=[r for r in csv.DictReader(target_file.open()) if r['scenario']==p.name.removesuffix('.input.json')];ck(len(csvrows)==len(tuples))
 for z,(v,w,q),u in zip(csvrows,tuples,x['units']):
  ck(z['key' if native else 'fips']==u['key']);old=w*(2*q-1);required=(goal-(net-old)+w)/(2*w)
  close(z['selected_only_required_A_share'],required,1e-9);ck(z['selected_only_status']==('impossible' if required>1 else 'secured' if required<0 else 'feasible'))
 maxdiff=max(maxdiff,abs(float(d)-o['uniform']['clipped_share_shift']));maxres=max(maxres,abs(float(goal)-math.fsum(z['target_pair_net_contribution'] for z in o['units'])));target_rows+=len(tuples)
 proofs.append({'scenario':p.name,'units':len(tuples),'full_state':not native,'target_pair_margin':x['target'],'bounded_share_shift':float(d),'unbounded_share_shift':float(unbounded),'exact_net_residual':'0','native_current_join':False})
ck(len(proofs)==20 and target_rows==8414)
result={'status':'pass_independent_source_weight_exact_rational_piecewise_roots','checks':N,'historical_source_county_rows':360,'complete_state_models':18,'qualified_native_subset_models':2,'contribution_and_selected_only_rows':target_rows,'maximum_shift_difference':maxdiff,'maximum_output_net_residual_votes':maxres,'producer_import_or_write':False,'canonical_native_dispatch':[],'method':'Source-checked full certificate vectors and literal native TOTAL positions; independent exact-rational affine breakpoint sweep rather than producer bisection. Every county including nonpriority remains in state models. Unknown outside-native contexts are excluded only from explicitly bounded subset models, never statewide allocated.','proofs':proofs}
out=S/'data/coordinator-baseline-math-review.json';b=(json.dumps(result,indent=2)+'\n').encode()
if '--check' in sys.argv:ck(out.read_bytes()==b)
else:out.write_bytes(b)
print(json.dumps({k:v for k,v in result.items() if k!='proofs'}))
