from pathlib import Path
import json,gzip,re,csv
ROOT=Path(__file__).resolve().parents[3];B=ROOT/'data/baselines'
def main():
 pins=json.loads((B/'source/pins.json').read_text())['pins'];rows=[];checks=[];reg=[]
 for p in pins:
  role=p['role'] or '';url=p['url'] or '';h=p['raw_sha256']
  if 'Turnout by County' not in role and 'general registration sensitivity: By County'!=role:continue
  pages=gzip.decompress((B/'extracted'/f'{h}.layout.txt.gz').read_bytes()).decode().split('\f')[:-1];local=[];footer=None
  turnout='Turnout by County' in role
  for page,body in enumerate(pages,1):
   for ln,line in enumerate(body.splitlines(),1):
    m=re.match(r'^\s*(\d{3})\s+([A-Z]+)\s+(.*)$',line)
    fm=re.match(r'^\s*(?:Totals|Statewide totals)\s+(.*)$',line)
    if not m and not fm:continue
    values=re.findall(r'\d[\d,]*(?:\.\d+)?\s*%?',m[3] if m else fm[1]);nums=[v.strip().replace(' ','') for v in values]
    if turnout:
     assert len(nums)==12,(url,page,ln,nums)
     vals={k:int(nums[i].replace(',','')) for i,k in [(0,'total_registration'),(1,'number_voting'),(3,'D_registration'),(4,'D_number_voting'),(6,'R_registration'),(7,'R_number_voting'),(9,'other_registration'),(10,'other_number_voting')]}
     if fm:footer=vals;continue
     year=int(re.search(r'(2020|2022|2024)',body)[0]);r=dict(year=year,county_code=m[1],county_literal=m[2],source_sha256=h,page=page,line=ln,raw=line,**vals,total_turnout_percent_raw=nums[2],D_turnout_percent_raw=nums[5],R_turnout_percent_raw=nums[8],other_turnout_percent_raw=nums[11],definition='SBE Number voting; unofficial administrative turnout, not candidate choice or eligible remainder')
    else:
     assert len(nums)==13,(page,ln,nums)
     vals={k:int(nums[i]) for i,k in [(0,'precinct_count'),(1,'D_registration'),(2,'R_registration'),(3,'other_registration'),(4,'independent_registration'),(5,'libertarian_registration'),(6,'green_registration'),(7,'constitution_registration'),(8,'reform_registration'),(9,'socialist_workers_registration'),(12,'total_registration')]}
     if fm:footer=vals;continue
     r=dict(county_code=m[1],county_literal=m[2],source_sha256=h,page=page,line=ln,raw=line,**vals,printed_date='September, 2024',url_filename_scope='November General 2024',definition='Registration statistics snapshot; printed September date retained; not2026 voter eligibility')
    local.append(r)
  assert len(local)==120 and len(set(r['county_code'] for r in local))==120,(url,len(local))
  assert footer is not None
  sums={k:sum(r[k] for r in local) for k in footer};assert sums==footer,(url,sums,footer)
  checks.append(dict(source_sha256=h,url=url,counties=len(local),printed_footer=footer,independent_county_sums=sums,source_headers=pages[0].splitlines()[:6]))
  (rows if turnout else reg).extend(local)
 for name,rr in [('county-admin-turnout',rows),('county-registration',reg)]:
  with (B/'extracted'/f'{name}.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rr[0]);w.writeheader();w.writerows(rr)
 (B/'extracted/admin-controls.json').write_text(json.dumps(checks,indent=2)+'\n')
 print('turnout county rows',len(rows),'registration county rows',len(reg))
if __name__=='__main__':main()
