import gzip,json,subprocess,sys,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;out=[]
for n in ['2024-native-base-native-volume','2020-parish-base-2024-volume-mix']:
 p=D/'scenarios'/f'{n}.input.json.gz';b=gzip.decompress(p.read_bytes());r=subprocess.run([sys.executable,'-B',str(D/'calculator.py'),'-'],input=b,capture_output=True);assert r.returncode==0 and r.stderr==b''
 a=json.loads(r.stdout);expected=json.loads(gzip.decompress((D/'scenarios'/f'{n}-tie.output.json.gz').read_bytes()));assert a==expected
 dst=D/'fixtures'/f'{n}.actual-cli.stdout.json.gz';dst.write_bytes(gzip.compress(r.stdout,mtime=0));out.append({'scenario':n,'input_sha256':hashlib.sha256(b).hexdigest(),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'exit':r.returncode,'stderr':'','units':len(a['units']),'passed':True})
(D/'fixtures/historical-cli-results.json').write_text(json.dumps(out,indent=2)+'\n');print('Source CLI fixtures passed',len(out))
