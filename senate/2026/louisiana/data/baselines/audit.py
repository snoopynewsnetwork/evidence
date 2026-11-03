"""READ-ONLY exact membership/hash/size/source/schema/link/coverage audit. Emits strict JSON only."""
import csv,gzip,hashlib,json,math,re,sys
from pathlib import Path
from collections import Counter,defaultdict
D=Path(__file__).resolve().parent;ROOT=D.parents[4];STATE=D.parents[1];H=lambda b:hashlib.sha256(b).hexdigest();checks=Counter();issues=[]
def test(ok,label,detail=None):
 checks[label]+=1
 if not ok:issues.append({'check':label,'detail':detail})
def load(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
try:
 owned=sorted([STATE/'county-partisanship.md',D.parent/'county-baselines.csv',*[p for p in D.rglob('*') if p.is_file()]])
 for p in owned:test(p.stat().st_size<40000000,'strict_file_bound',str(p));test('__pycache__' not in p.parts and 'node_modules' not in p.parts,'no_cache_dependency_dirs',str(p))
 receipts=json.load(open(D/'source/receipts.json'))
 for p in sorted((D/'source').glob('*.receipt.json')):receipts.append(json.load(open(p)))
 duplicate_json_fields=[]
 def unique_pairs(a):
  o={}
  for k,v in a:
   if k in o:duplicate_json_fields.append(k)
   o[k]=v
  return o
 for r in receipts:
  p=ROOT/r['reference_path'] if 'reference_path' in r else D/'source'/r['asset'];stored=p.read_bytes();raw=gzip.decompress(stored);test(H(stored)==r['stored_sha256'] and H(raw)==r['raw_sha256'] and len(raw)==r['bytes'],'original_hash_and_size',r['id']);test(all(k in r for k in ['url','final_url','retrieved_at_utc','status','headers']),'receipt_fields',r['id'])
  if raw.lstrip().startswith((b'{',b'[')):json.loads(raw,object_pairs_hook=unique_pairs)
 test(not duplicate_json_fields,'no_silent_original_duplicate_keys',duplicate_json_fields)
 frozen=load(D/'original-freeze.json')
 for a in frozen['assets']:
  p=D/a['path'];test(p.exists() and H(p.read_bytes())==a['sha256'] and p.stat().st_size==a['bytes'],'original_freeze_exact_asset',a['path'])
 P=list(csv.DictReader((D/'parish-controls.csv').open()));N=load(D/'native-results.json.gz');C=load(D/'controls.json');CC=list(csv.DictReader((D/'candidates.csv').open()));cov=load(D/'native-coverage.json');hier=load(D/'native-hierarchy.json.gz');positions=load(D/'native-position-links.json.gz');scopes=load(D/'scope-controls.json');nativebases=load(D/'native-baselines.json.gz');baseline=list(csv.DictReader((D.parent/'county-baselines.csv').open()));allorders=load(D/'all-source-orders.json.gz');priority=load(D/'historical-priority-contract.json.gz');scenario_summary=list(csv.DictReader((D/'state-scenarios.csv').open()));unit_scenarios=load(D/'all-unit-scenarios.json.gz');groups=load(D/'priority-contributions.json')
 test(len(P)==192 and len(baseline)==192 and len(CC)==39 and len(N)==12060,'whole_assignment_coverage');test(len({r['key'] for r in N})==len(N),'native_key_uniqueness');test({r['key'] for r in N}=={r['key'] for r in positions}=={r['key'] for r in nativebases},'native_position_baseline_closure');test(len(hier)==192 and len(cov)==192,'parent_context_coverage')
 for y in C:
  p=[r for r in P if r['year']==y];n=[r for r in N if r['year']==y];cc=[r for r in CC if r['year']==y];test(len(p)==64 and len({r['parish_code'] for r in p})==64,'all64_parishes_'+y);test(len(n)==C[y]['native_count'],'native_complete_'+y);sv=C[y]['candidate_totals']
  test([sum(json.loads(r['candidate_votes'])[j] for r in p) for j in range(len(cc))]==sv,'state_candidate_balance_'+y);test([sum(json.loads(r['candidate_votes'])[j] for r in n) for j in range(len(cc))]==sv,'native_candidate_balance_'+y);test(sum(sv)==C[y]['all_candidate_votes'],'complete_denominator_'+y)
  for r in p:
   a=[z for z in n if z['parish_code']==r['parish_code']];v=json.loads(r['candidate_votes']);test([sum(json.loads(z['candidate_votes'])[j] for z in a) for j in range(len(v))]==v,'each_parish_native_candidate_balance');hh=next(h for h in hier if h['year']==y and h['parish_code']==r['parish_code']);test(hh['native_disjoint_children']==[z['key'] for z in a],'hierarchy_exact_order')
  for kind,v in C[y]['method_candidate_totals'].items():test([sum(json.loads(r['candidate_votes'])[j] for r in n if r['type']==kind) for j in range(len(v))]==v,'method_candidate_balance')
  nb=[r for r in nativebases if r['year']==y];test(abs(math.fsum(r['pair_weight'] for r in nb)-1)<1e-12 and abs(math.fsum(r['all_candidate_weight'] for r in nb)-1)<1e-12,'all_native_weights_'+y)
  for field,rfield in [('All','qualified'),('All_Voted','voted')]:test(sum(int(r[rfield]) for r in p)==int(scopes[y]['race_high_level'][field]),'selected_race_control_'+y)
 for label,o in allorders.items():
  a=o['full_order'];test(a==sorted(a,key=lambda z:(-z['votes'],z['key'])),'full_descending_order');test(len({r['key'] for r in a})==len(a),'rank_unique_keys');T=sum(r['votes'] for r in a);cum=0;cut=None
  for i,r in enumerate(a,1):
   cum+=r['votes'];test(r['rank']==i and r['cumulative_votes']==cum,'rank_source_position')
   if cut is None and 5*cum>=4*T:cut=i;prior=cum-r['votes'];cross=cum
  test(T==o['total'] and cut==o['minimum80_count'] and o['threshold']==(4*T+4)//5 and prior==o['previous'] and cross==o['crossing'],'minimum_integer80_'+label)
 test(priority['current_canonical_dispatch'] is None and priority['current_canonical_units']==[],'current_dispatch_null_empty');test(priority['2024']['native']['count']==1516 and priority['2024']['native']['crossing']==1605649,'native_primary_contract')
 for p in sorted((D/'scenarios').glob('*.input.json.gz')):
  x=load(p);y=p.name[:4];level='native' if '-native-' in p.name else 'parish';expected={r['key'] for r in N if r['year']==y} if level=='native' else {'LA:'+r['parish_code'] for r in P if r['year']==y};test({u['key'] for u in x['units']}==expected,'scenario_all_units_including_nonpriority')
 for s in scenario_summary:
  g=[r for r in groups if r['scenario']==s['scenario'] and r['target_pair_margin']==float(s['target_pair_margin'])];test(len(g)==2 and abs(sum(r['pair_volume'] for r in g)-float(s['pair_volume']))<1e-7 and abs(sum(r['pair_weight'] for r in g)-1)<1e-10,'outsidepriority_complete_state')
 q=load(D/'validation.json');rep=load(D/'reproduction.json');peer=load(D/'peer-source-agreement.json');test(q['passed'] and q['actual_cli_fixture_count']==61 and len(q['scenario_checks'])==36 and q['selected_only_checks']==73512,'substantive_offline_QA');test(rep['passed'],'offline_original_reproduction');test(peer['pass_comparison'] and not peer['issues'],'captured_peer_source_agreement');test(all(r['passed'] for r in load(D/'fixtures/historical-cli-results.json')),'complete_source_actual_CLI')
 capture=load(D/'peer-capture/capture.json')
 for a in capture['files']:
  p=D/'peer-capture'/a['captured_path'];test(H(p.read_bytes())==a['sha256'] and p.stat().st_size==a['bytes'],'peer_capture_exact_bytes')
 for a in load(D/'peer-capture/receipt-capture.json'):
  p=D/'peer-capture'/a['captured_receipt'];test(H(p.read_bytes())==a['receipt_sha256'],'captured_peer_receipt_exact')
 for p in [STATE/'county-partisanship.md',D/'source/SCHEMA.md']:
  txt=p.read_text()
  for url in re.findall(r'\]\(([^)]+)\)',txt):
   if url.startswith(('https://','http://','#')):continue
   target=url.split('#')[0];future=(p.parent/target).resolve() in {D/'final-seal.json',D/'asset-manifest.json'};test((p.parent/target).exists() or ('--preseal' in sys.argv and future),'relative_link_exists',dict(file=str(p),link=url))
 manifest=D/'asset-manifest.json'
 if manifest.exists():
  m=load(manifest);expected={str(p.relative_to(ROOT)) for p in owned if p!=manifest};actual={a['path'] for a in m['assets']};test(expected==actual,'manifest_exact_membership',{'missing':sorted(expected-actual),'extra':sorted(actual-expected)});test(len(actual)==len(m['assets']),'manifest_no_duplicate_paths')
  for a in m['assets']:
   p=ROOT/a['path'];test(p.exists() and H(p.read_bytes())==a['sha256'] and p.stat().st_size==a['bytes'],'manifest_exact_hash_size',a['path'])
 else:test('--preseal' in sys.argv,'manifest_exists')
 seal=D/'final-seal.json';test(seal.exists() or '--preseal' in sys.argv,'seal_exists');test((D/'source/SCHEMA.md').stat().st_size>5000,'complete_schema')
except Exception as e:issues.append(dict(check='audit_exception',detail=repr(e)))
result=dict(passed=not issues,read_only=True,checks=dict(checks),total_checks=sum(checks.values()),issues=issues,scope='Owned exact membership/hash/size/source/schema/links and historical arithmetic fields only; no future/final outcome, current identity/geometry, legal call or calibration proof')
print(json.dumps(result,indent=2,allow_nan=False));sys.exit(bool(issues))
