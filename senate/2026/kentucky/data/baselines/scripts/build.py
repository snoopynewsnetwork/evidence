"""Build complete county scenarios and separate source-local native subset sensitivities."""
from pathlib import Path
import json,csv,collections,gzip,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];B=ROOT/'data/baselines'
def dump(p,o):p.write_text(json.dumps(o,indent=2,allow_nan=False)+'\n')
def cli(inp,out):
 r=subprocess.run([sys.executable,str(B/'scripts/calculator.py'),str(inp)],capture_output=True,text=True)
 out.write_text(r.stdout);assert r.returncode==0 and not r.stderr,(inp,r.stdout,r.stderr)
 return json.loads(r.stdout)
def writecsv(path,rows):
 with path.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 pins=json.loads((B/'source/pins.json').read_text())['pins'];p=next(p for p in pins if p['role']=='2024 Census county FIPS identity only')
 html=gzip.decompress((ROOT/p['path']).read_bytes()).decode();fips={}
 for tr in re.findall(r'<tr>(.*?)</tr>',html,re.S):
  cols=dict(re.findall(r'<td headers="header(\d+)">(.*?)</td>',tr,re.S))
  if '7' in cols:fips[cols['7'].lower()]=(cols['3'],cols['7'])
 assert len(fips)==120
 fields=list(csv.DictReader((B/'extracted/certificate-fields.csv').open()));cs=json.loads((B/'extracted/candidates.json').read_text());by={}
 for y in [2020,2022,2024]:
  by[y]={};g=collections.defaultdict(list)
  for r in fields:
   if int(r['year'])==y and r['scope']=='county':g[r['county_literal']].append(r)
  for c,rs in g.items():
   rs.sort(key=lambda r:int(r['column']));votes=[int(r['votes']) for r in rs];fid,cn=fips[c.lower()]
   by[y][fid]=dict(year=y,county_literal=c,census_name=cn,fips=fid,A=votes[1],B=votes[0],other=sum(votes[2:]),all=sum(votes),pair=sum(votes[:2]),
    A_share=votes[1]/sum(votes[:2]),participation=sum(votes[:2])/sum(votes),source_sha256=rs[0]['source_sha256'],source_page=int(rs[0]['page']),source_line=int(rs[0]['line']),candidate_vector=json.dumps(votes))
  assert len(by[y])==120
 rows=[]
 for y in by:
  for fid,r in sorted(by[y].items()):rows.append(dict(r,A_identity=next(c['name'] for c in cs if c['year']==y and c['column']==2),B_identity=next(c['name'] for c in cs if c['year']==y and c['column']==1),A_pair_margin=(r['A']-r['B'])/r['pair'],A_full_field_share=r['A']/r['all'],ballots_cast='',registration='',geography='certificate county parent',native_join='not established'))
 writecsv(ROOT/'data/county-baselines.csv',rows)
 ranks=sorted(by[2024].values(),key=lambda r:(-r['all'],r['fips']));total=sum(r['all'] for r in ranks);cum=0;rankrows=[];cross=None
 for i,r in enumerate(ranks,1):
  prior=cum;cum+=r['all']
  if cross is None and 5*cum>=4*total:cross=i
  rankrows.append(dict(rank=i,fips=r['fips'],county_literal=r['county_literal'],contest_votes=r['all'],cumulative=cum,state_total=total,cumulative_share=cum/total,previous_below_80=5*prior<4*total))
 writecsv(B/'county-order.csv',rankrows)
 dump(B/'priority.json',dict(canonical_native_order=None,canonical_native_top15_share=None,canonical_native_minimum80=None,dispatch_keys=[],
  reason='2024 Scott recap is cumulative; Elliott image-only; remaining raw native/full-field scopes not closed. Historical native 2020/2022 candidates unavailable statewide.',
  county_sensitivity=dict(total=total,top15_votes=sum(r['all'] for r in ranks[:15]),top15_share=sum(r['all'] for r in ranks[:15])/total,minimum80_count=cross,
   crossing_votes=rankrows[cross-1]['cumulative'],preceding_votes=rankrows[cross-2]['cumulative'],keys=[r['fips'] for r in ranks[:cross]])))
 scenarios=[];targets=[];d=B/'scenarios';d.mkdir(exist_ok=True)
 for anchor in [2024,2020,2022]:
  candidates=sorted([c for c in cs if c['year']==anchor],key=lambda c:c['column']);otherids=[c['key'] for c in candidates[2:]]
  for mix,label in [(2022,'low-midterm'),(2024,'base-presidential'),(2020,'high-presidential')]:
   units=[]
   for fid,r in sorted(by[anchor].items()):
    vec=json.loads(r['candidate_vector']);ot=sum(vec[2:]);alloc={n:(v/ot if ot else (1. if j==0 else 0.)) for j,(n,v) in enumerate(zip(otherids,vec[2:]))}
    # Allocation in zero-observed-other counties is an explicit mathematical convention;
    # positive other pool is zero there because historical participation is 1.
    units.append(dict(key=fid,counted=dict(A=0,B=0,other={n:0 for n in otherids}),remaining=by[mix][fid]['all'],participation=r['participation'],share=r['A_share'],other_allocation=alloc))
   for target in [0,.01]:
    name=f'county-anchor{anchor}-mix{mix}-margin{target}';inp=dict(mode='historical',pair=[candidates[1]['name'],candidates[0]['name']],others=otherids,other_scope='named',target=target,assumptions=f'{label}: all-candidate volume and county mix from {mix} certificate; pair participation and preference from {anchor}; every120county included; no native crossyear join or2026 forecast',units=units)
    dump(d/(name+'.input.json'),inp);res=cli(d/(name+'.input.json'),d/(name+'.result.json'))
    scenarios.append(dict(name=name,anchor=anchor,volume_mix_year=mix,label=label,target=target,final_pair_denominator=res['final_pair_denominator'],final_all_candidate_denominator=res['final_all_candidate_denominator'],baseline_net=res['baseline_final_pair_net'],**res['uniform']))
    for u in res['units']:
     othernet=res['baseline_final_pair_net']-u['baseline_pair_net_contribution'];req=(target*res['final_pair_denominator']-othernet+u['pair_pool'])/(2*u['pair_pool']) if u['pair_pool'] else None
     targets.append(dict(scenario=name,fips=u['key'],county_literal=by[anchor][u['key']]['county_literal'],preference_anchor=anchor,volume_mix_year=mix,state_target_pair_margin=target,all_candidate_volume=u['remaining'],pair_participation=u['pair_pool']/u['remaining'],pair_volume=u['pair_pool'],weight=u['pair_weight'],baseline_A_share=u['share'],target_A_share=u['target_A_share'],target_pair_margin=2*u['target_A_share']-1,target_full_candidate_A_share=u['target_A_share']*u['pair_pool']/u['remaining'],baseline_pair_net=u['baseline_pair_net_contribution'],target_pair_net=u['target_pair_net_contribution'],net_gain=u['net_gain'],one_A_share_point_net_votes=u['one_A_share_point_net_votes'],selected_only_required_A_share=req,selected_only_status='impossible' if req>1 else 'secured' if req<0 else 'feasible',other_counties_assumption='all other counties fixed at unshifted stated anchor preferences and stated mix volumes'))
 dump(B/'state-scenarios.json',scenarios);writecsv(B/'county-targets.csv',targets)
 # Source-local subset is explicitly separate from statewide scenario/dispatch.
 native=json.loads((B/'extracted/native-known-pair-units.json').read_text())+json.loads((B/'extracted/elliott-manual.json').read_text());nr=[];native_targets=[]
 for r in native:
  if r['pair']>0:nr.append(dict(key=r['key'],counted=dict(A=0,B=0,other={'unallocated native other':0}),remaining=r['all_candidate_printed_total'],participation=r['pair_participation'],share=r['A_pair_share'],other_allocation={'unallocated native other':1}))
 for target in [0,.01]:
  name=f'native-known-subset-margin{target}';inp=dict(mode='historical',pair=['Kamala D. HARRIS','Donald J. TRUMP'],others=['unallocated native other'],other_scope='unresolved',target=target,assumptions='Known source-local pair/control contexts only; unallocated native other retains generic/named scope unknown; no complete-state claim; no crossyear join',units=nr)
  dump(d/(name+'.input.json'),inp);res=cli(d/(name+'.input.json'),d/(name+'.result.json'))
  for u in res['units']:
   fixed=res['baseline_final_pair_net']-u['baseline_pair_net_contribution'];req=(target*res['final_pair_denominator']-fixed+u['pair_pool'])/(2*u['pair_pool'])
   native_targets.append(dict(scenario=name,key=u['key'],pair_volume=u['pair_pool'],all_candidate_volume=u['remaining'],pair_participation=u['pair_pool']/u['remaining'],weight=u['pair_weight'],baseline_A_share=u['share'],target_A_share=u['target_A_share'],target_pair_margin=2*u['target_A_share']-1,baseline_net=u['baseline_pair_net_contribution'],target_net=u['target_pair_net_contribution'],net_gain=u['net_gain'],one_A_share_point_net_votes=u['one_A_share_point_net_votes'],selected_only_required_A_share=req,selected_only_status='impossible' if req>1 else 'secured' if req<0 else 'feasible',other_units='all other known-subset units fixed at unshifted own source preferences/volumes; omitted/unavailable universe remains unknown and cannot be a full-state target'))
 writecsv(B/'native-known-subset-targets.csv',native_targets)
 dump(B/'native-subset-scope.json',dict(included_positive_pair_keys=[r['key'] for r in native if r['pair']>0],zero_pair_contexts=[r for r in native if r['pair']==0],unresolved_contexts='extracted/native-unresolved-pair-contexts.json',full_state=False,canonical_native_dispatch=[]))
 print('county baselines',len(rows),'scenario targets',len(targets),'county80',cross,'native subset',len(nr))
if __name__=='__main__':main()
