"""Presentation-only partitions and explicit complete-field constraints; all units retained."""
import csv,gzip,json,math
from pathlib import Path
D=Path(__file__).resolve().parent;P=json.loads(gzip.decompress((D/'historical-priority-contract.json.gz').read_bytes()));C=json.load(open(D/'controls.json'));N=json.loads(gzip.decompress((D/'native-results.json.gz').read_bytes()));sc=list(csv.DictReader((D/'state-scenarios.csv').open()));groups=[];constraints=[]
for s in sc:
 name=s['scenario'];y=s['preference_year'];level=s['level'];target=float(s['target_pair_margin']);suffix='tie' if target==0 else 'Aplus1';x=json.loads(gzip.decompress((D/'scenarios'/f'{name}.input.json.gz').read_bytes()));o=json.loads(gzip.decompress((D/'scenarios'/f'{name}-{suffix}.output.json.gz').read_bytes()));priority=set(P[y][level]['priority_keys']);units=o['uniform'].get('contributions',[])
 for label,flag in [('priority',True),('outside-priority',False)]:
  a=[r for r in units if (r['key'].removeprefix('LA:') in priority if level=='parish' else r['key'] in priority)==flag];groups.append(dict(scenario=name,target_pair_margin=target,group=label,unit_count=len(a),pair_volume=math.fsum(r['pair_volume'] for r in a),pair_weight=math.fsum(r['pair_weight'] for r in a),baseline_net=math.fsum(r['baseline_net_votes'] or 0 for r in a),target_net=math.fsum(r['target_net_votes'] or 0 for r in a),net_gain=math.fsum(r['net_gain'] or 0 for r in a)))
 # All other named candidates held at source allocation. A must separately beat every named other.
 others={n:math.fsum(u['volume']*(1-u['participation'])*u['other_allocation'][n] for u in x['units']) for n in x['other_candidates']};V=o['final_pair_votes'];F=o['final_all_candidate_votes'];m=max(others.values(),default=0)
 constraints.append(dict(scenario=name,target_pair_margin=target,all_candidate_volume=F,pair_volume=V,other_candidate_votes=others,A_pair_share=(1+target)/2,A_candidate_votes_at_pair_target=V*(1+target)/2,B_candidate_votes_at_pair_target=V*(1-target)/2,plurality_requires_A_pair_share_strictly_above=max(.5,m/V) if V else None,majority_requires_A_pair_share_strictly_above=F/(2*V) if V else None,pair_target_does_not_imply_legal_outcome=True))
for name,x in [('priority-contributions.json',groups),('full-field-constraints.json',constraints)]: (D/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
