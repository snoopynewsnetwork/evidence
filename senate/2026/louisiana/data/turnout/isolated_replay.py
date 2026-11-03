"""Run exact captured own original producers in a temporary audit-hook sandbox.
No peer producer is imported or executed; no current discovery/source/helper is read.
"""
from pathlib import Path
import datetime,gzip,hashlib,io,json,os,subprocess,sys,tarfile,tempfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
CHILD=r'''
import sys,os,json,pathlib,runpy,sysconfig,socket,importlib
base=pathlib.Path(sys.argv[1]).resolve();target=sys.argv[2];repo=pathlib.Path(sys.argv[3]).resolve();denials=[]
runtime=[pathlib.Path(sysconfig.get_path(k)).resolve()for k in ['stdlib','platstdlib','purelib','platlib']]
def within(p,root):return p==root or root in p.parents
def hook(event,args):
 if event=='open':
  name=args[0]
  if isinstance(name,int):return
  q=pathlib.Path(os.fsdecode(name)).resolve();mode=args[1];flags=args[2]if len(args)>2 else 0
  writing=(isinstance(mode,str)and any(c in mode for c in 'wax+'))or(isinstance(flags,int)and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
  if writing and not within(q,base):raise PermissionError('DENY outside-temp write '+str(q))
  if not writing and not(within(q,base)or any(within(q,x)for x in runtime)):raise PermissionError('DENY external/current/mutable source read '+str(q))
  if not writing and ('/peer-capture/'in str(q)or q.name in ['compare_peer.py','acquire.py','freeze_originals.py','freeze_acquired.py']):raise PermissionError('DENY peer/helper source read '+str(q))
 if event.startswith('socket.')or event in ['subprocess.Popen','os.system','os.exec','os.posix_spawn']:raise PermissionError('DENY network/process producer '+event)
 if event in ['os.mkdir','os.remove','os.rmdir','os.rename','os.replace']:
  for v in args[:2]if event in ['os.rename','os.replace']else args[:1]:
   if isinstance(v,(str,bytes))and not within(pathlib.Path(os.fsdecode(v)).resolve(),base):raise PermissionError('DENY outside-temp mutation')
 if event=='import'and args[0].split('.')[0]in ['acquire','freeze_originals','freeze_acquired','compare_peer','calculator','reproduce','enrich','supplement','build','source_cli']:raise PermissionError('DENY producer/helper import '+args[0])
sys.dont_write_bytecode=True;sys.addaudithook(hook)
sys.path.insert(0,str(base/'data/turnout'))
probes=[('network',lambda:socket.socket()),('mutable_news',lambda:open(repo/'senate/2026/louisiana/data/news/manifest.json','rb')),('coordinator_helper',lambda:open(repo/'senate/2026/louisiana/data/preflight_primary_sources.py','rb')),('peer_current_source',lambda:open(repo/'senate/2026/louisiana/data/baselines/native-results.json.gz','rb')),('current_discovery',lambda:open(repo/'senate/2026/louisiana/data/turnout/source/original-pins.json','rb')),('outside_temp_write',lambda:open(base.parent/'denied-outside-replay.tmp','wb')),('producer_import',lambda:__import__('acquire'))]
for name,f in probes:
 try:f()
 except PermissionError as e:denials.append({'probe':name,'denied':True,'error':str(e)})
 else:raise AssertionError('Sandbox unexpectedly allowed '+name)
print('SANDBOX_DENIALS='+json.dumps(denials),flush=True)
sys.path.insert(0,str(base/'data/turnout'));os.chdir(base)
runpy.run_path(str(base/'data/turnout'/target),run_name='__main__')
'''
def main():
    d=R/'history/packaging-repair';index=json.loads((d/'own-prior-inventory.json').read_bytes());parts=[]
    for p in index['ordered_archive_parts']:
        b=(R/p['path']).read_bytes();assert sha(b)==p['sha256'];parts.append(b)
    archive=b''.join(parts);assert sha(archive)==index['archive_sha256'];t=tarfile.open(fileobj=io.BytesIO(gzip.decompress(archive)),mode='r:')
    expected={x['path']:x for x in index['members']};proof={'scope':'Captured own original extraction/build scripts only, individual fixed own body+receipt pins; no live peer/current discovery/network/producer helpers','archive_sha256':sha(archive),'runs':[],'whole_byte_comparison':[],'metadata_exceptions':[]}
    # Required original phase scripts and fixed body/receipt inputs are copied by exact stored bytes.
    with tempfile.TemporaryDirectory(prefix='la-original-replay-')as temp:
        base=Path(temp);whitelist=['extract_originals.py','build_turnout.py']
        for name,member in expected.items():
            if not name.startswith('data/turnout/'):continue
            rel=name.removeprefix('data/turnout/')
            if rel.startswith('peer-capture/')or rel.startswith('history/'):continue
            if rel.endswith('.py')and rel not in whitelist+['acquire.py']:continue
            b=t.extractfile(name).read();assert sha(b)==member['sha256'];q=base/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        # Own source-agreement status is captured metadata only, not a peer producer/data input.
        runner=base/'runner.py';runner.write_text(CHILD);repo=R.parents[4]
        for script in whitelist:
            result=subprocess.run([sys.executable,str(runner),str(base),script,str(repo)],capture_output=True,text=True,cwd=base,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            savebase=d/('isolated-'+script)
            savebase.with_suffix(savebase.suffix+'.stdout').write_text(result.stdout);savebase.with_suffix(savebase.suffix+'.stderr').write_text(result.stderr)
            proof['runs'].append({'captured_script':script,'captured_script_sha256':sha(t.extractfile('data/turnout/'+script).read()),'returncode':result.returncode,'stdout_sha256':sha(result.stdout.encode()),'stderr_sha256':sha(result.stderr.encode()),'denials':json.loads(next(x.split('=',1)[1]for x in result.stdout.splitlines()if x.startswith('SANDBOX_DENIALS=')))if'SANDBOX_DENIALS='in result.stdout else[]})
            if result.returncode:
                (d/'isolated-replay-failed-proof.json').write_text(json.dumps(proof,indent=2)+'\n');raise AssertionError('Captured original phase failed; whole logs retained: '+script)
        generated=['data/turnout/extract/'+y+'-whole-workbook-positions.json.gz'for y in ['2024','2022','2020']]+['data/turnout/extract/source-only-selected-controls.json.gz','data/turnout/historical-controls.json','data/turnout/source-statistics-controls.json.gz','data/turnout/native-control-discrepancies.json','data/turnout/statistics-scope-discrepancies.json','data/turnout/method-candidate-controls.json','data/turnout/candidate-controls.csv','data/turnout/orders-summary.json','data/turnout/priority-set.json','data/county-turnout.csv']
        generated += [n for n in expected if n.startswith('data/turnout/orders/')or(n.startswith('data/turnout/extract/')and n.endswith(('-native.json.gz','-parishes.json')))]
        for name in sorted(set(generated)):
            old=t.extractfile(name).read();new=(base/name).read_bytes();entry={'path':name,'old_sha256':sha(old),'new_sha256':sha(new),'old_bytes':len(old),'new_bytes':len(new),'whole_bytes_equal':old==new};proof['whole_byte_comparison'].append(entry)
            if old!=new:
                # Preserve complete old/new bodies and the actual failed byte comparison before qualification.
                (d/(name.replace('/','__')+'.old.gz')).write_bytes(gzip.compress(old,mtime=0));(d/(name.replace('/','__')+'.replayed.gz')).write_bytes(gzip.compress(new,mtime=0));raise AssertionError('Whole generated bytes differ: '+name)
    proof['status']='pass';proof['network_and_external_read_write_denials_exercised']=True;proof['producer_import_denial_exercised']=True
    (R/'repair-proof/isolated-original-replay.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'status':'pass','exact_generated_files':len(proof['whole_byte_comparison']),'denial_probes':sum(len(x['denials'])for x in proof['runs'])}))
if __name__=='__main__':main()
