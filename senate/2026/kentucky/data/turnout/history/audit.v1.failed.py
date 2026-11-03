#!/usr/bin/env python3
"""Full offline audit. --record writes preseal validation only; --final is strictly read-only."""
import csv,gzip,json,re,hashlib,subprocess,sys,collections,datetime,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def read(name):return json.load(open(R/name))
def readl(name):return [json.loads(x) for x in gzip.decompress((R/name).read_bytes()).decode().splitlines()]
def require(ok,message):
 if not ok:raise AssertionError(message)
def owned_files():return sorted([S/'turnout.md',S/'data/county-turnout.csv']+[p for p in R.rglob('*') if p.is_file()])
def rankcheck(x):
 order=x['order'];n=x['denominator'];require(len(order)==x['units'] and len({q['key'] for q in order})==len(order),'rank identities')
 require(order==sorted(order,key=lambda z:(-z['votes'],z['key'])),'descending complete key order');cum=0
 for i,q in enumerate(order,1):
  require(isinstance(q['votes'],int) and q['votes']>=0,'negative/noninteger rank input');cum+=q['votes'];require(q['rank']==i and q['cumulative_votes']==cum,'rank/cumulative');require(q['share_numerator']==q['votes'] and q['share_denominator']==n,'exact denominator');require(abs(q['share']-q['votes']/n)<1e-14 and abs(q['cumulative_share']-cum/n)<1e-14,'weights')
 require(cum==n and abs(sum(q['share'] for q in order)-1)<1e-12,'all units weight/denominator')
 top=x['top15'];require(top['keys']==[q['key'] for q in order[:15]] and top['votes']==sum(q['votes'] for q in order[:15]),'top15')
 m=x['min80'];k=m['count'];require(k>0 and m['votes']==sum(q['votes'] for q in order[:k]) and m['votes']*5>=n*4,'crossing80');require(m['preceding_count']==k-1 and m['preceding_votes']==sum(q['votes'] for q in order[:k-1]) and m['preceding_votes']*5<n*4,'minimum80');require(m['crossing_key']==order[k-1]['key'] and m['crossing_votes']==order[k-1]['votes'],'crossing identity')
 require(x['priority_keys']==[q['key'] for q in order[:max(15,k)]],'ordered priority');require(x['remainder']['keys']==[q['key'] for q in order[k:]] and x['remainder']['votes']==n-m['votes'] and x['remainder']['count']==len(order)-k,'full remainder')
def nullcheck(x):
 for k in ['order','top15','min80','priority','remainder']:require(x[k] is None,'canonical native must stay NULL: '+k)
 require(x['dispatch_keys']==[] and x['ordered_priority_keys']==[] and x['complete_coverage'] is False,'empty dispatch guard');require(all(v is False or v is None for v in x['flags'].values()),'nonapproval guard')
 for k,v in x['canonical_statewide_native'].items():require(v==[] if k=='dispatch_keys' else v is None,'nested canonical null guard')
checks={};warnings=[]
files=owned_files();require(all(p.exists() for p in files),'owned required files')
require(all(p.stat().st_size<40000000 for p in files),'strict artifact size');require(not any('__pycache__' in p.parts or p.suffix=='.pyc' or any(z in p.parts for z in ['node_modules','.cache','.venv']) for p in files),'no dependency/cache files');require(not any(p.is_symlink() for p in files),'no mutable symlink assets');checks['owned_size_cache_bounds']=len(files)
# Every original is checked as an exact entity; all HTTP observations remain distinct receipts.
raw={};stored={}
for z in read('source/refs.json'):
 p=S/z['path'];b=p.read_bytes();v=gzip.decompress(b);require(sha(b)==z['stored_sha256'] and sha(v)==z['raw_sha256'] and len(b)==z['stored_bytes'] and len(v)==z['raw_bytes'],'shared source pin '+str(p));raw[z['raw_sha256']]=v;stored[z['raw_sha256']]=p
for p in sorted((R/'source/bodies').glob('*.gz')):
 b=p.read_bytes();v=gzip.decompress(b);require(sha(v)==p.stem,'owned byhash entity');require(sha(v) not in stored,'original entity must be stored once/byhash');raw[sha(v)]=v;stored[sha(v)]=p
for p in (R/'source/receipts').glob('*.json'):
 x=json.load(open(p))
 for hop in x.get('hops',[]):
  h=hop['raw_sha256'];require(h in raw and len(raw[h])==hop['raw_bytes'],'receipt body pin');q=R/hop['body'];require(sha(q.read_bytes())==hop['stored_sha256'] and q.stat().st_size==hop['stored_bytes'],'receipt stored pin');require(hop['status'] in range(100,600) and isinstance(hop['headers'],dict),'HTTP metadata')
 if x.get('error'):require(x.get('hops')==[] or bool(x['hops']),'preserve failed receipt')
entities=read('source/entities.json');require(len({z['raw_sha256'] for z in entities})==len(entities),'source entity uniqueness');require({z['raw_sha256'] for z in entities}==set(raw),'full entity membership');checks['original_entities']=len(raw)
# Offline replay every captured PDF's complete text, using stdin/stdout; no disk or network writes.
replayed=0
for p in sorted((R/'extracts').glob('*.layout.txt')):
 h=p.name.split('.')[0]
 if h not in raw:continue
 require(raw[h].startswith(b'%PDF'),'PDF magic '+h)
 z=subprocess.run(['pdftotext','-layout','-','-'],input=raw[h],capture_output=True);require(z.returncode==0 and z.stdout==p.read_bytes(),'offline complete PDF text replay '+h)
 if z.stderr:warnings.append({'source_sha256':h,'tool':'pdftotext','returncode':z.returncode,'stderr':z.stderr.decode(errors='replace')})
 replayed+=1
checks['complete_pdf_text_replays']=replayed
# Frozen original-first bodies are independently hash verified; mutable current derivatives are never numeric inputs here.
for name in ['history/original-first/witness.json','history/original-first-v2/witness.json']:
 w=read(name)
 for z in w['bodies']:
  p=R/z['immutable_body'];v=gzip.decompress(p.read_bytes());require(sha(v)==z['sha256'] and len(v)==z['bytes'],'original first witness body')
 for z in w['owned_originals']:require(sha((R/z['path']).read_bytes())==z['stored_sha256'] and z['raw_sha256'] in raw,'original first raw pin')
checks['independent_original_first_witnesses']=2
fields=read('extracts/certificate-fields.json');ctrl=read('extracts/certificate-controls.json');headers=read('extracts/certificate-headers.json');expected={'2024-president':17,'2022-senate':4,'2020-senate':8};countysets=[]
for z in fields+ctrl:
 lines=(R/'extracts'/f"{z['source_sha256']}.layout.txt").read_text().split('\f')[z['page']-1].splitlines();line=lines[z['line']-1];require(line==z['raw_line'] and line[z['character_start']:z['character_end']]==z['raw_token'],'exact certificate source position');require(int(z['raw_token'].replace(',',''))==z['value'] and z['value']>=0,'certificate original integer')
for contest,width in expected.items():
 a=[z for z in fields if z['contest']==contest];b=[z for z in ctrl if z['contest']==contest];cs={z['county'] for z in a};countysets.append(cs);require(len(a)==120*width and len(cs)==120 and len(b)==width,'all counties/candidates')
 require(len({(z['county'],z['candidate_column']) for z in a})==len(a),'candidate identity uniqueness')
 for i in range(1,width+1):require(sum(z['value'] for z in a if z['candidate_column']==i)==next(z['value'] for z in b if z['candidate_column']==i),'primary statewide candidate reconciliation')
 for c in cs:require({z['candidate_column'] for z in a if z['county']==c}==set(range(1,width+1)),'complete county candidate universe')
 require(all(len(z['candidates_display_transcription'])==width for z in headers if z['contest']==contest),'candidate/header width')
require(all(x==countysets[0] for x in countysets),'all contest same120 parents');checks['certificate_county_cells']=len(fields);checks['certificate_footer_controls']=len(ctrl)
# Complete original native row positions; methods are never summed together with TOTAL.
native=readl('extracts/native-fields.jsonl.gz');method_exceptions=[]
for z in native:
 line=(R/'extracts'/f"{z['source_sha256']}.layout.txt").read_text().split('\f')[z['page']-1].splitlines()[z['line']-1];require(line==z['raw_line'],'native complete original line')
 for token in z['tokens']:
  require(line[token['start']:token['end']]==token['raw_token'] and int(token['raw_token'].replace(',',''))==token['value'] and token['value']>=0,'native source token')
 if z['scope']=='president' and len(z['tokens'])>1:
  v=[q['value'] for q in z['tokens']];total=v[-1] if z['format']=='choice' else v[0];parts=v[:-1] if z['format']=='choice' else v[1:]
  if total!=sum(parts):method_exceptions.append({'source_sha256':z['source_sha256'],'page':z['page'],'line':z['line'],'label':z['label'],'source_values':v})
require(not method_exceptions,'source native method balance exceptions '+str(method_exceptions[:2]));checks['native_positioned_rows']=len(native)
manual=read('extracts/elliott-manual-fields.json');require(len(manual)==84 and len({z['unit_key'] for z in manual})==7,'Elliott complete seven image precincts')
for z in manual:require((R/z['page_image']).is_file() and z['tokens'][0]['value']>=0,'manual image source witness')
units=readl('native-units.jsonl.gz');require(len(units)==3221 and len({z['key'] for z in units})==len(units),'native identity coverage');require(len({z['county_fips'] for z in units})==120,'native inventory all parent120')
for u in units:
 require(u['source_row_sum_matches_cast'] is not False and u['cast_row_count']<=1,'native candidates/cast no duplicate source total');require(len(u['certified_candidate_columns'])==17,'all17 columns incl null');require(u['source_sha256'] in raw,'native raw reference');require(u['current_identity_approved'] is False and u['cross_year_join'] is False and u['geometry_approved'] is False,'native negative approval guard')
 for col in u['certified_candidate_columns']:
  if col['value'] is None:require(col['null_status']=='not_separately_available_or_ambiguous','missing native not zero')
checks['native_source_entities']=len(units)
# All turnout/registration original source rows and explicit parent/footer party controls.
stat=read('extracts/statistics-fields.json');bysrc=collections.defaultdict(list)
for z in stat:
 line=(R/'extracts'/f"{z['source_sha256']}.layout.txt").read_text().split('\f')[z['page']-1].splitlines()[z['line']-1];require(line==z['raw_line'],'statistics exact source position');require(all(v>=0 for v in z['source_columns']),'statistics count bounds');bysrc[z['source_sha256']].append(z)
 if z.get('number_voting') is not None:
  v=z['source_columns'];require(len(v)==8 and v[0]==v[2]+v[4]+v[6] and v[1]==v[3]+v[5]+v[7],'turnout party controls');require(z['candidate_votes'] is None and z['ballots_cast'] is None,'voter history not ballots/candidate votes')
for h,a in bysrc.items():
 county=[z for z in a if z['scope']=='county'];footer=[z for z in a if z['scope']=='state_footer']
 if county:
  require(len(county)==120 and len({z['source_county_code'] for z in county})==120,'statistics120 county IDs');require(len(footer)==1,'statistics printed state footer');width=len(footer[0]['source_columns']);require(all(len(z['source_columns'])==width for z in county),'statistics column widths');require([sum(z['source_columns'][i] for z in county) for i in range(width)]==footer[0]['source_columns'],'statistics whole-state printed control')
regnative=[z for z in stat if z['source_role']=='general registration sensitivity: By Precinct' and z['scope']=='native_registration_or_participation'];require(len(regnative)==3232,'all3232 original registration native identities');checks['statistics_positioned_rows']=len(stat)
# Complete county CSV integer sums, independent footer denominator and all ordering variants.
fips=read('extracts/county-fips.json');require(len(fips)==120 and len({z['fips'] for z in fips})==120,'county FIPS coverage');csvrows=list(csv.DictReader(open(S/'data/county-turnout.csv')));require(len(csvrows)==120 and len({z['fips'] for z in csvrows})==120,'CSV120 uniqueness')
for contest,width in expected.items():
 cols=[f'{contest}_column_{i:02}' for i in range(1,width+1)]
 for i,col in enumerate(cols,1):require(sum(int(z[col]) for z in csvrows)==next(z['value'] for z in ctrl if z['contest']==contest and z['candidate_column']==i),'CSV each candidate statewide')
for z in csvrows:require(z['canonical_native_rank']=='' and z['canonical_native_priority']=='' and z['native_dispatch_approved']=='False','CSV null dispatch')
sens=read('county-sensitivity.json')
for x in sens.values():rankcheck(x);require(x['units']==120,'all county sensitivity120')
k=read('known-native-order.json');rankcheck(k);require(k['units']==3220 and k['denominator']==sum(u['votes'] for u in units if u['scope']!='county_cumulative_summary'),'qualified native full universe')
contract=read('priority-set.json');nullcheck(contract);require(len(contract['coverage'])==120 and len({q['fips'] for q in contract['coverage']})==120,'dispatch all120 parents');require(sum(len(q['available_native_constituents']) for q in contract['coverage'])==3221,'all native constituents dispatch contract')
require(next(q for q in contract['coverage'] if q['county']=='Scott')['recap_scope']=='county_cumulative_only_no_native','Scott unavailable native parent retained');require(next(q for q in contract['coverage'] if q['county']=='Magoffin')['recap_scope']=='Mail_In_only_native_slices','Magoffin filter retained')
checks['all_orders_integer_80']=len(sens)+1
# Negative audits must reject bad complete orders and attempts to replace canonical nulls with county priorities.
negative=[]
for label,mutate in [('negative vote',lambda x:x['order'][0].__setitem__('votes',-1)),('wrong denominator',lambda x:x.__setitem__('denominator',x['denominator']+1)),('nonminimum80',lambda x:x['min80'].__setitem__('preceding_votes',x['min80']['votes'])),('missing remainder',lambda x:x['remainder']['keys'].pop()),('reversed order',lambda x:x['order'].reverse())]:
 x=copy.deepcopy(sens['2024-president']);mutate(x)
 try:rankcheck(x)
 except AssertionError:negative.append(label)
 else:raise AssertionError('negative checker accepted '+label)
x=copy.deepcopy(contract);x['order']=sens['2024-president']['order']
try:nullcheck(x)
except AssertionError:negative.append('county substitution rejected')
else:raise AssertionError('negative null guard accepted county substitution')
checks['negative_cases_rejected']=negative
# All relative artifact/report links are bounded and resolve; external URLs are primary source citations, never fetched in audit.
links=[]
for p in [S/'turnout.md',R/'source/SCHEMA.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('https://','http://','#')):continue
  q=(p.parent/target.split('#')[0]).resolve();require(q.is_relative_to(S.resolve()) and q.exists(),'relative link/bounds '+str(p)+': '+target);links.append(target)
for z in read('source/entities.json'):
 for target in z['receipts']:require((R/target).is_file(),'entity receipt link')
checks['relative_links']=len(links)
if '--final' in sys.argv:
 manifest=read('asset-manifest.json');listed=manifest['files'];actual={str(p.relative_to(S)) for p in owned_files() if p!=R/'asset-manifest.json'};require({z['path'] for z in listed}==actual and len(listed)==len(actual),'FINAL complete manifest membership, excludes only itself')
 for z in listed:
  p=S/z['path'];require(p.is_file() and p.stat().st_size==z['bytes'] and sha(p.read_bytes())==z['sha256'] and z['bytes']<40000000,'FINAL asset hash/size '+z['path'])
 seal=read('finalseal.json');require('asset_manifest_sha256' not in seal,'no reverse manifest digest cycle');require(seal['validation_sha256']==sha((R/'validation.json').read_bytes()),'validation seal');require(read('validation.json')['status']=='preseal_checks_satisfied','preseal validation record')
 print(json.dumps({'status':'PASS','final_readonly':True,'checks':checks,'source_tool_warnings':warnings,'owned_members_verified':len(actual),'manifest_sha256':sha((R/'asset-manifest.json').read_bytes()),'no_owned_writes_performed':True},indent=2))
else:
 result={'status':'preseal_checks_satisfied','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'source_tool_warnings':warnings,'canonical_native_complete':False,'dispatch_keys':[],'independent_peer_agreement':False,'coordinator_accepted':False,'network_calls':0}
 if '--record' in sys.argv:(R/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
