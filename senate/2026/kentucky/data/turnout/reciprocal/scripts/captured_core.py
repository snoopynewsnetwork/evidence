"""Strict captured whole-body reader. No producer import, network, discovery or mutable peer read."""
import json,gzip,hashlib
from pathlib import Path
STATE=Path(__file__).resolve().parents[4]
ROOT=STATE/'data/turnout/reciprocal'
def sha(b):return hashlib.sha256(b).hexdigest()
class Capture:
 def __init__(self,name):
  self.index_path=ROOT/name/'index.json';self.index=json.loads(self.index_path.read_bytes());self.entries={z['path']:z for z in self.index['files']}
 def body(self,path):
  z=self.entries[path]
  if 'captured_body' in z:
   b=(STATE/z['captured_body']).read_bytes();assert sha(b)==z['captured_stored_sha256'];b=gzip.decompress(b)
  else:
   ref=z.get('immutable_whole_reference',z.get('immutable_original_reference'));assert ref is not None;b=(STATE/ref).read_bytes()
  assert sha(b)==z['sha256'] and len(b)==z['bytes'],path
  return b
 def json(self,path):return json.loads(self.body(path))
 def jsonl(self,path):
  b=self.body(path);b=gzip.decompress(b) if path.endswith('.gz') else b
  return [json.loads(z) for z in b.decode().splitlines()]
 def verify_all(self):
  for p in self.entries:self.body(p)
  return len(self.entries)
