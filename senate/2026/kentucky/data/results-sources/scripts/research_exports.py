import xml.etree.ElementTree as ET,gzip,concurrent.futures
from inspect_html import BASE,load
from public_lists import NS
from capture import fetch
if __name__=='__main__':
 r,_=load('reports-2026-files');root=ET.fromstring(gzip.decompress((BASE/r['hops'][-1]['response_body']['path']).read_bytes()));tasks=[]
 for p in root.findall('.//m:properties',NS):
  d={x.tag.rsplit('}',1)[-1]:x.text for x in p}
  if d.get('Name','').endswith('.csv') and d.get('ServerRelativeUrl'):
   tasks.append(('export-'+d['Name'].rsplit('.',1)[0].lower(),'https://elect.ky.gov'+d['ServerRelativeUrl']))
 def work(t):
  label,url=t
  if (BASE/'receipts'/f'{label}.json').exists():return label,'retained'
  r=fetch(label,url);return label,r['hops'][-1]['status']
 print('whole published CSV exports',len(tasks),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for x in pool.map(work,tasks):print(*x,flush=True)
