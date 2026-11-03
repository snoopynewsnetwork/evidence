"""Independent read-only replay of every frozen body and ordered source reference."""
from pathlib import Path
import csv,gzip,hashlib,io,json,tarfile
S=Path(__file__).resolve().parents[1];D=S/'data';N=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sem(x):return sha(enc(x))
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError(k)
  d[k]=v
 return d
def read(p):
 b=p.read_bytes();b=gzip.decompress(b) if p.name.endswith('.gz') else b
 parse=lambda b:json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
 if '.jsonl' in p.name:return [parse(l) for l in b.splitlines() if l]
 if '.json' in p.name:return parse(b)
 return list(csv.reader(io.StringIO(b.decode('utf-8-sig'),newline='')))
a=read(D/'coordinator-source-research-acceptance.json');c=read(S/a['frozen_contract']['path']);ck(len(a['complete_root_field_semantics'])==len(c))
for z in a['frozen_file_pins']:
 b=(S/z['path']).read_bytes();ck(len(b)==z['bytes'] and sha(b)==z['sha256'],'whole fixed file')
for z in a['complete_root_field_semantics']:ck(sem(c[z['pointer'][1:]])==z['full_recursive_semantic_sha256'],'complete root')
for z in a['complete_source_companion_files']:ck(sem(read(S/z['path']))==z['full_semantic_sha256'],'complete companion')
last=None;obj=None;refs=0
for part in a['complete_source_object_reference_bodies']:
 b=(S/part['path']).read_bytes();raw=gzip.decompress(b);ck(sha(b)==part['sha256'] and len(b)==part['bytes'] and sha(raw)==part['complete_reconstructed_sha256'] and len(raw)==part['complete_reconstructed_bytes'],'whole partition');lines=raw.splitlines();ck(len(lines)==part['complete_object_count'])
 for line in lines:
  z=json.loads(line)
  if z['file']!=last:obj=read(S/z['file']);last=z['file']
  v=obj
  if z['pointer']:
   for k in z['pointer'][1:].split('/'):
    key=k.replace('~1','/').replace('~0','~');v=v[int(key)] if isinstance(v,list) else v[key]
  ck(sem(v)==z['full_recursive_semantic_sha256'],'complete recursive container');refs+=1
ck(refs==a['complete_source_object_count'])
tarcaches={}
for z in a['historical_full_body_resolvers']:
 st=z['storage']
 if st['kind']=='lossless_gzip_body':raw=gzip.decompress((S/st['file']['path']).read_bytes())
 else:
  p=st['archive']['path']
  if p not in tarcaches:
   with tarfile.open(S/p,'r:gz') as tf:tarcaches[p]={m.name:tf.extractfile(m).read() for m in tf if m.isfile()}
  raw=tarcaches[p][st['member']]
 ck(sha(raw)==z['sha256'] and len(raw)==z['bytes'],'whole historical resolver')
ck(a['dispatch_keys']==[] and a['certified_native_minimum80'] is None and a['current_geography_approved'] is False)
out={'status':'pass_every_fixed_body_root_companion_recursive_reference_and_historical_resolver','checks':N,'roots':len(c),'companions':len(a['complete_source_companion_files']),'complete_recursive_references':refs,'partitions':len(a['complete_source_object_reference_bodies']),'fixed_files':len(a['frozen_file_pins']),'whole_historical_resolvers':len(a['historical_full_body_resolvers']),'authority_path':'data/coordinator-source-research-acceptance.json','authority_sha256':sha((D/'coordinator-source-research-acceptance.json').read_bytes()),'canonical_native_priority':None,'producer_write':False,'network':False}
(D/'coordinator-source-acceptance-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
