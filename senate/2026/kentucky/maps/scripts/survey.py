from common import *
from acquire import fetch,raw
from html.parser import HTMLParser
import urllib.parse,concurrent.futures
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.cur=None
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a':self.cur={'href':d.get('href',''),'text':''}
 def handle_data(self,s):
  if self.cur is not None:self.cur['text']+=s
 def handle_endtag(self,t):
  if t=='a' and self.cur is not None:self.links.append(self.cur);self.cur=None
PARENT='https://elect.ky.gov/Resources/Pages/County-Election-Plans.aspx'
def main():
 r=fetch(PARENT,'county-plan-parent');b=raw(r);assert b
 parser=Links();parser.feed(b.decode('utf-8'));links=parser.links
 county_links=[dict(x,url=urllib.parse.urljoin(PARENT,x['href'])) for x in links if '.pdf' in x['href'].lower()]
 print('complete PDF links',len(county_links),flush=True)
 save(ROOT/'source/county-plan-links.json',{'parent_url':PARENT,'all_anchor_objects':links,'pdf_links':county_links})
 def one(x):
  rr=fetch(x['url'],'county-election-plan: '+x['text']);return dict(x,receipt_role=rr['role'],receipt=rr)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(one,county_links))
 save(ROOT/'source/county-plan-inventory.json',results)
 urls=[('https://technology.ky.gov/GIS/Pages/default.aspx','DGI-authority-parent'),('https://www.kygeonet.ky.gov/','KYGeoNet-parent'),('https://opengisdata.ky.gov/','DGI-open-data-parent'),('https://elect.ky.gov/Pages/default.aspx','SBE-parent'),('https://services3.arcgis.com/ghsX9CKghMvyYjBU/ArcGIS/rest/services/sbe_vtd_cities_260827/FeatureServer','SBE-DGI-city-overlay-service'),('https://kygisserver.ky.gov/arcgis/rest/services/GeoprocessingServices/Ky_ABC_Identify_WGS84WM/MapServer','DGI-ABC-service')]
 for u,role in urls:
  rr=fetch(u+('?f=pjson' if u.endswith(('FeatureServer','MapServer')) else ''),role)
  bb=raw(rr)
  if bb and not u.endswith(('FeatureServer','MapServer')):
   p=Links();p.feed(bb.decode('utf-8',errors='replace'));save(ROOT/'source'/f'{role}-links.json',p.links)
 for u,role in [(urls[-2][0]+'/0','SBE-DGI-city-overlay-layer'),(urls[-1][0]+'/0','DGI-ABC-VTD-layer')]:fetch(u+'?f=pjson',role)
if __name__=='__main__':main()
