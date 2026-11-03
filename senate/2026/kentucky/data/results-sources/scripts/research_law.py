"""Read only explicit observed statute links; preserve all effective versions."""
import concurrent.futures,urllib.parse,re
from inspect_html import load,BASE
from capture import fetch
WANTED={'krs117-current':['.015','.022','.035','.076','.077','.085','.0851','.086','.0861','.087','.275','.305','.383','.228','.265'],'krs118-current':['.015','.025','.027','.035','.205','.215','.305','.387','.425','.125','.129','.165','.212','.315','.367'],'krs120':['.055','.095','.155','.157','.165','.185','.195']}
if __name__=='__main__':
 tasks=[]
 for label,wanted in WANTED.items():
  r,s=load(label)
  for a in s.links:
   text=a['text'].strip();m=re.match(r'\.(\d+)\s',text)
   if m and '.'+m[1] in wanted:
    u=urllib.parse.urljoin(r['hops'][-1]['url'],a['attrs']['href']);tasks.append((label+'-'+m[1]+'-'+u.rsplit('=',1)[-1],u))
 def work(t):
  label,url=t
  if (BASE/'receipts'/f'{label}.json').exists():return label,'retained'
  r=fetch(label,url);return label,r['hops'][-1]['status']
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p:
  for r in p.map(work,tasks):print(*r,flush=True)
