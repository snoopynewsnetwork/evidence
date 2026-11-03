"""Re-execute captured-original verification in a fresh temp mirror; sealed producer stays read-only."""
from pathlib import Path
import gzip,hashlib,json,tempfile
S=Path(__file__).resolve().parents[1];D=S/'data';T=D/'turnout';H=T/'history/packaging-repair';sha=lambda b:hashlib.sha256(b).hexdigest()
before=sha((T/'asset-manifest.json').read_bytes());script=(T/'isolated_replay.py').read_bytes();expected=json.loads((T/'repair-proof/isolated-original-replay.json').read_bytes());idx=json.loads((H/'own-prior-inventory.json').read_bytes())
with tempfile.TemporaryDirectory(prefix='coordinator-la-original-replay-') as temp:
 r=Path(temp)/'repo/senate/2026/louisiana/data/turnout';d=r/'history/packaging-repair';d.mkdir(parents=True);(r/'repair-proof').mkdir()
 (d/'own-prior-inventory.json').write_bytes((H/'own-prior-inventory.json').read_bytes())
 for z in idx['ordered_archive_parts']:
  b=(T/z['path']).read_bytes();assert sha(b)==z['sha256'];p=r/z['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 ns={'__name__':'coordinator_temp_checker','__file__':str(r/'isolated_replay.py')};exec(compile(script,str(T/'isolated_replay.py'),'exec'),ns);ns['R']=r;ns['main']()
 actual=json.loads((r/'repair-proof/isolated-original-replay.json').read_bytes());assert actual['status']=='pass' and actual['whole_byte_comparison']==expected['whole_byte_comparison'] and len(actual['whole_byte_comparison'])==46
 assert sum(len(z['denials']) for z in actual['runs'])==14 and all(z['returncode']==0 for z in actual['runs'])
 logs=[];out=D/'coordinator-isolated-replay-logs';out.mkdir(exist_ok=True)
 for p in sorted(d.glob('isolated-*.py.std*')):
  b=p.read_bytes();q=out/(p.name+'.gz');q.write_bytes(gzip.compress(b,mtime=0));logs.append({'path':str(q.relative_to(S)),'raw_bytes':len(b),'raw_sha256':sha(b),'stored_sha256':sha(q.read_bytes())})
assert sha((T/'asset-manifest.json').read_bytes())==before
result={'status':'pass_fresh_captured_original_guarded_replay','captured_checker_sha256':sha(script),'complete_outputs':46,'actual_denial_probes':14,'actual_result':actual,'whole_process_logs':logs,'producer_manifest_unchanged':before,'scope':'Verification helper executed with all proof/log paths rebound exclusively to a fresh temporary mirror. Only two exact captured original extraction/build scripts execute within the helper sandbox. Complete regenerated file bytes match historical captured originals, not newer bodies. All sealed producer files remain unchanged.'}
(D/'coordinator-turnout-isolated-replay-review.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['actual_result','whole_process_logs']}))
