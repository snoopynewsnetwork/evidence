#!/usr/bin/env python3
import json,re,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=[]
for x in json.load(open(R/'extracts/portfolio.json')):
 if not x['role'].startswith('2024 county recap:'):continue
 county=x['role'].split(': ',1)[1];h=x['source_sha256'];p=(R/'extracts'/f'{h}.layout.txt').read_text().split('\f');fields=[]
 for page,text in enumerate(p,1):
  lines=text.splitlines()
  for i,l in enumerate(lines[:15]):
   if 'Ballots Cast' in l and not 'Ballots Cast -' in l:
    for k in range(i+1,min(i+4,len(lines))):
     m=re.search(r'(\d[\d,]*)\s*$',lines[k])
     if m:fields.append({'kind':'county_header_ballots','value':int(m[1].replace(',','')),'page':page,'label_line':i+1,'value_line':k+1,'raw_label_line':l,'raw_value_line':lines[k]});break
   if re.match(r'Run (Date|Time)',l):fields.append({'kind':'source_run_clock','page':page,'line':i+1,'raw_line':l,'timezone':None})
   if re.search(r'\d+ of \d+ = [\d.]+%',l):fields.append({'kind':'source_reporting_completeness_label','page':page,'line':i+1,'raw_line':l,'means_vote_completion':False})
 vals={f['value'] for f in fields if f['kind']=='county_header_ballots'}
 assert len(vals)<=1,(county,vals)
 out.append({'county':county,'source_sha256':h,'header_ballots_cast':next(iter(vals)) if vals else None,'header_ballots_status':'explicit repeated header, source scope only' if vals else 'not in captured header','fields':fields})
(R/'extracts/recap-report-controls.json').write_text(json.dumps(out,indent=2)+'\n')
