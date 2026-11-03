from acquire import *
import urllib.parse

def main():
 u='https://kygisserver.ky.gov/arcgis/rest/services/GeoprocessingServices/Ky_ABC_Identify_WGS84WM/MapServer'
 probes=[]
 for method in ['GET','POST']:
  query={'where':'1=1','objectIds':'1','outFields':'*','returnGeometry':'true','returnZ':'true','returnM':'true','returnTrueCurves':'true','f':'json'};b=urllib.parse.urlencode(query).encode()
  r=fetch(u+'/0/query'+('?'+b.decode() if method=='GET' else ''),'DGI-bounded-full-field-single-ID-diagnostic',method=method,payload=b if method=='POST' else None,headers={'Content-Type':'application/x-www-form-urlencoded'} if method=='POST' else None);probes.append(r)
  print(method,raw(r),flush=True)
 after={}
 for k,url in [('service',u+'?f=pjson'),('layer',u+'/0?f=pjson'),('count',u+'/0/query?'+urllib.parse.urlencode({'where':'1=1','returnCountOnly':'true','f':'json'})),('ids',u+'/0/query?'+urllib.parse.urlencode({'where':'1=1','returnIdsOnly':'true','f':'json'}))]:after[k]=fetch(url,'DGI-failure-after-'+k,observation='dgi-failure-after')
 failures=[]
 for p in sorted((ROOT/'source/receipts').glob('*.json')):
  r=strict(p.read_bytes())
  if r['role'].startswith('dgi-vtd-batch-'):failures.append(r)
 save(ROOT/'source/dgi-vtd-unavailable.json',{'status':'Complete geometry unavailable from observed source. HTTP200 JSON errors are failures, never geometry.','all_failed_batch_attempts':failures,'bounded_diagnostic_probes':probes,'after_controls':after,'full_native_geometries_acquired':False,'no_simplification_or_repair':True})
if __name__=='__main__':main()
