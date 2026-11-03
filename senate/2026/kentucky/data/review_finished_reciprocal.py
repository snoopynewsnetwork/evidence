"""Coordinator whole-body bridge; reads immutable captures and final producer seals only."""
from pathlib import Path
import gzip,hashlib,json
S=Path(__file__).resolve().parents[1];D=S/'data';T=D/'turnout';B=D/'baselines';n=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def ck(v,label):
 global n
 n+=1
 assert v,label
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)}
seals=[]
for root,extras,digest,count in [(T,['turnout.md','data/county-turnout.csv'],'b72ab95194d9e748a7c15163a9f5eb13db1ff0596fc9e4d1d77fb84a9036946f',5008),(B,['county-partisanship.md','data/county-baselines.csv'],'9415e66193d21382abc5bc9f5ab97b3943ce2498c64e33acb3aade7dfdf5b2a4',1971)]:
 m=load(root/'asset-manifest.json');rows=m['files'];ck(len(rows)==count and sha((root/'asset-manifest.json').read_bytes())==digest,'final manifest pin')
 actual={str(p.relative_to(S)) for p in root.rglob('*') if p.is_file() and p!=root/'asset-manifest.json'}|set(extras)
 ck(actual=={r['path'] for r in rows},'complete final membership')
 for r in rows:ck(pin(S/r['path'])==r,'whole final sealed body');ck(r['bytes']<40000000,'strict object bound')
 seals.append(pin(root/'asset-manifest.json'))
caps={};changed=[]
for role,want in [('own-pre-resume',2735),('peer-final',1972)]:
 idx=load(T/'reciprocal'/role/'index.json');ck(len(idx['files'])==want,'complete capture count');bodies={}
 for r in idx['files']:
  if 'captured_body' in r:
   z=(S/r['captured_body']).read_bytes();ck(sha(z)==r['captured_stored_sha256'] and len(z)==r['captured_stored_bytes'],'stored complete capture');body=gzip.decompress(z)
  else:body=(S/r.get('immutable_whole_reference',r.get('immutable_original_reference'))).read_bytes()
  ck(len(body)==r['bytes'] and sha(body)==r['sha256'],'whole oldpath bytes');bodies[r['path']]=body
  if role=='own-pre-resume' and sha((S/r['path']).read_bytes())!=r['sha256']:changed.append(r['path'])
  if role=='peer-final':ck((S/r['path']).read_bytes()==body,'captured final peer still frozen')
 oldmf=json.loads(bodies['data/'+('turnout' if role=='own-pre-resume' else 'baselines')+'/asset-manifest.json'])
 for r in oldmf['files']:ck(sha(bodies[r['path']])==r['sha256'] and len(bodies[r['path']])==r['bytes'],'every historical manifest target reconstructed')
 caps[role]=(idx,bodies)
old=json.loads(caps['own-pre-resume'][1]['data/turnout/priority-set.json']);new=load(T/'priority-set.json')
meta={'peer_agreement_status','captured_final_source_core_review'}
ck({k:v for k,v in old.items() if k not in meta}=={k:v for k,v in new.items() if k not in meta},'full contract every nonreview field unchanged')
ck((S/'data/county-turnout.csv').read_bytes()==caps['own-pre-resume'][1]['data/county-turnout.csv'],'original full CSV byte exact')
ck(all(new[k] is None for k in ['order','top15','min80','priority','remainder']) and new['dispatch_keys']==new['ordered_priority_keys']==[],'canonical native NULL empty dispatch')
ck(len(new['coverage'])==120 and len({r['fips'] for r in new['coverage']})==120,'all120 full parent packets')
review=load(T/'reciprocal/review.json');ck(review['all_original_numeric_source_order_null_mask_admin_fields_unchanged'] is True and review['coordinator_acceptance'] is False,'qualified reciprocal review')
out={'status':'pass_complete_final_seals_and_immutable_oldbody_bridge','checks':n,'final_producer_seals':seals,'complete_old_turnout_bodies':2735,'complete_final_peer_bodies':1972,'changed_old_paths':changed,'contract_metadata_exceptions':sorted(meta),'canonical_native_priority':None,'dispatch_keys':[],'scope':'Whole old body and every old manifest target verified at exact oldpath+SHA from immutable capture, never newer rewritten bodies. Full current contract except explicit peer-review metadata and full original CSV unchanged. Existing independent original/math/CLI/history checks retain their exact original-phase scope. No equality of future peer outcomes/calculators/scenarios inferred.','producer_write':False,'network':False}
(D/'coordinator-turnout-reciprocal-final-review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
