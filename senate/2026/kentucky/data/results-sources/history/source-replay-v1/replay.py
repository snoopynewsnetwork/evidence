"""Independent complete frozen-source replay. Authorities are PATH ONLY.
No producer code is imported. No current aggregate discovery or network occurs.
"""
import csv,gzip,hashlib,io,json,pathlib,sys,tarfile,tempfile,collections
STATE=pathlib.Path(__file__).resolve().parents[3]
AUTH=STATE/'data/coordinator-source-research-acceptance.json'
CONTRACT=STATE/'data/turnout/priority-set.json'
def pairs(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate JSON key '+k)
  d[k]=v
 return d
def strict(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sem(x):return sha(canon(x))
def check(b,r,prefix=''):
 assert len(b)==r[prefix+'bytes'],('size',r.get('path'))
 assert sha(b)==r[prefix+'sha256'],('hash',r.get('path'))
 return b
def pointer(x,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def containers(x,p=''):
 if isinstance(x,(dict,list)):
  yield p,x
  it=x.items() if isinstance(x,dict) else enumerate(x)
  for k,v in it:yield from containers(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))
def parse(b,fmt):
 if fmt=='csv_full_header_and_rows':return list(csv.reader(io.StringIO(b.decode('utf-8'))))
 if fmt=='jsonl_full_ordered_array':return [strict(x) for x in b.splitlines() if x.strip()]
 return strict(b)
def run(out=None):
 a=strict(AUTH.read_bytes());p=strict(CONTRACT.read_bytes());check(CONTRACT.read_bytes(),a['frozen_contract'])
 assert len(a['complete_root_field_semantics'])==len(p)==31
 for r in a['complete_root_field_semantics']:assert sem(pointer(p,r['pointer']))==r['full_recursive_semantic_sha256']
 assert p['coverage']==a['all_complete_parent_objects'];assert len(p['coverage'])==120
 assert not a['dispatch_keys'] and a['ordered_priority_keys'] is None
 assert all(p[k] is None for k in ['order','top15','min80','priority','remainder'])
 fixed={x['path']:x for x in a['frozen_file_pins']}
 for r in fixed.values():check((STATE/r['path']).read_bytes(),r)
 def raw(path):
  b=(STATE/path).read_bytes()
  if path in fixed:check(b,fixed[path])
  return gzip.decompress(b) if path.endswith('.gz') else b
 docs={};formats={}
 for r in a['complete_source_companion_files']:
  b=(STATE/r['path']).read_bytes();check(b,r);b=gzip.decompress(b) if r['path'].endswith('.gz') else b
  d=parse(b,r['format']);assert sem(d)==r['full_semantic_sha256'],('semantic',r['path']);assert len(d)==r['complete_length']
  docs[r['path']]=d;formats[r['path']]=r['format']
  if out:
   dest=out/'complete-companions'/r['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 for r in a['complete_opaque_invalid_fixture_files']:
  b=check((STATE/r['path']).read_bytes(),r);b=gzip.decompress(b) if r['path'].endswith('.gz') else b
  try:strict(b)
  except (ValueError,UnicodeError):pass
  else:raise AssertionError('raw-invalid fixture admitted')
 def expected():
  for r in a['complete_root_field_semantics']:yield 'data/turnout/priority-set.json',r['pointer'],pointer(p,r['pointer'])
  for r in a['complete_source_companion_files']:
   for q,v in containers(docs[r['path']]):yield r['path'],q,v
 exp=iter(expected());seen=collections.Counter();total=0
 for part in a['complete_source_object_reference_bodies']:
  b=check((STATE/part['path']).read_bytes(),part);b=gzip.decompress(b)
  assert len(b)==part['complete_reconstructed_bytes'] and sha(b)==part['complete_reconstructed_sha256']
  n=0
  for line in b.splitlines():
   r=strict(line);file,q,v=next(exp)
   assert r['file']==file and r['pointer']==q,('ordered reference',file,q)
   assert sem(v)==r['full_recursive_semantic_sha256'],('recursive semantic',file,q)
   n+=1;seen[file]+=1
  assert n==part['complete_object_count'];total+=n
  print('replayed partition',total,flush=True)
 assert next(exp,None) is None and total==a['complete_source_object_count']
 assert dict(seen)==a['source_objects_by_file']
 historical=0;tar_members=0;bindings=0
 # Whole historic bodies, plus complete old path/hash bindings from frozen indexes.
 for r in a['historical_full_body_resolvers']:
  f=r['storage']['file'];b=check((STATE/f['path']).read_bytes(),f);b=gzip.decompress(b);check(b,r);historical+=1
  if b[257:262]==b'ustar':
   with tarfile.open(fileobj=io.BytesIO(b),mode='r:') as tf:
    for m in tf:
     if m.isfile():assert len(tf.extractfile(m).read())==m.size;tar_members+=1
 for name in ['data/turnout/reciprocal/own-pre-resume/index.json','data/turnout/reciprocal/peer-final/index.json']:
  for r in docs[name]['files']:
   if 'captured_body' in r:
    b=(STATE/r['captured_body']).read_bytes();assert len(b)==r['captured_stored_bytes'] and sha(b)==r['captured_stored_sha256'];check(gzip.decompress(b),r)
   else:
    path=r.get('immutable_body',r.get('path'));check((STATE/path).read_bytes(),r)
   bindings+=1
 for r in a['complete_original_entity_roles']:
  b=(STATE/r['path']).read_bytes();check(b,r,'stored_');rb=gzip.decompress(b) if r['path'].endswith('.gz') else b;check(rb,r,'raw_')
 # These artifacts are substantive source bodies, never a serialized launch authority.
 if out:
  (out/'complete-parent-hierarchy.json').write_bytes(canon(docs['data/turnout/coverage.json'])+b'\n')
 summary={'strict_json':True,'root_fields':31,'fixed_files':len(fixed),'complete_companions':len(docs),'ordered_references':total,'partitions':len(a['complete_source_object_reference_bodies']),'whole_historical_resolvers':historical,'historical_path_bindings':bindings,'tar_members':tar_members,'original_entity_roles':len(a['complete_original_entity_roles']),'county_parents':120,'retained_recap_entities':a['captured_recap_source_entities'],'source_native_slices':a['qualified_native_source_slices'],'reported_source_marks':a['qualified_source_votes'],'canonical_order':None,'dispatch_keys':[],'current_matches':None}
 return summary
if __name__=='__main__':
 with tempfile.TemporaryDirectory(prefix='ky-q3-reconstruction-') as td:
  result=run(pathlib.Path(td));print(json.dumps(result,sort_keys=True))
