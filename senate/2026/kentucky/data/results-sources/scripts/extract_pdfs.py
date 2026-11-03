import json,gzip,subprocess,tempfile,pathlib,hashlib
from inspect_html import BASE
if __name__=='__main__':
 out=BASE/'pdf-extracts';out.mkdir(exist_ok=True);records=[]
 for p in sorted((BASE/'receipts').glob('*.json')):
  r=json.loads(p.read_bytes());h=r['hops'][-1];ref=h['response_body']
  if not ref:continue
  b=gzip.decompress((BASE/ref['path']).read_bytes())
  if not b.startswith(b'%PDF-'):continue
  digest=hashlib.sha256(b).hexdigest()
  with tempfile.TemporaryDirectory() as td:
   f=pathlib.Path(td)/'source.pdf';f.write_bytes(b);record={'receipt':str(p.relative_to(BASE)),'raw_sha256':digest,'derivatives':{}}
   for name,args in [('layout',['pdftotext','-layout',str(f),'-']),('pdfinfo',['pdfinfo',str(f)])]:
    run=subprocess.run(args,capture_output=True);dest=out/(digest+'.'+name+'.txt.gz');dest.write_bytes(gzip.compress(run.stdout,mtime=0));record['derivatives'][name]={'file':str(dest.relative_to(BASE)),'exit':run.returncode,'stderr':run.stderr.decode('utf-8','replace'),'complete_stdout_bytes':len(run.stdout)}
   records.append(record)
 (out/'index.json').write_text(json.dumps(records,indent=2)+'\n');print('complete PDF extractions',len(records))
