"""Bounded public source capture. Explicit URL arguments; no auth or discovery."""
import datetime,gzip,hashlib,json,pathlib,subprocess,tempfile,urllib.parse,sys
BASE=pathlib.Path(__file__).resolve().parents[1]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def store(b):
 h=sha(b);z=gzip.compress(b,mtime=0); p=BASE/'bodies'/f'{h}.gz';p.parent.mkdir(exist_ok=True)
 if len(z)>=40000000:raise ValueError('whole compressed object requires explicit lossless partition')
 if p.exists():assert gzip.decompress(p.read_bytes())==b
 else:p.write_bytes(z)
 return {'path':str(p.relative_to(BASE)),'raw_bytes':len(b),'raw_sha256':h,'stored_bytes':len(z),'stored_sha256':sha(z)}
def fetch(label,url,method='GET',body=None,headers=None):
 headers=headers or {'User-Agent':'KentuckyOfficialSourceResearch/1.0','Accept':'*/*','Accept-Encoding':'identity'}
 receipt={'label':label,'started_utc':now(),'request':{'url':url,'method':method,'body':body,'configured_headers':headers,'timeout_seconds':35,'maximum_redirects':8},'hops':[]}
 for n in range(9):
  hop={'url':url,'method':method,'body':body,'configured_headers':headers,'started_utc':now()}
  with tempfile.TemporaryDirectory() as td:
   hp=pathlib.Path(td)/'headers';bp=pathlib.Path(td)/'body';cmd=['curl','--silent','--show-error','--max-time','35','--connect-timeout','12','--request',method,'--dump-header',str(hp),'--output',str(bp),'--write-out','%{http_code}',url]
   for k,v in headers.items():cmd+=['--header',k+': '+v]
   if body is not None:cmd+=['--data-raw',body]
   r=subprocess.run(cmd,capture_output=True);hb=hp.read_bytes() if hp.exists() else b'';bb=bp.read_bytes() if bp.exists() else None
   hop.update({'ended_utc':now(),'curl_exit':r.returncode,'curl_stdout':r.stdout.decode('utf-8','replace'),'curl_stderr':r.stderr.decode('utf-8','replace'),'header_bytes':store(hb),'headers_latin1':hb.decode('latin1'),'response_body':store(bb) if bb is not None else None,'body_availability':'captured' if bb is not None else 'unavailable; no response entity observed','status':int(r.stdout) if r.stdout.strip().isdigit() and int(r.stdout)>0 else None})
   receipt['hops'].append(hop)
   if r.returncode:break
   loc=None
   for line in hb.decode('latin1').splitlines():
    if line.lower().startswith('location:'):loc=line.split(':',1)[1].strip()
   if hop['status'] not in [301,302,303,307,308] or not loc:break
   url=urllib.parse.urljoin(url,loc)
   if hop['status']==303 or (hop['status'] in [301,302] and method=='POST'):method='GET';body=None
 receipt['ended_utc']=now();p=BASE/'receipts'/f'{label}.json';p.parent.mkdir(exist_ok=True)
 if p.exists():raise ValueError('receipt already exists; use a new attempt label')
 p.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');return receipt
if __name__=='__main__':
 for arg in sys.argv[1:]:
  label,url=arg.split('=',1);r=fetch(label,url);print(label,r['hops'][-1]['status'],r['hops'][-1]['curl_exit'])
