"""Bounded anonymous public source fetch. Each acquisition has complete final entity receipt."""
import sys,json,gzip,hashlib,urllib.request,urllib.error,datetime
from pathlib import Path
D=Path(__file__).resolve().parent
name,url=sys.argv[1:]; t=datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
 r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Louisiana historical research (public read-only)','Accept-Encoding':'identity'}),timeout=40)
 b=r.read();status=r.status;headers=dict(r.headers);final=r.url
except urllib.error.HTTPError as r:
 b=r.read();status=r.code;headers=dict(r.headers);final=r.url
s=gzip.compress(b,mtime=0);p=D/'source'/f'{name}.gz';p.write_bytes(s)
x=dict(id=name,url=url,final_url=final,retrieved_at_utc=t,status=status,headers=headers,raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),stored_sha256=hashlib.sha256(s).hexdigest(),stored_bytes=len(s),asset=p.name,redirect_scope='urllib follows redirects; only final response entity/headers retained')
(p.with_suffix('.receipt.json')).write_text(json.dumps(x,indent=2)+'\n');print(name,status,len(b))
