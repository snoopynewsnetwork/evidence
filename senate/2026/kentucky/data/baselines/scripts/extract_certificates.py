"""Independent source-position parser of complete SBE original certificates."""
from pathlib import Path
import json,gzip,re,csv
ROOT=Path(__file__).resolve().parents[3]; B=ROOT/'data/baselines'
SPECS={2024:('20241223120817',range(2,8),[
 ('Donald J. TRUMP','J. D. VANCE','Republican Party'),('Kamala D. HARRIS','Tim WALZ','Democratic Party'),
 ('Robert F. KENNEDY JR.','Nicole SHANAHAN','Independent'),('Jill STEIN','Samson KPADENOU','Kentucky Party'),
 ('Chase OLIVER','Mike TER MAAT','Libertarian Party'),('Shiva AYYADURAI','Crystal ELLIS','Independent'),
 ('Peter SONSKI','Lauren ONAK','Write-In'),('Claudia DE LA CRUZ','Karina GARCIA','Write-In'),
 ('Cornel WEST','Melina ABDULLAH','Write-In'),('James D. SODERNA','Matthew J. TREWHELLA','Write-In'),
 ('Jay J. BOWMAN','De BOWMAN','Write-In'),('Joseph KISHORE','Jerry WHITE','Write-In'),
 ('John CHENG','Wayne WALIGORSKI','Write-In'),('Billy KELLEY JR.','Jason HOLDEMAN','Write-In'),
 ('Cherunda FOX','Harlan McVAY JR.','Write-In'),('Andre Ramon McNEIL SR.','Roschelle McNEIL','Write-In'),
 ('Future Madam POTUS','Jessica KENNEDY','Write-In')]),
 2022:('20221223031129',range(2,7),[(n,None,p) for n,p in [('Rand PAUL','Republican Party'),('Charles BOOKER','Democratic Party'),('Charles Lee THOMASON','Write-In'),('Billy Ray WILSON','Write-In')]]),
 2020:('20201120170339',range(8,11),[(n,None,p) for n,p in [('Mitch McCONNELL','Republican Party'),('Amy McGRATH','Democratic Party'),('Brad BARRON','Libertarian Party'),('Paul John FRANGEDAKIS','Write-In'),('Daniel COBBLE','Write-In'),('Randall Lee TEEGARDEN','Write-In'),('Harold H. FITZPATRICK','Write-In'),('Demetra WYSINGER','Write-In')]])}
def main():
 pins=json.loads((B/'source/pins.json').read_text())['pins']; rows=[]; headers=[]; candidates=[]; checks=[]
 for year,(stamp,pages,cs) in SPECS.items():
  pin=next(p for p in pins if p['role']==f'sbe-{year}-archive-{stamp}'); h=pin['raw_sha256']
  text=gzip.decompress((B/'extracted'/f'{year}-full-layout.txt.gz').read_bytes()).decode().split('\f')
  for i,(name,mate,party) in enumerate(cs):candidates.append(dict(year=year,column=i+1,key=f'{h}:column:{i+1}',name=name,running_mate=mate,party=party,display='Manual header transcription; exact raw spacing/case retained separately',source_sha256=h))
  countyrows=[]; foot=None
  for page in pages:
   lines=text[page-1].splitlines(); first=None
   for ln,line in enumerate(lines,1):
    m=re.match(r'^\s*(Total Votes|[A-Za-z]+)\s+([\d,]+(?:\s+[\d,]+)*)\s*$',line)
    if not m:continue
    toks=list(re.finditer(r'[\d,]+',line[m.start(2):])); assert len(toks)==len(cs),(year,page,ln,line)
    if first is None:first=ln
    vals=[]
    for col,t in enumerate(toks,1):
     val=int(t[0].replace(',','')); vals.append(val)
     rows.append(dict(year=year,county_literal=m[1],scope='state-footer' if m[1]=='Total Votes' else 'county',page=page,line=ln,column=col,char_start=m.start(2)+t.start(),raw_token=t[0],votes=val,candidate_key=f'{h}:column:{col}',source_sha256=h,raw_line=line))
    if m[1]=='Total Votes':assert foot is None;foot=vals
    else:countyrows.append((m[1],vals))
   headers.append(dict(year=year,page=page,source_sha256=h,raw_header_lines=lines[:first-1]))
  assert len(countyrows)==120 and len(set(x[0] for x in countyrows))==120
  sums=[sum(x[1][c] for x in countyrows) for c in range(len(cs))];assert sums==foot,(year,sums,foot)
  checks.append(dict(year=year,counties=120,columns=len(cs),candidate_sums=sums,printed_footer=foot,all_candidate_total=sum(sums),ballots_cast=None,registration=None,under=None,over=None,method='Not printed in certificate contest tables',source_sha256=h))
 with (B/'extracted/certificate-fields.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 for name,obj in [('certificate-headers',headers),('candidates',candidates),('certificate-controls',checks)]: (B/'extracted'/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
 print(checks)
if __name__=='__main__': main()
