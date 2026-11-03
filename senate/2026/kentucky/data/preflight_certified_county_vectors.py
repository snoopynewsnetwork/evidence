"""Source-only county controls from retained complete Kentucky certifications.

No county result is a substitute for a native precinct scope. This preflight
does not approve a historical priority, current ballot or reporting crosswalk.
"""
from pathlib import Path
import csv,gzip,hashlib,io,json,re,subprocess

DATA=Path(__file__).resolve().parent
ROOT=DATA.parent
SPECS=[
 dict(year=2024,stamp='20241223120817',office='President and Vice President of the United States',pages=[2,3,4,5,6,7],candidates=[
 ('Donald J. TRUMP','J. D. VANCE','Republican Party'),('Kamala D. HARRIS','Tim WALZ','Democratic Party'),('Robert F. KENNEDY JR.','Nicole SHANAHAN','Independent'),('Jill STEIN','Samson KPADENOU','Kentucky Party'),('Chase OLIVER','Mike TER MAAT','Libertarian Party'),('Shiva AYYADURAI','Crystal ELLIS','Independent'),('Peter SONSKI','Lauren ONAK','Write-In'),('Claudia DE LA CRUZ','Karina GARCIA','Write-In'),('Cornel WEST','Melina ABDULLAH','Write-In'),('James D. SODERNA','Matthew J. TREWHELLA','Write-In'),('Jay J. BOWMAN','De BOWMAN','Write-In'),('Joseph KISHORE','Jerry WHITE','Write-In'),('John CHENG','Wayne WALIGORSKI','Write-In'),('Billy KELLEY JR.','Jason HOLDEMAN','Write-In'),('Cherunda FOX','Harlan McVAY JR.','Write-In'),('Andre Ramon McNEIL SR.','Roschelle McNEIL','Write-In'),('Future Madam POTUS','Jessica KENNEDY','Write-In')]),
 dict(year=2022,stamp='20221223031129',office='United States Senator',pages=[2,3,4,5,6],candidates=[('Rand PAUL',None,'Republican Party'),('Charles BOOKER',None,'Democratic Party'),('Charles Lee THOMASON',None,'Write-In'),('Billy Ray WILSON',None,'Write-In')]),
 dict(year=2020,stamp='20201120170339',office='United States Senator',pages=[8,9,10],candidates=[('Mitch McCONNELL',None,'Republican Party'),('Amy McGRATH',None,'Democratic Party'),('Brad BARRON',None,'Libertarian Party'),('Paul John FRANGEDAKIS',None,'Write-In'),('Daniel COBBLE',None,'Write-In'),('Randall Lee TEEGARDEN',None,'Write-In'),('Harold H. FITZPATRICK',None,'Write-In'),('Demetra WYSINGER',None,'Write-In')])
]

def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(ROOT)),bytes=len(b),sha256=sha(b))

def main():
 manifest=json.loads((DATA/'news/manifest.json').read_bytes());source_findings=[];field_rows=[];county_sets=[]
 for spec in SPECS:
  year=spec['year'];entry=next(r for r in manifest if r['id']==f'sbe-{year}-archive-{spec["stamp"]}')
  original=DATA/'news'/entry['asset'];pdf=gzip.decompress(original.read_bytes());assert pdf.startswith(b'%PDF-')and sha(pdf)==entry['raw_sha256']
  result=subprocess.run(['pdftotext','-layout','-','-'],input=pdf,capture_output=True,check=True)
  textpath=DATA/f'news/sbe-{year}-archive-{spec["stamp"]}.txt';assert result.stdout==textpath.read_bytes()
  pages=result.stdout.decode().split('\f');rows=[];n=len(spec['candidates']);raw_headers=[]
  for page in spec['pages']:
   lines=pages[page-1].splitlines();first_row=None
   for lineno,line in enumerate(lines,1):
    m=re.fullmatch(r'\s*([A-Za-z][A-Za-z .-]*?)\s{2,}([\d,]+(?:\s+[\d,]+)+)\s*',line)
    if not m:continue
    tokens=m[2].split();assert len(tokens)==n,(year,page,lineno,m[1],len(tokens))
    for token in tokens:assert re.fullmatch(r'(?:0|[1-9]\d{0,2}(?:,\d{3})*|[1-9]\d*)',token)
    if first_row is None:first_row=lineno
    rows.append(dict(literal_row_label=m[1],actual_PDFpage=page,positioned_text_line=lineno,original_positioned_line=line,raw_numeric_tokens=tokens,candidate_values=[int(t.replace(',',''))for t in tokens],role='state_footer'if m[1]=='Total Votes'else'county_control'))
   assert first_row is not None
   raw_headers.append(dict(actual_PDFpage=page,full_raw_positioned_header_lines=lines[:first_row-1]))
  assert len(rows)==121 and rows[-1]['role']=='state_footer'
  counties=rows[:-1];assert len({r['literal_row_label']for r in counties})==120
  county_sets.append({r['literal_row_label']for r in counties})
  sums=[sum(r['candidate_values'][i]for r in counties)for i in range(n)];assert sums==rows[-1]['candidate_values']
  candidates=[dict(source_column=i+1,candidate_display_transcribed_from_original_header=c[0],running_mate_display_transcribed_from_original_header=c[1],party_or_writein_header_literal=c[2],header_transcription_basis='Complete original first table page visually inspected; raw positioned header lines retained separately without normalization.')for i,c in enumerate(spec['candidates'])]
  for row in rows:
   for i,(token,value)in enumerate(zip(row['raw_numeric_tokens'],row['candidate_values'])):
    field_rows.append(dict(election_year=year,office=spec['office'],source_raw_sha256=sha(pdf),actual_PDFpage=row['actual_PDFpage'],positioned_text_line=row['positioned_text_line'],literal_row_label=row['literal_row_label'],role=row['role'],source_candidate_column=i+1,candidate=candidates[i]['candidate_display_transcribed_from_original_header'],running_mate=candidates[i]['running_mate_display_transcribed_from_original_header'],party_or_writein_header_literal=candidates[i]['party_or_writein_header_literal'],raw_numeric_token=token,value=value))
  previews=[pin(DATA/f'qa/county-primary-originals/{year}-p{p}-complete-original.png')for p in [spec['pages'][0],spec['pages'][-1]]]
  source_findings.append(dict(election_year=year,office=spec['office'],source_observation_id=entry['id'],requested_URL=entry['url'],final_URL=entry['final_url'],original_stored_pin=pin(original),raw_original_bytes=len(pdf),raw_original_sha256=sha(pdf),positioned_text_pin=pin(textpath),actual_table_PDFpages=spec['pages'],source_header_metadata=candidates,raw_positioned_headers_by_page=raw_headers,county_rows=120,candidate_columns=n,county_candidate_positions=120*n,state_footer_positions=n,source_candidate_sums=sums,state_source_named_total=sum(sums),all_county_rows=rows,visually_inspected_complete_original_page_previews=previews,preview_parameters=dict(renderer='pdftoppm',maximum_dimension_pixels=2600,deskew_rotation_enhancement='none'),pdftotext_warnings=result.stderr.decode(errors='replace')))
 assert county_sets[0]==county_sets[1]==county_sets[2]
 flat=io.StringIO(newline='');writer=csv.DictWriter(flat,fieldnames=list(field_rows[0]));writer.writeheader();writer.writerows(field_rows)
 p=DATA/'coordinator-certified-county-fields.csv.gz';p.write_bytes(gzip.compress(flat.getvalue().encode(),mtime=0))
 out=dict(status='pass_bounded_original_certification_county_candidate_preparation',source_findings=source_findings,county_candidate_positions=sum(s['county_candidate_positions']for s in source_findings),state_footer_positions=sum(s['state_footer_positions']for s in source_findings),all120_literal_county_sets_equal=True,flat_source_fields=pin(p),raw_originals_duplicated=False,scope='Coordinator preparation only. Full selected candidate columns, paired presidential running mates, literal Write-In columns and all120 county controls are retained. Source column counts are17/4/8, not separate votes for the paired running mates. All numeric county fields are read from the original PDF text layer and close the corresponding printed state footer; six complete first/final table pages were rendered and visually inspected. This is not a manual reading of every county glyph, complete federal/certification/amendment chronology, physical precinct/method/ballot/registration evidence, named-writein native allocation, current identity/geometry or accepted80percent dispatch. No missing field is filled from residuals, names or other years. Future independent workers must extract the retained original bytes themselves.',actual_question_workers_launched=False,formal_priority_accepted=False,current_geography_approved=False,current_vote_feed_admitted=False)
 p=DATA/'coordinator-certified-county-preflight.json';p.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(dict(output=pin(p),county_candidate_positions=out['county_candidate_positions'],state_footer_positions=out['state_footer_positions'],totals={str(s['election_year']):s['state_source_named_total']for s in source_findings})))

if __name__=='__main__':main()
