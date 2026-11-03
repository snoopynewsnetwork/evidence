from pathlib import Path
import collections,gzip,hashlib,json,subprocess,datetime,re
r=Path('/Users/tqbf/codebase/snn/senate/2026/kentucky');n=r/'data/news';p=n/'manifest.json';a=json.loads(p.read_text());canon={};records=[]
for x in a:
 if not re.fullmatch(r'sbe-(2020|2022|2024)-archive-\d{14}',x['id']):continue
 b=gzip.decompress((n/x['asset']).read_bytes());assert b.startswith(b'%PDF-') and hashlib.sha256(b).hexdigest()==x['raw_sha256']
 key=x['raw_sha256'];old=x['asset']
 if key in canon:
  target=canon[key];assert (n/old).read_bytes()==(n/target).read_bytes()
  x['asset']=target;x['storage_note']='Identical original/stored hashes across distinct archived observations; body retained once. CDX digest differences are not treated as returned-byte differences.'
  if old!=target:(n/old).unlink()
 else:canon[key]=old
 info=subprocess.run(['pdfinfo','-'],input=b,capture_output=True,check=True).stdout.decode();text=subprocess.run(['pdftotext','-layout','-','-'],input=b,capture_output=True,check=True).stdout
 pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1));textpath=n/(Path(canon[key]).name.removesuffix('.html.gz')+'.txt');textpath.write_bytes(text)
 oldtext=n/(x['id']+'.txt')
 if oldtext!=textpath and oldtext.exists():assert oldtext.read_bytes()==text;oldtext.unlink()
 records.append({'id':x['id'],'requested_url':x['url'],'final_url':x['final_url'],'original_bytes':len(b),'original_sha256':key,'stored_path':'data/news/'+x['asset'],'pages':pages,'text_path':str(textpath.relative_to(r)),'text_sha256':hashlib.sha256(text).hexdigest(),'source_pdf_metadata':{k:v for k,v in [line.split(':',1)for line in info.splitlines()if line.startswith(('CreationDate:','ModDate:','Pages:'))]}})
p.write_text(json.dumps(a,indent=2)+'\n')
out={'status':'pass_primary_archived_original_acquisition_only','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Coordinator preparation, no question agents or accepted priority. Direct official sources403; exact CDX-listed archive original bytes recovered. Native county recap originals still unrecovered.','PDF_observations':records,'unique_original_bodies':len(canon),'qualifications':['Distinct CDX digests nevertheless returned byte-identical originals for each year in these observations; every requested/final URL remains separate. No archive chronology/correction cause inferred.','2024 primary parent labels amendedDecember9; internal PDF metadata dates alone do not prove amendment timing.','Jefferson2020 nominalPDF200 redirected to current generic Voting HTML; not acquired as original resultPDF.','Complete candidate identities/counties/native/method and120-county exact80 need independent question-worker extraction; no provisional priority accepted.']}
(r/'data/coordinator-archive-preflight.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'PDF_observations':len(records),'unique_original_bodies':len(canon),'page_counts_by_year':{str(y):next(z['pages']for z in records if z['id'].startswith('sbe-'+str(y)))for y in [2024,2022,2020]}}))
