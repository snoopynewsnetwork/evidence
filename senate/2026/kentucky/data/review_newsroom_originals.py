"""Coordinator retained Kentucky newsroom/primary-source entity audit; no fetch."""
from pathlib import Path
import gzip,hashlib,json,sys
S=Path(__file__).resolve().parents[1];D=S/'data';R=D/'news'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)}
outpath=D/'coordinator-newsroom-original-review.json'
rs=[r['complete_receipt'] for r in json.loads(outpath.read_bytes())['complete_individual_receipts_and_body_pins']] if '--check' in sys.argv else json.loads((R/'manifest.json').read_bytes());assert len(rs)==35
bodies={};pins=[]
for r in rs:
 p=R/r['asset'];z=p.read_bytes();b=gzip.decompress(z);assert sha(z)==r['stored_sha256'] and sha(b)==r['raw_sha256'] and len(b)==r['bytes'] and len(z)<40000000
 bodies[r['id']]=b;pins.append({'complete_receipt':r,'stored_body':pin(p),'complete_raw_bytes':len(b),'complete_raw_sha256':sha(b)})
t=bodies['wkyt-results'].decode();start=t.index('Fusion.contentCache=')+len('Fusion.contentCache=');cache,n=json.JSONDecoder().raw_decode(t[start:]);items=cache['gsync-elections'];assert len(items)==1;q=next(iter(items));params=json.loads(q);assert params=={'arc-site':'wkyt','includeTestResults':False};d=items[q]['data'];e=d['selectedElection'];assert e['id']=='2361' and e['name']=='Primary 2026' and not e['isActive'];races=e['races'];assert len(races)==194;choices=[c for r in races for c in r['candidates']];assert len(choices)==648 and any(c['votes']>0 for c in choices);senate=[r for r in races if r['name'].startswith('U.S. Senate')];assert len(senate)==2 and all('Estimated 99%' in r['reportingInfo'] for r in senate);assert '\"displayTestData\":true' in t
product={'original_HTML':next(r['stored_body'] for r in pins if r['complete_receipt']['id']=='wkyt-results'),'complete_cache_raw_character_span':[start,start+n],'cache_semantic_sha256':sha(canon(cache)),'complete_cache':cache,'actual_backend_parameters':params,'separate_UI_displayTestData':True,'scope':'Inactive primary counts only. Estimated99% is not exact remaining votes. No November returns/roster/currentID/admission.'}
p=D/'coordinator-newsroom-wkyt-complete-cache.json.gz';b=gzip.compress((json.dumps(product,ensure_ascii=False,indent=2)+'\n').encode(),mtime=0)
if '--check' in sys.argv:assert p.read_bytes()==b
elif p.exists():assert p.read_bytes()==b
else:p.write_bytes(b)
assert b'73761/28480.html' in bodies['ket-election'];assert next(r for r in rs if r['id']=='ket-primary-ap')['status']==403;assert next(r for r in rs if r['id']=='nyt-elections')['status']==403
result={'status':'pass_complete_retained_Kentucky_news_primary_and_archived_original_entities','complete_legacy_observations':35,'complete_individual_receipts_and_body_pins':pins,'WKYT':{'selected_id':'2361','selected_name':e['name'],'active':False,'races':194,'choices':648,'complete_Senate_primary_objects':senate,'publisher_updatedDate':e['updatedDate'],'dataTransformedAt':e['dataTransformedAt'],'backend_includeTestResults':False,'separate_UI_displayTestData':True,'complete_cache':pin(p)},'KET':'Actual AP73761/layout28480 iframe from primary election hub; sample403; November source/cadence unverified.','NYT':'Direct403 retained; exact November Senate product/access/cadence unverified, manual fallback.','archive_scope':'Official historical county canvass and two observed recap originals retained through literal Wayback source URLs; direct403/errors and every archived version remain separate. These are immutable original-source leads for future independent extraction, not accepted native completeness/current geometry.','provenance_limit':'Legacy complete entity/finalURL/status/headers/UTC retained; full intermediate redirects or wire/TLS framing not claimed. Later regional WBKO/WYMT pack has complete separate hops/objects.','question_workers_launched':False,'November_votes_IDs_legal_geography_pool_cadence_collector_or_probability_admission':False}
b=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
if '--check' in sys.argv:assert outpath.read_bytes()==b
else:outpath.write_bytes(b)
print(json.dumps({'status':result['status'],'complete_entities':35,'primary_races':194,'primary_choices':648,'November_admitted':False}))
