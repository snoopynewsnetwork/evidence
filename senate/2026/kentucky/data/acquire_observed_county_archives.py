"""Bounded archive lookup for two actual previously observed official recap URLs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import gzip,hashlib,importlib.util,json,urllib.parse
DATA=Path(__file__).resolve().parent
NEWS=DATA/'news'
URLS={
 'estill':'https://elect.ky.gov/results/2020-2029/PublishingImages/2020General/61657_20201211_RECAP.pdf',
 'lyon':'https://elect.ky.gov/results/2020-2029/PublishingImages/2020General/61002_20201118_RECAP.pdf'
}
def main():
 sp=importlib.util.spec_from_file_location('retained_fetch',NEWS/'fetch_evidence.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
 path=NEWS/'manifest.json';rows=json.loads(path.read_bytes());known={r['id']:r for r in rows}
 def retain(items):
  missing=[x for x in items if x[0]not in known]
  with ThreadPoolExecutor(max_workers=2)as pool:new=list(pool.map(mod.fetch,missing))
  for r in new:
   if r.get('asset'):
    match=next((old for old in rows if old.get('raw_sha256')==r.get('raw_sha256')and old.get('stored_sha256')==r.get('stored_sha256')),None)
    if match and match['asset']!=r['asset']:
     duplicate=NEWS/r['asset'];assert duplicate.read_bytes()==(NEWS/match['asset']).read_bytes();duplicate.unlink();r['asset']=match['asset'];r['storage_note']='Exact previously retained original/stored entity reused without duplicate bytes; observation URL/headers/UTC remain separate.'
   rows.append(r);known[r['id']]=r
  if new:
   temp=path.with_suffix('.tmp');temp.write_text(json.dumps(rows,indent=2)+'\n');temp.replace(path)
  return [known[k]for k,u in items]
 catalogs=retain([(f'sbe-2020-{tag}-observed-recap-cdx','https://web.archive.org/cdx/search/cdx?'+urllib.parse.urlencode(dict(url=url,output='json',filter='statuscode:200',collapse='digest')))for tag,url in URLS.items()])
 requests=[];findings=[]
 for tag,row in zip(URLS,catalogs):
  f=dict(county=tag,actual_previously_observed_official_URL=URLS[tag],catalog_observation_id=row['id'],catalog_status=row.get('status'),exposed_originals=[])
  if row.get('status')==200:
   raw=gzip.decompress((NEWS/row['asset']).read_bytes());table=json.loads(raw)
   if len(table)>1:
    keys=table[0];records=[dict(zip(keys,r))for r in table[1:]]
    chosen=[records[0]]if len(records)==1 else[records[0],records[-1]]
    for r in chosen:
     assert r['statuscode']=='200';timestamp=r['timestamp'];original=r['original'];key=f'sbe-2020-{tag}-recap-archive-{timestamp}';url=f'https://web.archive.org/web/{timestamp}id_/{original}'
     requests.append((key,url));f['exposed_originals'].append(dict(catalog_record=r,observation_id=key))
   f['matching_catalog_records']=max(0,len(table)-1)
  findings.append(f)
 retain(requests)
 for f in findings:
  for r in f['exposed_originals']:
   obs=known[r['observation_id']];r['HTTPstatus']=obs.get('status');r['complete_entity_bytes']=obs.get('bytes');r['raw_sha256']=obs.get('raw_sha256')
   if obs.get('asset'):
    body=gzip.decompress((NEWS/obs['asset']).read_bytes());r['PDFmagic']=body.startswith(b'%PDF-');r['retained_asset']='data/news/'+obs['asset']
 out=dict(status='bounded_actual_county_recap_archive_discovery_only',source_findings=findings,qualification='Only actual previously observed official recap URLs were catalog queried; download timestamps/originalURLs come from returned status200 catalog records. Empty exact queries are not absence under other links. A valid original body still needs page/native/candidate/method/source-control review; no complete120county/native or current authority/priority approval.')
 (DATA/'coordinator-county-recap-archive-discovery.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out))
if __name__=='__main__':main()
