"""Real CLI tests plus independent rational piecewise and denominator controls."""
from pathlib import Path
from fractions import Fraction as F
import json,subprocess,sys,copy,math
B=Path(__file__).resolve().parents[1];D=B/'fixtures';D.mkdir(exist_ok=True)
def unit(k='u',A=120,Bv=100,Z=50,r=100,p=.8,q=.75):return dict(key=k,counted=dict(A=A,B=Bv,other={'Z':Z}),remaining=r,participation=p,share=q,other_allocation={'Z':1})
base=dict(mode='live',pair=['A','B'],others=['Z'],other_scope='named',target=0,selected_unit='u',assumptions='Synthetic arithmetic fixture; all remaining volumes/preferences explicit',units=[unit()])
cases=[]
def case(name,x,valid=True,expected=None):cases.append((name,x,valid,expected))
case('counted-fixed-final-denominator',base,expected='fixed')
x=copy.deepcopy(base);x['units'][0]['share']=None;case('unknown-positive-pool',x,expected='unknown')
x=copy.deepcopy(base);x['units'][0].update(remaining=0,share=None);case('no-pool-secured',x,expected='no-pool')
x=copy.deepcopy(base);x['units'][0]=unit(A=1000,Bv=0,r=10);case('selected-secured-negative-share',x,expected='secured')
x=copy.deepcopy(base);x['units'][0]=unit(A=0,Bv=1000,r=10);case('selected-impossible-over-one',x,expected='impossible')
x=copy.deepcopy(base);x['units']+=[unit('other',r=20,q=None)];case('selected-only-unknown-other',x,expected='unknown-other')
x=copy.deepcopy(base);x.pop('selected_unit');x['mode']='historical';x['units']=[unit('hi',0,0,0,90,1,.95),unit('lo',0,0,0,10,1,.05)];case('endpoint-clipping',x,expected='clipping')
x=copy.deepcopy(base);x['units'][0]=unit(A=0,Bv=0,Z=0,r=100,p=0,q=None);case('zero-pair-undefined',x,expected='zero-pair')
x=copy.deepcopy(base);x['units'][0]=unit(A=20,Bv=10,Z=80,r=0,q=None);case('pair-leader-loses-full-field',x,expected='loses-field')
x=copy.deepcopy(base);x['units'][0]=unit(A=100,Bv=200,r=100,p=.8,q=.75);case('bounded-impossible-counted-fixed',x,expected='bounded-impossible')
x=copy.deepcopy(base);x['target']=.01;case('positive-cushion',x,expected='piecewise')
x=copy.deepcopy(base);x['other_scope']='unresolved';case('generic-other-no-legal-plurality',x,expected='unresolved')
for branch in ['unknown','no-pool']:
 for defect in ['duplicate','missing','blank','nonstring']:
  x=copy.deepcopy(base);x.pop('selected_unit');x['units'][0].update(share=None,remaining=0 if branch=='no-pool' else 100)
  y=unit('second')
  if defect=='duplicate':y['key']='u'
  if defect=='missing':y.pop('key')
  if defect=='blank':y['key']=' \t '
  if defect=='nonstring':y['key']=2
  x['units'].append(y);case(branch+'-global-key-'+defect,x,False)
for name,v in [('bool',True),('null',None),('text','0'),('nan',float('nan')),('positive-infinity',float('inf')),('negative-infinity',-float('inf')),('below',-1.01),('above',1.01)]:
 x=copy.deepcopy(base);x['target']=v;case('invalid-target-'+name,x,False)
for name,patch in [('negative-count',('A',-1)),('bool-count',('A',True)),('null-count',('B',None)),('negative-other',('other',{'Z':-1}))]:
 x=copy.deepcopy(base);x['units'][0]['counted'][patch[0]]=patch[1];case(name,x,False)
for name,k,v in [('negative-pool','remaining',-1),('text-pool','remaining','2'),('share-over-one','share',1.1),('bool-share','share',False),('participation-negative','participation',-.1),('allocation-unbalanced','other_allocation',{'Z':.5}),('allocation-bool','other_allocation',{'Z':True}),('counted-total-below-pair','counted_total',1)]:
 x=copy.deepcopy(base);x['units'][0][k]=v;case(name,x,False)
x=copy.deepcopy(base);x['units'][0]=unit(A=1e308,Bv=1e308);case('aggregate-overflow',x,False)
x=copy.deepcopy(base);x['others']=['A'];case('candidate-collision',x,False)
x=copy.deepcopy(base);x['mode']='probability';case('unsupported-setting',x,False)
x=copy.deepcopy(base);x['selected_unit']='absent';case('selected-key-absent',x,False)
x=copy.deepcopy(base);x['units'][0]['key']=' u ';x['selected_unit']=' u ';case('literal-whitespace-key-preserved',x,expected='literal-key')
case('duplicate-object-field','{"mode":"live","mode":"historical"}',False)
x=copy.deepcopy(base);x['units'][0]=unit(A=0,Bv=0,Z=0,r=300,p=.2,q=.6);x['target']=.01;case('pair-target-feasible-full-field-impossible',x,expected='target-loses-field')
def rat(x):return F(str(x))
def independent_piecewise(inp):
 # Enumerate exact affine segments between all clipping breakpoints.
 units=inp['units'];pp=[rat(u['remaining'])*rat(u['participation']) for u in units];net=sum(rat(u['counted']['A'])-rat(u['counted']['B']) for u in units)
 total=sum(rat(u['counted']['A'])+rat(u['counted']['B']) for u in units)+sum(pp);goal=rat(inp['target'])*total
 events={F(-1):F(0),F(1):F(0)}
 for u,w in zip(units,pp):
  if not w:continue
  q=rat(u['share'])
  events[-q]=events.get(-q,F(0))+2*w;events[1-q]=events.get(1-q,F(0))-2*w
 points=sorted(events);value=net-sum(pp);slope=F(0)
 for l,r in zip(points,points[1:]):
  slope+=events[l];right=value+slope*(r-l)
  if value<=goal<=right:
   root=l if slope==0 else l+(goal-value)/slope
   direct=net+sum(w*(2*min(F(1),max(F(0),rat(u['share'])+root))-1) for u,w in zip(units,pp) if w)
   assert direct==goal;return float(root),float(goal),float(total)
  value=right
 return None,float(goal),float(total)
def run(name,data,valid,expected):
 raw=data if isinstance(data,str) else json.dumps(data,indent=2,allow_nan=True)
 ip=D/(name+'.input.json');ip.write_text(raw+'\n')
 r=subprocess.run([sys.executable,str(B/'scripts/calculator.py'),str(ip)],capture_output=True,text=True)
 (D/(name+'.stdout.json')).write_text(r.stdout);(D/(name+'.transport.json')).write_text(json.dumps(dict(exit=r.returncode,stderr=r.stderr,argv=['python','scripts/calculator.py','fixtures/'+ip.name]),indent=2)+'\n')
 out=json.loads(r.stdout,parse_constant=lambda s:(_ for _ in ()).throw(AssertionError(s)));assert not r.stderr,(name,r.stderr)
 assert r.returncode==(0 if valid else 2),(name,out,r.returncode)
 if not valid:assert out['status']=='invalid-input';return dict(case=name,passed=True,expected='invalid-input')
 if expected=='fixed':
  assert out['baseline_final_candidate_votes']=={'A':180.,'B':120.,'Z':70.};assert out['final_pair_denominator']==300 and out['final_all_candidate_denominator']==370
  assert out['counted_A']==120 and out['counted_B']==100;assert abs(out['selected_only']['required_A_share']-.375)<1e-12
  f=out['uniform']['full_field_at_pair_target'];assert f['candidate_votes']['A']==f['candidate_votes']['B'] and f['strict_A_plurality'] is False
 if expected=='unknown':assert 'unknown' in out['status'] and out['final_all_candidate_denominator']==370
 if expected=='no-pool':assert out['no_positive_pool'] and out['uniform']['status']=='no-positive-pair-pool'
 if expected in ('secured','impossible'):assert out['selected_only']['status']==expected;assert (out['selected_only']['required_A_share']<0 if expected=='secured' else out['selected_only']['required_A_share']>1)
 if expected=='unknown-other':assert out['selected_only']['status']=='unknown other-unit assumptions'
 if expected=='clipping':assert out['uniform']['clipping_active'];assert abs(out['uniform']['clipped_share_shift']-out['uniform']['unbounded_share_shift'])>.01
 if expected=='zero-pair':assert not out['pair_share_defined'] and out['baseline_final_pair_margin'] is None
 if expected=='loses-field':assert out['baseline_final_pair_net']>0 and out['baseline_full_field_A_plurality'] is False
 if expected=='bounded-impossible':assert out['uniform']['status']=='impossible bounded target'
 if expected=='unresolved':assert out['baseline_full_field_A_plurality']=='unresolved other identities'
 if expected=='literal-key':assert out['units'][0]['key']==' u '
 if expected=='target-loses-field':
  assert out['uniform']['status']=='feasible' and out['uniform']['full_field_at_pair_target']['strict_A_plurality'] is False
  assert out['selected_only']['status']=='feasible' and out['selected_only']['full_field_boundary_status']=='impossible'
  assert abs(out['selected_only']['full_field_strict_plurality_boundary_A_share']-4)<1e-12
 if out.get('uniform',{}).get('status')=='feasible':
  d,goal,T=independent_piecewise(data);assert abs(d-out['uniform']['clipped_share_shift'])<1e-10
  assert abs(out['uniform']['achieved_pair_net']-goal)<1e-7
 return dict(case=name,passed=True,expected=expected)
def main():
 checks=[run(*c) for c in cases];scenario_checks=[]
 for ip in sorted((B/'scenarios').glob('*.input.json')):
  inp=json.loads(ip.read_text());out=json.loads(ip.with_name(ip.name.replace('.input.','.result.')).read_text());d,goal,T=independent_piecewise(inp)
  assert abs(d-out['uniform']['clipped_share_shift'])<1e-10,ip
  assert abs(sum(u['pair_weight'] for u in out['units'])-1)<1e-10,ip
  assert abs(sum(u['target_pair_net_contribution'] for u in out['units'])-goal)<1e-6,ip
  assert abs(sum(u['baseline_pair_net_contribution'] for u in out['units'])-out['baseline_final_pair_net'])<1e-6,ip
  assert abs(sum(u['net_gain'] for u in out['units'])-(goal-out['baseline_final_pair_net']))<1e-6,ip
  assert abs(sum(u['remaining'] for u in inp['units'])-out['final_all_candidate_denominator'])<1e-6,ip
  if inp['target']==0:
   field=out['uniform']['full_field_at_pair_target'];A,Bb=inp['pair'];assert field['candidate_votes'][A]==field['candidate_votes'][Bb],ip
   if inp['other_scope']=='named':assert field['strict_A_plurality'] is False,ip
  scenario_checks.append(dict(input=ip.name,units=len(inp['units']),independent_piecewise_root=d,target_net=goal,passed=True))
 obj=dict(status='passed',real_cli_fixtures=checks,independent_scenario_checks=scenario_checks,method='Independent Fraction affine-segment enumeration, explicit denominator/counted controls, actual subprocess CLI exit/strictJSON/stderr checks; no calculator code imported')
 (B/'proof/calculator-validation.json').write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n');print('passed',len(checks),'CLI fixtures,',len(scenario_checks),'independent scenario roots')
if __name__=='__main__':main()
