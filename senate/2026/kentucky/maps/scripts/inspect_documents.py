from common import *
import fitz,re

def convert(x):
 if isinstance(x,dict):return {k:convert(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [convert(v) for v in x]
 if isinstance(x,(fitz.Rect,fitz.Point)):return {'native_type':type(x).__name__,'complete_coordinates':list(x)}
 return x

def main():
 inv=strict((ROOT/'documents/inventory.json').read_bytes());links=[];selected=[]
 for r in inv:
  d=fitz.open(stream=body(ROOT/r['entity']['path']),filetype='pdf');pages=[]
  for i,p in enumerate(d):
   ls=p.get_links();urls=re.findall(r'https?://[^\s<>]+',p.get_text())
   if ls or urls:pages.append({'page':i+1,'complete_link_annotations':convert(ls),'all_text_urls':urls})
  links.append({'county_label':r['county_label'],'pages':pages})
  if r['county_label'] in ['Boone','Jefferson','Scott','Cumberland','Magoffin','Montgomery','Pike','Fayette']:
   i=len(d)-1;p=d[i];path=ROOT/'proof'/f"detail-{r['county_label'].lower()}-p{i+1}.png";p.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(str(path));selected.append({'county_label':r['county_label'],'page':i+1,'path':str(path.relative_to(ROOT))})
 save(ROOT/'documents/complete-link-annotations.json',links);save(ROOT/'proof/selected-original-page-renders.json',selected)
 print('links',[(x['county_label'],p) for x in links for p in x['pages']][:10]);print('selected',selected)
if __name__=='__main__':main()
