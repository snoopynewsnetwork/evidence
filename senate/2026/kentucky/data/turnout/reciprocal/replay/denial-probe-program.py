import os,sys,json,socket,subprocess,importlib.util
from pathlib import Path
C=json.load(open(os.environ['KY_GUARD_CONFIG']));S=Path(C['real_state']);out=[]
def attempt(label,f):
 try:f()
 except PermissionError as e:
  assert 'KY_EXERCISED_DENIAL:' in str(e);out.append({'probe':label,'denied':True,'error':str(e)})
 else:raise AssertionError('DENIAL PROBE UNEXPECTEDLY ALLOWED '+label)
attempt('network DNS/socket',lambda:socket.getaddrinfo('example.com',443))
attempt('mutable newsroom aggregate',lambda:(S/'data/news/manifest.json').read_bytes())
attempt('coordinator numerical aggregate',lambda:(S/'data/coordinator-certified-county-preflight.json').read_bytes())
attempt('peer discovery',lambda:list((S/'data/baselines').iterdir()))
attempt('current peer body',lambda:(S/'data/baselines/priority.json').read_bytes())
attempt('producer helper read',lambda:(S/'data/preflight_certified_county_vectors.py').read_bytes())
attempt('producer writer execution',lambda:subprocess.run([sys.executable,str(S/'data/baselines/scripts/build.py')]))
attempt('unapproved acquisition helper',lambda:subprocess.run(['curl','https://example.com']))
attempt('write outside temp',lambda:Path('/private/tmp/ky-denied-outside-replay-probe').write_text('must not be written'))
print(json.dumps(out,indent=2))
