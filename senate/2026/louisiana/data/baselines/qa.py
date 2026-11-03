"""Actual CLI fixtures and independent piecewise root/whole-state arithmetic checks."""
import copy,csv,gzip,hashlib,json,math,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent;F=D/'fixtures';F.mkdir(exist_ok=True)
def dump(p,x):p.write_text(json.dumps(x,allow_nan=False,indent=2)+'\n')
def unit(key='u',remaining=100,share=.5,part=.8,counted=None):return dict(key=key,counted=counted or {'A':10,'B':20,'C':5},remaining=remaining,share=share,participation=part,other_allocation={'C':1})
def base(units=None,**kw):return dict(mode='live',A='A',B='B',other_candidates=['C'],target=0,units=[unit()] if units is None else units,**kw)
fixtures=[]
def case(n,x,expect):fixtures.append((n,x,expect))
case('counted-fixed-final-denominator',base(),{'final_pair_votes':110,'final_all_candidate_votes':135,'baseline_lead':-10,'final_candidate_votes':{'A':50,'B':60,'C':25},'uniform.unbounded_shift':.0625})
case('unknown-positive-pool',base([unit(share=None)]),{'status':'unknown-preference','baseline_lead':None})
case('no-pool-below',base([unit(remaining=0,share=None)]),{'no_positive_pool':True,'fixed_target_status':'below','uniform.status':'no-positive-pool'})
case('no-pool-secured',base([unit(remaining=0,counted={'A':30,'B':5,'C':0})]),{'fixed_target_status':'met','final_pair_votes':35})
case('negative-lead',base([unit(counted={'A':0,'B':150,'C':0})]),{'uniform.status':'impossible'})
case('secured-even-zero-share',base([unit(counted={'A':150,'B':0,'C':0})]),{'uniform.status':'already-secured'})
case('selected-only-impossible',base([unit(remaining=1)],selected_unit='u'),{'selected_only.status':'impossible','selected_only.required_share':6.75})
case('selected-only-secured',base([unit(remaining=1,counted={'A':20,'B':0,'C':0})],selected_unit='u'),{'selected_only.status':'already-secured','selected_only.required_share':-12})
case('selected-unknown-other',base([unit('u'),unit('v',share=None)],selected_unit='u'),{'selected_only.status':'unknown-other-units'})
case('selected-unknown-self-solvable',base([unit(share=None)],selected_unit='u'),{'selected_only.status':'feasible','selected_only.required_share':.5625})
case('zero-pair-undefined',base([unit(remaining=100,share=None,part=0,counted={'A':0,'B':0,'C':10})]),{'baseline_pair_margin':None,'final_pair_votes':0,'no_positive_pool':True})
case('pair-leader-loses-fullfield',base([unit(remaining=0,counted={'A':20,'B':10,'C':100})]),{'arithmetic_plurality_leaders':['C'],'baseline_lead':10})
x=dict(mode='historical',A='A',B='B',other_candidates=['C'],target=0,units=[dict(key='high',volume=10,participation=1,share=1,other_allocation={'C':0}),dict(key='low',volume=90,participation=1,share=0,other_allocation={'C':0})])
case('clipping-root-distinct',x,{'uniform.unbounded_shift':.4,'uniform.bounded_shift':4/9,'uniform.achieved_lead':0})
x=copy.deepcopy(x);x['target']=1;case('clipping-endpoint',x,{'uniform.bounded_shift':1,'uniform.achieved_lead':100})
x=base();x['units'][0]['key']=' u ';x['selected_unit']=' u ';case('literal-spaces-preserved',x,{'selected_only.status':'feasible'})
# Global key checks must precede unknown/no-pool branches, even when selected other key is valid.
for branch,remaining,share in [('unknown',100,None),('no-pool',0,None)]:
 for kind,key in [('duplicate','u'),('blank',' '),('nonstring',4),('missing','MISSING')]:
  a=unit('u',remaining=remaining,share=share);b=unit(key)
  if key=='MISSING':del b['key']
  case(branch+'-'+kind+'-key',base([a,b],selected_unit='u'),{'invalid':True})
for v in [True,None,'0',-1.01,1.01]:
 x=base();x['target']=v;case('invalid-target-'+repr(v),x,{'invalid':True})
for field,values in [('remaining',[-1,True,None,'2']),('participation',[-.1,1.1,True,None]),('share',[-.1,1.1,True,'0.5'])]:
 for v in values:
  x=base();x['units'][0][field]=v;case('invalid-'+field+'-'+repr(v),x,{'invalid':True})
for v in [-1,True,None,'3']:
 x=base();x['units'][0]['counted']['A']=v;case('invalid-count-'+repr(v),x,{'invalid':True})
x=base();x['units'][0]['other_allocation']['C']=.5;case('unbalanced-other',x,{'invalid':True})
x=base();x['B']='A';case('candidate-pair-collision',x,{'invalid':True})
x=base();x['other_candidates']=['A'];case('candidate-other-collision',x,{'invalid':True})
x=base();x['mode']='probability';case('unsupported-mode',x,{'invalid':True})
x=base();x['units'][0]['all_candidate_total']=5;case('all-total-smaller-pair',x,{'invalid':True})
x=base([unit('u',remaining=1e308),unit('v',remaining=1e308)]);case('aggregate-overflow',x,{'invalid':True})
# Raw malformed tokens duplicate fields cannot be represented in Python dictionaries.
raws={}
for tok in ['NaN','Infinity','-Infinity']:
 for field in ['target','remaining','share']:
  s=json.dumps(base());s=s.replace('"'+field+'": '+('0' if field=='target' else '100' if field=='remaining' else '0.5'),'"'+field+'": '+tok);raws['nonfinite-'+field+'-'+tok]=s
raws['duplicate-object-field']=json.dumps(base()).replace('"target": 0','"target": 0, "target": 0.01')
raws['duplicate-count-candidate']=json.dumps(base()).replace('"A": 10','"A": 10,"A": 2')
results=[];failures=[]
def close(got,want):
 if type(want) in (int,float) and type(got) in (int,float):return math.isclose(got,want,rel_tol=1e-12,abs_tol=1e-10)
 if isinstance(want,dict):return isinstance(got,dict) and got.keys()==want.keys() and all(close(got[k],v) for k,v in want.items())
 return got==want
def nested(o,k):
 for p in k.split('.'):o=o[p]
 return o
for name,x,expected in fixtures+[(n,s,{'invalid':True}) for n,s in raws.items()]:
 safe=''.join(c if c.isalnum() or c in '-_' else '_' for c in name);p=F/(safe+'.input.json');p.write_text(x if isinstance(x,str) else json.dumps(x,allow_nan=False,indent=2)+'\n')
 r=subprocess.run([sys.executable,'-B',str(D/'calculator.py'),str(p)],capture_output=True,text=True);(F/(safe+'.stdout.json')).write_text(r.stdout);(F/(safe+'.stderr.txt')).write_text(r.stderr);check=[]
 try:
  out=json.loads(r.stdout,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)));check.append(not r.stderr)
  if expected.get('invalid'):check.extend([r.returncode==2,out['status']=='invalid-input'])
  else:
   check.append(r.returncode==0)
   for k,v in expected.items():
    got=nested(out,k);check.append(close(got,v))
 except Exception as e:check.append(False)
 passed=all(check);record=dict(name=name,input=p.name,exit=r.returncode,expected=expected,passed=passed);results.append(record)
 if not passed:failures.append(record)
dump(F/'results.json',results)
# Independent piecewise inversion: solve affine segments between clipping breakpoints, no iterative bisection.
def independent_root(units,target):
 U=math.fsum(u['volume']*u['participation'] for u in units);points=sorted(set([-1,1]+[-u['share'] for u in units if u['share'] is not None]+[1-u['share'] for u in units if u['share'] is not None]));goal=(target+1)*U/2
 for lo,hi in zip(points,points[1:]):
  mid=(lo+hi)/2;intercept=0;slope=0
  for u in units:
   V=u['volume']*u['participation'];s=u['share']
   if s is None:continue
   if s+mid<=0:continue
   if s+mid>=1:intercept+=V
   else:intercept+=V*s;slope+=V
  if slope:
   d=(goal-intercept)/slope
   if lo-1e-12<=d<=hi+1e-12:return d
  elif abs(goal-intercept)<1e-8:return lo
 raise AssertionError('no independent feasible segment')
scenario_checks=[]
for p in sorted((D/'scenarios').glob('*.input.json.gz')):
 inp=json.loads(gzip.decompress(p.read_bytes()));units=inp['units'];U=math.fsum(u['volume']*u['participation'] for u in units);T=math.fsum(u['volume'] for u in units);M=math.fsum(u['volume']*u['participation']*(2*u['share']-1) for u in units if u['share'] is not None)
 for suffix,target in [('tie',0),('Aplus1',.01)]:
  out=json.loads(gzip.decompress(p.with_name(p.name.replace('.input.json.gz','-'+suffix+'.output.json.gz')).read_bytes()));u=out['uniform'];d=independent_root(units,target);con=u['contributions'];res=math.fsum(r['target_net_votes'] or 0 for r in con)-target*U
  ok=abs(d-u['bounded_shift'])<1e-11 and abs(res)<1e-7 and abs(sum(r['pair_weight'] for r in con)-1)<1e-10 and len(con)==len(units) and abs(T-out['final_all_candidate_votes'])<1e-7 and abs(M-out['baseline_lead'])<1e-7
  # Per-row direct controls, including fixed source mix, participation, weights, gains.
  for a,b in zip(units,con):
   V=a['volume']*a['participation'];q=None if a['share'] is None else min(1,max(0,a['share']+d));ok=ok and a['key']==b['key'] and abs(V-b['pair_volume'])<1e-8 and (q is None and b['target_share'] is None or q is not None and abs(q-b['target_share'])<1e-11)
  scenario_checks.append(dict(scenario=p.name,target=target,independent_shift=d,residual=res,unit_count=len(units),passed=bool(ok)))
  if not ok:failures.append(scenario_checks[-1])
# Every selected-only threshold stored independently checked by substitution into whole-state equation.
allunits=json.loads(gzip.decompress((D/'all-unit-scenarios.json.gz').read_bytes()));selected_bad=0
for r in allunits:
 q=r['selected_only_required_share'];V=r['pair_volume']
 if q is not None:
  residual=r['selected_only_fixed_other_net_votes']+V*(2*q-1)-r['target_pair_margin']*r['selected_only_final_pair_denominator']
  if abs(residual)>1e-7:selected_bad+=1
if selected_bad:failures.append({'selected_residual_failures':selected_bad})
validation=dict(actual_cli_fixture_count=len(results),actual_cli_passed=sum(r['passed'] for r in results),fixture_results='fixtures/results.json',scenario_checks=scenario_checks,selected_only_checks=len(allunits),selected_only_residual_failures=selected_bad,failures=failures,passed=not failures,scope='Arithmetic and supplied historical fields only; no calibrated probability, legal call, 2026 turnout/current geometry or future outcome validation')
dump(D/'validation.json',validation);print(json.dumps({'fixtures':len(results),'failures':failures,'scenario_checks':len(scenario_checks),'selected_only_checks':len(allunits)}));sys.exit(bool(failures))
