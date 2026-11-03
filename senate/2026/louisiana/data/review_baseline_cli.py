"""Independent actual CLI controls for fixed-count/remainder arithmetic and validation."""
from pathlib import Path
import copy,hashlib,json,subprocess,sys,tempfile
S=Path(__file__).resolve().parents[1];B=S/'data/baselines';C=B/'calculator.py';N=0;proof=[]
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
def strict(b):return json.loads(b,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def u(k,A,Bv,Cv,r,p,q):return {'key':k,'counted':{'A':A,'B':Bv,'C':Cv},'remaining':r,'participation':p,'share':q,'other_allocation':{'C':1}}
base={'mode':'live','A':'A','B':'B','other_candidates':['C'],'assumption':'Own stipulated arithmetic, not election prediction','target':0,'selected_unit':'u1','units':[u('u1',40,60,200,100,.8,.25)]};cases=[]
def add(name,x,valid=True,expected=None):cases.append((name,copy.deepcopy(x),valid,expected))
add('fixed-count-final-pair-and-complete-field',base,True,{'final_pair_votes':180,'final_all_candidate_votes':400,'counted_lead':-20,'baseline_lead':-60,'selected_required':.625,'candidate_votes':{'A':60,'B':120,'C':220},'leaders':['C']})
two=copy.deepcopy(base);two['units']=[u('u1',10,30,5,50,1,.2),u('u2',60,40,20,100,.5,.7)];add('other-unit-held-fixed',two,True,{'final_pair_votes':240,'final_all_candidate_votes':315,'baseline_lead':-10,'selected_required':.3,'uniform_shift':.05,'candidate_votes':{'A':115,'B':125,'C':75}})
x=copy.deepcopy(two);x['target']=.01;add('final-pair-cushion-denominator',x,True,{'selected_required':.324,'uniform_shift':.062})
x=copy.deepcopy(two);x['units'][0]['share']=None;add('selected-unknown-conditional-share',x,True,{'status':'unknown-preference','selected_required':.3})
x=copy.deepcopy(two);x['units'][1]['share']=None;add('unknown-other-unit-not-neutral',x,True,{'status':'unknown-preference','selected_status':'unknown-other-units'})
x=copy.deepcopy(base);x['units']=[u('u1',0,0,0,90,1,.99),u('u2',0,0,0,10,1,.01)];add('clipped-share-root-distinct-from-unbounded',x,True,{'uniform_shift':5/9-.99})
for r,p,q in [(0,1,None),(100,0,None)]:
 x=copy.deepcopy(base);x['units']=[u('u1',40,20,0,r,p,q)];add('no-positive-pair-pool-'+str(r),x,True,{'uniform_status':'no-positive-pool','selected_status':'no-positive-pool'})
for A,Bv,status in [(100,0,'already-secured'),(0,100,'impossible')]:
 x=copy.deepcopy(base);x['units']=[u('u1',A,Bv,0,10,1,.5)];add('raw-selected-'+status,x,True,{'selected_status':status})
x=copy.deepcopy(base);x['selected_unit']=None;add('explicit-null-selection-is-supported',x)
for target in [None,True,'0',-1.01,1.01,float('nan'),float('inf'),float('-inf')]:
 x=copy.deepcopy(base);x['target']=target;add('invalid-target-'+repr(target),x,False)
for key in ['', ' ',None,12,False,'u1']:
 x=copy.deepcopy(two);x['units'][0]['share']=None;x['units'][1]['key']=key;add('global-key-before-unknown-'+repr(key),x,False)
for field,value in [('remaining',-1),('remaining',None),('remaining',True),('participation',1.01),('participation',-1),('share',False),('share',1.01),('share',-1),('other_allocation',{'C':0}),('other_allocation',{'C':float('inf')}),('other_allocation',{}),('counted',None),('extra',0)]:
 x=copy.deepcopy(base);x['units'][0][field]=value;add('invalid-unit-'+field+'-'+repr(value),x,False)
for field,value in [('A',-1),('B',True),('C',None)]:
 x=copy.deepcopy(base);x['units'][0]['counted'][field]=value;add('invalid-counted-'+field,x,False)
for field,value in [('B','A'),('other_candidates',['A']),('mode','future'),('selected_unit','missing'),('units',None),('extra',1)]:
 x=copy.deepcopy(base);x[field]=value;add('invalid-setting-'+field,x,False)
x=copy.deepcopy(base);x['units'][0]['all_candidate_total']=299;add('inconsistent-counted-field-total',x,False)
x=copy.deepcopy(base);x['units'][0]['counted'].pop('C');add('missing-counted-other-field',x,False)
x=copy.deepcopy(base);x['units'][0]['counted']['A']=10**1000;add('overflow-integer-counted',x,False)
x=copy.deepcopy(two);x['units'][0]['remaining']=0;x['units'][0]['share']=None;x['units'][1]['share']=-1;add('global-invalid-share-outside-zero-pool',x,False)
with tempfile.TemporaryDirectory(prefix='snn-la-independent-cli-') as td:
 for i,(name,x,valid,expected) in enumerate(cases):
  raw=(json.dumps(x,allow_nan=True)+'\n').encode();p=Path(td)/f'{i}.json';p.write_bytes(raw);r=subprocess.run([sys.executable,'-B','-S',str(C),str(p)],capture_output=True);o=strict(r.stdout)
  ck(not r.stderr and r.returncode==(0 if valid else 2),(name,r.returncode,r.stderr));ck((o['status']!='invalid-input')==valid,name)
  if expected:
   for k,v in expected.items():
    got=o['selected_only']['required_share'] if k=='selected_required' else o['selected_only']['status'] if k=='selected_status' else o['uniform']['bounded_shift'] if k=='uniform_shift' else o['uniform']['status'] if k=='uniform_status' else o['final_candidate_votes'] if k=='candidate_votes' else o['arithmetic_plurality_leaders'] if k=='leaders' else o[k]
    ck(abs(got-v)<1e-10 if type(v) in (float,int) else got==v,(name,k,got,v))
  proof.append({'name':name,'expected_valid':valid,'actual_exit':r.returncode,'input_raw_utf8':raw.decode(),'input_sha256':hashlib.sha256(raw).hexdigest(),'complete_strict_output':o,'output_sha256':hashlib.sha256(r.stdout).hexdigest(),'empty_stderr':True,'independent_expected_quantities':expected})
 for name,raw in [('duplicate-root-field',b'{"mode":"live","mode":"historical"}'),('duplicate-unit-field',json.dumps(base).replace('"remaining": 100','"remaining": 100, "remaining": 50').encode())]:
  p=Path(td)/(name+'.json');p.write_bytes(raw);r=subprocess.run([sys.executable,'-B','-S',str(C),str(p)],capture_output=True);o=strict(r.stdout);ck(r.returncode==2 and not r.stderr and o['status']=='invalid-input',name);proof.append({'name':name,'expected_valid':False,'actual_exit':2,'input_raw_utf8':raw.decode(),'complete_strict_output':o,'output_sha256':hashlib.sha256(r.stdout).hexdigest(),'empty_stderr':True})
result={'status':'pass','checks':N,'actual_CLI_cases':len(proof),'expected_invalid':sum(not p['expected_valid'] for p in proof),'calculator_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'producer_import_or_write':False,'network':False,'method':'Own actual subprocess CLI fixtures with hand-derived fixed counts/final denominators, selected-only/clipping/unknown/no-pool controls, named third-candidate lead and strict global invalid rejection. Actual full inputs and strict output bodies retained; this is deterministic arithmetic, not legal call or probability.','proofs':proof}
out=S/'data/coordinator-baseline-cli-review.json';b=(json.dumps(result,indent=2)+'\n').encode()
if '--check' in sys.argv:ck(out.read_bytes()==b)
else:out.write_bytes(b)
print(json.dumps({k:v for k,v in result.items() if k!='proofs'}))
