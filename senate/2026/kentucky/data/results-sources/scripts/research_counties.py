"""Bounded office-site research from the complete official directory only."""
import concurrent.futures,json,urllib.parse,pathlib,gzip,sys
from public_lists import atom,element,NS
from inspect_html import BASE,HTML,load
from capture import fetch

def slug(s):return ''.join(c.lower() if c.isalnum() else '-' for c in s)
def plan():
 root,rows=atom('directory-roles');assert len(set(x['County'] for x in rows))==120
 return sorted(set(x['OData__x0067_295'] for x in rows if x.get('OData__x0067_295') and x['OData__x0067_295'].startswith(('http:','https:'))))
def capture_one(t):
 label,url=t;p=BASE/'receipts'/f'{label}.json'
 if p.exists():return label,'retained'
 r=fetch(label,url);return label,r['hops'][-1]['status']
def office_tasks():return [('office-'+str(i+1).zfill(3),u) for i,u in enumerate(plan())]
def candidates(label,stage):
 r,s=load(label);h=r['hops'][-1]
 if h['status']!=200:return []
 base=h['url'];links=[]
 for a in s.links:
  href=a['attrs'].get('href','')
  if not isinstance(href,str):continue
  url=urllib.parse.urljoin(base,href);words=(a['text']+' '+href).lower()
  if not url.startswith(('http:','https:')) or url==base or href.startswith(('#','mailto:','tel:')):continue
  if any(q in url.lower() for q in ['facebook','twitter','instagram','youtube','linkedin']):continue
  if stage==1:
   score=4*('result' in words)+2*('election' in words)+('voting' in words)
  else:score=5*('result' in words)+2*('2026' in words)+('general' in words)
  if score>=2 and not any(q in words for q in ['contact','request','register','registration','forms','filing','officer','location','calendar','ballot-request']):links.append((score,url,a))
 links.sort(key=lambda x:(-x[0],x[1]));return links
if __name__=='__main__':
 stage=int(sys.argv[1]);tasks=office_tasks()
 if stage>0:
  nexttasks=[]
  for label,url in tasks:
   current=label if stage==1 else label+'-elections'
   if not (BASE/'receipts'/f'{current}.json').exists():continue
   r=json.loads((BASE/'receipts'/f'{current}.json').read_bytes())
   if r['hops'][-1]['response_body'] is None:continue
   r,s=load(current)
   choices=candidates(current,stage)
   if choices:nexttasks.append((label+('-elections' if stage==1 else '-results'),choices[0][1]))
  tasks=nexttasks
 print('bounded tasks',len(tasks),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for answer in pool.map(capture_one,tasks):print(*answer,flush=True)
