"""Compare only captured historical source fields, never peer build/calculator or future outcomes."""
import json,gzip,hashlib,csv
from pathlib import Path
from collections import defaultdict
D=Path(__file__).resolve().parent;PC=D/'peer-capture';PEER=D.parent/'turnout';H=lambda b:hashlib.sha256(b).hexdigest()
# Capture complete original receipts BEFORE comparisons. Bodies remain immutable individual references.
if not (PC/'receipt-capture.json').exists():
 pins=[]
 for n in ['original-pins.json','acquired-pins.json']:pins+=json.loads((PC/n).read_text())['inputs']
 arr=[]
 for i,pin in enumerate(pins):
  b=(PEER/pin['receipt']).read_bytes();assert H(b)==pin['receipt_sha256'];name=f'receipt-{i:04}.json';(PC/name).write_bytes(b)
  if pin.get('body'):
   body=(PEER/pin['body']).read_bytes();assert H(body)==pin['stored_sha256'];raw=gzip.decompress(body);assert H(raw)==pin['raw_sha256'] and len(raw)==pin['bytes']
  arr.append(dict(pin,captured_receipt=name))
 (PC/'receipt-capture.json').write_text(json.dumps(arr,indent=2)+'\n')
peer=json.loads(gzip.decompress((PC/'independent-stable-schema.json.gz').read_bytes()));N=json.loads(gzip.decompress((D/'native-results.json.gz').read_bytes()));P=list(csv.DictReader((D/'parish-controls.csv').open()));C=json.loads((D/'controls.json').read_text());CC=list(csv.DictReader((D/'candidates.csv').open()));wb=json.loads(gzip.decompress((D/'source/workbook-position-witness.json.gz').read_bytes()));orders=json.loads(gzip.decompress((D/'historical-priority-contract.json.gz').read_bytes()));issues=[];checks=defaultdict(int)
def eq(a,b,label):
 checks[label]+=1
 if a!=b:issues.append(dict(field=label,own=a,peer=b))
positions={}
for y in C:
 parent=None
 for w in [r for r in wb if r['year']==y and r['sheet_name']=='Multi-Parish(Precinct)']:
  vals=[c['value'] for c in w['cells']]
  if vals and len(vals)==1 and vals[0] in {r['parish'] for r in P}:parent=vals[0]
  if parent and vals and len(vals)==len(C[y]['candidate_totals'])+1 and all(v is not None and v.isdigit() for v in vals[1:]):positions[(y,parent,vals[0],tuple(map(int,vals[1:])))]=(w['member'],w['physical_row'])
for y in C:
 own=[r for r in N if r['year']==y];pp=peer['native_vectors'][y];eq(len(own),len(pp),'native_length')
 for a,b in zip(own,pp):
  v=json.loads(a['candidate_votes']);eq(v,b['candidate_votes'],'native_candidate_vector');eq(a['parish_code'],b['parish_id'],'native_parish');eq(a['ward'],b['ward_literal'],'ward_literal');eq(a['precinct'],b['precinct_literal'],'precinct_literal');eq(a['source_native'],b['source_native_id'],'source_native_id');eq(a['csv_row'],b['csv_record_ordinal'],'csv_position');eq(a['api_ordinal']-1,b['native_votes_json_index'],'api_position');eq(a['has_reported'],b['has_reported_literal'],'has_reported');eq(None if a['qualified'] is None else int(a['qualified']),b['qualified'],'native_qualified_null');eq(None if a['voted'] is None else int(a['voted']),b['voted'],'native_voted_null')
  eq({'ward-precinct':'ward_precinct_source_row','early-aggregate':'early_aggregate','provisional-aggregate':'provisional_aggregate'}.get(a['type']),b['kind'],'method_kind')
  pos=positions[(y,a['parish'],a['ward']+' '+a['precinct'],tuple(v))];eq(pos,(b['xlsx_member'],b['xlsx_physical_row']),'workbook_position')
 for a,b in zip([r for r in P if r['year']==y],peer['parish_vectors'][y]):
  eq(json.loads(a['candidate_votes']),b['candidate_votes'],'parish_candidate_vector');eq(a['parish'],b['parish'],'parish_name');eq(int(a['qualified']),b['race_qualified'],'race_qualified');eq(int(a['voted']),b['race_voted'],'race_voted');eq(int(a['stats_qualified']),b['qualified'],'general_qualified');eq(int(a['stats_voted']),b['voted'],'general_voted');sub=[r for r in own if r['parish_code']==a['parish_code']]
  for typ,field in [('early-aggregate','early_votes'),('provisional-aggregate','provisional_votes'),('ward-precinct','ordinary_votes')]:eq(sum(r['all_candidate_votes'] for r in sub if r['type']==typ),b[field],field)
 for a,b in zip([r for r in CC if r['year']==y],peer['historical_controls'][y]['candidate_universe']):
  eq(a['choice_id'],b['choice_id'],'candidate_ID');eq(a['label'],b['header_literal'].replace('(OTHER)','(OTH)'),'candidate_header_explicit_alias');eq(int(a['source_column'])-1,b['source_column'],'source_column_base_adapter')
 eq(C[y]['candidate_totals'],peer['historical_controls'][y]['state_candidate_vector'],'state_candidate_vector')
 # Recompute every peer order from OWN original fields and exact key tie convention, with explicit adapter.
 for label,pr in peer['all_orders'].items():
  if not label.startswith(y+'-'):continue
  if '-native-' in label:
   ar=[dict(key=json.dumps([y,C[y]['race_id'],a['parish_code'],a['ward'],a['precinct']],separators=(',',':')),votes=a['all_candidate_votes']) for a in own]
  else:
   field=label.split('-parish-')[1];ar=[]
   for a in [r for r in P if r['year']==y]:
    sub=[r for r in own if r['parish_code']==a['parish_code']]
    if field in ('early_votes','ordinary_votes','provisional_votes'):
     typ={'early_votes':'early-aggregate','ordinary_votes':'ward-precinct','provisional_votes':'provisional-aggregate'}[field];v=sum(r['all_candidate_votes'] for r in sub if r['type']==typ)
    else:v=int(a[{'votes':'all_candidate_votes','qualified':'stats_qualified','voted':'stats_voted','race_qualified':'qualified','race_voted':'voted'}[field]])
    ar.append(dict(key='LA:'+a['parish_code'],votes=v))
  ar.sort(key=lambda z:(-z['votes'],z['key']));eq([(a['key'],a['votes']) for a in ar],[(a['key'],a['votes']) for a in pr['order']],'full_order_'+label)
  total=sum(a['votes'] for a in ar);cum=0;cut=None
  for i,a in enumerate(ar,1):
   cum+=a['votes']
   if cut is None and 5*cum>=4*total:cut=i
  eq(total,pr['denominator'],'order_denominator');eq(cut,pr['minimum80_count'],'minimum_integer80')
out=dict(scope='Captured historical original-source fields and explicit schema adapters only. No calculator equality, future/final outcome, current-ID/geometry or legal dispatch approval.',peer_id='50fd7a21-788d-47d2-b03a-2a379c81a18b',own_original_freeze_sha256=H((D/'original-freeze.json').read_bytes()),peer_schema_sha256=H((PC/'independent-stable-schema.json.gz').read_bytes()),checks=dict(checks),issues=issues,pass_comparison=not issues,adapters=['Candidate export OTH vs workbook OTHER retained literally; comparison explicit formatting alias','Own candidate source column 1-based vs peer zero-based','Key inserts race ID from own original metadata; tie order key literal lexicographic','Native kind label spellings explicitly mapped; originals unchanged'],gaps=['No current2026 native identity/geometry join or coordinator acceptance','Original receipts retain final entity only; intermediate redirect entities unknown'])
(D/'peer-source-agreement.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':sum(checks.values()),'issues':len(issues),'sample':issues[:3]}))
