#!/usr/bin/env python3
"""Execute captured OWN original phase only in an isolated temporary mirror with exercised denial guards."""
import os,sys,json,gzip,tempfile,subprocess,hashlib,shutil,re
from pathlib import Path
from captured_core import Capture,ROOT,STATE,sha
O=Capture('own-pre-resume');OUT=ROOT/'replay';OUT.mkdir(exist_ok=True)
PHASE=['extract_certificates.py','extract_portfolio.py','extract_native.py','manual_image_witness.py','handwritten_fields.py','jefferson_alternative_witness.py','extract_statistics.py','extract_report_controls.py','diagnose_native.py','build_turnout.py','write_report.py']
GUARD=r'''
import os,sys,json,pathlib
CFG=json.load(open(os.environ['KY_GUARD_CONFIG']));T=pathlib.Path(CFG['temporary_root']).resolve();S=pathlib.Path(CFG['real_state']).resolve();ALLOW={pathlib.Path(x).resolve() for x in CFG['original_read_paths']};SCRIPTS={pathlib.Path(x).resolve() for x in CFG['allowed_script_paths']}
def inside(p,root):
 try:return p.is_relative_to(root)
 except:return False
def path(x):
 if isinstance(x,(str,bytes,os.PathLike)):return pathlib.Path(os.fsdecode(x)).resolve()
 return None
def deny(reason):raise PermissionError('KY_EXERCISED_DENIAL:'+reason)
def writable(p):
 p=path(p)
 if p is not None and not inside(p,T):deny('writes outside isolated temporary root')
def guard(event,args):
 if event.startswith('socket.'):deny('network sockets/DNS')
 if event=='open':
  p=path(args[0]);mode=args[1];flags=args[2]
  writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
  if writing:writable(args[0])
  elif p is not None and inside(p,S) and not inside(p,T) and p not in ALLOW:deny('mutable producer/peer/news/coordinator read')
 if event in ('os.listdir','os.scandir'):
  p=path(args[0])
  if p is not None and inside(p,S) and not inside(p,T):deny('peer/producer discovery')
 if event in ('os.mkdir','os.remove','os.rmdir','os.unlink','os.truncate'):writable(args[0])
 if event in ('os.rename','os.replace'):writable(args[0]);writable(args[1])
 if event=='subprocess.Popen':
  cmd=args[1];cmd=list(cmd) if isinstance(cmd,(list,tuple)) else [cmd];exe=pathlib.Path(os.fsdecode(cmd[0])).name
  if exe in ['pdftotext','pdfinfo','pdftoppm']:
   for a in cmd[1:]:
    if isinstance(a,str) and '/' in a and not a.startswith('-'):
     p=path(a)
     if p is not None and not inside(p,T):deny('external tool path outside temporary root')
  elif exe.startswith('python'):
   if len(cmd)<2 or path(cmd[1]) not in SCRIPTS:deny('producer helper/writer execution')
  else:deny('unapproved subprocess/network helper')
sys.addaudithook(guard)
'''
with tempfile.TemporaryDirectory(prefix='ky-turnout-captured-replay-') as td:
 T=Path(td).resolve();S=T/'kentucky';R=S/'data/turnout';(R/'scripts').mkdir(parents=True);(R/'extracts').mkdir();(R/'history').mkdir();(R/'proof').mkdir();(R/'source/receipts').mkdir(parents=True);(R/'source/bodies').mkdir();(S/'data/news').mkdir(parents=True);G=T/'guard';G.mkdir();(G/'sitecustomize.py').write_text(GUARD)
 original_paths=[]
 # Stage all exact original-phase inputs, with each huge immutable entity reused read-only.
 for n,z in O.entries.items():
  if n.startswith('data/turnout/source/') or n.startswith('data/turnout/extracts/') or n.startswith('data/turnout/proof/') or n.startswith('data/turnout/scripts/'):
   target=S/n;target.parent.mkdir(parents=True,exist_ok=True)
   if n.startswith('data/turnout/source/bodies/'):
    src=STATE/n;target.symlink_to(src.resolve());original_paths.append(str(src.resolve()))
   else:target.write_bytes(O.body(n))
 for z in O.index['external_original_pins']:
  src=STATE/z['path'];target=S/z['path'];target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists():target.symlink_to(src.resolve())
  original_paths.append(str(src.resolve()))
 # Frozen histories/old witnesses are inputs to report provenance only; no current discovery.
 for n in O.entries:
  if n.startswith('data/turnout/history/') and n.endswith('/witness.json'):
   p=S/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(O.body(n))
 probe=T/'denial_probes.py';probe.write_text('''import os,sys,json,socket,subprocess,importlib.util\nfrom pathlib import Path\nC=json.load(open(os.environ['KY_GUARD_CONFIG']));S=Path(C['real_state']);out=[]\ndef attempt(label,f):\n try:f()\n except PermissionError as e:\n  assert 'KY_EXERCISED_DENIAL:' in str(e);out.append({'probe':label,'denied':True,'error':str(e)})\n else:raise AssertionError('DENIAL PROBE UNEXPECTEDLY ALLOWED '+label)\nattempt('network DNS/socket',lambda:socket.getaddrinfo('example.com',443))\nattempt('mutable newsroom aggregate',lambda:(S/'data/news/manifest.json').read_bytes())\nattempt('coordinator numerical aggregate',lambda:(S/'data/coordinator-certified-county-preflight.json').read_bytes())\nattempt('peer discovery',lambda:list((S/'data/baselines').iterdir()))\nattempt('current peer body',lambda:(S/'data/baselines/priority.json').read_bytes())\nattempt('producer helper read',lambda:(S/'data/preflight_certified_county_vectors.py').read_bytes())\nattempt('producer writer execution',lambda:subprocess.run([sys.executable,str(S/'data/baselines/scripts/build.py')]))\nattempt('unapproved acquisition helper',lambda:subprocess.run(['curl','https://example.com']))\nattempt('write outside temp',lambda:Path('/private/tmp/ky-denied-outside-replay-probe').write_text('must not be written'))\nprint(json.dumps(out,indent=2))\n''')
 cfg={'temporary_root':str(T),'real_state':str(STATE.resolve()),'original_read_paths':original_paths,'allowed_script_paths':[str(R/'scripts'/n) for n in PHASE]+[str(probe)]};config=T/'config.json';config.write_text(json.dumps(cfg));(OUT/'guard-config-template.json').write_text(json.dumps({**cfg,'temporary_root':'<isolated temp>','allowed_script_paths':[Path(x).name for x in cfg['allowed_script_paths']]},indent=2)+'\n');(OUT/'sitecustomize.py').write_text(GUARD);(OUT/'denial-probe-program.py').write_bytes(probe.read_bytes());env={**os.environ,'PYTHONPATH':str(G),'PYTHONDONTWRITEBYTECODE':'1','KY_GUARD_CONFIG':str(config),'TMPDIR':str(T)}
 logs=[]
 def run(label,cmd,data=None):
  z=subprocess.run(cmd,input=data,capture_output=True,env=env,cwd=T);(OUT/f'{label}.stdout').write_bytes(z.stdout);(OUT/f'{label}.stderr').write_bytes(z.stderr);logs.append({'step':label,'exit':z.returncode,'stdout_sha256':sha(z.stdout),'stderr_sha256':sha(z.stderr)});assert z.returncode==0,(label,z.stderr[-1500:]);return z
 run('denial-probes',[sys.executable,str(probe)])
 # Independently replay every complete captured PDF to exact layout, without using a mutable catalog.
 pdf_checks=[]
 bodies={}
 for n in O.entries:
  if re.fullmatch(r'data/turnout/source/bodies/[0-9a-f]{64}\.gz',n):bodies[Path(n).stem]=gzip.decompress(O.body(n))
 for z in O.index['external_original_pins']:
  bodies[z['raw_sha256']]=gzip.decompress((STATE/z['path']).read_bytes())
 for h,raw in sorted(bodies.items()):
  n=f'data/turnout/extracts/{h}.layout.txt'
  if raw.startswith(b'%PDF') and n in O.entries:
   z=run('pdf-'+h,['pdftotext','-layout','-','-'],raw);assert z.stdout==O.body(n),h;(R/'extracts'/f'{h}.layout.txt').write_bytes(z.stdout);pdf_checks.append({'source_sha256':h,'complete_layout_sha256':sha(z.stdout),'bytes':len(z.stdout)})
 # Child captured scripts execute through inherited sitecustomize guards, never producer/peer code.
 for name in PHASE:
  p=R/'scripts'/name;assert sha(p.read_bytes())==sha(O.body('data/turnout/scripts/'+name));run('script-'+name,[sys.executable,str(p)])
 # Whole generated bodies, including all full arrays, must equal captured historical outputs.
 expected=['data/county-turnout.csv','turnout.md']+[n for n in O.entries if n.startswith('data/turnout/extracts/') and not n.endswith('.ocr.txt')]+['data/turnout/'+n for n in ['county-sensitivity.json','native-units.jsonl.gz','known-native-order.json','source-native-statistics-identities.jsonl.gz','native-certificate-comparisons.json','coverage.json','priority-set.json','source/entities.json']]
 results=[]
 for n in sorted(set(expected)):
  p=S/n;assert p.is_file(),n;b=p.read_bytes();old=O.body(n);results.append({'oldpath':n,'old_sha256':sha(old),'replayed_sha256':sha(b),'bytes':len(b),'exact_whole_body_equal':b==old});assert b==old,('whole original-phase drift',n,sha(old),sha(b))
 (OUT/'whole-output-comparison.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'full-pdf-replays.json').write_text(json.dumps(pdf_checks,indent=2)+'\n');(OUT/'steps.json').write_text(json.dumps(logs,indent=2)+'\n');(OUT/'result.json').write_text(json.dumps({'status':'PASS','captured_own_scripts_only':PHASE,'complete_PDFs':len(pdf_checks),'whole_historical_outputs_exact':len(results),'network_mutable_peer_producer_outside_write_probes':'all actually denied','exceptions':[]},indent=2)+'\n');print('ORIGINAL PHASE REPLAY PASS',len(results),len(pdf_checks))
