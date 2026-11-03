#!/usr/bin/env python3
"""Reproduce certificate selected first/final table-page images from exact raw originals."""
import gzip,json,tempfile,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R.parents[1]
refs=json.load(open(R/'source/refs.json'))
for prefix,pages in [('69f32',[2,7]),('46b46',[2,6]),('66bb0',[8,10])]:
 z=next(x for x in refs if x['raw_sha256'].startswith(prefix))
 with tempfile.TemporaryDirectory(dir=R) as td:
  p=Path(td)/'original.pdf';p.write_bytes(gzip.decompress((S/z['path']).read_bytes()))
  for page in pages:
   result=subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','2400','-png',str(p),str(R/'proof'/f'certificate-{prefix}-page{page}')],capture_output=True)
   (R/'proof'/f'certificate-{prefix}-page{page}.render-receipt.json').write_text(json.dumps({'input_raw_sha256':z['raw_sha256'],'page':page,'returncode':result.returncode,'stdout':result.stdout.decode(errors='replace'),'stderr':result.stderr.decode(errors='replace')},indent=2)+'\n')
   result.check_returncode()
