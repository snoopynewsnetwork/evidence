"""Lossless source retained; OCR is a separately labelled, unaccepted derivative."""
from pathlib import Path
import json,gzip,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[3];B=ROOT/'data/baselines'
def main():
 pins=json.loads((B/'source/pins.json').read_text())['pins'];roles=['2024 county recap: Elliott','sbe-2020-estill-recap-archive-20210116034430','sbe-2020-lyon-recap-archive-20210116042754']
 for role in roles:
  p=next(p for p in pins if p['role']==role);h=p['raw_sha256'];raw=gzip.decompress((ROOT/p['path']).read_bytes());d=B/'extracted'/('ocr-'+h);d.mkdir(exist_ok=True)
  with tempfile.TemporaryDirectory() as tmp:
   t=Path(tmp);subprocess.run(['pdftoppm','-r','130','-png','-',str(t/'page')],input=raw,capture_output=True,check=True)
   for img in sorted(t.glob('page-*.png')):
    out=t/(img.stem+'-ocr');r=subprocess.run(['tesseract',str(img),str(out),'txt','tsv','hocr'],capture_output=True)
    for f in t.glob(out.name+'.*'):(d/(f.name+'.gz')).write_bytes(gzip.compress(f.read_bytes(),mtime=0))
    (d/(img.stem+'.stderr.txt')).write_bytes(r.stderr)
    assert r.returncode==0
   # Contact sheets for whole-page scope inspection; PNG source renders are reproducible.
   from PIL import Image,ImageOps,ImageDraw
   imgs=sorted(t.glob('page-*.png'))
   for i in range(0,len(imgs),4):
    sheet=Image.new('RGB',(1800,2400),'white')
    for j,png in enumerate(imgs[i:i+4]):
     im=Image.open(png).convert('RGB');im.thumbnail((890,1160));x=(j%2)*900;y=(j//2)*1200;sheet.paste(im,(x,y+25));ImageDraw.Draw(sheet).text((x+8,y+5),png.stem,fill='black')
    sheet.save(B/'proof'/f'{h[:8]}-pages{i+1}-{min(i+4,len(imgs))}.png')
  print(role,'OCR scope only; unverified numerical transcription',flush=True)
if __name__=='__main__':main()
