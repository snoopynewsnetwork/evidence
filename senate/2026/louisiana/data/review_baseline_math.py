"""Independent source-weight and exact-rational affine breakpoint audit, no producer imports."""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as Q
import csv,gzip,json,math,re
S=Path(__file__).resolve().parents[1];D=S/'data';B=D/'baselines';N=0
F=lambda v:Q(str(v))
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
def load(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def close(a,b,tol=2e-6):ck(a is not None and math.isfinite(float(a)) and abs(float(a)-float(b))<=tol,('numeric',a,float(b),tol))
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
 raise AssertionError('no exact affine segment')
ck(load(D/'coordinator-first-pair-original-review.json')['status'].startswith('pass'),'original source review')
P=list(csv.DictReader((B/'parish-controls.csv').open()));C=list(csv.DictReader((B/'candidates.csv').open()));NR=load(B/'native-results.json.gz');nb=load(B/'native-baselines.json.gz');par={(r['year'],r['parish_code']):r for r in P};native={r['key']:r for r in NR}
labels={y:[r['label'] for r in C if r['year']==y] for y in ['2024','2022','2020']};pairs={'2024':('Kamala D. Harris, Tim Walz Democratic (DEM)','Donald J. Trump, "JD" Vance Republican (REP)'), '2022':('Gary Chambers, Jr. (DEM)','John Kennedy (REP)'), '2020':('Adrian Perkins (DEM)','"Bill" Cassidy (REP)')}
# Named pair selection is explicit; other Democrats remain separate named candidates.
ix={y:tuple(labels[y].index(n) for n in pairs[y]) for y in labels};vectors={};pairtot={};tot={}
for r in NR+P:
 v=json.loads(r['candidate_votes']);vectors[r.get('key',(r['year'],r['parish_code']))]=v
for y in labels:
 vv=[json.loads(r['candidate_votes']) for r in P if r['year']==y];pairtot[y]=sum(v[ix[y][0]]+v[ix[y][1]] for v in vv);tot[y]=sum(map(sum,vv))
for z in nb:
 r=native[z['key']];v=vectors[z['key']];a,b=ix[r['year']];t=sum(v);w=v[a]+v[b]
 ck([z['A_votes'],z['B_votes'],z['other_votes'],z['all_candidate_votes'],z['pair_votes']]==[v[a],v[b],t-w,t,w]);close(z['pair_weight'],Q(w,pairtot[r['year']]),1e-12);close(z['all_candidate_weight'],Q(t,tot[r['year']]),1e-12)
 ck(z['share'] is None if not w else abs(z['share']-v[a]/w)<1e-12);ck(z['pair_participation'] is None if not t else abs(z['pair_participation']-w/t)<1e-12)
rows=load(B/'all-unit-scenarios.json.gz');targets={(r['scenario'],F(r['target_pair_margin']),r['key']):r for r in rows};ck(len(targets)==len(rows)==73512)
constraints={(r['scenario'],F(r['target_pair_margin'])):r for r in load(B/'full-field-constraints.json')};summaries={(r['scenario'],F(r['target_pair_margin'])):r for r in csv.DictReader((B/'state-scenarios.csv').open())};proofs=[];maxdiff=0.;maxres=0.;seen=0
for path in sorted((B/'scenarios').glob('*.input.json.gz')):
 x=load(path);name=path.name.removesuffix('.input.json.gz');year,level=name.split('-')[:2];ck((x['A'],x['B'])==pairs[year]);a,b=ix[year];others=[n for i,n in enumerate(labels[year]) if i not in (a,b)];ck(x['other_candidates']==others)
 source={('LA:'+r['parish_code']) if level=='parish' else r['key']:r for r in (P if level=='parish' else NR) if r['year']==year};ck(set(source)=={u['key'] for u in x['units']} and len(source)==len(x['units']))
 tuples=[];other_totals=defaultdict(Q)
 for u in x['units']:
  r=source[u['key']];v=json.loads(r['candidate_votes']);t=sum(v);pv=v[a]+v[b];q=Q(v[a],pv) if pv else None;p=Q(pv,t) if t else Q(0)
  if level=='parish':
   mix='2022' if '-low-' in name else '2024' if '-base-' in name else '2020';vol=F(par[mix,r['parish_code']]['all_candidate_votes'])
  else:
   scale=Q(4,5) if '-low-' in name else Q(6,5)*(Q(5,4) if r['type']=='early-aggregate' else 1) if '-high-' in name else Q(1);vol=t*scale
  close(u['volume'],vol,1e-7);close(u['participation'],p,1e-12);ck(u['share'] is None if q is None else abs(u['share']-float(q))<1e-12);ck(set(u['other_allocation'])==set(others))
  for i,n in enumerate(labels[year]):
   if i not in (a,b):close(u['other_allocation'][n],Q(v[i],t-pv) if t>pv else 0,1e-12)
  # Solve on exact decimal representations actually supplied to the CLI.
  vol=F(u['volume']);pool=vol*F(u['participation']);q=F(u['share']) if pool else Q(0);tuples.append((u['key'],vol,pool,q))
  for n in others:other_totals[n]+=vol*(1-F(u['participation']))*F(u['other_allocation'][n])
 pair=sum(w for k,v,w,q in tuples);full=sum(v for k,v,w,q in tuples);net=sum(w*(2*q-1) for k,v,w,q in tuples)
 for target,suffix in [(Q(0),'tie'),(Q(1,100),'Aplus1')]:
  o=load(path.with_name(name+'-'+suffix+'.output.json.gz'));goal=target*pair;d=root([(w,q) for k,v,w,q in tuples],goal);unbounded=(goal-net)/(2*pair);u=o['uniform'];ck(u['status']=='feasible' and o['unknown_units']==[]);close(o['final_pair_votes'],pair);close(o['final_all_candidate_votes'],full);close(o['baseline_lead'],net);close(u['bounded_shift'],d,1e-12);close(u['unbounded_shift'],unbounded,1e-12)
  ck(len(u['contributions'])==len(tuples));achieved=Q(0)
  for (k,v,w,q),z in zip(tuples,u['contributions']):
   ck(z['key']==k);newq=max(Q(0),min(Q(1),q+d));old=w*(2*q-1);new=w*(2*newq-1);achieved+=new;expected={'pair_volume':w,'pair_weight':w/pair,'all_volume_weight':v/full,'participation':w/v if v else 0,'target_share':newq,'target_net_votes':new,'baseline_net_votes':old,'net_gain':new-old,'one_share_point_net_votes':w/50}
   # A zero-pool source preference remains undefined in published row fields.
   for field,val in expected.items():
    if not w and field in ['target_share','target_net_votes','baseline_net_votes','net_gain']:ck(z[field] is None,('zero pool',field))
    else:close(z[field],val,1e-10 if 'weight' in field or 'share' in field or field=='participation' else 2e-6)
   ck(z['clipped']==(bool(w) and (q+d<0 or q+d>1)));row=targets[name,target,k];fixed=net-old;req=(goal-fixed+w)/(2*w) if w else None
   for field in z:ck(row[field]==z[field],('full contribution field',field))
   close(row['selected_only_fixed_other_net_votes'],fixed);close(row['selected_only_final_pair_denominator'],pair)
   if req is None:ck(row['selected_only_required_share'] is None and row['selected_only_status']=='no-positive-pool')
   else:close(row['selected_only_required_share'],req,1e-8);ck(row['selected_only_status']==('already-secured' if req<0 else 'impossible' if req>1 else 'feasible'))
   seen+=1
  ck(achieved==goal,'exact-rational zero residual')
  fc=constraints[name,target];close(fc['pair_volume'],pair);close(fc['all_candidate_volume'],full);close(fc['A_pair_share'],(1+target)/2,1e-12);close(fc['A_candidate_votes_at_pair_target'],pair*(1+target)/2);close(fc['B_candidate_votes_at_pair_target'],pair*(1-target)/2)
  for n,v in other_totals.items():close(fc['other_candidate_votes'][n],v)
  close(fc['plurality_requires_A_pair_share_strictly_above'],max(Q(1,2),max(other_totals.values())/pair),1e-12);close(fc['majority_requires_A_pair_share_strictly_above'],full/(2*pair),1e-12);ck(fc['pair_target_does_not_imply_legal_outcome'] is True)
  summary=summaries[name,target];close(summary['bounded_share_shift'],d,1e-12);close(summary['pair_volume'],pair);close(summary['all_candidate_volume'],full)
  maxdiff=max(maxdiff,abs(float(d)-u['bounded_shift']));maxres=max(maxres,abs(float(goal)-sum(z['target_net_votes'] or 0 for z in u['contributions'])));proofs.append({'scenario':name,'target_pair_margin':float(target),'units':len(tuples),'bounded_shift':float(d),'unbounded_shift':float(unbounded),'exact_affine_residual':'0'})
ck(len(proofs)==36 and seen==73512)
result={'status':'pass_independent_source_weight_exact_affine_roots','checks':N,'source_native_baselines':len(nb),'whole_state_targets':len(proofs),'all_unit_selected_and_contribution_rows':seen,'maximum_shift_difference':maxdiff,'maximum_floating_output_net_residual_votes':maxres,'method':'Source-checked full candidate vectors and explicit named-pair indices; independent Fraction affine-breakpoint sweep, not producer bisection. Every native or parish unit and every nonpriority source is included. Zero-pool preference remains unknown. All named other candidates remain separate; pair target does not certify plurality/majority or current legal outcome.','producer_import_or_write':False,'network':False,'proofs':proofs}
(D/'coordinator-baseline-math-review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='proofs'}))
