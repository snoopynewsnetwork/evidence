from common import *
import fitz,concurrent.futures
from PIL import Image,ImageOps,ImageDraw

def main():
 inv=strict((ROOT/'source/county-plan-inventory.json').read_bytes())
 def render(x):
  h=x['receipt']['hops'][-1];result={'county_label':x['text'],'url':x['url'],'response_status':h['status'],'entity':h.get('entity'),'pages':[],'scope':'Published 2026 primary county election plan. Not independently certified November geographic/reporting crosswalk.'}
  if not h.get('entity'):return result
  b=body(ROOT/h['entity']['path'])
  if not b.startswith(b'%PDF'):result['pdf_available']=False;return result
  result['pdf_available']=True;doc=fitz.open(stream=b,filetype='pdf');result['pdf_metadata']=doc.metadata;result['pdf_pages']=len(doc)
  out=ROOT/'documents'/h['entity']['raw_sha256'];out.mkdir(parents=True,exist_ok=True)
  texts=[]
  for i,page in enumerate(doc):
   # Complete page, no clipping/cropping/rotation/OCR repair. Small preview is a derivative.
   pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
   png=out/f'page-{i+1:04d}.png';pix.save(str(png));assert png.stat().st_size<40000000
   text=page.get_text(sort=False);texts.append(text)
   result['pages'].append({'page':i+1,'render':str(png.relative_to(ROOT)),'width':pix.width,'height':pix.height,'pdf_rect':list(page.rect),'pdf_rotation':page.rotation,'text_characters':len(text),'printed_map_word':bool(__import__('re').search(r'\b(map|boundary|boundaries|precincts)\b',text,__import__('re').I))})
  tb='\f'.join(texts).encode();(out/'complete-text.txt.gz').write_bytes(gzip.compress(tb,mtime=0));result['complete_text']=str((out/'complete-text.txt.gz').relative_to(ROOT));result['rendered_pages']=len(result['pages']);print(x['text'],len(doc),flush=True);return result
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(render,inv))
 save(ROOT/'documents/inventory.json',results)
 thumbs=[]
 for r in results:
  if not r['pages']:continue
  p=r['pages'][-1];im=Image.open(ROOT/p['render']).convert('RGB');im.thumbnail((220,260));tile=Image.new('RGB',(240,290),'white');tile.paste(im,((240-im.width)//2,20));ImageDraw.Draw(tile).text((5,275),r['county_label']+' p'+str(p['page']),fill='black');thumbs.append(tile)
 for start in range(0,len(thumbs),30):
  ims=thumbs[start:start+30];sheet=Image.new('RGB',(1440,290*((len(ims)+5)//6)),'#dddddd')
  for j,im in enumerate(ims):sheet.paste(im,((j%6)*240,(j//6)*290))
  sheet.save(ROOT/f'proof/plan-contact-{start//30+1}.jpg',quality=88)
 print('TOTAL',len(results),sum(r.get('pdf_pages',0) for r in results),flush=True)
if __name__=='__main__':main()
