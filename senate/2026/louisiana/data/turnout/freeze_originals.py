"""One-time recovery of complete original entities; replay never reads the news ledger."""
from pathlib import Path
import gzip, hashlib, json, datetime

ROOT = Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    news = ROOT.parent / 'news'
    ledger = json.loads((news/'manifest.json').read_bytes())
    pins = []
    for r in ledger:
        if not (r['id'].startswith('sos-') or r['id']=='governor-house-suspension'): continue
        if r['id']=='sos-media-public-example': continue  # no restricted interface used
        stored = (news/r['asset']).read_bytes()
        raw = gzip.decompress(stored)
        assert sha(stored)==r['stored_sha256'] and sha(raw)==r['raw_sha256'] and len(raw)==r['bytes']
        body = ROOT/'source'/f"{sha(raw)}.body.gz"
        if not body.exists(): body.write_bytes(gzip.compress(raw,mtime=0))
        receipt = dict(r)
        receipt.update(original_asset_readonly=str((news/r['asset']).relative_to(ROOT.parent.parent)),
                       original_stored_sha256=r['stored_sha256'],
                       asset=str(body.relative_to(ROOT)),stored_sha256=sha(body.read_bytes()),
                       redirect_history_scope='Legacy receipt preserves final entity and final headers only; intermediate redirect response entities unavailable.',
                       receipt_scope='Complete copied individual recovery receipt, not adoption of prepared counts')
        rp=ROOT/'source'/(r['id']+'.receipt.json')
        rp.write_text(json.dumps(receipt,indent=2)+'\n')
        pins.append(dict(id=r['id'],receipt=str(rp.relative_to(ROOT)),receipt_sha256=sha(rp.read_bytes()),
                         body=str(body.relative_to(ROOT)),raw_sha256=sha(raw),bytes=len(raw),stored_sha256=sha(body.read_bytes())))
    out=ROOT/'source'/'original-pins.json'
    assert not out.exists(), 'Do not replace an original freeze'
    out.write_text(json.dumps({'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                              'inputs':pins,'numerical_derivatives_read':False,'peer_agent_id':None},indent=2)+'\n')
    print(len(pins),'complete original entities pinned')
if __name__=='__main__': main()
