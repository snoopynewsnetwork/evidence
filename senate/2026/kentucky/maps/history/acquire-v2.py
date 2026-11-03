"""Bounded read-only acquisition. Preserve every attempted hop and entire entity."""
from common import *
import urllib.request,urllib.error,urllib.parse,datetime,socket,sys
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kw):return None
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(url,role,method='GET',payload=None,headers=None):
 configured={'User-Agent':'Kentucky-map-source-research/1.0','Accept-Encoding':'identity'};configured.update(headers or {})
 request={'url':url,'method':method,'body_utf8':None if payload is None else payload.decode(),'configured_headers':configured,'timeout_seconds':35,'options':{'automatic_redirects':False,'maximum_observed_hops':8,'read_only_public_source':True}}
 key=sha(canonical(request))[:20];dest=ROOT/'source/receipts'/f'{key}.json'
 if dest.exists():
  prior=strict(dest.read_bytes())
  if prior['hops'][-1].get('status') is not None:return prior
  dest=dest.with_name(dest.stem+'-reacquired.json')
  if dest.exists():return strict(dest.read_bytes())
 receipt={'role':role,'request':request,'started_utc':now(),'hops':[],'wire_bytes_available':False,'body_semantics':'Full HTTP response entity bytes returned by urllib; no invented transport/TLS metadata.'}
 current=url;opener=urllib.request.build_opener(NoRedirect)
 for i in range(8):
  hop={'request_url':current,'request_method':method,'request_body_utf8':request['body_utf8'],'configured_headers':configured,'started_utc':now()}
  try:
   req=urllib.request.Request(current,data=payload,headers=configured,method=method)
   try:res=opener.open(req,timeout=35)
   except urllib.error.HTTPError as e:res=e
   raw=res.read();hop.update({'status':res.code,'response_url':res.geturl(),'headers':list(res.headers.raw_items()),'ended_utc':now()})
   h=sha(raw);stored=gzip.compress(raw,mtime=0);assert len(stored)<40000000
   p=ROOT/'source/bodies'/f'{h}.gz'
   if not p.exists():p.write_bytes(stored)
   hop['entity']={'path':str(p.relative_to(ROOT)),'raw_bytes':len(raw),'raw_sha256':h,'stored_bytes':len(stored),'stored_sha256':sha(stored)}
   receipt['hops'].append(hop)
   if res.code in (301,302,303,307,308) and res.headers.get('Location'):
    current=urllib.parse.urljoin(current,res.headers['Location']);continue
   break
  except Exception as e:
   hop.update({'ended_utc':now(),'status':None,'headers':None,'entity':None,'error_type':type(e).__name__,'error':str(e),'metadata_availability':'No HTTP response observed; unavailable values remain null.'});receipt['hops'].append(hop);break
 receipt['ended_utc']=now();save(dest,receipt);print(role,receipt['hops'][-1].get('status'),receipt['hops'][-1].get('entity',{}),flush=True);return receipt

def raw(receipt):
 h=receipt['hops'][-1];return body(ROOT/h['entity']['path']) if h.get('entity') else None
if __name__=='__main__':fetch(sys.argv[1],sys.argv[2])
