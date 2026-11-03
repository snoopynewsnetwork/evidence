#!/usr/bin/env python3
"""Complete captured SOURCE CORE packets and actual full-context corruption fixtures."""
import json,gzip,copy,re,collections,sys
from captured_core import Capture,ROOT,sha
O=Capture('own-pre-resume');P=Capture('peer-final');D=ROOT/'fixtures';AUDIT_ONLY='--audit-only' in sys.argv
if not AUDIT_ONLY:D.mkdir(exist_ok=True);(D/'bodies').mkdir(exist_ok=True)
def binary(p,b):
 if AUDIT_ONLY:assert p.read_bytes()==b,('read-only fixture replay drift',str(p))
 else:p.write_bytes(b)
def text(p,s):binary(p,s.encode())
OWN=['extracts/certificate-fields.json','extracts/certificate-controls.json','extracts/certificate-headers.json','extracts/county-fips.json','extracts/native-fields.jsonl.gz','extracts/native-page-identities.jsonl.gz','extracts/elliott-manual-fields.json','extracts/historical-handwritten-fields.json','extracts/historical-handwritten-hierarchy.json','extracts/statistics-fields.json','native-units.jsonl.gz','source-native-statistics-identities.jsonl.gz','coverage.json','county-sensitivity.json','known-native-order.json','priority-set.json','source/refs.json','source/entities.json']
PEER=['extracted/certificate-fields.csv','extracted/candidates.json','extracted/certificate-headers.json','extracted/certificate-controls.json','extracted/native-observations.jsonl.gz','extracted/native-positional-fields.jsonl.gz','extracted/native-page-contexts.jsonl.gz','extracted/turnout-registration-positioned-controls.jsonl.gz','extracted/native-coverage.json','extracted/native-known-pair-units.json','extracted/native-unresolved-pair-contexts.json','extracted/elliott-manual.json','extracted/admin-controls.json','extracted/county-admin-turnout.csv','extracted/county-registration.csv','native-subset-scope.json','county-order.csv','priority.json','source/pins.json']
components={}
for side,cap,prefix,paths in [('own',O,'data/turnout/',OWN),('peer',P,'data/baselines/',PEER)]:
 for path in paths:
  full=prefix+path;z=cap.entries[full];components[side+':'+path]={'capture':side,'oldpath':full,'whole_sha256':z['sha256'],'bytes':z['bytes']}
# Each complete receipt and each original body role is included as a full companion, never a mutable aggregate.
for side,cap,prefix in [('own',O,'data/turnout/source/receipts/'),('peer',P,'data/baselines/source/receipts/')]:
 for path,z in cap.entries.items():
  if path.startswith(prefix):components[side+':receipt:'+path.rsplit('/',1)[1]]={'capture':side,'oldpath':path,'whole_sha256':z['sha256'],'bytes':z['bytes']}
base={'scope':'complete captured own and peer SOURCE CORE; immutable full body refs, no normalized alias packet','components':components,'own_whole_original_roles':O.index['external_original_pins'],'peer_whole_original_roles':P.index['complete_original_pin_roles'],'own_original_entities':O.json('data/turnout/source/entities.json'),'all_raw_originals_once_by_individual_pin':True,'canonical_admission':False}
text(D/'complete-positive.input.json',json.dumps(base,indent=2)+'\n');CACHE={}
def raw(ref):return (O if ref['capture']=='own' else P).body(ref['oldpath'])
def decoded(key):
 if key not in CACHE:
  b=raw(components[key]);n=components[key]['oldpath'];b=gzip.decompress(b) if n.endswith('.gz') else b;CACHE[key]=[json.loads(x) for x in b.decode().splitlines()] if '.jsonl' in n else json.loads(b) if n.endswith('.json') else b
 return CACHE[key]
def need(ok,why):
 if not ok:raise AssertionError(why)
def ranking(x):
 n=x['denominator'];a=x['order'];need(len(a)==x['units'] and len({q['key'] for q in a})==len(a),'full order uniqueness/coverage');need(a==sorted(a,key=lambda q:(-q['votes'],q['key'])),'descending complete order');c=0
 for i,q in enumerate(a,1):c+=q['votes'];need(q['votes']>=0 and q['rank']==i and q['cumulative_votes']==c and q['share_denominator']==n,'full integer/count/cumulative/denominator')
 need(c==n,'full order state arithmetic');m=x['min80'];k=m['count'];v=sum(q['votes'] for q in a[:k]);prev=sum(q['votes'] for q in a[:k-1]);need(m['votes']==v and v*5>=4*n and m['preceding_count']==k-1 and m['preceding_votes']==prev and prev*5<4*n,'minimum certified/source-scoped integer80 crossing');need(m['crossing_key']==a[k-1]['key'] and m['crossing_votes']==a[k-1]['votes'],'crossing original key');need(x['remainder']['keys']==[q['key'] for q in a[k:]] and x['remainder']['votes']==n-v,'complete ordered remainder');need(x['top15']['keys']==[q['key'] for q in a[:15]] and x['top15']['votes']==sum(q['votes'] for q in a[:15]),'complete top15');need(x['priority_keys']==[q['key'] for q in a[:max(15,k)]],'ordered priority')
def invariants(k,x):
 if k=='own:extracts/certificate-fields.json':
  need(len(x)==3480,'all120 candidate positions');need(len({(q['source_sha256'],q['county'],q['candidate_column']) for q in x})==3480,'candidate uniqueness')
 if k=='own:extracts/certificate-headers.json':
  for q in x:
   need('raw_lines' in q and q['raw_lines'],'complete original header');
   for c in q['candidates_display_transcription']:need(all(t in c for t in ['candidate','running_mate','party_or_ballot_label','column']),'candidate party/runningmate/header mask')
 if k=='own:extracts/native-fields.jsonl.gz':
  need(len(x)==58543,'complete raw native row coverage')
  for q in x:need(all(t in q for t in ['source_sha256','page','line','raw_line','tokens','native_label','unit_key','method_header']),'native full source/position/method companion');need(q['line'] is not None,'source position mask')
 if k=='own:native-units.jsonl.gz':
  need(len(x)==3221 and len({q['key'] for q in x})==3221,'complete native/admin source entity coverage/duplicates')
  for q in x:
   need(all(t in q for t in ['scope','candidate_rows','certified_candidate_columns','method_header_contexts','literal_native_label','source_sha256','ballots_cast','registration','blank_ballots','undervotes','overvotes']),'native context/method/admin/null companion');need(len(q['certified_candidate_columns'])==17,'all17 source candidate masks')
   for c in q['certified_candidate_columns']:need('value' in c and 'null_status' in c and 'reported_source_values' in c,'complete explicit unknown mask')
 if k=='own:coverage.json':
  need(len(x)==120 and len({q['fips'] for q in x})==120,'all120 parent coverage')
  need(sum(len(q['available_native_constituents']) for q in x)==3221,'all native/admin children retained')
  for q in x:need('unavailable_case' in q and q['canonical_native_complete'] is False,'unavailable parent/mask preserved')
 if k=='own:priority-set.json':
  need(all(x[t] is None for t in ['order','top15','min80','priority','remainder']),'canonical NULL/county substitution rejection');need(x['dispatch_keys']==[] and x['ordered_priority_keys']==[] and x['complete_coverage'] is False,'empty native dispatch');need(all(v is False or v is None for v in x['flags'].values()),'no current/legal/geographic/feed admission')
 if k=='own:known-native-order.json':ranking(x);need(x['units']==3220 and x['denominator']==2042278,'qualified native scope is fixed, not statewide canonical')
 if k=='own:county-sensitivity.json':
  for q in x.values():ranking(q)
  p=x['2024-president'];need(p['denominator']==2074530 and p['top15']['votes']==1094747 and p['min80']['count']==50 and p['min80']['votes']==1660226 and p['min80']['preceding_votes']==1650178 and p['min80']['crossing_key']=='21027','certified full120 candidate minimum')
 # Other components are full-body bound below, including all source/party/admin/statistical/source-position/null fields.
def verify(packet):
 need(set(packet['components'])==set(components),'complete source/context/order/companion component membership')
 need(packet['own_whole_original_roles']==base['own_whole_original_roles'] and packet['peer_whole_original_roles']==base['peer_whole_original_roles'] and packet['own_original_entities']==base['own_original_entities'],'complete individual source/receipt/role coverage')
 overrides=packet.get('complete_body_overrides',{})
 for k,ref in packet['components'].items():
  need(ref==components[k],'whole captured companion binding')
  if k in overrides:
   z=overrides[k];b=(ROOT/z['body']).read_bytes();need(sha(b)==z['stored_sha256'],'fixture full body transport');b=gzip.decompress(b);need(sha(b)==z['whole_sha256'],'fixture actual full input hash');x=[json.loads(s) for s in b.decode().splitlines()] if '.jsonl' in ref['oldpath'] else json.loads(b);invariants(k,x);need(x==decoded(k),'complete original field/count/null/admin/source-position drift: '+k)
  else:
   b=raw(ref);need(sha(b)==ref['whole_sha256'] and len(b)==ref['bytes'],'complete actual captured body');
   # Exercise structural/count/order checks once on the full actual positive corpus.
   if not POSITIVE_VALIDATED:invariants(k,decoded(k))
 return True
POSITIVE_VALIDATED=False;verify(base);POSITIVE_VALIDATED=True
cases=[]
def fixture(name,key,mutate):
 p=copy.deepcopy(base)
 if key is None:mutate(p)
 else:
  x=copy.deepcopy(decoded(key));mutate(x);path=components[key]['oldpath'];b=(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in x).encode() if '.jsonl' in path else json.dumps(x,ensure_ascii=False,indent=2).encode()+b'\n');h=sha(b);stored=gzip.compress(b,mtime=0);need(len(stored)<40000000,'strict complete fixture artifact bound');dest=D/'bodies'/f'{h}.gz';binary(dest,stored);p['complete_body_overrides']={key:{'body':str(dest.relative_to(ROOT)),'stored_sha256':sha(stored),'whole_sha256':h,'bytes':len(b)}}
 inp=D/f'{name}.input.json';text(inp,json.dumps(p,indent=2)+'\n')
 try:verify(p)
 except AssertionError as e:result={'fixture':name,'expected':'REJECT','actual':'REJECT','reason':str(e),'complete_packet_input_sha256':sha(inp.read_bytes()),'full_components':len(components)}
 else:raise AssertionError('CORRUPTION FIXTURE ACCEPTED '+name)
 text(D/f'{name}.result.json',json.dumps(result,indent=2)+'\n');cases.append(result)
fixture('missing-companion',None,lambda p:p['components'].pop('peer:extracted/native-observations.jsonl.gz'))
fixture('truncated-source-roles',None,lambda p:p['peer_whole_original_roles'].pop())
fixture('missing-candidate-position','own:extracts/certificate-fields.json',lambda x:x.pop())
fixture('missing-header','own:extracts/certificate-headers.json',lambda x:x[0].pop('raw_lines'))
fixture('missing-party','own:extracts/certificate-headers.json',lambda x:x[0]['candidates_display_transcription'][0].pop('party_or_ballot_label'))
fixture('missing-method','own:extracts/native-fields.jsonl.gz',lambda x:x[0].pop('method_header'))
fixture('missing-position','own:extracts/native-fields.jsonl.gz',lambda x:x[0].pop('line'))
fixture('missing-native-context','own:native-units.jsonl.gz',lambda x:x.pop())
fixture('duplicate-native-context','own:native-units.jsonl.gz',lambda x:x.append(copy.deepcopy(x[0])))
fixture('missing-parent','own:coverage.json',lambda x:x.pop())
fixture('missing-administrative-child','own:coverage.json',lambda x:next(q for q in x if q['county']=='Scott')['available_native_constituents'].clear())
def mask(x):
 q=next(c for u in x for c in u['certified_candidate_columns'] if c['value'] is None);q.pop('null_status')
fixture('missing-unknown-mask','own:native-units.jsonl.gz',mask)
fixture('wrong-full-order','own:known-native-order.json',lambda x:x['order'].reverse())
fixture('wrong-integer80','own:known-native-order.json',lambda x:x['min80'].__setitem__('count',1816))
fixture('county-substitution','own:priority-set.json',lambda x:x.__setitem__('order',decoded('own:county-sensitivity.json')['2024-president']['order']))
fixture('wrong-certified-minimum','own:county-sensitivity.json',lambda x:x['2024-president']['min80'].__setitem__('count',49))
fixture('current-admission','own:priority-set.json',lambda x:x['flags'].__setitem__('current_identity_approved',True))
text(D/'summary.json',json.dumps({'status':'PASS','positive_complete_actual_source_packet':'accepted','full_component_bodies':len(components),'corrupt_complete_packets_rejected':len(cases),'fixtures':cases,'scope':'source/count/order/context/companion/null/admin/party/method/position only; no calculator checks'},indent=2)+'\n');print('COMPLETE ACTUAL SOURCE PACKETS PASS',len(components),len(cases))
