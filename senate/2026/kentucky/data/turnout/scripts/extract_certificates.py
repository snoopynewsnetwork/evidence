#!/usr/bin/env python3
"""Independent original-body parser. No coordinator/peer vector inputs."""
import json,re,csv,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPECS=[('2024-president','69f32f69255f65c9e9ed7b05a1a60a7c17f6bcc8444548a1a34e6f936b42c6b1',2,7,[
 ('Donald J. TRUMP','J. D. VANCE','Republican Party'),('Kamala D. HARRIS','Tim WALZ','Democratic Party'),('Robert F. KENNEDY JR.','Nicole SHANAHAN','Independent'),('Jill STEIN','Samson KPADENOU','Kentucky Party'),('Chase OLIVER','Mike TER MAAT','Libertarian Party'),('Shiva AYYADURAI','Crystal ELLIS','Independent'),('Peter SONSKI','Lauren ONAK','Write-In'),('Claudia DE LA CRUZ','Karina GARCIA','Write-In'),('Cornel WEST','Melina ABDULLAH','Write-In'),('James D. SODERNA','Matthew J. TREWHELLA','Write-In'),('Jay J. BOWMAN','De BOWMAN','Write-In'),('Joseph KISHORE','Jerry WHITE','Write-In'),('John CHENG','Wayne WALIGORSKI','Write-In'),('Billy KELLEY JR.','Jason HOLDEMAN','Write-In'),('Cherunda FOX','Harlan McVAY JR.','Write-In'),('Andre Ramon McNEIL SR.','Roschelle McNEIL','Write-In'),('Future Madam POTUS','Jessica KENNEDY','Write-In')]),
 ('2022-senate','46b46cbad74d2c6a7cc03a30a85bac02e2e8d0c60ed02cd4b9e9f66ccedd64e5',2,6,[('Rand PAUL',None,'Republican Party'),('Charles BOOKER',None,'Democratic Party'),('Charles Lee THOMASON',None,'Write-In'),('Billy Ray WILSON',None,'Write-In')]),
 ('2020-senate','66bb0eedd13f43b09b2e42f9b6119bf292e6361b0657fc4e2ab56907c3511773',8,10,[('Mitch McCONNELL',None,'Republican Party'),('Amy McGRATH',None,'Democratic Party'),('Brad BARRON',None,'Libertarian Party'),('Paul John FRANGEDAKIS',None,'Write-In'),('Daniel COBBLE',None,'Write-In'),('Randall Lee TEEGARDEN',None,'Write-In'),('Harold H. FITZPATRICK',None,'Write-In'),('Demetra WYSINGER',None,'Write-In')])]
def extract():
 fields=[];headers=[];controls=[];county_sets=[]
 for contest,h,first,last,cands in SPECS:
  pages=(ROOT/'extracts'/f'{h}.layout.txt').read_text().split('\f');seen={};footer=None
  for pi in range(first-1,last):
   lines=pages[pi].splitlines();first_data=next(i for i,l in enumerate(lines) if re.match(r'^\s*[A-Za-z][A-Za-z .-]*?\s{2,}[\d,]+(?:\s+[\d,]+)*\s*$',l) and len(re.findall(r'[\d,]+',l))==len(cands))
   headers.append({'contest':contest,'source_sha256':h,'page':pi+1,'raw_lines':lines[:first_data],'candidates_display_transcription':[{'column':i+1,'candidate':c,'running_mate':v,'party_or_ballot_label':party,'transcription':'manual display from complete original header; literal positioned header retained'} for i,(c,v,party) in enumerate(cands)]})
   for li,line in enumerate(lines[first_data:],first_data+1):
    m=re.match(r'^\s*([A-Za-z][A-Za-z .-]*?)\s{2,}([\d,]+(?:\s+[\d,]+)*)\s*$',line)
    if not m:continue
    name=m[1].strip();tokens=list(re.finditer(r'[\d,]+',m[2]));assert len(tokens)==len(cands),(contest,pi+1,li,line)
    vals=[int(t[0].replace(',','')) for t in tokens]
    if name=='Total Votes':footer=vals
    else:assert name not in seen;seen[name]=vals
    for ci,((candidate,mate,party),token,value) in enumerate(zip(cands,tokens,vals),1):
     row={'contest':contest,'county':name if name!='Total Votes' else None,'scope':'county' if name!='Total Votes' else 'state_footer','source_sha256':h,'page':pi+1,'line':li,'character_start':m.start(2)+token.start(),'character_end':m.start(2)+token.end(),'raw_token':token[0],'raw_line':line,'candidate_column':ci,'candidate_key':f'{contest}:column:{ci}','candidate':candidate,'running_mate':mate,'party_or_ballot_label':party,'value':value,'null_status':'explicit_integer','method':None,'method_status':'not_separately_reported_in_certificate','ballots':None,'blank':None,'undervotes':None,'overvotes':None,'registration':None,'source_native_county_id':None}
     (controls if name=='Total Votes' else fields).append(row)
  assert len(seen)==120,(contest,len(seen));assert footer is not None
  sums=[sum(v[i] for v in seen.values()) for i in range(len(cands))];assert sums==footer,(contest,sums,footer)
  county_sets.append(set(seen));print(contest,len(seen),len(cands),sum(footer),footer)
 assert all(s==county_sets[0] for s in county_sets)
 return fields,headers,controls
if __name__=='__main__':
 a,b,c=extract()
 for name,rows in [('certificate-fields',a),('certificate-headers',b),('certificate-controls',c)]:
  (ROOT/'extracts'/f'{name}.json').write_text(json.dumps(rows,indent=2)+'\n')
