"""Independent complete read-only authority replay. Authority itself is path-only."""
from common import *
import tarfile,collections,itertools,time

def checked(pin):
 p=STATE/pin['path'];b=p.read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'],('raw pin',str(p));return b

def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):
   if isinstance(v,(dict,list)):yield from walk(v,p+'/'+str(i))

def main():
 t=time.time();a=strict(AUTH.read_bytes());p=strict((STATE/'data/turnout/priority-set.json').read_bytes())
 for r in a['complete_root_field_semantics']:assert sem(p[r['pointer'][1:]])==r['full_recursive_semantic_sha256']
 for pin in a['frozen_file_pins']:checked(pin)
 for pin in [a['frozen_contract']]+a['producer_seals']+a['independent_coordinator_reviews']:checked(pin)
 for pin in a['complete_source_companion_files']:
  checked(pin);x=structured(STATE/pin['path'],pin['format']);assert len(x)==pin['complete_length'];assert sem(x)==pin['full_semantic_sha256'],('companion',pin['path'])
 print('all fixed files and complete companions PASS',flush=True)
 for pin in a['complete_opaque_invalid_fixture_files']:checked(pin)
 tar_members=0
 for r in a['historical_full_body_resolvers']:
  raw=gzip.decompress(checked(r['storage']['file']));assert len(raw)==r['bytes'] and sha(raw)==r['sha256']
  if tarfile.is_tarfile(io.BytesIO(raw)):
   with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
    for m in tar:
     if m.isfile():assert len(tar.extractfile(m).read())==m.size;tar_members+=1
 print('all whole historical gzip/tar bodies PASS',flush=True)
 refs=0;current=None;expected=None;counts=collections.Counter()
 for part in a['complete_source_object_reference_bodies']:
  raw=gzip.decompress(checked(part));assert len(raw)==part['complete_reconstructed_bytes'] and sha(raw)==part['complete_reconstructed_sha256']
  rows=[strict(s) for s in raw.splitlines()];assert len(rows)==part['complete_object_count']
  for r in rows:
   if r['file']!=current:
    if expected is not None:assert next(expected,None) is None,('remaining refs',current)
    current=r['file'];x=structured(STATE/current)
    if current=='data/turnout/priority-set.json':expected=iter((('/'+k,v) for k,v in x.items()))
    else:expected=walk(x)
   ptr,value=next(expected);assert ptr==r['pointer'],('order',current,ptr,r['pointer']);assert sem(value)==r['full_recursive_semantic_sha256'],('semantic',current,ptr)
   refs+=1;counts[current]+=1
  print('partition',refs,flush=True)
 assert next(expected,None) is None
 assert refs==a['complete_source_object_count'] and dict(counts)==a['source_objects_by_file']
 # Original paths with source-relative spelling bind to the producer source roots.
 roles=0
 for r in a['complete_original_entity_roles']:
  candidates=[STATE/r['path'],STATE/'data/turnout'/r['path'],STATE/'data/baselines'/r['path']]
  paths=[p for p in candidates if p.is_file() and sha(p.read_bytes())==r['stored_sha256']];assert paths,('original',r['path'])
  b=paths[0].read_bytes();raw=gzip.decompress(b) if paths[0].suffix=='.gz' else b
  assert len(b)==r['stored_bytes'] and len(raw)==r['raw_bytes'] and sha(raw)==r['raw_sha256'];roles+=1
  for rp in r.get('receipts',[]):
   paths=[STATE/rp,STATE/'data/turnout'/rp,STATE/'data/baselines'/rp];assert any(p.is_file() for p in paths),('receipt',rp)
 result={'pass':True,'authority_path':str(AUTH.relative_to(STATE)),'root_semantics':len(a['complete_root_field_semantics']),'fixed_files':len(a['frozen_file_pins']),'complete_companions':len(a['complete_source_companion_files']),'ordered_recursive_references':refs,'partitions':len(a['complete_source_object_reference_bodies']),'whole_historical_resolvers':len(a['historical_full_body_resolvers']),'tar_members_read':tar_members,'original_entity_roles':roles,'seconds':time.time()-t,'scope':'Full frozen source authority, no producer imports or writes. Authority body/digest not retained.'}
 save(ROOT/'proof/authority-replay.json',result);print(result)
if __name__=='__main__':main()
