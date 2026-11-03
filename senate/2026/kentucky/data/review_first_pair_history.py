"""Complete original-first raw body preservation and scoped prior peer capture."""
from pathlib import Path
import gzip,hashlib,json,sys
S=Path(__file__).resolve().parents[1];T=S/'data/turnout';B=S/'data/baselines';N=0
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
stats={};optional=0
for label in ['original-first','original-first-v2','original-first-v3']:
 w=json.loads((T/'history'/label/'witness.json').read_bytes())
 for r in w['bodies']:
  b=(T/r['immutable_body']).read_bytes();v=gzip.decompress(b);ck(sha(v)==r['sha256'] and len(v)==r['bytes'])
  if 'immutable_stored_sha256' in r:ck(sha(b)==r['immutable_stored_sha256'])
  else:optional+=1
 stats['turnout_'+label+'_complete_frozen_bodies']=len(w['bodies'])
for label in ['original-first-freeze.json','original-first-freeze-v2.json']:
 w=json.loads((B/'proof'/label).read_bytes());rows=w.get('owned_files',w.get('files'));ck(bool(rows))
 for r in rows:
  b=(S/r['path']).read_bytes();ck(len(b)==r['bytes'] and sha(b)==r['sha256'])
 stats['baseline_'+label+'_complete_frozen_targets']=len(rows)
cap=json.loads((B/'peer/capture.json').read_bytes());ck(cap['captured_utc']>json.loads((B/'proof/original-first-freeze-v2.json').read_bytes())['frozen_utc'])
for r in cap['bodies']:
 b=(B/r['body']).read_bytes();v=gzip.decompress(b);ck(sha(b)==r['stored_sha256'] and sha(v)==r['raw_sha256'] and len(v)==r['raw_bytes'])
stats['baseline_captured_peer_original_v1_v2_bodies']=len(cap['bodies'])
by_page={r['page']:r for r in json.loads((B/'extracted/elliott-manual.json').read_bytes())}
values={1:[307,67,2,5,0,1,0,0,382,753,386,0],4:[325,67,0,0,0,0,0,0,392,608,397,0],7:[384,60,0,4,1,0,1,1,450,800,453,0],9:[407,120,5,3,3,4,0,0,542,972,555,0],11:[309,74,1,5,0,1,2,2,392,621,400,0],13:[312,70,1,1,0,1,0,0,385,609,389,0],15:[291,74,0,5,0,1,0,0,371,644,373,0]};images=[]
for page,read in values.items():
 r=by_page[page];ck(r['source_values']==read[:8] and r['all_candidate_printed_total']==read[8] and r['registered']==read[9] and r['ballots_cast']==read[10] and r['blank_ballots']==read[11])
 p=(S/'data/coordinator-visual-review'/f'elliott-fresh-p{page}.png') if page in [11,13,15] else T/'proof'/f'elliott-{page:02}.png';b=p.read_bytes();images.append({'state_relative_path':str(p.relative_to(S)),'sha256':sha(b),'bytes':len(b),'source_page':page,'source_values_president_6_regular_then_generic_then_unassigned_child':read[:8],'president_total':read[8],'registered':read[9],'ballots_total':read[10],'blank_ballots':read[11]})
result={'status':'pass','checks':N,'counts':stats,'original_first_chronology_before_baseline_peer_capture':True,'raw_whole_body_hash_size_always_checked':True,'optional_stored_gzip_pin_absent_on_metadata_entries':optional,'qualification_of_optional_storage_pins':'Three metadata entries per original-first generation omit stored gzip digest; all decoded hashes/bytes exact. Complete package manifest separately pins stored bytes. No witness/source edited.','exact_manual_scope':'Seven actual whole Elliott presidential/statistics pages1,4,7,9,11,13,15 viewed; every selected row independently read. Other9Elliottpages and otherPDFs automatic only unless separately named. No browser claim.','Elliott_images':images,'scope':'Full immutable original-first witness bodies and original-v1/v2 captured peer bytes; no current/future peer-contract/model/outcome equality. Raw PDF controls remain distinct from named-writein/certified allocation and physical precinct identity. No worker/source mutation.'}
out=S/'data/coordinator-first-pair-history-and-visual-review.json';b=(json.dumps(result,indent=2)+'\n').encode()
if '--check' in sys.argv:ck(out.read_bytes()==b)
else:out.write_bytes(b)
print(json.dumps({k:v for k,v in result.items() if k!='Elliott_images'}))
