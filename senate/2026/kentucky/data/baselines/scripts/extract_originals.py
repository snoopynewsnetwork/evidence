"""Independent whole-byte extraction. Never imports another worker's parser/data."""
from pathlib import Path
import json,gzip,hashlib,subprocess,re
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'data/baselines'
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    pins=json.loads((OUT/'source/pins.json').read_text())['pins']; done={}; rows=[]
    for pin in pins:
        h=pin['raw_sha256']
        if h in done: continue
        raw=gzip.decompress((ROOT/pin['path']).read_bytes()); assert sha(raw)==h
        if not raw.startswith(b'%PDF'): continue
        info=subprocess.run(['pdfinfo','-'],input=raw,capture_output=True,check=True).stdout
        layout=subprocess.run(['pdftotext','-layout','-','-'],input=raw,capture_output=True,check=True)
        bbox=subprocess.run(['pdftotext','-bbox-layout','-','-'],input=raw,capture_output=True)
        for kind,b in [('layout.txt',layout.stdout),('bbox.html',bbox.stdout),('pdfinfo.txt',info),('poppler-stderr.txt',layout.stderr+bbox.stderr)]:
            stored=gzip.compress(b,mtime=0); assert len(stored)<40000000
            (OUT/'extracted'/f'{h}.{kind}.gz').write_bytes(stored)
        pages=layout.stdout.decode().split('\f'); n=int(re.search(rb'Pages:\s+(\d+)',info)[1]); assert len(pages)-1==n
        rec=dict(raw_sha256=h,pages=n,layout_sha256=sha(layout.stdout),bbox_sha256=sha(bbox.stdout),bbox_exit=bbox.returncode,role=pin['role'],
            text_pages=sum(bool(p.strip()) for p in pages),image_only_pages=[i+1 for i,p in enumerate(pages[:n]) if not p.strip()])
        done[h]=rec; print(pin['role'],n,flush=True)
    (OUT/'extracted/document-inventory.json').write_text(json.dumps(list(done.values()),indent=2)+'\n')
if __name__=='__main__':main()
