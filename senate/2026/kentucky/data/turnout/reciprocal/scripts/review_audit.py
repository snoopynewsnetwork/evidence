#!/usr/bin/env python3
"""Complete captured-final source-core audit. --final performs no owned writes."""
import json,gzip,re,sys,subprocess,os,tempfile,contextlib,io
from pathlib import Path
from captured_core import Capture,ROOT,STATE,sha
R=ROOT.parent;O=Capture('own-pre-resume');P=Capture('peer-final');final='--final' in sys.argv
checks={}
def j(p):return json.loads(p.read_bytes())
def run(args):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 assert p.returncode==0,(args,p.returncode,p.stdout.decode(errors='replace'),p.stderr.decode(errors='replace'))
 return p
for C,n,mf,pin in [(O,2735,'data/turnout/asset-manifest.json','9721574f385847d85c2cea99e8704425838138d10e9958a81a2586e9fa9629e2'),(P,1972,'data/baselines/asset-manifest.json','9415e66193d21382abc5bc9f5ab97b3943ce2498c64e33acb3aade7dfdf5b2a4')]:
 assert C.verify_all()==n and sha(C.body(mf))==pin
 listed=C.json(mf)['files'];assert len(listed)==n-1 and {z['path'] for z in listed}|{mf}==set(C.entries)
 for z in listed:assert (z['sha256'],z['bytes'])==(C.entries[z['path']]['sha256'],C.entries[z['path']]['bytes'])
 for z in C.entries.values():
  if 'captured_body' in z:assert (STATE/z['captured_body']).stat().st_size==z['captured_stored_bytes']
 checks[C.index_path.parent.name+'_whole_bodies']=n
assert sha(P.body('data/baselines/finalseal.json'))=='57c55633ae06cb3799061f258ebe15fd2246549e5e59547070bab6d7312c4f68'
assert sha(O.body('data/turnout/priority-set.json'))=='fadb6c46ae1b1925cb409ce542732565978d6816fb37f86cfbadb4780dc94c62'
review=j(ROOT/'review.json')
assert sha(O.index_path.read_bytes())==review['own_pre_resume_body_index_sha256'] and sha(P.index_path.read_bytes())==review['peer_complete_body_index_sha256']
roles=P.index['complete_original_pin_roles']
assert roles==P.json('data/baselines/source/pins.json')['pins']
assert P.index['external_original_roles']==P.json('data/baselines/asset-manifest.json')['external_read_only_source_roles']
pins={(z['receipt'],z['hop']):z for z in roles}
for z in O.index['external_original_pins']+roles:
 b=(STATE/z['path']).read_bytes();raw=gzip.decompress(b)
 assert sha(b)==z['stored_sha256'] and len(b)==z['stored_bytes'] and sha(raw)==z['raw_sha256'] and len(raw)==z['raw_bytes']
 if 'receipt' in z:assert sha(P.body(z['receipt']))==z['receipt_sha256']
hops=0;ownhops=0
for name in P.entries:
 if not name.startswith('data/baselines/source/receipts/') or not name.endswith('.json'):continue
 receipt=P.json(name)
 for i,h in enumerate(receipt.get('hops',[])):
  if not h.get('body'):continue
  if (name,i) in pins:b=(STATE/pins[name,i]['path']).read_bytes()
  else:b=P.body('data/baselines/'+h['body']);ownhops+=1
  raw=gzip.decompress(b)
  assert sha(b)==h['stored_sha256'] and len(b)==h['stored_bytes'] and sha(raw)==h['raw_sha256'] and len(raw)==h['raw_bytes'],(name,i)
  hops+=1
checks['peer_receipt_hops']=hops;checks['peer_own_body_hops']=ownhops;checks['external_original_roles']=len(roles)
allowed={'turnout.md','data/turnout/source/SCHEMA.md','data/turnout/priority-set.json','data/turnout/validation.json','data/turnout/finalseal.json','data/turnout/asset-manifest.json'}
for p in O.entries:
 if p not in allowed:assert sha((STATE/p).read_bytes())==O.entries[p]['sha256'],('unauthorized original body change',p)
for p in ['turnout.md','data/turnout/source/SCHEMA.md']:assert (STATE/p).read_bytes().startswith(O.body(p))
a=O.json('data/turnout/priority-set.json');b=j(R/'priority-set.json')
assert set(b)-set(a)=={'captured_final_source_core_review'}
assert {k:v for k,v in a.items() if k!='peer_agreement_status'}=={k:v for k,v in b.items() if k not in ('peer_agreement_status','captured_final_source_core_review')}
assert b['captured_final_source_core_review']==review
assert sha((STATE/'data/county-turnout.csv').read_bytes())=='3e64920f66e59705766422d430c9bdf64c13d28d3433799d2159e892ac4a4629'
checks['original_unchanged_or_explicit_metadata_only']=len(O.entries)
# Independently re-execute review adapters against captured whole bytes; redirect every output to temp.
with tempfile.TemporaryDirectory(prefix='ky-final-source-audit-') as td:
 dest=Path(td)/'comparison';dest.mkdir()
 for name in ['reconcile.py','source_orders.py','source_hierarchy.py']:
  code=(ROOT/'scripts'/name).read_text()
  needle="OUT=ROOT/'comparison'" if name=='reconcile.py' else "D=ROOT/'comparison'"
  assert code.count(needle)==1;code=code.replace(needle,('OUT=' if name=='reconcile.py' else 'D=')+repr(str(dest)))
  # Preserve Path semantics while directing only review output, never changing source/count logic.
  code=code.replace(('OUT=' if name=='reconcile.py' else 'D=')+repr(str(dest)),('OUT=' if name=='reconcile.py' else 'D=')+'__import__("pathlib").Path('+repr(str(dest))+')')
  with contextlib.redirect_stdout(io.StringIO()):exec(compile(code,str(ROOT/'scripts'/name),'exec'),{'__name__':'__captured_readonly_audit__'})
  for out in dest.iterdir():assert out.read_bytes()==(ROOT/'comparison'/out.name).read_bytes(),('whole review output drift',out.name)
checks['full_source_core_order_hierarchy_recomputations']=3
summary=j(ROOT/'comparison/summary.json');assert summary['critical_difference_count']==0 and sum(summary['literal_or_schema_differences'].values())==88
assert summary['missing_peer_selected_native_observations']==summary['missing_peer_selected_statistics_observations']==0
replay=j(ROOT/'replay/result.json');assert replay['status']=='PASS' and replay['whole_historical_outputs_exact']==293 and replay['complete_PDFs']==134 and not replay['exceptions']
for z in j(ROOT/'replay/whole-output-comparison.json'):
 assert z['old_sha256']==z['replayed_sha256']==O.entries[z['oldpath']]['sha256'] and z['bytes']==O.entries[z['oldpath']]['bytes'] and z['exact_whole_body_equal']
probes=j(ROOT/'replay/denial-probes.stdout');assert len(probes)==9 and all(z['denied'] and z['error'].startswith('KY_EXERCISED_DENIAL:') for z in probes)
f=run([sys.executable,str(ROOT/'scripts/packet_checks.py'),'--audit-only']);assert b'PASS 382 17' in f.stdout
checks['complete_actual_corruption_packets_rejected']=17;checks['historical_exact_replay_outputs']=293;checks['exercised_denial_probes']=9
for p in [STATE/'turnout.md',R/'source/SCHEMA.md',ROOT/'README.md']:
 for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if link.startswith(('https://','http://','#')):continue
  target=(p.parent/link.split('#')[0]).resolve();assert target.is_relative_to(STATE.resolve()) and target.exists(),(p,link)
files=[STATE/'turnout.md',STATE/'data/county-turnout.csv']+[p for p in R.rglob('*') if p.is_file()]
for p in R.rglob('*'):
 assert not p.is_symlink() and p.name not in ('__pycache__','node_modules','.cache','.venv','venv'),p
for p in files:assert p.stat().st_size<40000000,p
# Original independently authored audit replays all134 complete PDFs and every own source/count/null/order/history reference.
original=run([sys.executable,str(R/'scripts/audit.py'),'--final' if final else '--record'])
original_result=json.loads(original.stdout);assert original_result['status']==('PASS' if final else 'preseal_checks_satisfied')
checks['original_full_offline_audit']=original_result['checks']
if final:
 mf=j(R/'asset-manifest.json');actual={str(p.relative_to(STATE)) for p in files if p!=R/'asset-manifest.json'}
 assert len(mf['files'])==len(actual) and {z['path'] for z in mf['files']}==actual
 for z in mf['files']:
  body=(STATE/z['path']).read_bytes();assert len(body)==z['bytes'] and sha(body)==z['sha256']
 checks['complete_manifest_targets']=len(actual)
else:
 (ROOT/'preseal-original-audit.stdout').write_bytes(original.stdout);(ROOT/'preseal-original-audit.stderr').write_bytes(original.stderr)
 result={'status':'PASS','scope':'captured-final source core only','checks':checks,'no_numeric_source_order_null_admin_changes':True}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','final_readonly':final,'checks':checks,'manifest_sha256':sha((R/'asset-manifest.json').read_bytes()) if final else None,'contract_sha256':sha((R/'priority-set.json').read_bytes()),'no_owned_writes_performed':final},indent=2))
