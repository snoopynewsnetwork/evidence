"""Independent complete OOXML/CSV/native JSON original-source audit."""
from pathlib import Path
from collections import Counter,defaultdict
from zipfile import ZipFile
from html import unescape
import csv,gzip,hashlib,io,json,posixpath,sys,xml.etree.ElementTree as ET
S=Path(__file__).resolve().parents[1];B=S/'data/baselines';ROOT=S.parents[2];N=0;stats=Counter()
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def unique(pairs):
 d={}
 for k,v in pairs:ck(k not in d,'duplicate source JSON field');d[k]=v
 return d
mf=load(B/'asset-manifest.json');before={};actual={str(p.relative_to(ROOT)) for p in B.rglob('*') if p.is_file() and p!=B/'asset-manifest.json'}|{str((S/'county-partisanship.md').relative_to(ROOT)),str((S/'data/county-baselines.csv').relative_to(ROOT))}
ck(len(mf['assets'])==1607 and {r['path'] for r in mf['assets']}==actual)
for r in mf['assets']:
 p=ROOT/r['path'];b=p.read_bytes();ck(not p.is_symlink() and len(b)==r['bytes']<40000000 and sha(b)==r['sha256']);before[r['path']]=sha(b)
receipts=load(B/'source/receipts.json')+[load(p) for p in sorted((B/'source').glob('*.receipt.json'))];raw={};parsed={}
for r in receipts:
 p=ROOT/r['reference_path'] if 'reference_path' in r else B/'source'/r['asset'];b=p.read_bytes();ck(len(b)<40000000 and sha(b)==r['stored_sha256']);data=gzip.decompress(b);ck(len(data)==r['bytes'] and sha(data)==r['raw_sha256'])
 ck(r['id'] not in raw,'unique source identity');raw[r['id']]=data
 if data.lstrip().startswith((b'{',b'[')):parsed[r['id']]=json.loads(data,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
 stats['whole_original_body_and_receipt_roles']+=1
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};rel_ns='http://schemas.openxmlformats.org/officeDocument/2006/relationships';workbook_rows={};witness=load(B/'source/workbook-position-witness.json.gz');position=0
for year in ['2024','2022','2020']:
 z=ZipFile(io.BytesIO(raw[f'sos-{year}-full-results-xlsx']));ck(z.testzip() is None and len(z.namelist())==len(set(z.namelist())))
 for info in z.infolist():ck(len(z.read(info))==info.file_size);stats['complete_workbook_ZIP_members']+=1
 shared=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  shared=[''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
 rels={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))};wb=ET.fromstring(z.read('xl/workbook.xml'));sheets=wb.find('m:sheets',ns)
 for si,sheet in enumerate(sheets,1):
  target=rels[sheet.attrib['{'+rel_ns+'}id']];member=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('xl',target));tree=ET.fromstring(z.read(member));rows=tree.find('m:sheetData',ns)
  for ri,row in enumerate(rows,1):
   cells=[]
   for ci,cell in enumerate(row,1):
    typ=cell.attrib.get('t');v=cell.find('m:v',ns)
    if typ=='inlineStr':val=''.join(cell.find('m:is',ns).itertext()) if cell.find('m:is',ns) is not None else None
    elif v is None:val=None
    elif typ=='s':val=shared[int(v.text)]
    elif typ in ('str','e'):val=v.text
    else:val=v.text
    cells.append({'physical_cell':ci,'attributes':dict(cell.attrib),'value':val,'xml':ET.tostring(cell,encoding='unicode')});stats['whole_physical_cell_values_and_XML_records']+=1
   got={'year':year,'sheet_ordinal':si,'sheet_name':sheet.attrib['name'],'member':member,'physical_row':ri,'row_attributes':dict(row.attrib),'cells':cells}
   ck(got==witness[position],('complete original physical OOXML row',year,member,ri));position+=1;workbook_rows[year,member,ri]=cells
ck(position==len(witness)==149741)
native=load(B/'native-results.json.gz');links=load(B/'native-position-links.json.gz');ck(len(native)==len(links)==12060);bykey={r['key']:r for r in native};linkbykey={r['key']:r for r in links};ck(len(bykey)==len(linkbykey)==12060)
summary=[]
for year,race,width,count in [('2024','67190',11,3933),('2022','61897',13,4065),('2020','59569',15,4062)]:
 rows=list(csv.reader(io.StringIO(raw[f'sos-{year}-selected-precinct-csv'].decode('utf-8-sig'))));header=rows[0];ck(len(header)==4+width and len(rows)-1==count)
 meta=next(r for r in parsed[f'sos-{year}-race-metadata']['Races']['Race'] if r['ID']==race);choices=meta['Choice'];ck(len(choices)==width);choiceids=[r['ID'] for r in choices];totals=[0]*width;parish_vectors=defaultdict(lambda:[0]*width)
 for ordinal,cells in enumerate(rows[1:],2):
  matches=[r for r in native if r['year']==year and r['csv_row']==ordinal];ck(len(matches)==1);r=matches[0];l=linkbykey[r['key']];votes=[int(v) for v in cells[4:]]
  ck((r['parish'],r['ward'],r['precinct'])==tuple(cells[1:4]) and r['key']==json.dumps([year,r['parish_code'],r['ward'],r['precinct']],separators=(',',':')))
  ck(json.loads(r['candidate_votes'])==votes and r['all_candidate_votes']==sum(votes))
  wc=workbook_rows[year,l['xlsx_member'],l['xlsx_physical_row']];ck([int(wc[i-1]['value']) for i in l['xlsx_candidate_cell_ordinals']]==votes and wc[0]['value']==l['workbook_display_literal'])
  api=parsed[r['api_source']]['Precincts']['Precinct'][r['api_ordinal']-1];ck(api['Precinct']==r['source_native'] and api['Precinct']==l['source_native'])
  ck([a['ID'] for a in api['Choice']]==choiceids and [int(a['VoteTotal']) for a in api['Choice']]==votes)
  for src,dst in [('VoterCountQualified','qualified'),('VoterCountVoted','voted'),('HasReported','has_reported')]:ck(api.get(src)==r[dst])
  ck(r['blank_under_over'] is None and l['api_source']==r['api_source'] and l['csv_record_ordinal']==ordinal)
  totals=[a+b for a,b in zip(totals,votes)];parish_vectors[r['parish_code']]=[a+b for a,b in zip(parish_vectors[r['parish_code']],votes)];stats['complete_three_lane_native_vectors']+=1;stats['native_candidate_cells']+=width
 parishcsv=list(csv.reader(io.StringIO(raw[f'sos-{year}-selected-parish-csv'].decode('utf-8-sig'))));ck(len(parishcsv)==65 and len(parishcsv[0])==width+2)
 candidates=[r for r in csv.DictReader((B/'candidates.csv').open()) if r['year']==year];ck(len(candidates)==width)
 for i,(r,meta_choice) in enumerate(zip(candidates,choices)):
  ck(r['label']==parishcsv[0][i+2] and r['metadata_label']==meta_choice['Desc'] and r['choice_id']==meta_choice['ID'] and int(r['source_column'])==i+3 and r['race_id']==race)
  ck(r['party']==r['label'].rsplit('(',1)[1].rstrip(')') and int(r['votes'])==totals[i] and int(r['all_candidate_total'])==sum(totals));stats['complete_candidate_label_party_metadata_controls']+=1
 controls=[r for r in csv.DictReader((B/'parish-controls.csv').open()) if r['year']==year];ck(len(controls)==len(parish_vectors)==64)
 for r in controls:
  row=next(v for v in parishcsv[1:] if v[1]==r['parish']);ck([int(v) for v in row[2:]]==parish_vectors[r['parish_code']])
  ck(json.loads(r['candidate_votes'])==parish_vectors[r['parish_code']] and int(r['all_candidate_votes'])==sum(parish_vectors[r['parish_code']]))
 summary.append({'year':year,'race':race,'native_records':count,'parishes':64,'candidate_columns':width,'complete_candidate_totals':totals,'all_candidate_total':sum(totals)})
pos=load(B/'source/json-position-witness.json.gz');k=0
def walk(sid,v,pointer='',ordinal=0):
 global k
 typ='object' if isinstance(v,dict) else 'array' if isinstance(v,list) else type(v).__name__;value=len(v) if isinstance(v,(dict,list)) else v
 ck(pos[k]==[sid,pointer,ordinal,typ,value],('complete JSON position',sid,pointer));k+=1
 if isinstance(v,dict):
  for i,(key,x) in enumerate(v.items(),1):walk(sid,x,pointer+'/'+key.replace('~','~0').replace('/','~1'),i)
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(sid,x,pointer+'/'+str(i),i+1)
ids=list(dict.fromkeys(v[0] for v in pos))
for sid in ids:walk(sid,parsed[sid])
ck(k==len(pos)==833897)
orders=load(B/'all-source-orders.json.gz');ck(len(orders)==27)
for label,v in orders.items():
 a=v['full_order'];ck(a==sorted(a,key=lambda r:(-r['votes'],r['key'])) and len({r['key'] for r in a})==len(a));total=sum(r['votes'] for r in a);cum=0;cut=None
 for i,r in enumerate(a,1):
  cum+=r['votes'];ck(r['rank']==i and r['cumulative_votes']==cum)
  if cut is None and 5*cum>=4*total:cut=(i,cum-r['votes'],cum)
 ck(total==v['total'] and cut==(v['minimum80_count'],v['previous'],v['crossing']) and v['threshold']==(4*total+4)//5)
for rel,h in before.items():ck(sha((ROOT/rel).read_bytes())==h,'all baseline sealed bytes unchanged')
result={'status':'pass','checks':N,'baseline_manifest_sha256':sha((B/'asset-manifest.json').read_bytes()),'counts':dict(stats),'complete_physical_workbook_rows':position,'complete_original_JSON_position_nodes':k,'source_JSON_contexts':len(ids),'source_contests':summary,'full_source_orders':len(orders),'native_primary':{'denominator':2006975,'native_units':3933,'minimum80':1516,'preceding1515':1605350,'crossing':1605649,'top15':689455,'crossing_geography':'Bienville ward06/precinct03 +299'},'manual_browser_or_image_claim':False,'current_native_geometry_or_ID_approval':False,'scope':'Independent whole receipt/body hash, ZIP/member/physical OOXML-cell/CSV/API/native positional and full JSON-source witness replay without producer imports/writers. General/race voter controls and current legal/geometry/ballot/remaining scopes stay qualified. Raw complete original lexical bytes retained; no source normalization, native allocation or forecast.','all_baseline_owned_bytes_unchanged':True}
out=S/'data/coordinator-first-pair-original-review.json';body=(json.dumps(result,indent=2)+'\n').encode()
if '--check' in sys.argv:ck(out.read_bytes()==body)
else:out.write_bytes(body)
print(json.dumps(result))
