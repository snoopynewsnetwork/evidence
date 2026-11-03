#!/usr/bin/env python3
"""Bounded original public acquisitions; only owned output paths. Entity bytes are decoded HTTP bodies."""
import requests,json,gzip,hashlib,datetime,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fetch(url,role,parent=None):
 now=datetime.datetime.now(datetime.timezone.utc).isoformat(); key=hashlib.sha256((now+url).encode()).hexdigest()[:16]
 receipt={'id':key,'requested_url':url,'retrieved_at_utc':now,'role':role,'parent':parent,'hops':[],'source_clock':None}
 try:
  r=requests.get(url,timeout=35,headers={'User-Agent':'KentuckyHistoricalResearch/1.0'},allow_redirects=False)
  for n in range(10):
   b=r.content;h=hashlib.sha256(b).hexdigest();p=ROOT/'source/bodies'/f'{h}.gz';p.parent.mkdir(exist_ok=True)
   if not p.exists(): p.write_bytes(gzip.compress(b,mtime=0))
   receipt['hops'].append({'url':r.url,'status':r.status_code,'headers':dict(r.headers),'raw_sha256':h,'raw_bytes':len(b),'body':str(p.relative_to(ROOT)),'stored_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'stored_bytes':p.stat().st_size})
   if not r.is_redirect:break
   r=requests.get(requests.compat.urljoin(r.url,r.headers['Location']),timeout=35,headers={'User-Agent':'KentuckyHistoricalResearch/1.0'},allow_redirects=False)
  receipt['final_url']=r.url;receipt['status']=r.status_code
 except Exception as e: receipt['error']=repr(e);b=b''
 (ROOT/'source/receipts'/f'{key}.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(key,receipt.get('status'),len(b),role,flush=True)
 return receipt,b
if __name__=='__main__':fetch(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else None)
