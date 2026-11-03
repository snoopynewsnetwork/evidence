"""Freeze complete qualified source research without inventing statewide native dispatch.

Every retained producer byte is individually pinned; every complete structured companion
and ordered container is referenced. Whole gzip and tar resolvers preserve older witnesses.
Producer acceptance/current flags are never edited.
"""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,io,json,tarfile
S=Path(__file__).resolve().parents[1];D=S/'data';T=D/'turnout';B=D/'baselines'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sem(x):return sha(enc(x))
def pin(p):
 b=p.read_bytes();assert len(b)<40000000
 return {'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)}
def pairs(items):
 d={}
 for k,v in items:
  if k in d:raise ValueError('duplicate JSON key '+k)
  d[k]=v
 return d
def jload(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def read(p):
 b=p.read_bytes();b=gzip.decompress(b) if p.name.endswith('.gz') else b
 if '.jsonl' in p.name:return [jload(l) for l in b.splitlines() if l]
 if '.json' in p.name:return jload(b)
 return list(csv.reader(io.StringIO(b.decode('utf-8-sig'),newline='')))
class Ledger:
 def __init__(self):self.parts=[];self.total=0;self.counts=Counter();self.start()
 def start(self):self.buf=io.BytesIO();self.gz=gzip.GzipFile(fileobj=self.buf,mode='wb',filename='',mtime=0);self.rawhash=hashlib.sha256();self.rawbytes=0;self.n=0
 def emit(self,file,pointer,value):
  if self.n==150000:self.close();self.start()
  b=enc({'file':file,'pointer':pointer,'full_recursive_semantic_sha256':sem(value)})+b'\n';self.gz.write(b);self.rawhash.update(b);self.rawbytes+=len(b);self.n+=1;self.total+=1;self.counts[file]+=1
 def walk(self,file,x,ptr=''):
  if isinstance(x,(dict,list)):
   self.emit(file,ptr,x)
   for k,v in x.items() if isinstance(x,dict) else enumerate(x):
    if isinstance(v,(dict,list)):self.walk(file,v,ptr+'/'+str(k).replace('~','~0').replace('/','~1'))
 def close(self):
  self.gz.close();p=D/f'coordinator-full-source-object-refs-v1-{len(self.parts)+1:04d}.jsonl.gz';b=self.buf.getvalue()
  if p.exists():assert p.read_bytes()==b
  else:p.write_bytes(b)
  self.parts.append({**pin(p),'complete_object_count':self.n,'complete_reconstructed_bytes':self.rawbytes,'complete_reconstructed_sha256':self.rawhash.hexdigest(),'format':'Every ordered reference in this complete partition; not a projection or sample.'})
def main():
 c=read(T/'priority-set.json');assert len(c['coverage'])==120 and c['complete_coverage'] is False
 assert all(c[k] is None for k in ['order','top15','min80','priority','remainder']) and c['dispatch_keys']==[]
 reviews=['coordinator-first-pair-original-review.json','coordinator-baseline-math-review.json','coordinator-baseline-cli-review.json','coordinator-first-pair-history-and-visual-review.json','coordinator-turnout-reciprocal-final-review.json']
 for name in reviews:assert str(read(D/name)['status']).lower().startswith('pass'),name
 fixed={};seals=[]
 def add(p,want=None):
  r=pin(p);assert want is None or all(r[k]==want[k] for k in ['path','bytes','sha256']);fixed[r['path']]=r;return r
 for root,digest,number,extras in [(T,'b72ab95194d9e748a7c15163a9f5eb13db1ff0596fc9e4d1d77fb84a9036946f',5008,['turnout.md','data/county-turnout.csv']),(B,'9415e66193d21382abc5bc9f5ab97b3943ce2498c64e33acb3aade7dfdf5b2a4',1971,['county-partisanship.md','data/county-baselines.csv'])]:
  m=read(root/'asset-manifest.json');rows=m['files'];assert len(rows)==number and sha((root/'asset-manifest.json').read_bytes())==digest
  assert {r['path'] for r in rows}=={str(p.relative_to(S)) for p in root.rglob('*') if p.is_file() and p!=root/'asset-manifest.json'}|set(extras)
  for r in rows:add(S/r['path'],r)
  seals.append({**add(root/'asset-manifest.json'),'owned_field':'files','owned_entries':number,'path_resolution':'state-relative'})
 originals=read(T/'source/entities.json')
 for r in originals:
  p=(S/r['path']) if r['path'].startswith('data/') else (T/r['path']);rr=add(p);raw=gzip.decompress(p.read_bytes());assert rr['sha256']==r['stored_sha256'] and rr['bytes']==r['stored_bytes'] and sha(raw)==r['raw_sha256'] and len(raw)==r['raw_bytes']
  for rel in r.get('receipts',[]):add(T/rel)
 history=[];structured=[];opaque=[];ledger=Ledger()
 for k,v in c.items():ledger.emit('data/turnout/priority-set.json','/'+k,v)
 for r in sorted(fixed.values(),key=lambda x:x['path']):
  p=S/r['path']
  if p.name.endswith('.tar.gz'):
   with tarfile.open(p,'r:gz') as tf:
    for m in tf:
     if m.isfile():
      raw=tf.extractfile(m).read();history.append({'original_path':m.name,'bytes':len(raw),'sha256':sha(raw),'storage':{'kind':'tar_gzip_member','archive':r,'member':m.name}})
  elif p.name.endswith('.gz'):
   raw=gzip.decompress(p.read_bytes());history.append({'original_path':None,'bytes':len(raw),'sha256':sha(raw),'storage':{'kind':'lossless_gzip_body','file':r},'path_binding':'Resolve original path and expected whole SHA from the complete captured witness/index companions; never substitute a newer mutable path.'})
  if not p.name.endswith(('.json','.json.gz','.jsonl.gz','.csv','.csv.gz')):continue
  try:x=read(p)
  except (ValueError,UnicodeError) as e:opaque.append({**r,'scope':'Retained whole invalid fixture/history, never coerced or admitted','parse_error':str(e)});continue
  structured.append({**r,'full_semantic_sha256':sem(x),'complete_length':len(x) if isinstance(x,(dict,list)) else None,'format':'csv_full_header_and_rows' if '.csv' in p.name else 'jsonl_full_ordered_array' if '.jsonl' in p.name else 'json','complete_body_required':True,'projection_or_subset_substitution':False});ledger.walk(r['path'],x)
 ledger.close()
 result={'schema':'KY-complete-qualified-source-research-authority-v1','status':'accepted_complete_available_historical_source_research_canonical_native_priority_unavailable','state':'KY','coordinator_agent_id':'d0fc3534-1613-4883-b48b-21a233fcfd9e','authority':'PATH ONLY downstream. Independently consume full authority in memory; never copy body/hash/reverse pin or change producer flags.','frozen_contract':pin(T/'priority-set.json'),'producer_seals':seals,'independent_coordinator_reviews':[pin(D/n) for n in reviews],'frozen_file_pins':sorted(fixed.values(),key=lambda x:x['path']),'complete_root_field_semantics':[{'pointer':'/'+k,'full_recursive_semantic_sha256':sem(v)} for k,v in c.items()],'complete_source_companion_files':structured,'complete_opaque_invalid_fixture_files':opaque,'complete_source_object_reference_bodies':ledger.parts,'complete_source_object_count':ledger.total,'source_objects_by_file':dict(ledger.counts),'historical_full_body_resolvers':history,'complete_original_entity_roles':originals,'all_county_research_parents':120,'all_complete_parent_objects':c['coverage'],'ordered_research_parent_keys':[r['fips'] for r in c['coverage']],'captured_recap_source_entities':3221,'qualified_native_source_slices':3220,'qualified_source_votes':2042278,'peer_separate_accepted_native_contexts':3150,'county_sensitivity':{'denominator':2074530,'top15_votes':1094747,'minimum80_count':50,'preceding49_votes':1650178,'crossing50_votes':1660226,'crossing_Breckinridge_votes':10048,'dispatch_substitute':False},'certified_native_full_order':None,'certified_native_top15':None,'certified_native_minimum80':None,'ordered_priority_keys':None,'canonical_remainder_keys':None,'dispatch_keys':[],'coverage_sequence_is_certified_vote_order':False,'source_qualifications':['All120 complete county source/parent arrays and every constituent/raw candidate/party/method/header/null/statistical/admin/position object retained. All full structured companion bodies and every ordered reference in every partition required; no sampling/projection. Full immutable original bytes/receipts and all whole captures required.','Scott is county-cumulative only, Magoffin Mail In-only. Turnout3220/2042278 and baseline3150/1969011 are distinct qualified observed universes. Baseline3127positivepair/23undefinedzero.70Laurel/Madison excluded unresolved additive contexts;167literal candidate associations remain unknown. No allocation, source residual repair, label normalization or geometric equivalence.','FayetteTrump-3/WhitleyHarris-1 source-vintage deltas; generic/named/NotAssigned child scopes and handwritten/null ambiguities retained. County50 and captured-native1817 are sensitivities ONLY, never dispatch. Equal-vote subset policies differ crossing labels; no order adoption.','All17/4/8 complete certificate columns close all120 parents and17/4/8 exact footer controls.2024pres2074530,2022otherClassIII1477830,2020sameClassII2135057. Full2020/2022native candidate/method universes unavailable. NumberVoting and registration source-date scopes distinct from certified physical ballots.','Source-core agreement only over exact captures, not calculators/scenarios/targets/outcomes/future peer bytes. Prior versions/errors/manual-review corrections retained whole. No producer writers/imports, mutable news aggregate/helpers/directory discovery, unfinished peer or optional coordinator proof build dependencies.','Question3 and question4 investigate ALL120 qualified county chains with all3221source entities and every available constituent. No certified native priority exists; do not invent a priority or use county50/known1817 as substitute. Current leaf/reporting/choice/geography matches remain null.','First action verify exact whole external authority and frozen contract pins, then parse full bodies in memory. Authority PATH ONLY downstream, all frozen producer flags remain untouched. Bounded work completes with meaningful negative and denied-network offline replay, sealFIRST/manifestLAST excluding only itself, final read-only audit and actual worker turn ends.'],'current_geography_approved':False,'current_November_returns_admitted':False,'current_choice_or_reporting_IDs_approved':False,'legal_native80_robustness_approved':False,'live_cadence_or_exact_remainder_approved':False,'collector_or_probability_approval':False}
 p=D/'coordinator-source-research-acceptance.json';b=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False).encode()+b'\n';assert len(b)<40000000
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b)
 print(json.dumps({'authority':pin(p),'roots':len(c),'companions':len(structured),'recursive_objects':ledger.total,'partitions':len(ledger.parts),'fixed_files':len(fixed),'historical_resolvers':len(history),'canonical_native_priority':None}))
if __name__=='__main__':main()
