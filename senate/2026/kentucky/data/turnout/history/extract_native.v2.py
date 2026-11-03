#!/usr/bin/env python3
"""Positioned original native presidential/statistical rows; retain source labels and method indexes."""
import json,re,gzip,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def value_tokens(s):
 return [{'raw_token':m[0],'value':int(m[0].replace(',','')),'start':m.start(),'end':m.end()} for m in re.finditer(r'(?<![\w.])\d[\d,]*(?![\w.%])',s)]
def parse_one(x):
 h=x['source_sha256'];t=(ROOT/'extracts'/f'{h}.layout.txt').read_text();county=x['role'].split(': ',1)[1];fields=[];pages=[];unknown=[]
 for pi,p in enumerate(t.split('\f'),1):
  if not p.strip():continue
  lines=p.splitlines();choice=any(re.match(r'^Choice\s+',l) for l in lines);unit=None;ballots=None
  for li,l in enumerate(lines):
   m=re.match(r'^(.+?)\s{3,}([\d,]+) ballots cast\s*$',l,re.I)
   if m: unit=re.split(r'\s{2,}',m[1].strip())[0];ballots={'value':int(m[2].replace(',','')),'line':li+1,'raw_line':l};break
  if unit is None:
   for li,l in enumerate(lines):
    m=re.match(r'^(.+?)\s{3,}([\d,]+) of ([\d,]+) registered voters',l)
    if m:unit=m[1].strip();ballots={'value':int(m[2].replace(',','')),'registered':int(m[3].replace(',','')),'line':li+1,'raw_line':l};break
   for li,l in enumerate(lines):
    if re.match(r'^Statistics\s+TOTAL',l.strip()):
     for previous in reversed(lines[:li]):
      if previous.strip():unit=previous.strip();break
     break
  # continuing ES&S pages keep unit immediately after county heading and before office title.
  if unit is None:
   for li,l in enumerate(lines[:15]):
    if re.match(r'^(?:[A-Z]\d{3}|ABSENTEE|PROVISIONAL|TOTAL|Absentee|EV |Early|Walk)',l.strip()):unit=l.strip();break
  if 'Cumulative Results Report' in p:unit='[COUNTY CUMULATIVE SUMMARY]'
  pres=[i for i,l in enumerate(lines) if re.search(r'PRESIDENT.*(?:VICE PRESIDENT|UNITED STATES)',l,re.I) and not re.search(r'^\s*(REP|DEM) ',l)]
  # Header witness retains complete source context and each page-native appearance even for unrelated offices.
  pages.append({'county':county,'source_sha256':h,'page':pi,'native_label':unit,'format':'choice' if choice else 'summary','header_lines':lines[:min(18,len(lines))],'president_title_lines':[lines[i] for i in pres],'unit_ballots':ballots})
  if not pres:continue
  if unit is None:unknown.append({'page':pi,'reason':'presidential page unit unresolved','header':lines[:20]})
  key=f'KY|2024|{county}|{h[:12]}|{unit}'
  # Statistics are stored independently from contest votes.
  for li,l in enumerate(lines[:pres[0]]):
   if re.match(r'^\s*(Registered Voters|Ballots Cast|Voter Turnout)\s*-',l):
    fields.append({'county':county,'source_sha256':h,'page':pi,'line':li+1,'native_label':unit,'unit_key':key,'scope':'statistics','raw_line':l,'label':re.split(r'\s{2,}',l.strip())[0],'tokens':value_tokens(l),'method_header':lines[max(0,li-7):li]})
  for start in pres:
   headers=[];block=[]
   for li in range(start+1,len(lines)):
    l=lines[li]
    if 'Report generated with' in l or re.search(r'(Precinct Summary|Run Date)',l):break
    if choice:
     if l.startswith('Choice'):headers.append(l);continue
     pairs=list(re.finditer(r'([\d,]+)\s+([\d.]+)%',l))
     if pairs:
      tokens=[{'raw_token':m[1],'value':int(m[1].replace(',','')),'start':m.start(1),'end':m.end(1),'source_percent':m[2]} for m in pairs]
      label=l[:pairs[0].start()].strip();kind='cast_votes' if label=='Cast Votes:' else 'candidate'
     elif re.match(r'^\s*(Undervotes|Overvotes):',l):
      tokens=value_tokens(l);label=l[:tokens[0]['start']].strip() if tokens else l.strip();kind='undervotes' if 'Undervotes' in label else 'overvotes'
     else:
      if l.strip():headers.append(l)
      continue
    else:
     m=re.match(r'^\s*(.+?)\s{2,}([\d,]+(?:\s+[\d,]+)*)\s*$',l)
     if not m:
      if l.strip():headers.append(l)
      continue
     label=m[1].strip();tokens=value_tokens(l[m.start(2):]);tokens=[{**z,'start':z['start']+m.start(2),'end':z['end']+m.start(2)} for z in tokens]
     if label=='TOTAL':headers.append(l);continue
     kind='cast_votes' if label=='Total Votes Cast' else 'contest_totals' if label=='Contest Totals' else 'writein_pool' if label=='Write-In Totals' else 'writein_unassigned' if label=='Not Assigned' else 'candidate'
    block.append({'county':county,'source_sha256':h,'page':pi,'line':li+1,'native_label':unit,'unit_key':key,'scope':'president','kind':kind,'label':label,'raw_line':l,'tokens':tokens,'method_header':headers.copy(),'format':'choice' if choice else 'summary'})
    if (choice and kind=='overvotes') or (not choice and kind in ('cast_votes','contest_totals')):break
   fields.extend(block)
 return fields,pages,unknown
if __name__=='__main__':
 portfolio=json.loads((ROOT/'extracts/portfolio.json').read_text());allfields=[];allpages=[];issues=[]
 for x in portfolio:
  if not x['role'].startswith('2024 county recap:'):continue
  a,b,c=parse_one(x);allfields.extend(a);allpages.extend(b);issues.append({'county':x['role'].split(': ',1)[1],'source_sha256':x['source_sha256'],'pages':x['pages'],'presidential_fields':len(a),'unresolved_pages':c,'image_only':x['text_bytes']<=x['pages']})
 for filename,rows in [('native-fields',allfields),('native-page-identities',allpages)]:
  data=''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows).encode();(ROOT/'extracts'/f'{filename}.jsonl.gz').write_bytes(gzip.compress(data,mtime=0))
 (ROOT/'extracts/native-parser-coverage.json').write_text(json.dumps(issues,indent=2)+'\n')
 print('fields',len(allfields),'pages',len(allpages),'county_sources',len(issues),'missing',[(x['county'],x['presidential_fields'],len(x['unresolved_pages'])) for x in issues if not x['presidential_fields'] or x['unresolved_pages']])
