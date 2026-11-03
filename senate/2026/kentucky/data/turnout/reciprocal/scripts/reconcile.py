#!/usr/bin/env python3
"""Captured-final SOURCE CORE only. Never reads current peer outputs or imports producer code."""
import json,gzip,csv,io,re,collections
from captured_core import Capture,ROOT,STATE,sha
O=Capture('own-pre-resume');P=Capture('peer-final');OUT=ROOT/'comparison';OUT.mkdir(exist_ok=True)
def save(n,x):
 b=json.dumps(x,ensure_ascii=False,indent=2).encode()+b'\n';p=OUT/n;p.write_bytes(b);assert len(b)<40000000

def gz(n,x):
 b=''.join(json.dumps(z,ensure_ascii=False)+'\n' for z in x).encode();b=gzip.compress(b,mtime=0);assert len(b)<40000000;(OUT/n).write_bytes(b)
def pos(z):return (z['source_sha256'],int(z['page']),int(z['line']))
def cfields(z):return (z['source_sha256'],int(z['page']),int(z['line']),int(z.get('candidate_column',z.get('column'))))
checks=collections.Counter();diffs=[]
def eq(a,b,label,key):
 checks[label]+=1
 if a!=b:diffs.append({'class':label,'source_key':key,'own':a,'captured_peer':b})
# Whole captured membership and original role receipts are checked independently of semantic adapters.
checks['own_complete_old_bodies']=O.verify_all();checks['peer_complete_final_bodies']=P.verify_all()
for z in P.index['complete_original_pin_roles']:
 b=(STATE/z['path']).read_bytes();r=gzip.decompress(b);assert sha(b)==z['stored_sha256'] and len(b)==z['stored_bytes'] and sha(r)==z['raw_sha256'] and len(r)==z['raw_bytes'];assert sha(P.body(z['receipt']))==z['receipt_sha256'];checks['peer_individual_original_role_pins']+=1
own_receipts={n.rsplit('/',1)[-1]:n for n in O.entries if n.startswith('data/turnout/source/receipts/')};peer_receipts={n.rsplit('/',1)[-1]:n for n in P.entries if n.startswith('data/baselines/source/receipts/')}
for name in sorted(own_receipts.keys()&peer_receipts.keys()):eq(O.body(own_receipts[name]),P.body(peer_receipts[name]),'exact_complete_receipt_bytes',name)
# Identical raw hash is the only source-document association; no county-name or later ID equivalence is inferred.
texts={};shared=[]
for n in O.entries:
 m=re.fullmatch(r'data/turnout/extracts/([a-f0-9]{64})\.layout\.txt',n)
 if not m:continue
 h=m[1];texts[h]=O.body(n).decode().split('\f');pn=f'data/baselines/extracted/{h}.layout.txt.gz'
 if pn in P.entries:
  pb=gzip.decompress(P.body(pn));eq(O.body(n),pb,'complete_original_layout_bytes',h);shared.append(h)
fields=O.json('data/turnout/extracts/certificate-fields.json')+O.json('data/turnout/extracts/certificate-controls.json');pf=list(csv.DictReader(io.StringIO(P.body('data/baselines/extracted/certificate-fields.csv').decode())));pi={cfields(z):z for z in pf};assert len(pi)==len(pf)==3509
for z in fields:
 q=pi[cfields(z)];k=cfields(z)
 for name,a,b in [('raw_line',z['raw_line'],q['raw_line']),('raw_token',z['raw_token'],q['raw_token']),('value',z['value'],int(q['votes'])),('char_start',z['character_start'],int(q['char_start'])),('scope',z['scope'],q['scope']),('county_literal',z['county'],q['county_literal'] or None)]:eq(a,b,'certificate_'+name,k)
 line=texts[k[0]][k[1]-1].splitlines()[k[2]-1];assert line==z['raw_line'] and line[z['character_start']:z['character_end']]==z['raw_token']
headers=O.json('data/turnout/extracts/certificate-headers.json');ph=P.json('data/baselines/extracted/certificate-headers.json');hmap={(z['source_sha256'],z['page']):z for z in ph}
for z in headers:eq(z['raw_lines'],hmap[(z['source_sha256'],z['page'])]['raw_header_lines'],'complete_literal_header_lines',(z['source_sha256'],z['page']))
cm={(z['source_sha256'],z['column']):z for z in P.json('data/baselines/extracted/candidates.json')}
for z in headers:
 for c in z['candidates_display_transcription']:
  q=cm[(z['source_sha256'],c['column'])]
  for name,a,b in [('candidate',c['candidate'],q['name']),('running_mate',c['running_mate'],q['running_mate']),('party',c['party_or_ballot_label'],q['party'])]:eq(a,b,'literal_manual_header_'+name,(z['source_sha256'],c['column']))
# All own raw native/stat rows, tokens and unknown representations, matched at original source positions.
native=O.jsonl('data/turnout/extracts/native-fields.jsonl.gz');obs=P.jsonl('data/baselines/extracted/native-observations.jsonl.gz');om={pos(z):z for z in obs};assert len(om)==len(obs)
missing_native=[]
for z in native:
 q=om.get(pos(z))
 if q is None:missing_native.append(z);continue
 eq(z['raw_line'],q['raw'],'native_raw_entire_line',pos(z));eq(z['native_label'],q['unit_literal'],'native_literal_label_representation',pos(z))
 for t in z['tokens']:
  line=texts[z['source_sha256']][z['page']-1].splitlines()[z['line']-1];assert line[t['start']:t['end']]==t['raw_token'];assert any(a['start']==t['start'] and a['end']==t['end'] and a['raw']==t['raw_token'] for a in q['tokens']),(pos(z),t,q['tokens']);checks['native_exact_source_count_token_positions']+=1
 for header in z['method_header']:
  assert header in texts[z['source_sha256']][z['page']-1].splitlines();checks['native_full_method_header_context_lines']+=1
stats=O.json('data/turnout/extracts/statistics-fields.json');ps=P.jsonl('data/baselines/extracted/turnout-registration-positioned-controls.jsonl.gz');sm={pos(z):z for z in ps};missing_stat=[]
for z in stats:
 q=sm.get(pos(z))
 if q is None:missing_stat.append(z);continue
 eq(z['raw_line'],q['raw'],'statistics_entire_raw_line',pos(z))
 line=texts[z['source_sha256']][z['page']-1].splitlines()[z['line']-1];assert line==z['raw_line'];checks['statistics_full_source_position_validated']+=1
# Verify every peer raw observation against the complete same original body, including those outside own selected rows.
for name,array in [('peer_raw_native',obs),('peer_raw_statistics',ps)]:
 for z in array:
  h,pg,li=pos(z);line=texts[h][pg-1].splitlines()[li-1];assert line==z['raw'],(name,pos(z))
  for t in z['tokens']:assert line[t['start']:t['end']]==t['raw'];checks[name+'_token_positions']+=1
  checks[name+'_complete_positioned_rows']+=1
# Independent all120 admin/party controls, without treating registration party as candidate preference.
statmap={pos(z):z for z in stats}
for q in csv.DictReader(io.StringIO(P.body('data/baselines/extracted/county-admin-turnout.csv').decode())):
 z=statmap[pos(q)];v=[int(q[k]) for k in ['total_registration','number_voting','D_registration','D_number_voting','R_registration','R_number_voting','other_registration','other_number_voting']];eq(z['source_columns'],v,'all120_year_admin_party_columns',pos(q))
for q in csv.DictReader(io.StringIO(P.body('data/baselines/extracted/county-registration.csv').decode())):
 z=statmap[pos(q)];v=[int(q[k]) for k in ['precinct_count','D_registration','R_registration','other_registration','independent_registration','libertarian_registration','green_registration','constitution_registration','reform_registration','socialist_workers_registration']];eq(z['source_columns'][:10],v,'all120_registration_party_columns',pos(q));eq(z['registered'],int(q['total_registration']),'all120_registration_total',pos(q))
# Page/header/admin identity arrays retain both literal schemas, including image-only and Scott null cases.
pages=O.jsonl('data/turnout/extracts/native-page-identities.jsonl.gz');pp=P.jsonl('data/baselines/extracted/native-page-contexts.jsonl.gz');pm={(z['source_sha256'],z['page']):z for z in pp}
for z in pages:
 q=pm[(z['source_sha256'],z['page'])];eq(z['native_label'],q['unit_literal'],'page_native_literal_representation',(z['source_sha256'],z['page']));assert z['header_lines'][:len(q['header_lines'])]==q['header_lines'] or q['header_lines'][:len(z['header_lines'])]==z['header_lines'];checks['complete_page_header_companions']+=1
units=O.jsonl('data/turnout/native-units.jsonl.gz');coverage=O.json('data/turnout/coverage.json');pc=P.json('data/baselines/extracted/native-coverage.json');pcmap={z['source_sha256']:z for z in pc};bycounty=collections.defaultdict(list)
for z in stats:
 if z['county']:bycounty[z['county'].casefold()].append(z)
parents=[]
for c in coverage:
 h=c['source_sha256'];q=pcmap[h];eq(c['source_pages'],q['pages'],'all120_original_page_coverage',h)
 parents.append({'county':c['county'],'own_complete_parent':c,'peer_complete_parent':q,'own_all_statistics_children':bycounty[c['county'].casefold()],'own_all_native_unit_children':[z for z in units if z['county_fips']==c['fips']],'peer_all_raw_page_children':[z for z in pp if z['source_sha256']==h]})
assert len(parents)==120
# Peer accepted subset is associated only using original A/B source positions, not literal-key repair.
lookup={pos(z):z for z in native};known=P.json('data/baselines/extracted/native-known-pair-units.json');mapped=[]
for q in known:
 def at(k):
  h,pg,li=re.fullmatch(r'([a-f0-9]+):p(\d+):l(\d+)',k).groups();return lookup[(h,int(pg),int(li))]
 a=at(q['A_row']);b=at(q['B_row']);value=lambda z:z['tokens'][-1 if z['format']=='choice' else 0]['value'];eq(value(a),q['A'],'accepted_subset_reported_candidate_A',q['key']);eq(value(b),q['B'],'accepted_subset_reported_candidate_B',q['key']);u=next(z for z in units if z['key']==a['unit_key']);eq(u['votes'],q['all_candidate_printed_total'],'accepted_subset_source_reported_marks',q['key']);mapped.append({'peer_full_source_context':q,'own_full_source_context':u})
ell=P.json('data/baselines/extracted/elliott-manual.json');em=O.json('data/turnout/extracts/elliott-manual-fields.json');eg=collections.defaultdict(list)
for z in em:eg[(z['source_sha256'],z['page'])].append(z)
for q in ell:
 a=eg[(q['source_sha256'],q['page'])];selected=[z for z in a if z['kind'] in ('candidate','writein_pool','writein_unassigned')];eq([z['tokens'][0]['value'] for z in selected],q['source_values'],'Elliott_all_selected_source_candidate_pool_child_values',(q['source_sha256'],q['page']));mapped.append({'peer_full_source_context':q,'own_full_source_context':next(z for z in units if z['source_sha256']==q['source_sha256'] and q['page'] in z['source_pages'])})
assert len(mapped)==3150 and len(known)==3143
unresolved=P.json('data/baselines/extracted/native-unresolved-pair-contexts.json');assert len(unresolved)==70
# Full county order/cumulative crossing is the shared sensitivity, separate from all native universes.
order=O.json('data/turnout/county-sensitivity.json')['2024-president'];co=list(csv.DictReader(io.StringIO(P.body('data/baselines/county-order.csv').decode())));assert len(co)==120
for a,b in zip(order['order'],co):
 for field,av,bv in [('key',a['key'],b['fips']),('rank',a['rank'],int(b['rank'])),('count',a['votes'],int(b['contest_votes'])),('cumulative',a['cumulative_votes'],int(b['cumulative'])),('denominator',order['denominator'],int(b['state_total']))]:eq(av,bv,'full_county_order_'+field,a['key'])
priority=P.json('data/baselines/priority.json');sens=priority['county_sensitivity'];assert priority['canonical_native_order'] is None and priority['canonical_native_top15_share'] is None and priority['canonical_native_minimum80'] is None and priority['dispatch_keys']==[]
for field,a,b in [('total',order['denominator'],sens['total']),('top15',order['top15']['votes'],sens['top15_votes']),('min80count',order['min80']['count'],sens['minimum80_count']),('min80votes',order['min80']['votes'],sens['crossing_votes']),('preceding',order['min80']['preceding_votes'],sens['preceding_votes']),('ordered50',order['priority_keys'],sens['keys'])]:eq(a,b,'county_integer80_contract_'+field,'all120')
# Both full literal differences and absent observation cases survive; none alter counts or producer outputs.
gz('literal-and-schema-differences.jsonl.gz',diffs);gz('missing-peer-native-observations.jsonl.gz',missing_native);gz('missing-peer-statistics-observations.jsonl.gz',missing_stat);gz('all120-complete-parent-child-packets.jsonl.gz',parents);gz('accepted-subset-complete-source-context-pairs.jsonl.gz',mapped)
summary={'scope':'Captured final SOURCE CORE only; no calculator/scenario/target/outcome or later/current/future equality conclusions','own_pre_resume_manifest':O.index['old_manifest_sha256'],'peer_final_manifest':P.index['manifest_sha256'],'peer_finalseal':P.index['finalseal_sha256'],'checks':dict(checks),'shared_complete_original_layouts':len(shared),'own_native_rows':len(native),'peer_raw_native_rows':len(obs),'own_statistics_rows':len(stats),'peer_raw_statistics_rows':len(ps),'missing_peer_selected_native_observations':len(missing_native),'missing_peer_selected_statistics_observations':len(missing_stat),'literal_or_schema_differences':dict(collections.Counter(z['class'] for z in diffs)),'accepted_peer_source_contexts':len(mapped),'peer_zero_pair_contexts':len(P.json('data/baselines/native-subset-scope.json')['zero_pair_contexts']),'peer_unresolved_contexts_excluded':unresolved,'own_unresolved_literal_associations':sum(z['kind']=='candidate' and z.get('certificate_column_association') is None for u in units for z in u['candidate_rows']),'own_qualified_native_scope':{'units':3220,'reported_marks':2042278,'not_canonical':True},'canonical_native_dispatch':False,'mutations_or_peer_repairs':False,'source_position_agreement_qualification':'Raw original bytes/positions and reported fields compared completely. Literal/manual-label representation differences are retained exactly, not normalized to claim agreement.'}
# Differences in actual counts/positions/raw bytes must fail; representational differences remain disclosed.
allowed_representation=lambda z:(z['class'] in ['native_literal_label_representation','page_native_literal_representation','literal_manual_header_candidate','literal_manual_header_running_mate','literal_manual_header_party'] or (z['class']=='certificate_scope' and z['own']=='state_footer' and z['captured_peer']=='state-footer') or (z['class']=='certificate_county_literal' and z['own'] is None and z['captured_peer']=='Total Votes'))
critical=[z for z in diffs if not allowed_representation(z)]
summary['critical_difference_count']=len(critical);save('summary.json',summary);print(json.dumps({k:v for k,v in summary.items() if k not in ['peer_unresolved_contexts_excluded']},indent=2));assert not critical,critical[:2]
