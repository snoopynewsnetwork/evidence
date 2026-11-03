from acquire import *
import concurrent.futures,urllib.parse
SERVICES=[('sbe-city-overlay','https://services3.arcgis.com/ghsX9CKghMvyYjBU/ArcGIS/rest/services/sbe_vtd_cities_260827/FeatureServer'),('dgi-vtd','https://kygisserver.ky.gov/arcgis/rest/services/GeoprocessingServices/Ky_ABC_Identify_WGS84WM/MapServer')]
def main():
 allsets=[]
 for name,u in SERVICES:
  controls={}
  def control(phase):
   rr={}
   for k,url in [('service',u+'?f=pjson'),('layer',u+'/0?f=pjson'),('count',u+'/0/query?'+urllib.parse.urlencode({'where':'1=1','returnCountOnly':'true','f':'json'})),('ids',u+'/0/query?'+urllib.parse.urlencode({'where':'1=1','returnIdsOnly':'true','f':'json'}))]:
    rr[k]=fetch(url,name+'-'+phase+'-'+k,observation=name+'-'+phase)
   controls[phase]=rr;return {k:strict(raw(v)) for k,v in rr.items()}
  before=control('before');ids=before['ids']['objectIds'];oid=before['ids']['objectIdFieldName'];assert len(ids)==len(set(ids))==before['count']['count'];requested=sorted(ids)
  batches=[requested[i:i+50] for i in range(0,len(requested),50)]
  def batch(arg):
   i,ids=arg;query={'objectIds':','.join(map(str,ids)),'outFields':'*','returnGeometry':'true','returnZ':'true','returnM':'true','returnTrueCurves':'true','f':'json'}
   rr=fetch(u+'/0/query?'+urllib.parse.urlencode(query),name+'-batch-'+str(i));b=raw(rr);x=strict(b);assert 'error' not in x, x
   fs=x['features'];returned=[f['attributes'][oid] for f in fs];assert len(returned)==len(set(returned))==len(ids) and set(returned)==set(ids),(name,i,ids,returned);assert not x.get('exceededTransferLimit',False)
   fields={f['name'] for f in before['layer']['fields']}
   for f in fs:assert set(f['attributes'])==fields,(name,'missing/full attributes',set(f['attributes'])^fields)
   return {'batch':i,'requested_ids':ids,'returned_ids_in_source_order':returned,'response':rr,'spatial_reference':x.get('spatialReference'),'feature_count':len(fs),'hasZ':x.get('hasZ'),'hasM':x.get('hasM')}
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(batch,enumerate(batches)))
  after=control('after');assert after['count']==before['count'];assert set(after['ids']['objectIds'])==set(ids) and after['ids']['objectIdFieldName']==oid
  result={'name':name,'url':u,'controls':controls,'batches':results,'object_id_field':oid,'total_features':len(ids),'before_after_ids_equal':True,'before_after_complete_layer_metadata_equal':before['layer']==after['layer'],'before_after_complete_service_metadata_equal':before['service']==after['service'],'input_constraints':'All observed IDs; disjoint <=50-ID requests; full attributes; no offset/outSR/precision/generalization/quantization. Preserve truecurves/Z/M/null geometries. No legal/result join approved.'}
  save(ROOT/'source'/f'{name}-complete-index.json',result);allsets.append({'name':name,'count':len(ids),'batches':len(batches)});print('COMPLETE',name,len(ids),flush=True)
 save(ROOT/'proof/gis-acquisition-summary.json',allsets)
if __name__=='__main__':main()
