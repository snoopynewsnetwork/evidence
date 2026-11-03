"""Bounded public authority captures. Each hop retained, no overwrite."""
from pathlib import Path
import urllib.request,urllib.error,json,gzip,hashlib,datetime,sys
B=Path(__file__).resolve().parents[1]
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):return None
def fetch(url,role,parent=None):
 rid=hashlib.sha256(url.encode()).hexdigest()[:20];dest=B/'source/receipts'/('own-'+rid+'.json')
 if dest.exists():
  prior=json.loads(dest.read_text())
  if 'error' not in prior:return prior
  dest=dest.with_name(dest.stem+'-retry1.json')
  if dest.exists():return json.loads(dest.read_text())
 rec=dict(requested_url=url,role=role,parent=parent,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),hops=[])
 opener=urllib.request.build_opener(NoRedirect)
 for _ in range(7):
  try:r=opener.open(urllib.request.Request(url,headers={'User-Agent':'Public election historical research; Python urllib'}),timeout=35)
  except urllib.error.HTTPError as e:r=e
  except Exception as e:rec['error']=repr(e);break
  body=r.read();h=hashlib.sha256(body).hexdigest();s=gzip.compress(body,mtime=0);assert len(s)<40000000
  d=B/'source/bodies';d.mkdir(exist_ok=True);p=d/(h+'.gz')
  if not p.exists():p.write_bytes(s)
  rec['hops'].append(dict(url=url,status=r.status,headers=dict(r.headers),raw_sha256=h,raw_bytes=len(body),body=str(p.relative_to(B)),stored_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),stored_bytes=p.stat().st_size))
  if r.status not in (301,302,303,307,308):break
  url=urllib.parse.urljoin(url,r.headers['Location'])
 rec['final_url']=url;rec['source_clock']=None;dest.write_text(json.dumps(rec,indent=2)+'\n');return rec
if __name__=='__main__':
 for path in ['2024.aspx','2022.aspx','2020.aspx','2020recap-sheets.aspx','2022-General-Recap-Sheets.aspx']:
  r=fetch('https://elect.ky.gov/results/2020-2029/Pages/'+path,'Current authority navigation '+path);print(path,[h['status'] for h in r['hops']],r.get('error'),flush=True)
