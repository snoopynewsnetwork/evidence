"""Prepare validation; seal first / manifest last; final exact read-only audit."""
from pathlib import Path
import json,csv,gzip,hashlib,re,math,datetime,sys,collections
B=Path(__file__).resolve().parents[1];ROOT=B.parents[1];MF=B/'asset-manifest.json';SEAL=B/'finalseal.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(raw):return json.loads(raw,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite JSON '+s)))
def csvrows(p):return list(csv.DictReader(p.open()))
def files():return sorted([ROOT/'county-partisanship.md',ROOT/'data/county-baselines.csv',*[p for p in B.rglob('*') if p.is_file() and p!=MF]])
def rowfile(p):return dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
def checks(final=False):
 check=[]
 def ok(name,condition,detail=None):
  assert condition,(name,detail);check.append(dict(check=name,passed=True,detail=detail))
 pins=strict((B/'source/pins.json').read_text())['pins'];bodyhashes={}
 for p in pins:
  f=ROOT/p['path'];stored=f.read_bytes();raw=gzip.decompress(stored)
  ok('individual original '+p['raw_sha256'][:12],len(stored)==p['stored_bytes'] and sha(stored)==p['stored_sha256'] and len(raw)==p['raw_bytes'] and sha(raw)==p['raw_sha256'] and len(stored)<40000000)
  receipt=ROOT/p['receipt'];ok('individual receipt '+receipt.name,sha(receipt.read_bytes())==p['receipt_sha256'])
  bodyhashes[p['raw_sha256']]=raw
 countyroles=[p for p in pins if p['role'] and p['role'].startswith('2024 county recap: ')]
 ok('all120whole county PDF originals',len(countyroles)==120 and len({p['role'] for p in countyroles})==120 and all(p['status']==200 and bodyhashes[p['raw_sha256']].startswith(b'%PDF') for p in countyroles))
 inv=strict((B/'extracted/document-inventory.json').read_text());ok('whole document inventory',len(inv)==133 and sum(r['pages'] for r in inv)==17073)
 for r in inv:
  text=gzip.decompress((B/'extracted'/f"{r['raw_sha256']}.layout.txt.gz").read_bytes());ok('whole layout '+r['raw_sha256'][:12],sha(text)==r['layout_sha256'] and text.count(b'\f')==r['pages'])
 for name in ['original-first-freeze.json','original-first-freeze-v2.json']:
  w=strict((B/'proof'/name).read_text());rr=w.get('owned_files',w.get('files'))
  for r in rr:
   p=ROOT/r['path'];ok('frozen own body '+str(r['path']),p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256'])
 fields=csvrows(B/'extracted/certificate-fields.csv');pos={(r['source_sha256'],r['page'],r['line'],r['column']) for r in fields};ok('complete3509unique candidate positions',len(fields)==3509 and len(pos)==3509)
 for r in fields:
  text=gzip.decompress((B/'extracted'/f"{r['source_sha256']}.layout.txt.gz").read_bytes()).decode();line=text.split('\f')[int(r['page'])-1].splitlines()[int(r['line'])-1];start=int(r['char_start']);token=r['raw_token']
  ok('candidate raw locator '+':'.join([r['year'],r['county_literal'],r['column']]),line==r['raw_line'] and line[start:start+len(token)]==token and int(token.replace(',',''))==int(r['votes']))
 for y,n in [(2024,17),(2022,4),(2020,8)]:
  rs=[r for r in fields if int(r['year'])==y and r['scope']=='county'];foot=[r for r in fields if int(r['year'])==y and r['scope']=='state-footer'];ok('allcounty/candidate coverage '+str(y),len(rs)==120*n and len({r['county_literal'] for r in rs})==120 and len(foot)==n)
  for c in range(1,n+1):ok('state candidate balance '+str(y)+'/'+str(c),sum(int(r['votes']) for r in rs if int(r['column'])==c)==next(int(r['votes']) for r in foot if int(r['column'])==c))
 county=csvrows(ROOT/'data/county-baselines.csv');ok('360county baselines',len(county)==360 and all(len({r['fips'] for r in county if int(r['year'])==y})==120 for y in [2024,2020,2022]))
 for r in county:
  v=strict(r['candidate_vector']);ok('county full/pair denominator '+r['year']+'/'+r['fips'],int(r['A'])==v[1] and int(r['B'])==v[0] and int(r['all'])==sum(v) and int(r['pair'])==sum(v[:2]) and int(r['other'])==sum(v[2:]) and r['ballots_cast']=='' and r['registration']=='')
 rank=csvrows(B/'county-order.csv');p=strict((B/'priority.json').read_text());cp=p['county_sensitivity'];vs=[int(r['contest_votes']) for r in rank];ok('full120descending county order',len(rank)==120 and len({r['fips'] for r in rank})==120 and vs==sorted(vs,reverse=True) and sum(vs)==2074530)
 ok('exact minimum integer80',cp['minimum80_count']==50 and 5*sum(vs[:49])<4*sum(vs)<=5*sum(vs[:50]) and cp['crossing_votes']==sum(vs[:50]) and cp['preceding_votes']==sum(vs[:49]) and cp['top15_votes']==sum(vs[:15]))
 ok('native canonical NULL/EMPTY',p['canonical_native_order'] is None and p['canonical_native_top15_share'] is None and p['canonical_native_minimum80'] is None and p['dispatch_keys']==[])
 contexts=[strict(s) for s in gzip.decompress((B/'extracted/native-page-contexts.jsonl.gz').read_bytes()).decode().splitlines()];ok('all16246native pages retained',len(contexts)==16246 and len({(r['source_sha256'],r['page']) for r in contexts})==16246)
 obs=[strict(s) for s in gzip.decompress((B/'extracted/native-observations.jsonl.gz').read_bytes()).decode().splitlines()];ok('native positional observation keys',len(obs)==148527 and len({r['observation_key'] for r in obs})==len(obs))
 native=strict((B/'extracted/native-known-pair-units.json').read_text());manual=strict((B/'extracted/elliott-manual.json').read_text());ok('known subset exact unique keys',len(native)==3143 and len(manual)==7 and len({r['key'] for r in native+manual})==3150 and all(not r['full_named_field_closure'] for r in native+manual))
 for r in native+manual:ok('native pair/control bounds '+r['key'],r['A']>=0 and r['B']>=0 and r['pair']==r['A']+r['B'] and r['all_candidate_printed_total']>=r['pair'] and (r['A_pair_share'] is None if r['pair']==0 else abs(r['A_pair_share']-r['A']/r['pair'])<1e-12))
 scope=strict((B/'native-subset-scope.json').read_text());ok('zero pair remains undefined',len(scope['zero_pair_contexts'])==23 and all(r['A_pair_share'] is None for r in scope['zero_pair_contexts']) and len(scope['included_positive_pair_keys'])==3127 and scope['canonical_native_dispatch']==[])
 admin=csvrows(B/'extracted/county-admin-turnout.csv');reg=csvrows(B/'extracted/county-registration.csv');ok('complete120parent admin scopes',len(admin)==360 and len(reg)==120 and all(len({r['county_code'] for r in admin if int(r['year'])==y})==120 for y in [2024,2020,2022]))
 ac=strict((B/'extracted/admin-controls.json').read_text());ok('every administrative state control',len(ac)==4 and all(r['printed_footer']==r['independent_county_sums'] for r in ac))
 results=list((B/'scenarios').glob('*.result.json'));ok('18state and2subset scenarios',len(results)==20)
 for f in results:
  x=strict(f.read_text());inp=strict(f.with_name(f.name.replace('.result.','.input.')).read_text());u=x['units'];ok('scenario full denominator '+f.name,abs(sum(z['remaining'] for z in u)-x['final_all_candidate_denominator'])<1e-6 and abs(sum(z['pair_pool'] for z in u)-x['final_pair_denominator'])<1e-6)
  ok('scenario contributions '+f.name,len(u)==(120 if f.name.startswith('county-') else 3127) and abs(sum(z['pair_weight'] for z in u)-1)<1e-10 and abs(sum(z['target_pair_net_contribution'] for z in u)-inp['target']*x['final_pair_denominator'])<1e-6 and abs(x['uniform']['residual'])<1e-6)
  if inp['target']==0:
   ff=x['uniform']['full_field_at_pair_target'];a,b=x['pair'];ok('mathematical tie not false lead '+f.name,ff['candidate_votes'][a]==ff['candidate_votes'][b] and (ff['strict_A_plurality'] is False if inp['other_scope']=='named' else ff['strict_A_plurality']=='unresolved other identities'))
 targets=csvrows(B/'county-targets.csv');nt=csvrows(B/'native-known-subset-targets.csv');ok('all unit targets included',len(targets)==2160 and len(nt)==6254)
 for r in targets:
  pool=float(r['pair_volume']);base=float(r['baseline_pair_net']);scenario=strict((B/'scenarios'/(r['scenario']+'.result.json')).read_text());fixed=scenario['baseline_final_pair_net']-base;req=(float(r['state_target_pair_margin'])*scenario['final_pair_denominator']-fixed+pool)/(2*pool)
  ok('selected-only county '+r['scenario']+'/'+r['fips'],abs(req-float(r['selected_only_required_A_share']))<1e-9 and r['selected_only_status']==('impossible' if req>1 else 'secured' if req<0 else 'feasible'))
 proof=strict((B/'proof/calculator-validation.json').read_text());ok('realCLI and independent rational roots',proof['status']=='passed' and len(proof['real_cli_fixtures'])==47 and len(proof['independent_scenario_checks'])==20 and all(r['passed'] for r in proof['real_cli_fixtures']+proof['independent_scenario_checks']))
 outs=list((B/'fixtures').glob('*.stdout.json'));ok('actual47CLI stdout/exit/stderr records',len(outs)==47)
 for f in outs:
  x=strict(f.read_text());t=strict(f.with_name(f.name.replace('.stdout.','.transport.')).read_text());ok('strictJSON CLI '+f.name,t['stderr']=='' and t['exit']==(2 if x['status']=='invalid-input' else 0))
 rp=strict((B/'proof/reproduction.json').read_text());ok('isolated exact-byte fresh-original reproduction',rp['status']=='passed' and all(r['passed'] for r in rp['checks']) and sum('source_sha256' in r for r in rp['checks'])==133)
 cap=strict((B/'peer/capture.json').read_text());ok('bounded peer stable role count',len(cap['bodies'])==373)
 for r in cap['bodies']:
  z=(B/r['body']).read_bytes();raw=gzip.decompress(z);ok('captured stable peer body '+r['raw_sha256'][:12],sha(z)==r['stored_sha256'] and sha(raw)==r['raw_sha256'] and len(raw)==r['raw_bytes'])
 pc=strict((B/'peer/comparison.json').read_text());ok('bounded field/order/coverage comparison',pc['certificate']['differences']==0 and pc['headers']['differences']==0 and pc['county_order80']['equal_full120_order'] and pc['elliott']['differences']==[] and pc['native']['common_source_positions']==58543 and pc['statistics']['exact complete raw row']==17052)
 for f in files():ok('asset strict size '+str(f.relative_to(ROOT)),0<=f.stat().st_size<40000000)
 ok('no owned caches/dependency trees',not any(p.name in ['__pycache__','node_modules','.cache'] for p in B.rglob('*')))
 for f in [ROOT/'county-partisanship.md',B/'source/SCHEMA.md',B/'CALCULATOR.md',B/'REPRODUCE.md']:
  for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
   if re.match(r'\w+://',target) or target.startswith('#'):continue
   path=target.split('#')[0];p=(f.parent/path).resolve()
   if p in [MF.resolve(),(B/'validation.json').resolve()] and not final:continue
   ok('relative link '+str(f.relative_to(ROOT))+' '+target,p.exists())
 return dict(status='passed',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Complete owned historical county arithmetic; qualified source-local native subset; canonical native NULL/EMPTY',checks=check,checks_count=len(check),all_source_origins_verified=True,material_gaps=['Scott cumulative native gap','Magoffin Mail In-only source','70unresolved Laurel/Madison quantitative contexts','generic/unassigned versus named-writein coverage','historical2020/2022fullnative candidate/method coverage unavailable','current ballot/legal/native geometry/feed/pool/calibration unknown'])
def main():
 mode=sys.argv[1] if len(sys.argv)==2 else ''
 if mode=='--prepare':
  x=checks();(B/'validation.json').write_text(json.dumps(x,indent=2)+'\n');print('prepared',x['checks_count'],'meaningful source/arithmetic/asset checks');return
 if mode=='--seal':
  assert not SEAL.exists() and not MF.exists(),'Existing seal/manifest immutable; preserve full prior package before any authorized repair'
  x=checks();v=strict((B/'validation.json').read_text());assert v['status']=='passed'
  seal=dict(sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='bounded owned package sealed',canonical_native_order=None,dispatch_keys=[],validation_sha256=sha((B/'validation.json').read_bytes()),report_sha256=sha((ROOT/'county-partisanship.md').read_bytes()),county_baselines_sha256=sha((ROOT/'data/county-baselines.csv').read_bytes()),original_witness_sha256=sha((B/'proof/original-first-freeze.json').read_bytes()),original_addendum_sha256=sha((B/'proof/original-first-freeze-v2.json').read_bytes()),manifest_rule='Current manifest written after this seal; excludes only itself; this seal contains no current manifest digest',preseal_owned_paths=[str(p.relative_to(ROOT)) for p in files()])
  SEAL.write_text(json.dumps(seal,indent=2)+'\n')
  mf=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),root='senate/2026/kentucky',exclusive_owned_scopes=['county-partisanship.md','data/county-baselines.csv','data/baselines/**'],excludes_only='data/baselines/asset-manifest.json',files=[rowfile(p) for p in files()],external_read_only_source_roles=pins_roles())
  MF.write_text(json.dumps(mf,indent=2)+'\n');print('seal first / manifest last complete',len(mf['files']),'owned files');return
 if mode=='--final':
  mf=strict(MF.read_text());expected={r['path']:r for r in mf['files']};actual={str(p.relative_to(ROOT)):p for p in files()};assert set(expected)==set(actual),(set(expected)-set(actual),set(actual)-set(expected))
  for k,p in actual.items():assert rowfile(p)==expected[k],k
  assert MF.stat().st_size<40000000
  x=checks(final=True);seal=strict(SEAL.read_text());assert seal['validation_sha256']==sha((B/'validation.json').read_bytes()) and 'current_manifest_sha256' not in seal
  print(json.dumps(dict(status='PASS',read_only=True,exact_owned_members=len(actual),all_hashes_bytes_equal=True,all_stored_files_strictly_under_40000000=True,checks=x['checks_count'],canonical_native_order=None,dispatch_keys=[],manifest_sha256=sha(MF.read_bytes()),seal_sha256=sha(SEAL.read_bytes()))));return
 raise SystemExit('Use --prepare, --seal or --final')
def pins_roles():return strict((B/'source/pins.json').read_text())['pins']
if __name__=='__main__':main()
