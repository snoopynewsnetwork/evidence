"""Restore prose word spacing while preserving code, hashes and link targets."""
import re,sys
from pathlib import Path
WORDS=set('Elliott Estill JSON McConnell Paul Senate actual additional all and as ballot below boundary candidate cannot captured certificate complete contest contexts counties county crossing descending despite expected forecast have headers historical image in independently individual marks match named native net observations on originals page pages pair parent parents pinned positive pp preferences president presidential recap recaps registration regular request requires results saved scanned selected source stable state supply turnout volume volumes weights witness zero'.split())
BEFORE=set('observed All is no The SBE in won and complete its calibrated minimum December all every each top A B only both remaining generic named Report from of prior return requires with each November September October'.split())
def format_text(s):
 parts=re.split(r'(`[^`]*`|\]\([^)]*\)|https?://[^\s)]+)',s)
 for i in range(0,len(parts),2):
  p=parts[i];p=re.sub(r'(\d)([A-Za-z]+)',lambda m:m[1]+' '+m[2] if m[2] in WORDS else m[0],p)
  p=re.sub(r'\b([A-Za-z]+)(\d)',lambda m:m[1]+' '+m[2] if m[1] in BEFORE else m[0],p)
  p=re.sub(r'\b([A-Za-z]{2,})(?=\d)',lambda m:m[0]+' ' if re.search(r'[g-zG-Z]',m[0]) and m[0] not in ('sha','SHA','UTF','MD') else m[0],p)
  p=re.sub(r',(?=202[0246]\b)',', ',p)
  p=re.sub(r'\b(all|every|each|top|A|B)(?=\d)',r'\1 ',p)
  p=p.replace('ClassIIseat','Class II seat').replace('ClassIIIseat','Class III seat')
  p=p.replace('20historical','20 historical').replace('2024page','2024 page').replace('0 for','0 for')
  parts[i]=p
 return ''.join(parts)
if __name__=='__main__':
 for name in sys.argv[1:]:
  p=Path(name);p.write_text(format_text(p.read_text()))
