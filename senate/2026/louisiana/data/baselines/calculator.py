"""Offline conditional pair arithmetic; no probabilities or legal election calls. See source/SCHEMA.md."""
import json,math,sys
class Invalid(ValueError):pass
def require(ok,message):
 if not ok:raise Invalid(message)
def num(x,label,lo=0,hi=None):
 require(type(x) in (int,float) and math.isfinite(x),label+' must be finite numeric')
 require(x>=lo and (hi is None or x<=hi),label+' outside bounds');return float(x)
def add(a):
 try:x=math.fsum(a)
 except (OverflowError,ValueError):raise Invalid('aggregate overflow')
 require(math.isfinite(x),'aggregate overflow');return x
def obj(x,required,optional=()):
 require(type(x)==dict,'expected object');require(set(required)<=set(x),'missing fields: '+str(set(required)-set(x)));require(set(x)<=set(required)|set(optional),'unsupported fields: '+str(set(x)-set(required)-set(optional)))
def identity(x):require(type(x)==str and bool(x.strip()),'identity must be nonblank string');return x
def validate(x):
 obj(x,('mode','A','B','other_candidates','target','units'),('selected_unit','assumption'))
 require(x['mode'] in ('historical','live'),'unsupported mode');A=identity(x['A']);B=identity(x['B']);require(type(x['other_candidates'])==list,'other_candidates must be array');names=[A,B]+[identity(n) for n in x['other_candidates']];require(len(names)==len(set(names)),'candidate identity collision')
 target=num(x['target'],'target',-1,1);require(type(x['units'])==list,'units must be array');keys=[]
 # Complete global identity validation before any arithmetic or unknown/no-pool branch.
 for u in x['units']:
  require(type(u)==dict,'unit must be object');require('key' in u,'missing unit key');keys.append(identity(u['key']))
 require(len(keys)==len(set(keys)),'duplicate unit keys');sel=x.get('selected_unit');require(sel is None or type(sel)==str and sel in keys,'selected_unit must exist')
 units=[]
 for u in x['units']:
  if x['mode']=='historical':
   obj(u,('key','volume','participation','share','other_allocation'),('all_candidate_total',));v=num(u['volume'],'volume');counted={n:0.0 for n in names}
  else:
   obj(u,('key','counted','remaining','participation','share','other_allocation'),('all_candidate_total',));v=num(u['remaining'],'remaining');require(type(u['counted'])==dict and set(u['counted'])==set(names),'counted must contain complete distinct candidate field');counted={n:num(u['counted'][n],'counted '+n) for n in names}
  p=num(u['participation'],'participation',0,1);s=u['share'];s=None if s is None else num(s,'share',0,1)
  require(type(u['other_allocation'])==dict and set(u['other_allocation'])==set(names[2:]),'other allocation requires complete field')
  alloc={n:num(a,'other allocation',0,1) for n,a in u['other_allocation'].items()}
  allocsum=add(alloc.values());require((not names[2:] and p==1) or (names[2:] and (abs(allocsum-1)<1e-12 or (v*(1-p)==0 and allocsum==0))),'other allocations must sum to one; no other field requires participation=1')
  C=add(counted.values());P=add([counted[A],counted[B]]);U=v*p;O=v*(1-p)
  if 'all_candidate_total' in u:
   t=num(u['all_candidate_total'],'all_candidate_total');require(t>=P,'all-candidate total smaller than pair');require(abs(t-(v if x['mode']=='historical' else C))<=1e-10*max(1,t),'all-candidate total unbalanced')
  units.append(dict(key=u['key'],counted=counted,remaining=v,pair_remaining=U,other_remaining=O,share=s,participation=p,other_allocation=alloc))
 add([v for u in units for v in [*u['counted'].values(),u['remaining']]])
 return units,names,target,sel

def calculate(x):
 units,names,t,selected=validate(x);A,B=names[:2];others=names[2:];CP=add(u['counted'][A]+u['counted'][B] for u in units);CL=add(u['counted'][A]-u['counted'][B] for u in units);U=add(u['pair_remaining'] for u in units);P=add([CP,U]);F=add(add(u['counted'].values())+u['remaining'] for u in units);unknown=[u['key'] for u in units if u['pair_remaining']>0 and u['share'] is None];base= None if unknown else add([CL]+[u['pair_remaining']*(2*u['share']-1) for u in units if u['pair_remaining']>0]);target=t*P
 out=dict(status='unknown-preference' if unknown else 'ok',mode=x['mode'],A=A,B=B,other_candidates=others,assumption=x.get('assumption'),target_pair_margin=t,counted_pair_votes=CP,counted_lead=CL,remaining_pair_votes=U,final_pair_votes=P,final_all_candidate_votes=F,unknown_units=unknown,baseline_lead=base,baseline_pair_margin=base/P if P>0 and base is not None else None,baseline_all_candidate_margin=base/F if F>0 and base is not None else None,no_positive_pool=U==0,units=units)
 out['fixed_target_status']='unknown' if base is None else 'met' if base>=target else 'below'
 candidate={n:add(u['counted'][n] for u in units) for n in names}
 for n in others:candidate[n]=add([candidate[n]]+[u['other_remaining']*u['other_allocation'][n] for u in units])
 if not unknown:
  candidate[A]=add([candidate[A]]+[u['pair_remaining']*u['share'] for u in units if u['pair_remaining']>0]);candidate[B]=add([candidate[B]]+[u['pair_remaining']*(1-u['share']) for u in units if u['pair_remaining']>0]);out['final_candidate_votes']=candidate;out['arithmetic_plurality_leaders']=[n for n,v in candidate.items() if v==max(candidate.values())] if candidate else []
 else:out['final_candidate_votes']=dict(candidate,**{A:None,B:None});out['arithmetic_plurality_leaders']=None
 if U==0:out['uniform']={'status':'no-positive-pool','unbounded_shift':None,'bounded_shift':None,'fixed_target_status':out['fixed_target_status']}
 elif unknown:out['uniform']={'status':'unknown-preference','unbounded_shift':None,'bounded_shift':None}
 else:
  unbounded=(target-base)/(2*U);low=CL-U;high=CL+U
  if target<low:out['uniform']=dict(status='already-secured',unbounded_shift=unbounded,bounded_shift=None,raw_target_lead=target,minimum_possible_lead=low)
  elif target>high:out['uniform']=dict(status='impossible',unbounded_shift=unbounded,bounded_shift=None,raw_target_lead=target,maximum_possible_lead=high)
  else:
   def net(d):return add([CL]+[u['pair_remaining']*(2*min(1,max(0,u['share']+d))-1) for u in units if u['pair_remaining']>0])
   lo=-1.0;hi=1.0
   for _ in range(90):
    mid=(lo+hi)/2
    if net(mid)<target:lo=mid
    else:hi=mid
   d=(lo+hi)/2;con=[]
   for u in units:
    q=None if u['share'] is None else min(1,max(0,u['share']+d));V=u['pair_remaining'];v=None if q is None else V*(2*q-1)
    con.append(dict(key=u['key'],pair_volume=V,pair_weight=V/U,all_volume_weight=u['remaining']/add(a['remaining'] for a in units) if add(a['remaining'] for a in units)>0 else None,participation=u['participation'],baseline_share=u['share'],target_share=q,target_net_votes=v,baseline_net_votes=None if u['share'] is None else V*(2*u['share']-1),net_gain=None if q is None else 2*V*(q-u['share']),one_share_point_net_votes=.02*V,clipped=q is not None and q!=u['share']+d))
   out['uniform']=dict(status='feasible',unbounded_shift=unbounded,bounded_shift=d,achieved_lead=net(d),residual=net(d)-target,contributions=con)
 if selected is not None:
  unit=next(u for u in units if u['key']==selected);otherunknown=[u['key'] for u in units if u['key']!=selected and u['pair_remaining']>0 and u['share'] is None];V=unit['pair_remaining']
  if otherunknown:out['selected_only']=dict(status='unknown-other-units',unknown_units=otherunknown,required_share=None)
  else:
   fixed=add([CL]+[u['pair_remaining']*(2*u['share']-1) for u in units if u['key']!=selected and u['pair_remaining']>0])
   if V==0:out['selected_only']=dict(status='no-positive-pool',required_share=None,fixed_lead=fixed,fixed_target_status='met' if fixed>=target else 'below')
   else:
    req=(target-fixed+V)/(2*V);out['selected_only']=dict(status='already-secured' if req<0 else 'impossible' if req>1 else 'feasible',required_share=req,fixed_other_and_counted_lead=fixed,selected_pair_volume=V,final_pair_target_lead=target)
 # Prevent derived overflow in every result branch, including unknown outputs.
 def finite(z):
  if isinstance(z,float):require(math.isfinite(z),'derived overflow')
  elif isinstance(z,dict):
   for v in z.values():finite(v)
  elif isinstance(z,list):
   for v in z:finite(v)
 finite(out);return out

def pairs(a):
 d={}
 for k,v in a:
  require(k not in d,'duplicate JSON object field: '+k);d[k]=v
 return d

def main():
 try:
  require(len(sys.argv)==2,'usage: calculator.py input.json or -');s=sys.stdin.read() if sys.argv[1]=='-' else open(sys.argv[1]).read();x=json.loads(s,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(Invalid('nonfinite JSON token: '+s)));o=calculate(x);print(json.dumps(o,allow_nan=False,separators=(',',':')))
 except (Invalid,json.JSONDecodeError,OSError,OverflowError,TypeError,ValueError) as e:
  print(json.dumps({'status':'invalid-input','error':str(e)},allow_nan=False));return 2
 return 0
if __name__=='__main__':sys.exit(main())
