"""Independent complete source bytes, certificate sections and positional fields."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,io,json,re,subprocess,sys
S=Path(__file__).resolve().parents[1];D=S/'data';T=D/'turnout';B=D/'baselines';N=0;stats=Counter()
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def lines(p):return [json.loads(v) for v in gzip.decompress(p.read_bytes()).splitlines()]
before={};seals={}
for name,base,extras,count in [('turnout',T,['turnout.md','data/county-turnout.csv'],2734),('baselines',B,['county-partisanship.md','data/county-baselines.csv'],1971)]:
 mf=load(base/'asset-manifest.json');rows=mf['files'];actual={str(p.relative_to(S)) for p in base.rglob('*') if p.is_file() and p!=base/'asset-manifest.json'}|set(extras)
 ck(len(rows)==count and len({r['path'] for r in rows})==count and {r['path'] for r in rows}==actual)
 for row in rows:
  p=S/row['path'];b=p.read_bytes();ck(not p.is_symlink() and len(b)==row['bytes']<40000000 and sha(b)==row['sha256']);before[row['path']]=sha(b)
 seals[name]=sha((base/'asset-manifest.json').read_bytes())
entities=load(T/'source/entities.json');bpins=load(B/'source/pins.json')['pins'];raw={};stored_roles=Counter()
for role,row in [('turnout',v) for v in entities]+[('baselines',v) for v in bpins]:
 path=(T/row['path']) if role=='turnout' and row['path'].startswith('source/') else S/row['path'];b=path.read_bytes();ck(len(b)==row['stored_bytes']<40000000 and sha(b)==row['stored_sha256']);data=gzip.decompress(b);ck(len(data)==row['raw_bytes'] and sha(data)==row['raw_sha256'])
 if row['raw_sha256'] in raw:ck(raw[row['raw_sha256']]==data)
 raw[row['raw_sha256']]=data;stored_roles[role]+=1
 if role=='baselines':ck(sha((S/row['receipt']).read_bytes())==row['receipt_sha256'])
 else:
  for rel in row['receipts']:ck((T/rel).is_file())
texts={};warnings=[];pdfpages=0
for p in sorted((T/'extracts').glob('*.layout.txt')):
 h=p.name.split('.')[0];ck(h in raw and raw[h].startswith(b'%PDF'));run=subprocess.run(['pdftotext','-layout','-','-'],input=raw[h],capture_output=True,check=True)
 ck(run.stdout==p.read_bytes(),'entire independent original PDF extraction');texts[h]=run.stdout.decode().split('\f');pdfpages+=run.stdout.count(b'\f');stats['complete_original_PDF_text_replays']+=1
 peer=B/'extracted'/f'{h}.layout.txt.gz'
 if peer.exists():ck(gzip.decompress(peer.read_bytes())==run.stdout);stats['shared_complete_PDF_texts']+=1
 if run.stderr:warnings.append({'raw_sha256':h,'tool':'pdftotext -layout','exit':run.returncode,'complete_stderr':run.stderr.decode(errors='replace')})
ck(stats['complete_original_PDF_text_replays']==134 and stats['shared_complete_PDF_texts']==133)
certificate_sources=[(2024,'2024-president','69f32f69255f65c9e9ed7b05a1a60a7c17f6bcc8444548a1a34e6f936b42c6b1',17,'President'),(2022,'2022-senate','46b46cbad74d2c6a7cc03a30a85bac02e2e8d0c60ed02cd4b9e9f66ccedd64e5',4,'United States Senator'),(2020,'2020-senate','66bb0eedd13f43b09b2e42f9b6119bf292e6361b0657fc4e2ab56907c3511773',8,'United States Senator')]
own={};own_positions={};footers={};section_controls=[]
for year,contest,h,width,title in certificate_sources:
 pages=texts[h];covers=[i for i,p in enumerate(pages) if 'For the office of' in p];starts=[i for i in covers if title in ' '.join(pages[i].split('For the office of',1)[1].split())];ck(len(starts)==1)
 start=starts[0];end=min([i for i in covers if i>start]+[len(pages)]);pattern=re.compile(r'^\s*([A-Za-z][A-Za-z .\'-]*?)\s+('+r'\d[\d,]*(?:\s+\d[\d,]*){'+str(width-1)+r'})\s*$');rows=[]
 for pg in range(start,end):
  for ln,text in enumerate(pages[pg].splitlines(),1):
   match=pattern.fullmatch(text)
   if not match:continue
   label=match[1].strip();tokens=list(re.finditer(r'\d[\d,]*',text[match.start(2):]));values=[int(m.group().replace(',','')) for m in tokens];ck(len(values)==width)
   if label=='Total Votes':ck(year not in footers);footers[year]=values
   else:ck((year,label) not in own);own[(year,label)]=values;rows.append(label)
   for col,(tok,value) in enumerate(zip(tokens,values),1):own_positions[(year,label,col)]={'page':pg+1,'line':ln,'character_start':match.start(2)+tok.start(),'raw_token':tok.group(),'raw_line':text,'value':value,'source_sha256':h}
 ck(len(rows)==len(set(rows))==120 and len(footers[year])==width)
 ck([sum(own[(year,label)][i] for label in rows) for i in range(width)]==footers[year]);section_controls.append({'year':year,'contest':contest,'source_raw_sha256':h,'whole_source_bytes':len(raw[h]),'cover_page':start+1,'section_end_exclusive_page':end+1,'counties':120,'candidate_columns':width,'complete_candidate_footer':footers[year],'state_reported_candidate_total':sum(footers[year])})
tf=load(T/'extracts/certificate-fields.json')+load(T/'extracts/certificate-controls.json');bf=list(csv.DictReader(io.StringIO((B/'extracted/certificate-fields.csv').read_text())))
for v in tf:
 year=int(v['contest'][:4]);label=v['county'] if v['scope']=='county' else 'Total Votes';r=own_positions[(year,label,v['candidate_column'])]
 ck(all(v[k]==r[k] for k in ['page','line','character_start','raw_token','raw_line','value','source_sha256']));ck(v['registration'] is None and v['ballots'] is None and v['blank'] is None and v['undervotes'] is None and v['overvotes'] is None);stats['whole_turnout_candidate_positions']+=1
for v in bf:
 r=own_positions[(int(v['year']),v['county_literal'] if v['scope']=='county' else 'Total Votes',int(v['column']))]
 ck(int(v['votes'])==r['value'] and int(v['page'])==r['page'] and int(v['line'])==r['line'] and int(v['char_start'])==r['character_start'] and all(v[k]==r[k] for k in ['source_sha256','raw_token','raw_line']));stats['whole_baseline_candidate_positions']+=1
ck(len(tf)==len(bf)==3509)
def literal_line(h,pg,ln):return texts[h][pg-1].splitlines()[ln-1]
for v in lines(T/'extracts/native-fields.jsonl.gz'):
 text=literal_line(v['source_sha256'],v['page'],v['line']);ck(text==v['raw_line'])
 for tok in v['tokens']:ck(text[tok['start']:tok['end']]==tok['raw_token'] and int(tok['raw_token'].replace(',',''))==tok['value']);stats['turnout_native_numeric_positions']+=1
 stats['whole_turnout_native_rows']+=1
for v in lines(B/'extracted/native-observations.jsonl.gz'):
 text=literal_line(v['source_sha256'],v['page'],v['line']);ck(text==v['raw'])
 for tok in v['tokens']:ck(text[tok['start']:tok['end']]==tok['raw']);stats['baseline_native_raw_token_positions']+=1
 stats['whole_baseline_native_rows']+=1
for v in load(T/'extracts/statistics-fields.json'):
 ck(literal_line(v['source_sha256'],v['page'],v['line'])==v['raw_line']);stats['whole_turnout_statistic_rows']+=1
for v in lines(B/'extracted/turnout-registration-positioned-controls.jsonl.gz'):
 text=literal_line(v['source_sha256'],v['page'],v['line']);ck(text==v['raw'])
 for tok in v['tokens']:ck(text[tok['start']:tok['end']]==tok['raw']);stats['baseline_statistic_raw_token_positions']+=1
 stats['whole_baseline_statistic_rows']+=1
tc=load(T/'priority-set.json');bc=load(B/'priority.json');ck(tc['dispatch_keys']==[] and tc['order'] is None and tc['top15'] is None and tc['min80'] is None and tc['priority'] is None and tc['remainder'] is None)
ck(bc['canonical_native_order'] is None and bc['canonical_native_top15_share'] is None and bc['canonical_native_minimum80'] is None and bc['dispatch_keys']==[])
rank=sorted([(label,sum(v)) for (year,label),v in own.items() if year==2024],key=lambda r:(-r[1],r[0]));total=sum(v for _,v in rank);cum=0;cut=None
for i,(name,votes) in enumerate(rank,1):
 before_sum=cum;cum+=votes
 if cut is None and 5*cum>=4*total:cut={'count':i,'votes':cum,'preceding_votes':before_sum,'crossing_county':name,'crossing_votes':votes}
ck(total==2074530 and sum(v for _,v in rank[:15])==1094747 and cut=={'count':50,'votes':1660226,'preceding_votes':1650178,'crossing_county':'Breckinridge','crossing_votes':10048})
ck(len(tc['coverage'])==120 and sum(len(v['available_native_constituents']) for v in tc['coverage'])==3221)
for path,digest in before.items():ck(sha((S/path).read_bytes())==digest,'all sealed owned bytes unchanged')
result={'status':'pass','checks':N,'sealed_worker_manifests':seals,'source_body_roles':dict(stored_roles),'unique_whole_original_entities':len(raw),'counts':dict(stats),'complete_automatically_extracted_PDF_pages':pdfpages,'independent_certificate_sections':section_controls,'county_only_sensitivity':{'denominator':total,'top15_votes':sum(v for _,v in rank[:15]),'minimum80':cut},'canonical_native_order':None,'canonical_native_dispatch':[],'coverage_parents':120,'source_native_constituents_in_inventory':3221,'scope':'Independently regex-parse original complete certificate office sections and every integer column before comparing producer fields; verify complete originals and all raw native/statistic positions. County rank is sensitivity only. Different candidate/native subset representations remain qualified, not normalized. Scanned/handwritten/generic/eligible/current scopes unresolved. No producer/peer helper import or writer, no network.','all_worker_owned_bytes_unchanged':True,'automatic_extraction_warnings_retained':len(warnings),'manual_visual_claim':False}
out=D/'coordinator-first-pair-original-review.json';warn=D/'coordinator-original-extraction-warnings.json.gz';wb=(json.dumps(warnings,ensure_ascii=False,indent=2)+'\n').encode()
if '--check' in sys.argv:ck(load(out)==result and gzip.decompress(warn.read_bytes())==wb)
else:out.write_text(json.dumps(result,indent=2)+'\n');warn.write_bytes(gzip.compress(wb,mtime=0))
print(json.dumps(result))
