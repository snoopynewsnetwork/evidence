import concurrent.futures,urllib.parse
from inspect_html import load,BASE
from capture import fetch
if __name__=='__main__':
 r,s=load('ballot-index');tasks=[]
 for n,a in enumerate(s.links):
  u=a['attrs'].get('href','')
  if '/ballots/' in u and '2026G' in u:tasks.append(('specimen-'+str(n).zfill(3),urllib.parse.quote(u,safe=':/%?=&')))
 print('observed whole specimens',len(tasks),flush=True)
 def work(t):
  label,url=t
  if (BASE/'receipts'/f'{label}.json').exists():return label,'retained'
  r=fetch(label,url);return label,r['hops'][-1]['status']
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for x in pool.map(work,tasks):print(*x,flush=True)
