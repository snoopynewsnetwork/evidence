"""Freeze individual receipts and bodies once, after bounded acquisition; no count import."""
from pathlib import Path
import datetime,gzip,hashlib,json
ROOT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    files=[];positions=[]
    for p in sorted((ROOT/'source').glob('*.*.receipt.json')):
        b=p.read_bytes();r=json.loads(b)
        pin={'receipt':str(p.relative_to(ROOT)),'receipt_sha256':sha(b),'id':r['id'],'status':r.get('status'),'complete_entity':r['complete_entity']}
        if r.get('complete_entity'):
            sb=(ROOT/r['body']).read_bytes();raw=gzip.decompress(sb)
            assert sha(sb)==r['stored_sha256'] and sha(raw)==r['raw_sha256'] and len(raw)==r['bytes']
            pin.update(body=r['body'],raw_sha256=sha(raw),bytes=len(raw),stored_sha256=sha(sb))
            try:
                obj=json.loads(raw)
                positions.append({'id':r['id'],'receipt':pin['receipt'],'raw_sha256':sha(raw),'whole_json':obj})
            except (ValueError,UnicodeDecodeError):pass
        files.append(pin)
    p=ROOT/'source/acquired-pins.json';assert not p.exists()
    p.write_text(json.dumps({'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':files},indent=2)+'\n')
    raw=(json.dumps(positions,ensure_ascii=False,separators=(',',':'))+'\n').encode()
    q=ROOT/'extract/acquired-whole-json-witness.json.gz';q.write_bytes(gzip.compress(raw,mtime=0))
    (ROOT/'source/acquired-original-first-witness.json').write_text(json.dumps({'pins_sha256':sha(p.read_bytes()),'whole_json_path':str(q.relative_to(ROOT)),'whole_json_sha256':sha(q.read_bytes()),'phase':'whole original source bodies and complete JSON structures before peer derivatives'},indent=2)+'\n')
    print(len(files),'receipts frozen;',len(positions),'complete JSON entities')
if __name__=='__main__':main()
