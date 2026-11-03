"""Historical scenario construction from independently frozen original extracts only."""
import csv,gzip,json,sys
from pathlib import Path
from collections import defaultdict
from calculator import calculate
D=Path(__file__).resolve().parent
C=json.loads((D/'controls.json').read_text());N=json.loads(gzip.decompress((D/'native-results.json.gz').read_bytes()));P=list(csv.DictReader((D/'parish-controls.csv').open()));cand=list(csv.DictReader((D/'candidates.csv').open()));pairs={'2024':(0,3),'2022':(1,4),'2020':(10,2)}
def dump(p,x):
 b=(json.dumps(x,allow_nan=False,separators=(',',':'))+'\n').encode();p=D/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(b,mtime=0) if p.suffix=='.gz' else b)
def write(p,rows):
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def makeunit(r,y,volume,methodscale=1):
 v=json.loads(r['candidate_votes']) if isinstance(r['candidate_votes'],str) else r['candidate_votes'];a,b=pairs[y];pv=v[a]+v[b];ov=sum(v)-pv;names=[x['label'] for x in cand if x['year']==y];others=[n for i,n in enumerate(names) if i not in (a,b)]
 return dict(key=r.get('key','LA:'+r['parish_code']),volume=volume*methodscale,participation=pv/sum(v) if sum(v)>0 else 0,share=v[a]/pv if pv>0 else None,other_allocation={n:(v[i]/ov if ov>0 else 0) for i,n in enumerate(names) if i not in (a,b)})
def input_for(rows,y,volumes,scale=1,method=None):
 names=[x['label'] for x in cand if x['year']==y];a,b=pairs[y]
 return dict(mode='historical',A=names[a],B=names[b],other_candidates=[n for i,n in enumerate(names) if i not in (a,b)],target=0,assumption='Historical named-pair preference/participation anchor '+y+'; all other named candidates retain source relative allocation. All units included; no cross-year native join.',units=[makeunit(r,y,volumes[r.get('key',r['parish_code'])],scale*(method if r.get('type')=='early-aggregate' else 1)) for r in rows])
summary=[];unitout=[];baseline=[]
# Baseline long CSV every parish/contest with complete source candidate field preserved in JSON array plus pair identities.
for r in P:
 y=r['year'];v=json.loads(r['candidate_votes']);a,b=pairs[y];cc=[x for x in cand if x['year']==y];party=defaultdict(int)
 for n,z in zip(cc,v):party[n['party']]+=z
 baseline.append(dict(year=y,race_id=r['race_id'],parish=r['parish'],parish_code=r['parish_code'],A=cc[a]['label'],B=cc[b]['label'],A_votes=v[a],B_votes=v[b],other_votes=sum(v)-v[a]-v[b],all_candidate_votes=sum(v),pair_votes=v[a]+v[b],A_pair_share=v[a]/(v[a]+v[b]) if v[a]+v[b]>0 else None,pair_margin=(v[a]-v[b])/(v[a]+v[b]) if v[a]+v[b]>0 else None,party_totals_json=json.dumps(party),candidate_headers_json=json.dumps([x['label'] for x in cc]),candidate_votes_json=json.dumps(v),qualified=r['qualified'],selected_race_voted=r['voted'],general_stats_voted=r['stats_voted'],ballots_cast=None,blank=None,undervotes=None,overvotes=None,generic_writeins=None,named_writeins=None))
write(D.parent/'county-baselines.csv',baseline)
for y in C:
 for level in ['parish','native']:
  rows=[r for r in (P if level=='parish' else N) if r['year']==y]
  if level=='parish':
   mixes=[('low-2022-volume-mix','2022'),('base-2024-volume-mix','2024'),('high-2020-volume-mix','2020')]
  else:mixes=[('low-0.8-native-volume',.8),('base-native-volume',1.0),('high-1.2-native-volume-early1.25',1.2)]
  for label,mix in mixes:
   if level=='parish':vol={r['parish_code']:int(r['all_candidate_votes']) for r in P if r['year']==mix};x=input_for(rows,y,vol)
   else:vol={r['key']:r['all_candidate_votes'] for r in rows};x=input_for(rows,y,vol,mix,1.25 if mix==1.2 else None)
   scenario=y+'-'+level+'-'+label;dump('scenarios/'+scenario+'.input.json.gz',x)
   for target in [0,.01]:
    x['target']=target;o=calculate(x);dump('scenarios/'+scenario+('-tie' if target==0 else '-Aplus1')+'.output.json.gz',o);u=o['uniform'];S=o['remaining_pair_votes'];M=o['baseline_lead'];F=o['final_all_candidate_votes']
    summary.append(dict(scenario=scenario,target_pair_margin=target,preference_year=y,volume_mix=str(mix),level=level,all_candidate_volume=F,pair_volume=S,pair_participation=S/F if F>0 else None,baseline_lead=M,baseline_pair_margin=o['baseline_pair_margin'],baseline_all_candidate_margin=o['baseline_all_candidate_margin'],unbounded_share_shift=u.get('unbounded_shift'),bounded_share_shift=u.get('bounded_shift'),status=u['status'],residual=u.get('residual')))
    if u['status']=='feasible':
     for c in u['contributions']:
      V=c['pair_volume'];fixed=M-(c['baseline_net_votes'] or 0);req=(target*S-fixed+V)/(2*V) if V>0 else None
      unitout.append(dict(scenario=scenario,target_pair_margin=target,**c,selected_only_required_share=req,selected_only_status='no-positive-pool' if V==0 else 'already-secured' if req<0 else 'impossible' if req>1 else 'feasible',selected_only_fixed_other_net_votes=fixed,selected_only_final_pair_denominator=S))
write(D/'state-scenarios.csv',summary);dump('all-unit-scenarios.json.gz',unitout)
# Exact source-native raw comparisons/participation rows for each baseline.
rows=[]
for r in N:
 y=r['year'];a,b=pairs[y];v=json.loads(r['candidate_votes']);T=sum(v);V=v[a]+v[b];S=sum(C[y]['candidate_totals'][i] for i in (a,b));rows.append(dict(key=r['key'],year=y,parish=r['parish'],ward=r['ward'],precinct=r['precinct'],type=r['type'],A_votes=v[a],B_votes=v[b],other_votes=T-V,all_candidate_votes=T,pair_votes=V,pair_participation=V/T if T>0 else None,share=v[a]/V if V>0 else None,pair_weight=V/S,all_candidate_weight=T/C[y]['all_candidate_votes'],baseline_net=v[a]-v[b],one_share_point_net_votes=.02*V))
dump('native-baselines.json.gz',rows)
print('Built',len(baseline),'parish baselines;',len(summary),'whole-state scenarios;',len(unitout),'unit target contributions;',len(rows),'native baselines')
