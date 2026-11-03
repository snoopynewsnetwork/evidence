"""Verify two complete archived originals without promoting blank scans to data."""
from pathlib import Path
import gzip,hashlib,json,re,struct,subprocess
DATA=Path(__file__).resolve().parent
ROOT=DATA.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(ROOT)),bytes=len(b),sha256=sha(b))
def main():
 rows={r['id']:r for r in json.loads((DATA/'news/manifest.json').read_bytes())};findings=[]
 for tag,stamp,npages,expected in [('estill','20210116034430',3,'7a1ea38703cec3aea59740a8e8e33b77b70b7d97207427438283767cd15f2149'),('lyon','20210116042754',2,'6b78a6d29739275ee907227703bdc99030e719ad69d63c767c4d765106eea6bb')]:
  row=rows[f'sbe-2020-{tag}-recap-archive-{stamp}'];p=DATA/'news'/row['asset'];z=p.read_bytes();raw=gzip.decompress(z);assert row['status']==200 and sha(raw)==row['raw_sha256']==expected and sha(z)==row['stored_sha256']and len(raw)==row['bytes']and raw.startswith(b'%PDF-')
  info=subprocess.run(['pdfinfo','-rawdates','-'],input=raw,capture_output=True,check=True);text=subprocess.run(['pdftotext','-layout','-','-'],input=raw,capture_output=True,check=True)
  metadata={}
  for line in info.stdout.decode().splitlines():
   if ':'in line:
    key,value=line.split(':',1)
    if key in ['Creator','Producer','CreationDate','ModDate','Pages','Page size','Page rot','PDF version']:metadata[key]=value.strip()
  assert int(metadata['Pages'])==npages and not text.stdout.strip(b'\f \r\n\t')
  tp=DATA/f'qa/county-recap-archives/{tag}-2020-complete-positioned-text.txt';assert text.stdout==tp.read_bytes()
  previews=[]
  for n in range(1,npages+1):
   rp=DATA/f'qa/county-recap-archives/{tag}-2020-complete-original-{n}.png';b=rp.read_bytes();assert b.startswith(b'\x89PNG\r\n\x1a\n');size=struct.unpack('>II',b[16:24]);assert max(size)==3000;previews.append(dict(actual_PDFpage=n,preview=pin(rp),pixel_dimensions=list(size)))
  findings.append(dict(county=tag,observed_official_original_URL=rows[f'sbe-2020-{tag}-native-original']['url'],archive_catalog_URL=rows[f'sbe-2020-{tag}-observed-recap-cdx']['url'],archive_observation_id=row['id'],requested_archive_URL=row['url'],final_URL=row['final_url'],retrieved_at_UTC=row['retrieved_at_utc'],stored_original=pin(p),raw_original_bytes=len(raw),raw_original_sha256=sha(raw),source_PDF_metadata=metadata,complete_positioned_text=pin(tp),original_text_layer_words=0,complete_pages_rendered_and_visually_inspected=previews,render_parameters=dict(renderer='pdftoppm',maximum_dimension_pixels=3000,deskew_rotation_enhancement='none'),observed_original_presentation='Handwritten county recapitulation tables with separately printed Mail-In/Walk-In/Total and local scan/eSlate/eScan columns; overlapping summaries, blank cells and unused template columns need independent field review. Estill PDF2 is sideways in the source, retained unchanged; its third actualPDFpage is a separate write-in sheet.'if tag=='estill'else'Handwritten county recapitulation tables with Mail-In/Walk-In and eSlate/eScan blocks, source totals and separate handwritten annotations. Numeric zeroes and blank cells are visibly distinct; do not equate blanks to zero or source blocks to current method IDs.',poppler_warnings=dict(pdfinfo=info.stderr.decode(errors='replace'),pdftotext=text.stderr.decode(errors='replace'))))
 out=dict(status='pass_two_actual_archived_county_originals_acquisition_and_visual_structure_only',source_findings=findings,new_actual_PDF_originals=2,complete_original_pages=5,source_native_candidate_vectors_transcribed=False,qualification='ExactCDX-exposed archived official URLs repair two previously live403 original lanes. All five actual original pages are complete, rendered and visually inspected; both PDF text layers are empty, so there is no machine numeric acceptance from text extraction. County/method/native columns overlap and handwritten reading still requires independent original transcription/control reconciliation. Source file/creation/archive/retrieval clocks are separate, no amendment chronology,120county native completeness, exact80/current geography/November approval or current count feed is established.',formal_priority_accepted=False,current_geography_approved=False)
 p=DATA/'coordinator-county-recap-archive-preflight.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(output=pin(p),complete_original_pages=5,new_PDF_originals=2)))
if __name__=='__main__':main()
