#!/usr/bin/env python3
"""Manual readings from inspected complete source-page renders, never peer/coordinator counts."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=json.load(open(R/'extracts/portfolio.json'));h=next(x['source_sha256'] for x in p if x['role']=='2024 county recap: Elliott')
# page, literal unit, registration, ballots, blank, six ballot-candidate columns in source order, pool, unassigned, printed contest total.
spec=[(1,'A101 Sandy Hook',753,386,0,[307,67,2,5,0,1],0,0,382),(4,'B101 Sandy Hook',608,397,0,[325,67,0,0,0,0],0,0,392),(7,'C101 Walnut Grove',800,453,0,[384,60,0,4,1,0],1,1,450),(9,'D101 Mocassin',972,555,0,[407,120,5,3,3,4],0,0,542),(11,'E101 Crackersneck',621,400,0,[309,74,1,5,0,1],2,2,392),(13,'F101 Bruin',609,389,0,[312,70,1,1,0,1],0,0,385),(15,'G101 Isonville',644,373,0,[291,74,0,5,0,1],0,0,371)]
labels=['REP Donald J. TRUMP/J.D. VANCE','DEM Kamala D. HARRIS/Tim WALZ','KEN Jill STEIN/Samson KPADENOU','IND Robert F. KENNEDY JR./Nicole SHANAHAN','IND Shiva AYYADURAI/Crystal ELLIS','LIB Chase OLIVER/Mike TER MAAT']
rows=[]
for page,unit,reg,ballots,blank,vs,pool,unassigned,total in spec:
 key=f'KY|2024|Elliott|{h[:12]}|{unit}'
 for label,value,kind,scope in [(label,v,'candidate','president') for label,v in zip(labels,vs)]+[('Write-In Totals',pool,'writein_pool','president'),('Not Assigned',unassigned,'writein_unassigned','president'),('Total Votes Cast',total,'cast_votes','president'),('Registered Voters - Total',reg,'registration','statistics'),('Ballots Cast - Total',ballots,'ballots','statistics'),('Ballots Cast - Blank',blank,'blank','statistics')]:
  rows.append({'county':'Elliott','source_sha256':h,'page':page,'line':None,'row_label':label,'native_label':unit,'unit_key':key,'scope':scope,'kind':kind,'label':label,'raw_line':None,'tokens':[{'value':value,'raw_token':str(value),'start':None,'end':None}],'method_header':['TOTAL'],'format':'summary','extraction':'manual visual transcription, complete original page render','page_image':f'proof/elliott-{page:02}.png','null_status':'explicit printed integer'})
 assert sum(vs)+pool==total
(R/'extracts/elliott-manual-fields.json').write_text(json.dumps(rows,indent=2)+'\n')
# All historical native columns retained, including unfilled template columns; numbers not safely read remain NULL.
historical=[]
for county,hsh,columns,pages in [('Estill','7a1ea38703cec3aea59740a8e8e33b77b70b7d97207427438283767cd15f2149', ['ABSENTEE Mail-In','ABSENTEE Walk-In','ABSENTEE Total']+[f'ESTILL COUNTY {n} Scan' for n in range(1,17)]+['GRAND TOTAL'],[1,2,3]),('Lyon','6b78a6d29739275ee907227703bdc99030e719ad69d63c767c4d765106eea6bb',['ABSENTEE Mail-In','ABSENTEE Walk-In (handwritten Early Vote)','ABSENTEE Total']+[f'LYON COUNTY {n} {method}' for n in range(1,9) for method in ['eSlate','eScan','Total']]+['GRAND TOTAL'],[1,2])]:
 historical.append({'county':county,'year':2020,'source_sha256':hsh,'pages':pages,'columns':columns,'column_relationship':'Total columns overlap constituent methods; no columns summed indiscriminately','handwriting_notes': 'Estill PDF2 sideways; separate write-in PDF3 is local offices. Scan1-3 marked early;4 BB&T;5-6 drive-through C/D;7 Annex;8 Extension office;9 High School;10-16 template labels retained.' if county=='Estill' else 'County1 A101-A102,2 B101-B102,3 C101-C102;4 handwritten Arthur Hutchcraft/Mail-in;5-8 template retained. No eSlate handwritten. Bottom handwritten Votes Cast4251, Reg Voters6691,63.6%.', 'numeric_transcription_status':'Original full page witnesses retained; uncertain handwriting cells remain unknown and are never used in statewide native order','ballots_source_label':'Votes Cast' if county=='Lyon' else None,'ballots':4251 if county=='Lyon' else None,'registration':6691 if county=='Lyon' else None,'blank':None,'undervotes':None,'overvotes':None,'current_geography_approved':False})
(R/'extracts/historical-handwritten-hierarchy.json').write_text(json.dumps(historical,indent=2)+'\n')
print('Manual Elliott rows',len(rows),'historical full originals/hierarchy',len(historical))
