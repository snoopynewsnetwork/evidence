"""Independent final membership, whole immutable history and unchanged source contract bridge."""
from pathlib import Path
import gzip,hashlib,io,json,tarfile
S=Path(__file__).resolve().parents[1];D=S/'data';T=D/'turnout';B=D/'baselines';R=Path.cwd();N=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def ck(v,label=''):
 global N
 N+=1
 assert v,label
def load(p):return json.loads(p.read_bytes())
def normalize(p):
 p=Path(p)
 return p.relative_to(S.relative_to(R)).as_posix() if p.parts[:3]==('senate','2026','louisiana') else p.as_posix()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)}
seals=[]
for root,num,digest,extra in [(T,733,'dffc8ddefc7f92f37b7c19e7a3c16c7d905c928f48e01f7d4e3f7edc2b96d69f',['turnout.md','data/county-turnout.csv']),(B,1607,'22aa501bcbcf9a6b99849e41859cf14a7d3216191e22d0f6dd68eced41fe897d',['county-partisanship.md','data/county-baselines.csv'])]:
 m=load(root/'asset-manifest.json');rows=m['assets'];ck(len(rows)==num and sha((root/'asset-manifest.json').read_bytes())==digest,'exact final manifest')
 ck({normalize(z['path']) for z in rows}=={str(p.relative_to(S)) for p in root.rglob('*') if p.is_file() and p!=root/'asset-manifest.json'}|set(extra),'complete final membership excludes only self')
 for z in rows:
  a=pin(S/normalize(z['path']));ck(a['bytes']==z['bytes'] and a['sha256']==z['sha256'],'whole final sealed file');ck(a['bytes']<40000000,'strict bound')
 seals.append(pin(root/'asset-manifest.json'))
captures={};changed=[];H=T/'history/packaging-repair'
for role,count in [('own',645),('peer',1608)]:
 idx=load(H/(role+'-prior-inventory.json'));ck(len(idx['members'])==count,'whole capture count');raw=b''
 for part in idx['ordered_archive_parts']:
  b=(T/part['path']).read_bytes();ck(sha(b)==part['sha256'] and len(b)==part['bytes'],'ordered archive part');raw+=b
 ck(sha(raw)==idx['archive_sha256'],'whole ordered archive hash')
 with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tf:bodies={normalize(m.name):tf.extractfile(m).read() for m in tf if m.isfile()}
 ck(set(bodies)=={normalize(z['path']) for z in idx['members']},'complete exact archive membership')
 for z in idx['members']:
  p=normalize(z['path']);b=bodies[p];ck(len(b)==z['bytes'] and sha(b)==z['sha256'],'whole captured oldpath')
  if role=='peer':ck((S/p).read_bytes()==b,'actual final peer bytes still frozen')
  elif (S/p).read_bytes()!=b:changed.append(p)
 oldmf=json.loads(bodies['data/'+('turnout' if role=='own' else 'baselines')+'/asset-manifest.json'])
 for z in oldmf['assets']:
  b=bodies[normalize(z['path'])];ck(len(b)==z['bytes'] and sha(b)==z['sha256'],'every old manifest target reconstructed')
 captures[role]=(idx,bodies)
ck(len(captures['own'][1])==645 and len(captures['own'][1])-len(json.loads(captures['own'][1]['data/turnout/asset-manifest.json'])['assets'])==2,'prior own manifest excluded self and audit; both whole bodies preserved')
for p in ['data/turnout/priority-set.json','data/county-turnout.csv','data/turnout/source/original-first-witness.json','data/turnout/source/acquired-original-first-witness.json']:
 ck((S/p).read_bytes()==captures['own'][1][p],'source contract/CSV/original witnesses byte unchanged')
c=load(T/'priority-set.json');ck(len(c['historical_native_constituents'])==3933 and len(c['ordered_priority_keys'])==1516 and len(c['ordered_remainder_keys'])==2417 and len(c['all_parishes'])==64 and c['current_native_dispatch']==[] and c['coordinator_acceptance'] is False,'historical complete current unapproved')
f=load(B/'original-freeze.json')
for a in f['assets']:
 b=(B/a['path']).read_bytes();ck(sha(b)==a['sha256'] and len(b)==a['bytes'],'complete original-only baseline frozen body')
peer=load(T/'repair-proof/captured-final-peer-source-verification.json');ck(peer['status']=='pass' and peer['differences']==[],'qualified source-only peer proof')
result={'status':'pass_final_membership_history_originalfirst_and_unchanged_contract','checks':N,'final_producer_seals':seals,'complete_old_turnout_bodies':645,'complete_final_peer_bodies':1608,'original_baseline_frozen_bodies':len(f['assets']),'prior_own_manifest_packaging_exception':'643 targets excluded itself and final-audit.json; all645 prior bodies preserved. Correct final733 targets include audit, seal, history and validation and exclude only manifest.','changed_old_paths':changed,'current_contract_and_original_CSV_byte_unchanged':True,'source_core_peer_equality_only':True,'current_native_dispatch':[],'coordinator_acceptance':False,'producer_write':False,'network':False,'scope':'Complete immutable captures verified by exact oldpath+whole SHA and every old manifest target, never comparing older witness hashes to rewritten current bodies. Final peer source freeze verified independently. No future or calculator/scenario/outcome equality inferred.'}
(D/'coordinator-turnout-reciprocal-final-review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
