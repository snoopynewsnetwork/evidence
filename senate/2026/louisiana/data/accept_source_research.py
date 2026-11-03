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
 c=read(T/'priority-set.json');assert len(c['all_parishes'])==64 and len(c['historical_native_constituents'])==3933 and len(c['ordered_priority_keys'])==1516 and len(c['ordered_remainder_keys'])==2417
 reviews=['coordinator-first-pair-original-review.json','coordinator-baseline-math-review.json','coordinator-baseline-cli-review.json','coordinator-turnout-reciprocal-final-review.json']
 for name in reviews:assert str(read(D/name)['status']).lower().startswith('pass'),name
 fixed={};seals=[]
 def norm(rel):return Path(rel).relative_to(S.relative_to(Path.cwd())).as_posix() if str(rel).startswith('senate/2026/louisiana/') else str(rel)
 def add(p,want=None):
  r=pin(p);assert want is None or (r['bytes']==want['bytes'] and r['sha256']==want['sha256']);fixed[r['path']]=r;return r
 for root,digest,number,extras in [(T,'dffc8ddefc7f92f37b7c19e7a3c16c7d905c928f48e01f7d4e3f7edc2b96d69f',733,['turnout.md','data/county-turnout.csv']),(B,'22aa501bcbcf9a6b99849e41859cf14a7d3216191e22d0f6dd68eced41fe897d',1607,['county-partisanship.md','data/county-baselines.csv'])]:
  m=read(root/'asset-manifest.json');rows=m['assets'];assert len(rows)==number and sha((root/'asset-manifest.json').read_bytes())==digest
  assert {norm(r['path']) for r in rows}=={str(p.relative_to(S)) for p in root.rglob('*') if p.is_file() and p!=root/'asset-manifest.json'}|set(extras)
  for r in rows:add(S/norm(r['path']),r)
  seals.append({**add(root/'asset-manifest.json'),'owned_field':'assets','owned_entries':number,'path_resolution':'state-relative for turnout; repository-relative for baselines'})
 originals=read(B/'source/receipts.json')+[read(p) for p in sorted((B/'source').glob('*.receipt.json'))]
 for r in originals:
  p=(Path.cwd()/r['reference_path']) if 'reference_path' in r else (B/'source'/r['asset']);rr=add(p);raw=gzip.decompress(p.read_bytes());assert rr['sha256']==r['stored_sha256'] and sha(raw)==r['raw_sha256'] and len(raw)==r['bytes']
 history=[];structured=[];opaque=[];ledger=Ledger()
 for k,v in c.items():ledger.emit('data/turnout/priority-set.json','/'+k,v)
 for r in sorted(fixed.values(),key=lambda x:x['path']):
  p=S/r['path']
  if p.name.endswith(('.tar.gz','.tar.gz.part001')):
   with tarfile.open(p,'r:gz') as tf:
    for m in tf:
     if m.isfile():
      raw=tf.extractfile(m).read();history.append({'original_path':m.name,'bytes':len(raw),'sha256':sha(raw),'storage':{'kind':'tar_gzip_member','archive':r,'member':m.name}})
  elif p.name.endswith('.gz'):
   raw=gzip.decompress(p.read_bytes());history.append({'original_path':None,'bytes':len(raw),'sha256':sha(raw),'storage':{'kind':'lossless_gzip_body','file':r},'path_binding':'Resolve original path+expected wholeSHA from complete capture/witness companions; never newer mutable bodies.'})
  if not p.name.endswith(('.json','.json.gz','.jsonl.gz','.csv','.csv.gz')):continue
  try:x=read(p)
  except (ValueError,UnicodeError) as e:opaque.append({**r,'scope':'Whole invalid fixture/history, not coerced or admitted','parse_error':str(e)});continue
  structured.append({**r,'full_semantic_sha256':sem(x),'complete_length':len(x) if isinstance(x,(dict,list)) else None,'format':'csv_full_header_and_rows' if '.csv' in p.name else 'jsonl_full_ordered_array' if '.jsonl' in p.name else 'json','complete_body_required':True,'projection_or_subset_substitution':False});ledger.walk(r['path'],x)
 ledger.close();full=c['full_order'];priority=c['ordered_priority_keys'];rest=c['ordered_remainder_keys'];assert [r['key'] for r in full]==priority+rest
 result={'schema':'LA-complete-historical-source-research-authority-v1','status':'accepted_complete_historical_source_research_only','state':'LA','coordinator_agent_id':'d0fc3534-1613-4883-b48b-21a233fcfd9e','authority':'PATH ONLY downstream. Full external authority consumed in memory; never copy/hash/reverse-pin or change producer flags.','frozen_contract':pin(T/'priority-set.json'),'producer_seals':seals,'independent_coordinator_reviews':[pin(D/n) for n in reviews],'frozen_file_pins':sorted(fixed.values(),key=lambda x:x['path']),'complete_root_field_semantics':[{'pointer':'/'+k,'full_recursive_semantic_sha256':sem(v)} for k,v in c.items()],'complete_source_companion_files':structured,'complete_opaque_invalid_fixture_files':opaque,'complete_source_object_reference_bodies':ledger.parts,'complete_source_object_count':ledger.total,'source_objects_by_file':dict(ledger.counts),'historical_full_body_resolvers':history,'complete_original_entity_roles':originals,'all_parish_research_parents':64,'all_complete_parent_objects':c['all_parishes'],'full_native_contexts':3933,'all_complete_native_objects':c['historical_native_constituents'],'ordered_full_keys':[r['key'] for r in full],'ordered_priority_keys':priority,'ordered_remainder_keys':rest,'ordered_priority_parent_keys':[r['key'] for r in c['all_parishes'] if r['ordered_priority_native_keys']],'historical_priority':c['historical_priority'],'current_dispatch_keys':[],'source_qualifications':['All64 parish full/source/ranked/priority/remainder child arrays and3933native fullcandidate/header/method/null/admin/physicalposition/source objects retained, every root/companion/container across every ordered partition required. All original whole receipts/entities and historical capture bodies independently pinned; never votes-only projection/current substitution.','2024pres3933/11candidate2006975,2022otherIII Senate4065/13candidate1383290,2020sameII Senate4062/15candidate2071543. All12060native rows/192parishes/39candidate columns close CSV/XLSX/API. Historical native exact80=1516/1605649 after1515/1605350, Bienville06/03+299;top15689455. Priority1452ordinary+64EarlyVoting, noProvisional;all64priorityparents.24parishes/Washington is sensitivityONLY. No2024Senate.','General-vs-selected-race votercontrol differences2022voted-10,2020qualified-15/voted+13, nativequalified/votedmissing5/11/13ordinary+adminunknown. Truephysicalballots/blankunder-over/write-in scope unknown. Earlyaggregate composition/rollcutoff not inferred. No allocation or normalization; complete source clocks/labels/physicalOOXMLordinal cells/missingr attributes retained.','Source-only captured peer agreement, not calculators/scenarios/targets/outcomes/futurebytes. Both differing currentauthorityHTML observations retained separately. Initial parish-primary scope correction and packaging exception preserved whole; latest turnover MF excludes onlyself. No producer imports/writers,mutable aggregates/helpers/discovery,unfinished peer or optional coordinator review build dependency.','Question3 and4 investigate all64 actual priority-parent chains and full3933/1516/2417 hierarchy with allnative/method/admin/context source objects. Administrative early/provisional units have no inferred polygon. Current leaf/reporting/choice/geographic matches remain null.','Current Senate closedparty nomination/general plurality rules must be checked official enacted/effective texts and actual final roster; do not transplant historical majority primary/runoff or House exception into2026Senate. Current setup metadata not votes/cadence/exhaustive signed ballot. No forecast/collector/probability.','First action verify every byte of exact authority andcontract, strictparsefull bodies in memory. AuthorityPATHONLY, frozenproducerflagsuntouched. Bounded source research/meaningful negatives/deniednetwork exactreplay/sealFIRST/MFLAST excludingONLYitself/finalREADONLY/noownedwritesthenactualEND. Later legal/current/admission qualifications not indefinite worker gates.'],'current_geography_approved':False,'current_November_returns_admitted':False,'current_choice_or_reporting_IDs_approved':False,'legal_native80_robustness_approved':False,'live_cadence_or_exact_remainder_approved':False,'collector_or_probability_approval':False}
 p=D/'coordinator-priority-acceptance.json';b=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False).encode()+b'\n';assert len(b)<40000000
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b)
 print(json.dumps({'authority':pin(p),'roots':len(c),'companions':len(structured),'recursive_objects':ledger.total,'partitions':len(ledger.parts),'fixed_files':len(fixed),'historical_resolvers':len(history),'native_priority':1516}))
if __name__=='__main__':main()
