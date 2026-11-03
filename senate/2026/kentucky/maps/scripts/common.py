import json,hashlib,gzip,pathlib,csv,io
STATE=pathlib.Path(__file__).resolve().parents[2]
ROOT=STATE/'maps'
AUTH=STATE/'data/coordinator-source-research-acceptance.json'
def pairs(ps):
 d={}
 for k,v in ps:
  if k in d:raise ValueError('duplicate JSON key '+k)
  d[k]=v
 return d
def strict(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sem(x):return sha(canonical(x))
def save(p,o):
 p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);b=json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False).encode()+b'\n';assert len(b)<40000000;p.write_bytes(b)
def body(p):
 b=p.read_bytes();return gzip.decompress(b) if p.suffix=='.gz' else b
def structured(p,fmt=None):
 b=body(p)
 if fmt=='csv_full_header_and_rows' or p.suffix=='.csv':return list(csv.reader(io.StringIO(b.decode('utf-8'))))
 if fmt=='jsonl_full_ordered_array' or '.jsonl' in p.name:return [strict(x) for x in b.splitlines() if x.strip()]
 return strict(b)
