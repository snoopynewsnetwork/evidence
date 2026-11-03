"""Original-only explicit controls, hierarchy and source-position links; no peer inputs."""
import csv,gzip,json,hashlib
from pathlib import Path
from collections import Counter
D=Path(__file__).resolve().parent;R=D.parents[4]
receipts=json.loads((D/'source/receipts.json').read_text());raw={}
for r in receipts:raw[r['id']]=gzip.decompress((R/r['reference_path']).read_bytes())
for p in sorted((D/'source').glob('*.receipt.json')):
 r=json.loads(p.read_text());raw[r['id']]=gzip.decompress((D/'source'/r['asset']).read_bytes())
C=json.load(open(D/'controls.json'));P=list(csv.DictReader((D/'parish-controls.csv').open()));N=json.loads(gzip.decompress((D/'native-results.json.gz').read_bytes()));wb=json.loads(gzip.decompress((D/'source/workbook-position-witness.json.gz').read_bytes()));out={};hier=[];positions={};descriptions=[]
for y in C:
 cc=C[y];date={'2024':'11/05/2024','2022':'11/08/2022','2020':'11/03/2020'}[y];dates=json.loads(raw['sos-graphical-election-dates'])['Dates']['Date'];e=next(d for d in dates if d['ElectionDate']==date);rs=json.loads(raw[f'{y}-StatsRace'])['Stats'];state=rs['HighLevel'];sp=rs['ParishLevel']['Parish'];gen=json.loads(raw['stats2024-state' if y=='2024' else f'stats{y}-Statewide'])['Stats'];native=[r for r in N if r['year']==y];parish=[r for r in P if r['year']==y]
 out[y]={'election':e,'race_high_level':state,'race_parish_level':sp,'general_stats_state':gen,'race_stats_WriteTime':rs['WriteTime'],'null_contexts':dict(ballots_cast=None,blank=None,undervotes=None,overvotes=None,generic_writeins=None,named_writeins=None,registration_active_inactive_scope=None,roll_cutoff=None),'differences':[]}
 for r in parish:
  delta={k:int(r[a])-int(r[b]) for k,a,b in [('qualified','qualified','stats_qualified'),('voted','voted','stats_voted')]};out[y]['differences'].append({'code':r['parish_code'],'parish':r['parish'],**delta})
  arr=[a for a in native if a['parish_code']==r['parish_code']];hier.append({'year':y,'parish_code':r['parish_code'],'parish':r['parish'],'parent_is_overlapping_aggregate':True,'native_disjoint_children':[a['key'] for a in arr],'method_children':{k:[a['key'] for a in arr if a['type']==k] for k in sorted({a['type'] for a in arr})},'statistics_source':f'{y}-StatsRaceParish-'+r['parish_code'],'statistics_rows_are_overlapping_voter_controls':True})
 # Explicit source-native position mapping from all physical row/cell witness, no named-only assumptions.
 parent=None
 for w in [r for r in wb if r['year']==y and r['sheet_name']=='Multi-Parish(Precinct)']:
  vals=[c['value'] for c in w['cells']]
  if vals and len(vals)==1 and vals[0] in {r['parish'] for r in parish}:parent=vals[0]
  if parent and vals and len(vals)==len(cc['candidate_totals'])+1 and all(v is not None and v.isdigit() for v in vals[1:]):positions[(parent,vals[0],tuple(map(int,vals[1:])))]=(w['member'],w['physical_row'])
 for a in native:
  v=json.loads(a['candidate_votes']);member,row=positions[(a['parish'],a['ward']+' '+a['precinct'],tuple(v))];descriptions.append({'key':a['key'],'year':y,'race_id':cc['race_id'],'xlsx_member':member,'xlsx_physical_row':row,'xlsx_candidate_cell_ordinals':list(range(2,len(v)+2)),'csv_record_ordinal':a['csv_row'],'csv_candidate_column_ordinals':list(range(5,len(v)+5)),'api_source':a['api_source'],'api_pointer':'/Precincts/Precinct/'+str(a['api_ordinal']-1),'ward_literal':a['ward'],'precinct_literal':a['precinct'],'workbook_display_literal':a['ward']+' '+a['precinct'],'source_native':a['source_native']})
for n,x in [('scope-controls.json',out),('native-hierarchy.json.gz',hier),('native-position-links.json.gz',descriptions)]:
 b=(json.dumps(x,separators=(',',':'),allow_nan=False)+'\n').encode();(D/n).write_bytes(gzip.compress(b,mtime=0) if n.endswith('.gz') else b)
print('Complete hierarchy and positions',len(descriptions))
