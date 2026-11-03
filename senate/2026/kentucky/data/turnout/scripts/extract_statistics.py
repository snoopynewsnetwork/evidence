#!/usr/bin/env python3
"""Source-scoped turnout/registration parent/native/admin rows; no cross-year native join."""
import json,re,gzip,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows=[]
for x in json.load(open(R/'extracts/portfolio.json')):
 if not x['role'].startswith(('unofficial turnout sensitivity','general registration sensitivity')):continue
 h=x['source_sha256'];county=None;code=None
 for page,p in enumerate((R/'extracts'/f'{h}.layout.txt').read_text().split('\f'),1):
  for li,l in enumerate(p.splitlines(),1):
   if x['role']=='general registration sensitivity: By Precinct':
    ch=re.match(r'^\s*(\d{3})\s+([A-Z][A-Z ]+)\s*$',l)
    if ch:code=ch[1];county=ch[2].strip();continue
    rg=re.match(r'^(.+?)\s+((?:[\dA-Z]+-){3}[\dA-Z]+)\s+((?:\d[\d,]*\s+){11}\d[\d,]*)\s*$',l)
    if rg:
     vals=[int(v.replace(',','')) for v in rg[3].split()]
     rows.append({'source_sha256':h,'source_role':x['role'],'source_header':p.splitlines()[:6],'page':page,'line':li,'raw_line':l,'source_county_code':code,'county':county,'label':rg[1].strip(),'scope':'native_registration_or_participation','district_source_string':rg[2],'source_columns':vals,'registered':vals[-1],'number_voting':None,'ballots_cast':None,'candidate_votes':None,'registration_status':'source Total Registered; active/inactive unknown','join_to_recap_native':False});continue
    rg=re.match(r'^\s*(.+?Totals.+?)\s{2,}((?:\d[\d,]*\s+){11}\d[\d,]*)\s*$',l)
    if rg:
     vals=[int(v.replace(',','')) for v in rg[2].split()]
     rows.append({'source_sha256':h,'source_role':x['role'],'source_header':p.splitlines()[:6],'page':page,'line':li,'raw_line':l,'source_county_code':code,'county':county,'label':rg[1].strip(),'scope':'administrative_summary','source_columns':vals,'registered':vals[-1],'number_voting':None,'ballots_cast':None,'candidate_votes':None,'join_to_recap_native':False});continue
   m=re.match(r'^\s*(\d{3})\s+([A-Z][A-Z ]+?)\s{2,}([\d,].*)$',l)
   if m:code=m[1];county=m[2].strip();label=county;scope='county';start=m.start(3)
   else:
    m=re.match(r'^\s*(Statewide totals|Totals|District [A-Z]|[A-Z]\d{3}[A-Z]?(?:\s+[^\d]+)?)\s{2,}([\d,].*)$',l)
    if not m:continue
    label=m[1].strip();scope='state_footer' if label in ['Statewide totals','Totals'] else 'administrative_summary' if label.startswith('District ') else 'native_registration_or_participation';start=m.start(2)
   tail=l[start:];clean=re.sub(r'[\d.]+\s*%','',tail)
   vals=[int(v.replace(',','')) for v in re.findall(r'\d[\d,]*',clean)]
   rows.append({'source_sha256':h,'source_role':x['role'],'source_header':p.splitlines()[:6],'page':page,'line':li,'raw_line':l,'source_county_code':code if scope!='state_footer' else None,'county':county if scope!='state_footer' else None,'label':label,'scope':scope,'source_columns':vals,'percentages':re.findall(r'[\d.]+\s*%',tail),'registered':vals[-1] if x['role'].startswith('general registration') else vals[0],'number_voting':None if x['role'].startswith('general registration') else vals[1],'registration_status':'source Total Reg.; active/inactive subdivision unknown','ballots_cast':None,'candidate_votes':None,'join_to_recap_native':False})
(R/'extracts/statistics-fields.json').write_text(json.dumps(rows,indent=2)+'\n')
# Census historical county identifiers, no geometry or later legal-eligibility inference.
from html.parser import HTMLParser
class Table(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.row=[];self.cell=None
 def handle_starttag(self,t,a):
  if t=='tr':self.row=[]
  if t in ['td','th']:self.cell=''
 def handle_data(self,d):
  if self.cell is not None:self.cell+=d
 def handle_endtag(self,t):
  if t in ['td','th'] and self.cell is not None:self.row.append(self.cell.strip());self.cell=None
  if t=='tr' and self.row:self.rows.append(self.row);self.row=[]
for f in (R/'source/receipts').glob('*.json'):
 x=json.load(open(f))
 if x.get('role')=='2024 Census county FIPS identity only':
  hop=x['hops'][-1];z=Table();z.feed(gzip.decompress((R/hop['body']).read_bytes()).decode());out=[]
  for i,row in enumerate(z.rows):
   if len(row)>8 and re.fullmatch(r'21\d{3}',row[2]):out.append({'fips':row[2],'county':row[6],'source_row':i+1,'raw_cells':row,'source_sha256':hop['raw_sha256']})
  assert len(out)==120,len(out);(R/'extracts/county-fips.json').write_text(json.dumps(out,indent=2)+'\n')
print('statistics',len(rows),'county rows',sum(x['scope']=='county' for x in rows))
