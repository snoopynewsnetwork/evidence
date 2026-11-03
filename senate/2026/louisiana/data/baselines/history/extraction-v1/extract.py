"""Original-only extraction. Standard library; physical OOXML ordinals, raw CSV positions, JSON pointers."""
import csv,gzip,hashlib,io,json,posixpath,zipfile,xml.etree.ElementTree as E
from pathlib import Path
from collections import Counter,defaultdict
D=Path(__file__).resolve().parent; ROOT=D.parents[4]; S=D/'source'
h=lambda b:hashlib.sha256(b).hexdigest()
def dump(p,x):
 b=(json.dumps(x,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n').encode();p=D/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(b,mtime=0) if p.suffix=='.gz' else b)
def csvout(p,rows):
 with (D/p).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
receipts=json.loads((S/'receipts.json').read_text()); raw={}
for r in receipts:
 b=(ROOT/r['reference_path']).read_bytes(); v=gzip.decompress(b); assert h(b)==r['stored_sha256'] and h(v)==r['raw_sha256'] and len(v)==r['bytes'];raw[r['id']]=v
for p in sorted(S.glob('*.receipt.json')):
 r=json.loads(p.read_text());b=(S/r['asset']).read_bytes();v=gzip.decompress(b);assert h(b)==r['stored_sha256'] and h(v)==r['raw_sha256'] and len(v)==r['bytes'];raw[r['id']]=v;receipts.append(r)
# Complete raw JSON trees incl nulls, order and nonselected metadata stay in original bodies.
# Witness every node with child ordinal and pointer; duplicate fields survive as ordered pairs.
nodes=[]
def walk(x,src,path='',ordinal=0):
 typ='object' if isinstance(x,dict) else 'array' if isinstance(x,list) else type(x).__name__
 nodes.append([src,path,ordinal,typ,x if not isinstance(x,(list,dict)) else len(x)])
 if isinstance(x,dict):
  for i,(k,v) in enumerate(x.items(),1):walk(v,src,path+'/'+k.replace('~','~0').replace('/','~1'),i)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,src,path+'/'+str(i),i+1)
for k,v in raw.items():
 if v.lstrip().startswith((b'{',b'[')):
  x=json.loads(v);walk(x,k)
dump('source/json-position-witness.json.gz',nodes)
ns={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};rn='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
workbooks={};wbw=[]
for y in ('2024','2022','2020'):
 z=zipfile.ZipFile(io.BytesIO(raw[f'sos-{y}-full-results-xlsx'])); rel={x.attrib['Id']:x.attrib['Target'] for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
 sheets=[]
 for si,sh in enumerate(E.fromstring(z.read('xl/workbook.xml')).find('x:sheets',ns),1):
  target=rel[sh.attrib[rn]]; member=posixpath.normpath(posixpath.join('xl',target)) if not target.startswith('/') else target[1:];rr=[]
  for ri,row in enumerate(E.fromstring(z.read(member)).find('x:sheetData',ns),1):
   cells=[];vals=[]
   for ci,c in enumerate(row,1):
    text=c.find('x:v',ns); inline=c.find('x:is',ns)
    val=text.text if text is not None else ''.join(inline.itertext()) if inline is not None else None
    vals.append(val);cells.append({'physical_cell':ci,'attributes':c.attrib,'value':val,'xml':E.tostring(c,encoding='unicode')})
   rr.append(vals);wbw.append({'year':y,'sheet_ordinal':si,'sheet_name':sh.attrib['name'],'member':member,'physical_row':ri,'row_attributes':row.attrib,'cells':cells})
  sheets.append({'name':sh.attrib['name'],'member':member,'rows':rr})
 workbooks[y]=sheets
dump('source/workbook-position-witness.json.gz',wbw)
controls={};parish_rows=[];native_rows=[];candidate_rows=[];coverage=[];rankings={};contexts=[]
for y,race in [('2024','67190'),('2022','61897'),('2020','59569')]:
 tables={}
 for level,offset in [('parish',2),('precinct',4)]:
  rr=list(csv.reader(io.StringIO(raw[f'sos-{y}-selected-{level}-csv'].decode('utf-8-sig'))));head=rr[0];assert all(len(r)==len(head) for r in rr)
  tables[level]=(head,rr[1:]);dump(f'source/{y}-{level}-csv-positions.json.gz',{'header':head,'rows':[{'physical_row':i+2,'values':r} for i,r in enumerate(rr[1:])]})
 ph,pr=tables['parish'];nh,nr=tables['precinct'];assert ph[2:]==nh[4:];names=ph[2:];assert len(pr)==64;parishes=[r[1] for r in pr]
 md=json.loads(raw[f'sos-{y}-race-metadata'])['Races'];races=md['Race'];races=races if isinstance(races,list) else [races];meta=next(r for r in races if r['ID']==race);choices=meta['Choice'];assert len(choices)==len(names)
 # Three exact views: CSV native -> parish -> XLSX statewide and local source rows.
 state=[sum(int(r[2+j]) for r in pr) for j in range(len(names))];native_sum=[sum(int(r[4+j]) for r in nr) for j in range(len(names))];assert state==native_sum
 totals=[];matched=Counter()
 for sheet in workbooks[y][:2]:
  rows=sheet['rows']; ci=next(i for i,r in enumerate(rows) if r and r[0]==meta['SpecificTitle']); header=rows[ci+1];assert [n.replace('(OTHER)','(OTH)') for n in header[1:]]==names
  totalrow=rows[ci+2];assert totalrow[0]=='Total Votes';assert list(map(int,totalrow[1:]))==state
  selected=rows[ci+3:];selected=selected[:next((i for i,r in enumerate(selected) if not r or r[0] is None),len(selected))]
  if sheet['name']=='Multi-Parish(Parish)':
   assert [r[0] for r in selected]==parishes
   for a,b in zip(selected,pr):assert list(map(int,a[1:]))==list(map(int,b[2:]))
  else:
   # native rows begin parish heading, candidate heading, then ward/precinct rows; verified below by positional vector+label.
   expected=Counter((r[1],r[2]+' '+r[3],tuple(map(int,r[4:]))) for r in nr);seen=Counter();parent=None
   for row in rows[ci+3:]:
    if not row or row[0] is None:continue
    if row[0] in parishes and len(row)==1:parent=row[0];continue
    if parent and len(row)==len(names)+1 and row[0] not in ('Total Votes',) and all(v is not None and v.isdigit() for v in row[1:]):seen[(parent,row[0],tuple(map(int,row[1:])))]+=1
   # Retain exact coverage diagnostics; no invented rows or residual repair.
   totals.append({'sheet':sheet['name'],'expected':sum(expected.values()),'matched':sum((expected&seen).values()),'missing':list((expected-seen).items())[:8],'extra':list((seen-expected).items())[:8]})
 for j,(name,ch) in enumerate(zip(names,choices)):
  candidate_rows.append(dict(year=y,race_id=race,source_column=j+3,choice_id=ch['ID'],label=name,metadata_label=ch['Desc'],party=name.rsplit('(',1)[-1].rstrip(')'),votes=state[j],all_candidate_total=sum(state),share=state[j]/sum(state)))
 counts=Counter();method=defaultdict(lambda:[0]*len(names))
 bypar=json.loads(raw[f'{y}-VotesRaceByParish'])['Parishes']['Parish'];assert len(bypar)==64
 stats=json.loads(raw[f'stats{y}-Parish'])['Stats'];statestate=json.loads(raw['stats2024-state' if y=='2024' else f'stats{y}-Statewide'])['Stats'];assert len(stats['Parish'])==64
 for field in ('All','All_Voted','Dem','Rep','PartyOther','Dem_Voted','Rep_Voted','PartyOther_Voted'):
  assert sum(int(p[field]) for p in stats['Parish'])==int(statestate[field])
 for pi,p in enumerate(pr,1):
  pv=f'{pi:02}'; api=next(v for v in bypar if v['ParishValue']==pv);assert [int(c['VoteTotal']) for c in api['Choice']]==list(map(int,p[2:]));assert [c['ID'] for c in api['Choice']]==[c['ID'] for c in choices]
  st=next(v for v in stats['Parish'] if v['Option']==pv)
  parish_rows.append(dict(year=y,race_id=race,parish=p[1],parish_code=pv,all_candidate_votes=sum(map(int,p[2:])),candidate_votes=json.dumps(list(map(int,p[2:]))),qualified=int(api['VoterCountQualified']),voted=int(api['VoterCountVoted']),stats_qualified=int(st['All']),stats_voted=int(st['All_Voted']),precincts_expected=int(api['PrecinctsExpected']),precincts_reporting=int(api['PrecinctsReporting']),absentee_expected=int(api['NumAbsenteeExpected']),absentee_reporting=int(api['NumAbsenteeReporting']),blank_under_over=None))
  source=f'{y}-VotesRaceByPrecinct-{pv}';apirows=json.loads(raw[source])['Precincts']['Precinct'];apirows=apirows if isinstance(apirows,list) else [apirows]
  sr=json.loads(raw[f'{y}-StatsRaceParish-{pv}'])['Stats']['Precinct'];sr=sr if isinstance(sr,list) else [sr]
  # Never infer identity equivalence of statistics ordering. Keep both sets and differences.
  srmap={q['Precinct']:q for q in sr};sub=[(i+2,r) for i,r in enumerate(nr) if r[1]==p[1]];assert len(sub)==len(apirows)
  for (pos,r),a in zip(sub,apirows):
   key=json.dumps([y,pv,r[2],r[3]],separators=(',',':'));assert not counts[key];counts[key]+=1
   votes=list(map(int,r[4:]));assert votes==[int(c['VoteTotal']) for c in a['Choice']];assert [c['ID'] for c in a['Choice']]==[c['ID'] for c in choices]
   identity=(r[2]+'/'+r[3]) if r[3] else r[2];typ='early-aggregate' if r[2]=='Early Voting' else 'provisional-aggregate' if r[2]=='Provisional Votes' else 'ward-precinct';method[typ]=[x+v for x,v in zip(method[typ],votes)]
   native_rows.append(dict(year=y,race_id=race,parish=p[1],parish_code=pv,key=key,ward=r[2],precinct=r[3],source_native=a['Precinct'],csv_identity=identity,source_identity_equal=identity==a['Precinct'],type=typ,csv_row=pos,api_source=source,api_ordinal=apirows.index(a)+1,all_candidate_votes=sum(votes),candidate_votes=json.dumps(votes),qualified=a.get('VoterCountQualified'),voted=a.get('VoterCountVoted'),has_reported=a.get('HasReported'),stats_exact_label=srmap.get(a['Precinct']),blank_under_over=None))
  coverage.append(dict(year=y,parish=p[1],code=pv,csv_native=len(sub),result_native=len(apirows),statistics_native=len(sr),exact_native_label_overlap=len(set(a['Precinct'] for a in apirows)&set(srmap)),native_qualified_sum=sum(int(a['VoterCountQualified']) for a in apirows),native_voted_sum=sum(int(a['VoterCountVoted']) for a in apirows),statistics_qualified_sum=sum(int(a['All']) for a in sr),statistics_voted_sum=sum(int(a['All_Voted']) for a in sr),parish_qualified=int(api['VoterCountQualified']),parish_voted=int(api['VoterCountVoted'])))
 ranked=sorted([x for x in parish_rows if x['year']==y],key=lambda x:(-x['all_candidate_votes'],x['parish']));cum=0;out=[];cut=None
 for i,x in enumerate(ranked,1):
  cum+=x['all_candidate_votes'];hit=5*cum>=4*sum(state)
  if hit and cut is None:cut=i
  out.append(dict(rank=i,parish=x['parish'],code=x['parish_code'],votes=x['all_candidate_votes'],cumulative=cum,total=sum(state),minimum80=(cut is None or i==cut),share=x['all_candidate_votes']/sum(state)))
 rankings[y]={'order':out,'minimum80_count':cut,'threshold_ceiling':(4*sum(state)+4)//5,'top15_sum':sum(x['votes'] for x in out[:15]),'native_order':sorted([{'key':x['key'],'votes':x['all_candidate_votes']} for x in native_rows if x['year']==y],key=lambda x:(-x['votes'],x['key']))}
 controls[y]=dict(race_id=race,candidate_totals=state,all_candidate_votes=sum(state),candidate_count=len(names),parishes=64,native_count=len(nr),metadata=meta,metadata_clock=md['WriteTime'],workbook_native_reconciliation=totals,method_candidate_totals=dict(method),stats_state=statestate)
csvout('parish-controls.csv',parish_rows);csvout('candidates.csv',candidate_rows)
dump('native-results.json.gz',native_rows);dump('native-coverage.json',coverage);dump('controls.json',controls);dump('full-orders.json.gz',rankings)
# Witness complete extraction + scripts + full receipts before any peer access. This immutable seal is additive only.
paths=[p for p in D.rglob('*') if p.is_file() and 'original-freeze' not in str(p) and p.name not in ('pin_originals.py',)]
dump('original-freeze.json',{'scope':'Original-only historical fields; before any turnout derivatives, parsers, controls or reports opened','assets':[{'path':str(p.relative_to(D)),'sha256':h(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(paths)],'external_originals':receipts,'controls':controls,'full_order_sha256':h((D/'full-orders.json.gz').read_bytes())})
print(json.dumps({y:{k:v for k,v in c.items() if k in ('all_candidate_votes','candidate_count','native_count','workbook_native_reconciliation')} for y,c in controls.items()},indent=2))
