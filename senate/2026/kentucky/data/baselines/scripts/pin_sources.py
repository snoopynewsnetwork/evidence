"""One-time individual-receipt capture; no peer numerical derivatives read."""
from pathlib import Path
import gzip, hashlib, json, datetime
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'data/baselines'
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    target=OUT/'source/pins.json'
    if target.exists(): raise SystemExit('Pins already frozen; use read-only verification.')
    pins=[]
    for f in sorted((ROOT/'data/turnout/source/receipts').glob('*.json')):
        rb=f.read_bytes(); r=json.loads(rb)
        # Acquisition receipts only, never extract/rank/script data.
        dest=OUT/'source/receipts'/f.name; dest.write_bytes(rb)
        hops=r.get('hops')
        if hops is None:
            hops=[dict(r,body='data/news/'+r['asset'])]
        for i,h in enumerate(hops):
            body=h.get('body')
            if not body: continue
            p=ROOT/body if body.startswith('data/') else ROOT/'data/turnout'/body
            stored=p.read_bytes(); raw=gzip.decompress(stored)
            assert sha(raw)==h['raw_sha256'],p
            assert sha(stored)==h['stored_sha256'],p
            assert len(stored)<40000000,p
            pins.append(dict(receipt=str(dest.relative_to(ROOT)),receipt_sha256=sha(rb),hop=i,
                path=str(p.relative_to(ROOT)),raw_sha256=sha(raw),stored_sha256=sha(stored),
                raw_bytes=len(raw),stored_bytes=len(stored),role=r.get('role',r.get('id')),
                url=h.get('url',r.get('requested_url',r.get('url'))),status=h.get('status'),
                magic=raw[:16].hex()))
    target.write_text(json.dumps(dict(captured_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        boundary='Only complete individual HTTP receipts and original bodies; no peer extracts, ranking, parser, controls or diagnostic tables read.',pins=pins),indent=2)+'\n')
    print('Pinned',len(pins),'individual body roles')
if __name__=='__main__': main()
