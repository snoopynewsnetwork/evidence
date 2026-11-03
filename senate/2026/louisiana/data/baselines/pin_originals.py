"""One-time original preparation. Final replay uses pinned receipts only, never news ledger."""
import gzip,hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent; N=D.parent/'news'
h=lambda b:hashlib.sha256(b).hexdigest()
receipts=[]
for r in json.loads((N/'manifest.json').read_text()):
 if not r['id'].startswith(('sos-','governor-')):continue
 if r['id']=='sos-media-public-example':continue
 b=(N/r['asset']).read_bytes();raw=gzip.decompress(b)
 assert h(b)==r['stored_sha256'] and h(raw)==r['raw_sha256'] and len(raw)==r['bytes']
 r=dict(r,reference_path=str((N/r['asset']).relative_to(D.parents[4])),stored_bytes=len(b),redirect_scope='Receipt retains final entity/headers only; intermediate redirect entities unknown')
 receipts.append(r)
(D/'source/receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
