"""Source-scoped raw presidential/native/admin observations; no identity normalization."""
from pathlib import Path
import gzip,json,re,csv
ROOT=Path(__file__).resolve().parents[3]; B=ROOT/'data/baselines'
NUM=re.compile(r'(?<![\w.])\d[\d,]*(?:\.\d+)?%?(?!\w)')
def tokens(line):return [dict(raw=m[0],start=m.start(),end=m.end()) for m in NUM.finditer(line)]
def main():
 pins=json.loads((B/'source/pins.json').read_text())['pins']; inv=json.loads((B/'extracted/document-inventory.json').read_text()); byhash={x['raw_sha256']:x for x in inv}
 observations=[]; contexts=[]; coverage=[]; controls=[]
 for pin in pins:
  role=pin['role'];h=pin['raw_sha256'];f=B/'extracted'/f'{h}.layout.txt.gz'
  if not f.exists():continue
  native=role and role.startswith('2024 county recap: ')
  control=role and ('sensitivity:' in role or 'registration workbook' in role)
  if not native and not control:continue
  pages=gzip.decompress(f.read_bytes()).decode().split('\f')[:-1]
  if control:
   for p,body in enumerate(pages,1):
    for ln,line in enumerate(body.splitlines(),1):
     if line.strip():controls.append(dict(source_sha256=h,role=role,page=p,line=ln,raw=line,tokens=tokens(line)))
   continue
  county=role.split(': ',1)[1];units=set();candidate_count=0;pres_pages=[]; methods=[]
  for p,body in enumerate(pages,1):
   lines=body.splitlines();unit=None;unitline=None;incontest=False
   # Explicit printed page header only. No numeric/name-range inference.
   for ln,line in enumerate(lines,1):
    m=re.match(r'^(\S.*?)\s{3,}(?:[\d,]+ ballots cast|[\d,]+ of [\d,]+ registered voters = [\d.]+%)\s*$',line,re.I)
    if m:unit=m[1];unitline=ln;break
   if unit is None and 'Summary' in body[:100] or unit is None and 'Electionware' in body:
    for ln,line in enumerate(lines[:17],1):
     if ln>3 and line.strip() and not line.startswith(' ') and not any(t in line for t in ['County','November','Statistics','Registered','Ballots','Voter','TOTAL','Report','Election','OFFICIAL','Precinct']):
      unit=line;unitline=ln;break
   if 'Cumulative Results Report' in body[:100]:unit=None;unitline=None
   if unit is not None:units.add(unit)
   pagectx=dict(source_sha256=h,county=county,page=p,unit_literal=unit,unit_header_line=unitline,
     scope='county cumulative' if 'Cumulative Results Report' in body[:100] else ('source native label' if unit is not None else 'unresolved page context'),
     header_lines=lines[:max(unitline or 0,15)],method_headers=[])
   for ln,line in enumerate(lines,1):
    upper=line.upper()
    if 'PRESIDENT' in upper and 'VICE' in upper and 'UNITED STATES' in upper:incontest=True;pres_pages.append(p)
    elif incontest and (' - (Vote for' in line or re.search(r'^\s+(?:U\.S\.|UNITED STATES|STATE |COMMONWEALTH|CONSTITUTIONAL|CIRCUIT)',line)) and 'PRESIDENT' not in upper:incontest=False
    if ('Choice' in line and 'Party' in line) or ('TOTAL' in line and ('Election' in line or len(line.split())==1)):
     pagectx['method_headers'].append(dict(line=ln,raw=line));methods.append(line)
    admin=any(t in line for t in ['Ballots Cast','Registered Voters','Voter Turnout','Run Time','Run Date','Polling Places','Precinct Summary -','Report generated'])
    if incontest or admin:
     if not line.strip():continue
     kind='context'
     if 'Write-In Totals' in line:kind='overlapping write-in parent'
     elif 'Write-In:' in line:kind='named write-in child'
     elif 'Not Assigned' in line:kind='unassigned write-in child'
     elif re.match(r'^\s*(Cast Votes:|Total Votes Cast|Contest Totals|Undervotes:|Overvotes:)',line):kind='contest control'
     elif re.search(r'\b(REP|DEM|IND|LIB|KEN|KY)\b',line) and tokens(line):kind='candidate'
     elif incontest and '%' in line and tokens(line):kind='candidate or control continuation'
     if kind in ('candidate','candidate or control continuation','named write-in child'):candidate_count+=1
     observations.append(dict(source_sha256=h,county=county,page=p,line=ln,unit_literal=unit,unit_header_line=unitline,
       observation_key=f'{h}:p{p}:l{ln}',kind=kind,presidential_context=incontest,raw=line,tokens=tokens(line)))
   contexts.append(pagectx)
  coverage.append(dict(county=county,source_sha256=h,pages=len(pages),text_pages=byhash[h]['text_pages'],
    image_only_pages=byhash[h]['image_only_pages'],bbox_exit=byhash[h]['bbox_exit'],native_literal_labels=sorted(units),
    observed_label_count=len(units),president_pages=sorted(set(pres_pages)),candidate_line_observations=candidate_count,
    scope='county cumulative only' if county=='Scott' else 'source-native observations; closure not assumed',
    complete_native_universe=False,reason='Cumulative source' if county=='Scott' else ('Image-only source' if not candidate_count else 'Native labels/method observations retained; full-field additive closure requires source-scope verification'),
    method_headers=list(dict.fromkeys(methods))))
 for name,obj in [('native-observations',observations),('native-page-contexts',contexts),('turnout-registration-positioned-controls',controls)]:
  raw=''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in obj).encode();stored=gzip.compress(raw,mtime=0);assert len(stored)<40000000;(B/'extracted'/f'{name}.jsonl.gz').write_bytes(stored)
 (B/'extracted/native-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
 print('120 coverage entries required:',len(coverage),'observations',len(observations),'contexts',len(contexts),'controls',len(controls))
if __name__=='__main__':main()
