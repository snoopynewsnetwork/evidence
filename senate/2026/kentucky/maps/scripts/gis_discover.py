from acquire import *
from survey import Links
import re,urllib.parse

def main():
 portal=raw(fetch('https://opengisdata.ky.gov/','DGI-open-data-parent')).decode()
 decoded=urllib.parse.unquote(portal)
 # Exact percent-encoded embedded JSON is retained in original HTML; retain full decoded meta objects.
 class Meta(Links):
  def __init__(self):super().__init__();self.meta=[]
  def handle_starttag(self,t,a):
   super().handle_starttag(t,a)
   d=dict(a)
   if t=='meta' and d.get('content','').startswith('%7B'):
    try:self.meta.append({'attributes':d,'decoded_complete_object':strict(urllib.parse.unquote(d['content']))})
    except ValueError:pass
 m=Meta();m.feed(portal);save(ROOT/'source/portal-complete-config.json',m.meta)
 for u,role in [('https://services3.arcgis.com/ghsX9CKghMvyYjBU/ArcGIS/rest/services/sbe_vtd_cities_260827/FeatureServer','SBE-DGI-city-overlay-service'),('https://kygisserver.ky.gov/arcgis/rest/services/GeoprocessingServices/Ky_ABC_Identify_WGS84WM/MapServer','DGI-ABC-service')]:
  meta=strict(raw(fetch(u+'?f=pjson',role)));item=meta.get('serviceItemId')
  if item:
   for suffix in ['', '/data']:
    fetch('https://www.arcgis.com/sharing/rest/content/items/'+item+suffix+'?f=pjson',role+'-item'+suffix.replace('/','-'))
  rr=fetch(u+'/0?f=pjson',role+'-layer');layer=strict(raw(rr));print('GIS',role,'OID',layer.get('objectIdField'), 'SR',layer.get('extent',{}).get('spatialReference'),'Z/M',layer.get('hasZ'),layer.get('hasM'),flush=True)
  for query in [{'where':'1=1','returnCountOnly':'true','f':'json'},{'where':'1=1','returnIdsOnly':'true','f':'json'}]:
   rr=fetch(u+'/0/query?'+urllib.parse.urlencode(query),role+'-initial-control');o=strict(raw(rr));print('CONTROL',role,str(o)[:1000],flush=True)
if __name__=='__main__':main()
