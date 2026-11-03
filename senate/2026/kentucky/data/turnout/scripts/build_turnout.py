#!/usr/bin/env python3
"""Deterministic owned calculations from independent original-first field witnesses."""
import csv,gzip,json,re,collections,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R.parents[1]
def put(name,obj):
 p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def jsonl(name,rows):
 (R/name).write_bytes(gzip.compress(''.join(json.dumps(z,ensure_ascii=False)+'\n' for z in rows).encode(),mtime=0))
def readl(name):return [json.loads(s) for s in gzip.decompress((R/name).read_bytes()).decode().splitlines()]
def ranking(rows,key='votes'):
 a=sorted(rows,key=lambda z:(-z[key],z['key']));n=sum(z[key] for z in a);cum=0;order=[];cross=None
 for i,z in enumerate(a,1):
  before=cum;cum+=z[key];q={**z,'rank':i,'cumulative_votes':cum,'share_numerator':z[key],'share_denominator':n,'share':z[key]/n if n else None,'cumulative_share':cum/n if n else None};order.append(q)
  if cross is None and cum*5>=n*4:cross={'count':i,'votes':cum,'share':cum/n,'preceding_count':i-1,'preceding_votes':before,'preceding_share':before/n,'crossing_key':z['key'],'crossing_votes':z[key]}
 top=sum(z[key] for z in a[:15]);k=cross['count'] if cross else 0
 return {'denominator':n,'units':len(a),'tie_rule':'descending integer votes then ascending complete owned source key','top15':{'count':min(15,len(a)),'votes':top,'share':top/n if n else None,'keys':[z['key'] for z in a[:15]]},'min80':cross,'priority_keys':[z['key'] for z in a[:max(15,k)]],'order':order,'remainder':{'count':len(a)-k,'votes':n-(cross['votes'] if cross else 0),'keys':[z['key'] for z in a[k:]]}}
cert=json.load(open(R/'extracts/certificate-fields.json'));headers=json.load(open(R/'extracts/certificate-headers.json'));controls=json.load(open(R/'extracts/certificate-controls.json'));fips=json.load(open(R/'extracts/county-fips.json'));F={x['county'].casefold():x['fips'] for x in fips};by=collections.defaultdict(lambda:collections.defaultdict(dict))
for x in cert:by[x['contest']][x['county']][x['candidate_column']]=x['value']
counties=sorted(by['2024-president']);C={c.casefold():c for c in counties};N=lambda c:C[c.casefold()]
assert len(F)==len(counties)==120
sensitivity={}
for contest,values in by.items():
 rows=[{'key':F[c.casefold()],'county':c,'votes':sum(v.values())} for c,v in values.items()];sensitivity[contest]=ranking(rows)
stat=json.load(open(R/'extracts/statistics-fields.json'));stat_sources={};county_stats=collections.defaultdict(dict)
for z in stat:
 if z['scope']!='county' or 'by county' not in z['source_role'].casefold():continue
 h=z['source_sha256'];header=' '.join(z['source_header']);year=next((str(y) for y in [2020,2022,2024] if f'{y} General Election' in header),None)
 if year:
  role=f'unofficial_voter_history_{year}';county_stats[N(z['county'])][role]=z;stat_sources[role]=h
 else:role='registration_snapshot_PDF_titled_September_2024';county_stats[N(z['county'])][role]=z;stat_sources[role]=h
for role,h in stat_sources.items():
 field='registered' if role.startswith('registration_') else 'number_voting'
 rows=[{'key':F[c.casefold()],'county':c,'votes':z[role][field]} for c,z in county_stats.items() if role in z]
 assert len(rows)==120,(role,len(rows));sensitivity[role]=ranking(rows)
 if role.startswith('unofficial_'):
  sensitivity[role+'_registration']=ranking([{'key':F[c.casefold()],'county':c,'votes':z[role]['registered']} for c,z in county_stats.items()])
put('county-sensitivity.json',sensitivity)
# Source rows stay source scoped; all raw candidate fields are retained, no source-candidate-key dedup.
fields=readl('extracts/native-fields.jsonl.gz')+json.load(open(R/'extracts/elliott-manual-fields.json'));groups=collections.defaultdict(list)
for z in fields:groups[z['unit_key']].append(z)
pages=readl('extracts/native-page-identities.jsonl.gz');pagegroups=collections.defaultdict(list)
for z in pages:
 if z['native_label'] is not None:pagegroups[(z['county'],z['source_sha256'],z['native_label'])].append(z)
patterns=[r'\bTRUMP\b',r'\bHARRIS\b',r'\bKENNEDY\b',r'\bSTEIN\b',r'\bOLIVER\b',r'\bAYYADURAI\b',r'\bSONSKI\b',r'\bCRUZ\b',r'\bWEST\b',r'\bSODERNA\b',r'\bBOWMAN\b',r'\bKISHORE\b',r'\bCHENG\b',r'\bKELL[YE]Y?\b',r'\bFOX\b',r'\bMCN[Ee][ILl][ILl]?\b|ANDRE RAMON|ANDREW RAMON',r'FUTURE MADAM']
units=[];balance=[];candidate_native=collections.defaultdict(lambda:collections.defaultdict(list))
for key,rows in sorted(groups.items()):
 pres=[z for z in rows if z['scope']=='president'];stats=[z for z in rows if z['scope']=='statistics']
 if not pres:continue
 first=pres[0];county=N(first['county']);fmt=first['format'];val=lambda z:z['tokens'][-1 if fmt=='choice' else 0]['value'];where=lambda z:{'source_sha256':z['source_sha256'],'page':z['page'],'line':z.get('line'),'label':z['label']}
 u={'key':key,'county':county,'county_fips':F[county.casefold()],'source_sha256':first['source_sha256'],'literal_native_label':first['native_label'],'source_native_id':re.match(r'^[A-Z]\d{3}[A-Z]?',first['native_label']).group(0) if re.match(r'^[A-Z]\d{3}[A-Z]?',first['native_label']) else None,'native_identity_type':'source_reporting_group; precinct/combined/style/admin equivalence unapproved','scope':'county_cumulative_summary' if first['native_label']=='[COUNTY CUMULATIVE SUMMARY]' else 'mail_in_only_slice' if county=='Magoffin' else 'captured_native_source_slice','method_header_contexts':[{'page':z['page'],'line':z.get('line'),'raw_header_lines':z['method_header']} for z in pres if z['kind'] in ('cast_votes','contest_totals') or z is first],'candidate_rows':[],'ballots_cast':None,'blank_ballots':None,'registration':None,'undervotes':None,'overvotes':None,'source_pages':sorted({z['page'] for z in pres}),'current_identity_approved':False,'geometry_approved':False,'cross_year_join':False,'source_position_unit_header':[]}
 mapped=collections.defaultdict(list);pool=[];unassigned=[];cast=[]
 for z in pres:
  rec={**where(z),'kind':z['kind'],'values_in_source_method_order':[a['value'] for a in z['tokens']],'total':val(z),'null_status':'explicit_source_integer'}
  if z['kind'] in ('candidate','writein_pool','writein_unassigned'):
   if z['kind']=='candidate':
    matches=[i for i,p in enumerate(patterns,1) if re.search(p,z['label'],re.I)]
    # KENNEDY running mate on a write-in line is not the Robert Kennedy candidate.
    if 17 in matches:matches=[17]
    if 3 in matches and 'FUTURE' in z['label'].upper():matches.remove(3)
    rec['certificate_column_association']=matches[0] if len(matches)==1 else None;rec['association_status']='manual name/header association; raw label retained' if len(matches)==1 else 'unresolved literal identity'
    if len(matches)==1:mapped[matches[0]].append(rec);candidate_native[county][matches[0]].append(rec)
   if z['kind']=='writein_pool':pool.append(rec)
   if z['kind']=='writein_unassigned':unassigned.append(rec)
   u['candidate_rows'].append(rec)
  elif z['kind']=='cast_votes':cast.append(rec)
  elif z['kind']=='undervotes':u['undervotes']=rec
  elif z['kind']=='overvotes':u['overvotes']=rec
 # candidate sum excludes named/unassigned children when generic pool is present.
 selected=[z for z in pres if z['kind']=='writein_pool' or (z['kind']=='candidate' and (fmt=='choice' or not z['label'].startswith('Write-In:')))]
 total=sum(val(z) for z in selected);u['source_candidate_sum']=total;u['source_reported_cast_votes']=cast[0]['total'] if len(cast)==1 else None;u['cast_votes_source_rows']=cast
 u['votes']=u['source_reported_cast_votes'] if len(cast)==1 else total;u['votes_definition']='reported cast votes including generic write-ins/unassigned where present; otherwise explicit candidate-plus-generic-pool sum'
 u['source_row_sum_matches_cast']=None if len(cast)!=1 else total==cast[0]['total'];u['cast_row_count']=len(cast)
 if len(cast)>1 or u['source_row_sum_matches_cast'] is False:balance.append({'key':key,'sum':total,'cast_rows':cast})
 u['certified_candidate_columns']=[{'column':i,'reported_source_values':mapped[i],'value':mapped[i][0]['total'] if len(mapped[i])==1 else None,'null_status':'explicit source row' if len(mapped[i])==1 else 'not_separately_available_or_ambiguous'} for i in range(1,18)]
 for z in stats:
  v=z['tokens'][0]['value'] if z['tokens'] else None
  if z['label'].startswith('Registered Voters'):u['registration']={'value':v,'source':where(z),'status':'source printed registration; zero is retained, not eligible-voter proof'}
  if z['label'].startswith('Ballots Cast - Total'):u['ballots_cast']={'value':v,'source':where(z)}
  if z['label'].startswith('Ballots Cast - Blank'):u['blank_ballots']={'value':v,'source':where(z)}
 pg=pagegroups.get((first['county'],first['source_sha256'],first['native_label']),[])
 for q in pg:
  if q.get('unit_ballots'):
   u['source_position_unit_header'].append({'page':q['page'],**q['unit_ballots']})
   if u['ballots_cast'] is None:u['ballots_cast']={'value':q['unit_ballots']['value'],'source':{'page':q['page'],'line':q['unit_ballots']['line'],'raw_line':q['unit_ballots']['raw_line']}}
 units.append(u)
assert not balance,balance[:3]
jsonl('native-units.jsonl.gz',units)
known=[{'key':u['key'],'county':u['county'],'county_fips':u['county_fips'],'native_label':u['literal_native_label'],'votes':u['votes'],'scope':u['scope']} for u in units if u['scope']!='county_cumulative_summary']
known_order=ranking(known);known_order['qualification']='Captured source-native report slices only; excludes Scott summary, includes Magoffin Mail In slice, varies write-in universe. Not a complete statewide native election geography, no dispatch.';put('known-native-order.json',known_order)
# Retain all source-native participation/registration/admin identities independently; no equality to recap IDs inferred.
constituents=collections.defaultdict(list)
for z in stat:
 if z['county'] and z['scope'] in ('native_registration_or_participation','administrative_summary'):
  constituents[N(z['county'])].append({'source_sha256':z['source_sha256'],'source_role':z['source_role'],'label':z['label'],'scope':z['scope'],'page':z['page'],'line':z['line'],'registration':z.get('registered'),'number_voting':z.get('number_voting'),'recap_join_approved':False})
jsonl('source-native-statistics-identities.jsonl.gz',[{'county':c,'constituents':a} for c,a in sorted(constituents.items())])
# Every county/candidate comparison uses available raw source rows only; absent named write-ins remain null.
comparisons=[]
for county in counties:
 us=[u for u in units if u['county']==county];h=us[0]['source_sha256'] if us else None
 for i in range(1,18):
  cells=[q for u in us for q in u['certified_candidate_columns'] if q['column']==i];values=[q['value'] for q in cells if q['value'] is not None]
  complete=bool(cells) and len(values)==len(cells);available_sum=sum(values) if values else None
  comparisons.append({'county':county,'county_fips':F[county.casefold()],'column':i,'certificate_value':by['2024-president'][county][i],'source_sha256':h,'source_unit_count':len(us),'explicit_value_unit_count':len(values),'all_captured_units_have_column':complete,'available_source_sum':available_sum,'source_sum':available_sum if complete else None,'difference':available_sum-by['2024-president'][county][i] if complete else None,'scope':'Mail In only' if county=='Magoffin' else 'county cumulative only' if county=='Scott' else 'captured native source','missing_is_zero':False})
put('native-certificate-comparisons.json',comparisons)
# County CSV is explicitly a parent-level sensitivity, never canonical native dispatch.
recapcontrols={x['county'].casefold():x for x in json.load(open(R/'extracts/recap-report-controls.json'))}
county_order=sensitivity['2024-president'];rankmap={z['county']:z for z in county_order['order']};priority=county_order['priority_keys'];csvrows=[]
for county in counties:
 z=rankmap[county];row={'county':county,'fips':F[county.casefold()],'geography_type':'county_parent_sensitivity','rank_president_2024':z['rank'],'president_2024_total':z['votes'],'share_president_2024':z['share'],'cumulative_votes_president_2024':z['cumulative_votes'],'cumulative_share_president_2024':z['cumulative_share'],'county_top15_sensitivity':z['rank']<=15,'county_min80_sensitivity':z['rank']<=county_order['min80']['count'],'county_priority_sensitivity':F[county.casefold()] in priority,'senate_2022_total':sum(by['2022-senate'][county].values()),'senate_2020_total':sum(by['2020-senate'][county].values()),'canonical_native_rank':None,'canonical_native_priority':None,'native_dispatch_approved':False}
 for contest in by:
  for i,v in sorted(by[contest][county].items()):row[f'{contest}_column_{i:02}']=v
 for role,zs in county_stats[county].items():
  row[role+'_registered']=zs['registered'];row[role+'_number_voting']=zs['number_voting']
 us=[u for u in units if u['county']==county];row['captured_native_source_units']=sum(u['scope']!='county_cumulative_summary' for u in us);row['recap_source_reported_contest_votes']=sum(u['votes'] for u in us);row['recap_source_scope']='Mail In only' if county=='Magoffin' else 'county cumulative only' if county=='Scott' else 'native source, raw candidate/write-in universe';row['recap_ballots_sum']=sum(u['ballots_cast']['value'] for u in us) if all(u['ballots_cast'] is not None for u in us) else None;row['recap_reported_ballots']=recapcontrols[county.casefold()]['header_ballots_cast'] if recapcontrols[county.casefold()]['header_ballots_cast'] is not None else row['recap_ballots_sum'];row['recap_reported_ballots_scope']=row['recap_source_scope'];row['certified_ballots_cast']=None;row['eligible_voter_denominator']=None
 csvrows.append(row)
assert all(z['recap_reported_ballots'] is not None for z in csvrows)
sensitivity['captured_recap_ballots_source_scope']=ranking([{'key':z['fips'],'county':z['county'],'votes':z['recap_reported_ballots'],'scope':z['recap_reported_ballots_scope']} for z in csvrows]);sensitivity['captured_recap_ballots_source_scope']['qualification']='Source-scoped captured report ballots, includes Mail In-only Magoffin; not a statewide certified ballot control or turnout rate.'
put('county-sensitivity.json',sensitivity)
with (S/'data/county-turnout.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(csvrows[0]));writer.writeheader();writer.writerows(sorted(csvrows,key=lambda z:z['rank_president_2024']))
coverage=[]
portfolio=json.load(open(R/'extracts/portfolio.json'))
for county in counties:
 us=[u for u in units if u['county']==county];src=next(x for x in portfolio if x['role'].startswith('2024 county recap:') and N(x['role'].split(': ',1)[1])==county)
 coverage.append({'county':county,'fips':F[county.casefold()],'certificate_parent_available':True,'recap_original_available':True,'source_sha256':src['source_sha256'],'source_pages':src['pages'],'recap_scope':'county_cumulative_only_no_native' if county=='Scott' else 'Mail_In_only_native_slices' if county=='Magoffin' else 'captured_native_report','canonical_native_complete':False,'available_native_constituents':[{'key':u['key'],'literal_id':u['source_native_id'],'literal_label':u['literal_native_label'],'scope':u['scope'],'source_pages':u['source_pages'],'method_header_contexts':u['method_header_contexts'],'administrative_case':u['source_native_id'] is None,'current_geographic_approval':False} for u in us],'unavailable_case':'No native presidential rows in live/archived county cumulative report' if county=='Scott' else 'Non-Mail-In contest methods unavailable in captured recap' if county=='Magoffin' else 'Complete source-native valid-write-in/certified-vintage reconciliation not established','separate_statistics_constituents_count':len(constituents[county]),'statistics_constituents_file':'source-native-statistics-identities.jsonl.gz'})
put('coverage.json',coverage)
flags={k:False for k in ['current_identity_approved','legal_approved','geographic_approved','eligible_writein_approved','november_2026_approved','live_ids_verified','cadence_verified','exact_remaining_pool_known','collector_implemented','forecast_implemented','calibrated','canonical_native_coverage_complete','coordinator_accepted','independent_peer_agreement']}
contract={'state':'KY','question':'turnout','primary_election':'2024-11-05','primary_contest':'President and Vice President of the United States','certified_county_candidate_total':sum(z['value'] for z in controls if z['contest']=='2024-president'),'source_universe':'all named ballot and named valid write-in ticket columns in amended certificate; native generic-write-in universes separately retained','complete_coverage':False,'order':None,'top15':None,'min80':None,'priority':None,'remainder':None,'ordered_priority_keys':[],'dispatch_keys':[],'canonical_statewide_native':{'total':None,'order':None,'top15':None,'min80':None,'priority':None,'remainder':None,'dispatch_keys':[]},'county_sensitivity_file':'county-sensitivity.json','qualified_known_native_file':'known-native-order.json','complete_candidate_fields_file':'extracts/certificate-fields.json','native_full_fields_file':'extracts/native-fields.jsonl.gz','native_manual_fields_file':'extracts/elliott-manual-fields.json','native_units_file':'native-units.jsonl.gz','coverage':coverage,'all_statistics_native_admin_constituents_file':'source-native-statistics-identities.jsonl.gz','historical_native_hierarchy_file':'extracts/historical-handwritten-hierarchy.json','peer_agent_id':'ce1620b8-8df0-406b-bdb1-a8522aeea2f4','peer_existence_proof':'user coordinator informational update; not agreement','peer_agreement_status':'pending captured-final comparison','flags':flags,'bounded_research_complete':True,'external_gate_is_worker_finish_requirement':False}
put('priority-set.json',contract)
# Source entity index includes all original source bodies exactly once by raw hash, with every acquisition role.
entities={}
for z in json.load(open(R/'source/refs.json')):entities[z['raw_sha256']]={**z,'storage_basis':'shared immutable original pin; stored once outside owned package','roles':[],'receipts':[]}
for f in sorted((R/'source/receipts').glob('*.json')):
 z=json.load(open(f));rs=z.get('hops',[]) or ([{'raw_sha256':z['raw_sha256']}] if z.get('raw_sha256') else [])
 for hop in rs:
  h=hop['raw_sha256'];entities.setdefault(h,{'raw_sha256':h,'path':hop.get('body'),'raw_bytes':hop.get('raw_bytes'),'stored_sha256':hop.get('stored_sha256'),'stored_bytes':hop.get('stored_bytes'),'storage_basis':'owned original byhash','roles':[],'receipts':[]});entities[h]['roles'].append(z.get('role',z.get('id')));entities[h]['receipts'].append(str(f.relative_to(R)))
put('source/entities.json',list(entities.values()))
print('built',len(csvrows),'county rows;',len(units),'source units;',len(known),'known native slices;',len(comparisons),'candidate comparisons; canonical NULL/dispatch EMPTY')
print('county primary',county_order['top15'],county_order['min80'])
