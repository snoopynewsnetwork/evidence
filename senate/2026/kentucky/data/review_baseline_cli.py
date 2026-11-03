"""Actual independent CLI cases, including fixed counts and early-return guards."""
from pathlib import Path
import copy,gzip,hashlib,json,math,subprocess,sys,tempfile
S=Path(__file__).resolve().parents[1];B=S/'data/baselines';C=B/'scripts/calculator.py';checks=0;proof=[]
def ck(v,msg=''):
 global checks
 checks+=1
 assert v,(checks,msg)
def strict(b):return json.loads(b,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def u(k,A,Bv,O,r,p,q):return {'key':k,'counted':{'A':A,'B':Bv,'other':{'C':O}},'remaining':r,'participation':p,'share':q,'other_allocation':{'C':1}}
base={'mode':'live','pair':['A','B'],'others':['C'],'other_scope':'named','assumptions':'Independent synthetic fixed-count illustration; no election forecast','target':0,'selected_unit':'u1','units':[u('u1',40,60,200,100,.8,.25)]}
cases=[]
def add(name,x,valid=True,expected=None):cases.append((name,copy.deepcopy(x),valid,expected))
add('counted-fixed-final-denominator-pair-tie-loses-full-field',base,True,{'final_pair_denominator':180,'final_all_candidate_denominator':400,'counted_A':40,'counted_B':60,'selected_required':.625,'baseline_net':-60,'full_boundary':2.25,'strict_plurality':False})
two=copy.deepcopy(base);two['units']=[u('u1',10,30,5,50,1,.2),u('u2',60,40,20,100,.5,.7)]
add('two-unit-other-fixed-threshold',two,True,{'final_pair_denominator':240,'final_all_candidate_denominator':315,'selected_required':.3,'baseline_net':-10,'uniform_shift':.05,'strict_plurality':False})
x=copy.deepcopy(two);x['target']=.01;add('one-point-pair-margin-final-denominator',x,True,{'selected_required':.324,'uniform_shift':.062,'strict_plurality':True})
x=copy.deepcopy(two);x['units'][0]['share']=None;add('selected-unknown-still-conditional',x,True,{'status':'unknown positive-pair-pool preferences','selected_required':.3})
x=copy.deepcopy(two);x['units'][1]['share']=None;add('other-unknown-retained',x,True,{'status':'unknown positive-pair-pool preferences','selected_status':'unknown other-unit assumptions'})
x=copy.deepcopy(base);x['units']=[u('u1',0,0,0,90,1,.99),u('u2',0,0,0,10,1,.01)];add('bounded-root-differs-from-linear',x,True,{'uniform_shift':5/9-.99,'strict_plurality':False})
for r,p,q in [(0,1,None),(100,0,None)]:
 x=copy.deepcopy(base);x['units']=[u('u1',40,20,0,r,p,q)];add('no-positive-pair-pool-'+str(r),x,True,{'uniform_status':'no-positive-pair-pool','selected_status':'no-positive-pair-pool'})
for A,Bv,status in [(100,0,'secured'),(0,100,'impossible')]:
 x=copy.deepcopy(base);x['units']=[u('u1',A,Bv,0,10,1,.5)];add('raw-selected-'+status,x,True,{'selected_status':status})
for target in [None,True,'0',-1.01,1.01,float('nan'),float('inf'),float('-inf')]:
 x=copy.deepcopy(base);x['target']=target;add('invalid-target-'+repr(target),x,False)
for key in ['', ' ',None,12,False,'u1']:
 x=copy.deepcopy(two);x['units'][0]['share']=None;x['units'][1]['key']=key;add('global-key-guard-before-unknown-'+repr(key),x,False)
for field,value in [('remaining',-1),('remaining',None),('remaining',True),('participation',1.01),('participation',-1),('share',False),('share',1.01),('share',-1),('other_allocation',{'C':0}),('other_allocation',{'C':float('inf')}),('other_allocation',{}),('counted',None),('extra',0)]:
 x=copy.deepcopy(base);x['units'][0][field]=value;add('invalid-unit-'+field+'-'+repr(value),x,False)
for field,value in [('A',-1),('B',True),('other',{'C':-1}),('other',{'wrong':0})]:
 x=copy.deepcopy(base);x['units'][0]['counted'][field]=value;add('invalid-counted-'+field+'-'+repr(value),x,False)
for field,value in [('pair',['A','A']),('others',['A']),('other_scope','eligible'),('mode','future'),('assumptions',''),('selected_unit','missing'),('units',[]),('extra',1)]:
 x=copy.deepcopy(base);x[field]=value;add('invalid-setting-'+field,x,False)
x=copy.deepcopy(base);x['units'][0]['counted_total']=299;add('inconsistent-full-counted-total',x,False)
x=copy.deepcopy(base);x['mode']='historical';add('historical-mode-cannot-consume-counted-votes',x,False)
x=copy.deepcopy(base);x['units'][0]['counted']['A']=10**1000;add('overflow-counted-integer',x,False)
x=copy.deepcopy(two);x['units'][0]['remaining']=0;x['units'][0]['share']=None;x['units'][1]['share']=-1;add('global-share-guard-before-no-pool',x,False)
with tempfile.TemporaryDirectory(prefix='snn-ky-independent-cli-') as td:
 for i,(name,x,valid,expect) in enumerate(cases):
  raw=(json.dumps(x,allow_nan=True)+'\n').encode();p=Path(td)/f'{i}.json';p.write_bytes(raw);r=subprocess.run([sys.executable,'-B','-S',str(C),str(p)],capture_output=True);o=strict(r.stdout)
  ck(r.stderr==b'' and r.returncode==(0 if valid else 2),name);ck((o['status']!='invalid-input')==valid,name)
  if expect:
   for key,value in expect.items():
    got=(o['selected_only']['required_A_share'] if key=='selected_required' else o['selected_only']['status'] if key=='selected_status' else o['baseline_final_pair_net'] if key=='baseline_net' else o['selected_only']['full_field_strict_plurality_boundary_A_share'] if key=='full_boundary' else o['uniform']['clipped_share_shift'] if key=='uniform_shift' else o['uniform']['status'] if key=='uniform_status' else o['uniform']['full_field_at_pair_target']['strict_A_plurality'] if key=='strict_plurality' else o[key])
    ck((isinstance(got,(int,float)) and abs(got-value)<1e-10) if type(value) in (int,float) else got==value,(name,key,got,value))
  proof.append({'name':name,'expected_valid':valid,'actual_exit':r.returncode,'input_raw_sha256':hashlib.sha256(raw).hexdigest(),'input_raw_utf8':raw.decode(),'complete_strict_output':o,'strict_output_sha256':hashlib.sha256(r.stdout).hexdigest(),'empty_stderr':True,'expected_quantities':expect})
 # JSON grammar/identity collisions must fail through the real CLI as well.
 for name,raw in [('duplicate-root-field',b'{"mode":"live","mode":"historical"}'),('duplicate-nested-unit-field',json.dumps(base).replace('"remaining": 100','"remaining": 100, "remaining": 50').encode())]:
  p=Path(td)/(name+'.json');p.write_bytes(raw);r=subprocess.run([sys.executable,'-B','-S',str(C),str(p)],capture_output=True);ck(r.returncode==2 and not r.stderr and strict(r.stdout)['status']=='invalid-input',name);proof.append({'name':name,'expected_valid':False,'actual_exit':2,'input_raw_sha256':hashlib.sha256(raw).hexdigest(),'input_raw_utf8':raw.decode(),'complete_strict_output':strict(r.stdout),'strict_output_sha256':hashlib.sha256(r.stdout).hexdigest(),'empty_stderr':True})
result={'status':'pass','checks':checks,'actual_CLI_cases':len(proof),'expected_invalid':sum(not p['expected_valid'] for p in proof),'calculator_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'producer_import_or_write':False,'network':False,'method':'Own synthetic exact expectations; real subprocess CLI, strict JSON/exits/empty stderr. Counted fixed, final denominators, selected-only full-field boundary, pair tie versus plurality, clipped roots, unknown/no-pool and global rejection before early returns.','proofs':proof}
out=D=S/'data/coordinator-baseline-cli-review.json';body=(json.dumps(result,indent=2)+'\n').encode()
if '--check' in sys.argv:ck(out.read_bytes()==body)
else:out.write_bytes(body)
print(json.dumps({k:v for k,v in result.items() if k!='proofs'}))
