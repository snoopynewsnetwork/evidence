#!/usr/bin/env python3
import sys,json,gzip,urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from acquire import fetch,ROOT
class Links(HTMLParser):
 def __init__(self): super().__init__();self.links=[];self.href=None;self.label=''
 def handle_starttag(self,t,a):
  if t=='a':self.href=dict(a).get('href');self.label=''
 def handle_data(self,d):
  if self.href:self.label+=d
 def handle_endtag(self,t):
  if t=='a' and self.href:self.links.append((self.label.strip(),self.href));self.href=None
parents=[('2024-recaps','https://elect.ky.gov/results/2020-2029/Pages/2024General-Recap-Sheets.aspx'),('turnout-index','https://elect.ky.gov/Resources/Pages/Turnout.aspx'),('registration-index','https://elect.ky.gov/Resources/Pages/Registration-Statistics.aspx')]
plan=[]
for label,url in parents:
 rec,b=fetch(url,label);p=Links();p.feed(b.decode(errors='replace'))
 for text,href in p.links:
  full=urllib.parse.urljoin(url,href)
  if label=='2024-recaps' and '/GeneralRecaps/' in href:plan.append({'label':text,'url':full,'role':'2024 county recap','parent':url})
  if label=='turnout-index' and ('2024G' in href or '2022G' in href or '2020G' in href) and ('county' in href.lower() or 'precinct' in href.lower()):plan.append({'label':text,'url':full,'role':'unofficial turnout sensitivity','parent':url})
  if label=='registration-index' and ('General%202024' in href or 'General 2024' in href or 'General%202022' in href or 'General 2022' in href or 'General%202020' in href or 'General 2020' in href) and ('county' in href.lower() or 'precinct' in href.lower()):plan.append({'label':text,'url':full,'role':'general registration sensitivity','parent':url})
(ROOT/'source/acquisition-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
# bounded: each actual indexed link once; no guessed API or private source.
for item in plan:
 fetch(item['url'],item['role']+': '+item['label'],item['parent'])
