"""Offline conditional arithmetic. Usage: python calculator.py input.json"""
import json,sys,math
class Invalid(ValueError):pass
def need(ok,msg):
 if not ok:raise Invalid(msg)
def num(x,label,lo=None,hi=None):
 need(type(x) in (int,float),label+' must be numeric (not bool/null/text)')
 try:need(math.isfinite(x),label+' must be finite')
 except OverflowError:raise Invalid(label+' overflow')
 need(lo is None or x>=lo,label+' below bound');need(hi is None or x<=hi,label+' above bound');return x
def obj(x,label):need(type(x) is dict,label+' must be an object');return x
def key(x,label):need(type(x) is str and bool(x.strip()),label+' must be a nonblank string');return x
def closed(x,allowed,label):need(set(x)<=set(allowed),label+' unsupported fields: '+str(set(x)-set(allowed)))
def add(xs,label):
 try:y=math.fsum(xs)
 except (OverflowError,ValueError):raise Invalid(label+' overflow')
 return num(y,label)
def pairs(p):
 d={}
 for k,v in p:
  need(k not in d,'duplicate JSON object field: '+k);d[k]=v
 return d
def calculate(x):
 obj(x,'input');closed(x,['mode','pair','others','other_scope','units','target','selected_unit','assumptions'],'input')
 need(x.get('mode') in ('historical','live'),'unsupported mode')
 need(type(x.get('assumptions')) is str and bool(x['assumptions'].strip()),'explicit assumptions required')
 pair=x.get('pair');need(type(pair) is list and len(pair)==2,'pair must have two identities')
 ids=[key(c,'candidate identity') for c in pair];others=x.get('others');need(type(others) is list,'others must be a list')
 ids += [key(c,'other candidate identity') for c in others];need(len(ids)==len(set(ids)),'candidate identity collision')
 need(x.get('other_scope') in ('named','unresolved'),'unsupported other_scope')
 target=num(x.get('target'),'target',-1,1)
 units=x.get('units');need(type(units) is list and len(units)>0,'units must be a nonempty list')
 seen=set();us=[]
 # Complete global validation precedes any unknown/selection/no-pool branch.
 for i,u in enumerate(units):
  obj(u,'unit');closed(u,['key','counted','counted_total','remaining','participation','share','other_allocation'],'unit')
  k=key(u.get('key'),'unit key');need(k not in seen,'duplicate unit key: '+k);seen.add(k)
  c=obj(u.get('counted'),'counted');closed(c,['A','B','other'],'counted')
  ca=num(c.get('A'),'counted A',0);cb=num(c.get('B'),'counted B',0)
  co=obj(c.get('other'),'counted other');need(set(co)==set(others),'counted other identities must match others')
  for n,v in co.items():num(v,'counted other '+n,0)
  ct=add([ca,cb,*co.values()],'counted total')
  if 'counted_total' in u:need(num(u['counted_total'],'supplied counted_total',0)==ct,'supplied counted total disagrees with complete field')
  r=num(u.get('remaining'),'remaining',0);p=num(u.get('participation'),'participation',0,1)
  q=u.get('share');need('share' in u,'share field required (null is explicitly unknown)')
  if q is not None:num(q,'share',0,1)
  al=obj(u.get('other_allocation'),'other_allocation');need(set(al)==set(others),'other allocation identities must match others')
  for n,v in al.items():num(v,'other allocation '+n,0,1)
  if al:need(abs(add(al.values(),'allocation sum')-1)<1e-12,'unbalanced supplied-other allocation')
  need(r*(1-p)==0 or bool(al),'positive nonpair pool requires supplied other allocation')
  if x['mode']=='historical':need(ct==0,'historical counted must be zero')
  us.append(dict(key=k,A=ca,B=cb,other=co,counted_total=ct,remaining=r,pair_pool=r*p,share=q,allocation=al))
 selected=x.get('selected_unit')
 if 'selected_unit' in x:need(key(selected,'selected_unit') in seen,'selected key does not exist')
 pool=add([u['remaining'] for u in us],'remaining pool');pp=add([u['pair_pool'] for u in us],'pair pool')
 countedA=add([u['A'] for u in us],'counted A');countedB=add([u['B'] for u in us],'counted B')
 finalpair=add([countedA,countedB,pp],'final pair');finalall=add([u['counted_total']+u['remaining'] for u in us],'final all candidate')
 net=countedA-countedB;goal=target*finalpair;num(goal,'target net')
 base=dict(status='ok',mode=x['mode'],pair=pair,others=others,other_scope=x['other_scope'],assumptions=x['assumptions'],target_pair_margin=target,
  counted_A=countedA,counted_B=countedB,remaining_all_candidate_pool=pool,remaining_pair_pool=pp,final_pair_denominator=finalpair,
  final_all_candidate_denominator=finalall,pair_share_defined=finalpair>0,no_positive_pool=pool==0,no_positive_pair_pool=pp==0,
  legal_outcome='not determined by pair arithmetic',units=us)
 otherfinal={n:add([u['other'][n]+(u['remaining']-u['pair_pool'])*u['allocation'][n] for u in us],'final other') for n in others}
 def field(A):
  votes={pair[0]:A,pair[1]:finalpair-A,**otherfinal}
  return dict(candidate_votes=votes,strict_A_plurality='unresolved other identities' if x['other_scope']=='unresolved' else all(A>v for n,v in votes.items() if n!=pair[0]),
    A_share_all_candidate=A/finalall if finalall else None,pair_net_over_all_candidate=(2*A-finalpair)/finalall if finalall else None,
    legal_outcome='conditional supplied-field comparison only; final ballot/eligible identities/rules not determined')
 unknown=[u['key'] for u in us if u['pair_pool']>0 and u['share'] is None]
 base['unknown_preference_units']=unknown
 if selected is not None:
  u=next(u for u in us if u['key']==selected);unknown_other=[k for k in unknown if k!=selected]
  if unknown_other:base['selected_only']=dict(status='unknown other-unit assumptions',unknown_units=unknown_other)
  else:
   fixed=add([net,*[v['pair_pool']*(2*v['share']-1) for v in us if v['key']!=selected and v['pair_pool']>0]],'selected fixed net')
   if u['pair_pool']==0:base['selected_only']=dict(status='no-positive-pair-pool',fixed_target_status='secured' if fixed>=goal else 'impossible',required_A_share=None)
   else:
    req=(goal-fixed+u['pair_pool'])/(2*u['pair_pool']);num(req,'selected required share')
    base['selected_only']=dict(status='secured' if req<0 else 'impossible' if req>1 else 'feasible',required_A_share=req,
      feasible_A_share=max(0,min(1,req)),all_other_units_fixed=True,fixed_net_votes=fixed)
    fixedA=add([countedA,*[v['pair_pool']*v['share'] for v in us if v['key']!=selected and v['pair_pool']>0]],'selected fixed A')
    if 0<=req<=1:base['selected_only']['field_at_pair_requirement']=field((finalpair+goal)/2)
    if x['other_scope']=='named':
     boundary=max([(finalpair/2-fixedA)/u['pair_pool'],*[(v-fixedA)/u['pair_pool'] for v in otherfinal.values()]])
     num(boundary,'full field boundary')
     base['selected_only']['full_field_strict_plurality_boundary_A_share']=boundary
     base['selected_only']['full_field_boundary_status']='secured' if boundary<0 else 'impossible' if boundary>=1 else 'feasible, requires strictly above boundary'
    else:base['selected_only']['full_field_boundary_status']='unresolved other identities'
 if unknown:
  base['status']='unknown positive-pair-pool preferences';return base
 def evaluate(shift):
  return add([net,*[u['pair_pool']*(2*max(0,min(1,u['share']+shift))-1) for u in us if u['pair_pool']>0]],'final net')
 current=evaluate(0);base['baseline_final_pair_net']=current;base['baseline_final_pair_margin']=current/finalpair if finalpair else None
 base['fixed_target_status']='secured' if current>=goal else 'below target'
 finalA=add([countedA,*[u['pair_pool']*u['share'] for u in us if u['pair_pool']>0]],'final A');finalB=finalpair-finalA
 base['baseline_final_candidate_votes']={pair[0]:finalA,pair[1]:finalB,**otherfinal}
 base['baseline_full_field_A_plurality']='unresolved other identities' if x['other_scope']=='unresolved' else (all(finalA>v for n,v in base['baseline_final_candidate_votes'].items() if n!=pair[0]))
 if pp==0:
  base['uniform']=dict(status='no-positive-pair-pool',unbounded_share_shift=None,clipped_share_shift=None,residual=current-goal);return base
 delta=(goal-current)/(2*pp);num(delta,'unbounded share shift')
 lo=evaluate(-1);hi=evaluate(1)
 if goal<lo or goal>hi:
  base['uniform']=dict(status='secured at every feasible share' if goal<lo else 'impossible bounded target',unbounded_share_shift=delta,clipped_share_shift=None,minimum_net=lo,maximum_net=hi);return base
 left=-1.;right=1.
 for _ in range(100):
  mid=(left+right)/2
  if evaluate(mid)<goal:left=mid
  else:right=mid
 d=(left+right)/2;achieved=evaluate(d)
 for u in us:
  u['pair_weight']=u['pair_pool']/pp
  u['baseline_pair_net_contribution']=u['pair_pool']*(2*u['share']-1) if u['pair_pool'] else 0
  u['one_A_share_point_net_votes']=.02*u['pair_pool']
  u['target_A_share']=max(0,min(1,u['share']+d)) if u['share'] is not None else None
  u['target_pair_net_contribution']=u['pair_pool']*(2*u['target_A_share']-1) if u['pair_pool'] else 0
  u['net_gain']=u['target_pair_net_contribution']-u['baseline_pair_net_contribution']
 base['uniform']=dict(status='feasible',unbounded_share_shift=delta,clipped_share_shift=d,clipping_active=any(u['share'] is not None and not 0<=u['share']+d<=1 for u in us if u['pair_pool']>0),
  achieved_pair_net=achieved,residual=achieved-goal,minimum_net=lo,maximum_net=hi)
 base['uniform']['full_field_at_pair_target']=field((finalpair+goal)/2)
 base['uniform']['full_field_quantity_basis']='Pair target denominator identity; numerical clipped-root contributions/residual reported separately'
 return base
def main():
 try:
  need(len(sys.argv)==2,'usage: calculator.py input.json')
  with open(sys.argv[1]) as f:x=json.load(f,object_pairs_hook=pairs,parse_constant=lambda s: (_ for _ in ()).throw(Invalid('nonfinite JSON token '+s)))
  result=calculate(x)
  print(json.dumps(result,allow_nan=False,sort_keys=True));return 0
 except (Invalid,ValueError,OverflowError,TypeError,KeyError,ZeroDivisionError,RecursionError,OSError) as e:
  print(json.dumps(dict(status='invalid-input',error=str(e)),allow_nan=False));return 2
if __name__=='__main__':sys.exit(main())
