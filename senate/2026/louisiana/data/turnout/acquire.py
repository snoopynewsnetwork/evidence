"""Bounded anonymous read-only public downloads, complete entities and per-hop receipts.
Usage: python3 acquire.py ID URL [PARENT_ID]. Never fetches November count files.
"""
from pathlib import Path
import datetime,gzip,hashlib,json,sys,urllib.request,urllib.error
ROOT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(sid,url,parent=None):
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    hops=[]
    class Redirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            b=fp.read(); bp=ROOT/'source'/f'{sha(b)}.body.gz'
            if not bp.exists():bp.write_bytes(gzip.compress(b,mtime=0))
            hops.append({'url':req.full_url,'status':code,'headers':list(headers.items()),'body':str(bp.relative_to(ROOT)),'raw_sha256':sha(b),'bytes':len(b),'location':newurl})
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    receipt={'id':sid,'requested_url':url,'parent_source_id':parent,'retrieval_started_utc':stamp,'method':'GET','redirects':hops}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Louisiana historical election research','Accept-Encoding':'identity'})
        try:r=urllib.request.build_opener(Redirect).open(req,timeout=45)
        except urllib.error.HTTPError as e:r=e
        with r:
            raw=r.read(39000000+1)
            assert len(raw)<=39000000,'Bounded response exceeded; not stored as complete'
            bp=ROOT/'source'/f'{sha(raw)}.body.gz'
            if not bp.exists():bp.write_bytes(gzip.compress(raw,mtime=0))
            receipt.update(final_url=r.geturl(),status=r.code,headers=list(r.headers.items()),raw_sha256=sha(raw),bytes=len(raw),body=str(bp.relative_to(ROOT)),stored_sha256=sha(bp.read_bytes()),complete_entity=True)
    except Exception as e:receipt.update(error=repr(e),complete_entity=False)
    receipt['retrieval_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=ROOT/'source'/f'{sid}.{stamp}.receipt.json';p.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'receipt':str(p.relative_to(ROOT)),**{k:receipt.get(k) for k in ['id','status','bytes','error','raw_sha256']}}))
    return receipt
if __name__=='__main__':fetch(*sys.argv[1:])
