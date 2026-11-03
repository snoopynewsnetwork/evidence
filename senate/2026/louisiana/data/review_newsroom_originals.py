"""Retained-byte coordinator preparation only; no acquisition or live admission."""
from pathlib import Path
from html.parser import HTMLParser
import gzip,hashlib,json,sys
S=Path(__file__).resolve().parents[1];D=S/'data';R=D/'news';OUT=D/'coordinator-newsroom-original-review.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)}
class Iframes(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.frames=[]
 def handle_starttag(self,t,a):
  if t=='iframe':self.frames.append(dict(a))
old=json.loads(OUT.read_bytes()) if '--check' in sys.argv else None
receipts=[r['complete_receipt'] for r in old['complete_individual_receipts_and_body_pins']] if old else json.loads((R/'manifest.json').read_bytes())
pins=[];setups=[];iframes=[];errors=[]
for r in receipts:
 if not r.get('asset'):
  assert r.get('error') or r.get('requests_error');errors.append({'complete_receipt':r,'scope':'No complete entity/status/header is invented for transport error.'});continue
 p=R/r['asset'];stored=p.read_bytes();raw=gzip.decompress(stored);assert len(stored)<40000000 and sha(stored)==r['stored_sha256'] and sha(raw)==r['raw_sha256'] and len(raw)==r['bytes']
 pins.append({'complete_receipt':r,'stored_body':pin(p),'complete_raw_bytes':len(raw),'complete_raw_sha256':sha(raw)})
 if b'<iframe' in raw.lower():
  parser=Iframes();parser.feed(raw.decode('utf-8',errors='replace'));ap=[f for f in parser.frames if 'apelections.org' in f.get('src','')]
  if ap:iframes.append({'source_id':r['id'],'actual_literal_AP_iframe_attributes':ap,'scope':'Actual source embedding only; not fresh November product or accessible-count claim.'})
 if b'Fusion.contentCache=' not in raw:continue
 text=raw.decode('utf-8',errors='strict');start=text.index('Fusion.contentCache=')+len('Fusion.contentCache=');cache,length=json.JSONDecoder().raw_decode(text[start:])
 if 'gsync-elections' not in cache:continue
 entries=[]
 for query,payload in cache['gsync-elections'].items():
  params=json.loads(query);data=payload['data'];e=data.get('selectedElection') if isinstance(data,dict) else None;races=(e.get('races') or []) if e else [];choices=[c for v in races for c in (v.get('candidates') or [])]
  entries.append({'actual_backend_parameters':params,'selected_id':e.get('id') if e else None,'selected_name':e.get('name') if e else None,'selected_isActive':e.get('isActive') if e else None,'selected_race_count':len(races),'selected_candidate_object_count':len(choices),'all_selected_candidate_values_zero':all(c.get('votes')==0 for c in choices) if choices else None,'literal_updatedDate':e.get('updatedDate') if e else None,'literal_dataTransformedAt':e.get('dataTransformedAt') if e else None,'complete_listed_elections':data.get('elections') if isinstance(data,dict) else None,'complete_Senate_named_objects':[v for v in races if 'senat' in v.get('name','').lower()]})
 full={'original_HTML':pin(p),'complete_cache_raw_character_span':[start,start+length],'cache_semantic_sha256':sha(canon(cache)),'complete_cache':cache,'scope':'Whole retained cache, no execution, source count adoption, current roster/ID/election admission.'}
 q=D/('coordinator-newsroom-'+r['id']+'-complete-cache.json.gz');b=gzip.compress((json.dumps(full,ensure_ascii=False,indent=2)+'\n').encode(),mtime=0)
 if '--check' in sys.argv:assert q.read_bytes()==b
 elif q.exists():assert q.read_bytes()==b
 else:q.write_bytes(b)
 setups.append({'source_id':r['id'],'source_url':r['url'],'complete_cache_derivative':pin(q),'literal_UI_displayTestData_true_present':'"displayTestData":true' in text,'literal_UI_displayTestData_false_present':'"displayTestData":false' in text,'actual_cache_entries':entries,'scope':'Frontend flags and backend parameters distinct; selected name/clocks/counts describe retained source only, not November certification/current source availability.'})
result={'status':'pass_complete_retained_entities_and_literal_news_product_scopes_preparation_only','state':S.name,'complete_legacy_observations':len(receipts),'complete_individual_receipts_and_body_pins':pins,'complete_no_entity_failure_receipts':errors,'whole_GSync_cache_products':setups,'actual_AP_iframe_observations':iframes,'provenance_limit':'Legacy complete response entity/final URL/status/finalheaders/retrieval UTC only, no invented intermediate redirect bodies/headers/TLS wire framing. Individual receipts frozen here; check mode does not rediscover a mutable aggregate.','question_workers_launched':False,'scope':'Coordinator preparation, not historical/current numerical acceptance. Official archived PDF/CSV/OOXML/JSON originals in this ledger remain source leads for future independent original-first workers. No new fetch/auth/challenge action, browser render, supplier-independence claim, November votes/current IDs/legal/geometry/cadence/eligible pool/collector/forecast/calibration approval.'}
b=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
if '--check' in sys.argv:assert OUT.read_bytes()==b
else:OUT.write_bytes(b)
print(json.dumps({'status':result['status'],'state':S.name,'complete_entities':len(pins),'no_entity_errors':len(errors),'whole_cache_products':[{ 'source':p['source_id'],'products':[{k:e[k] for k in ['selected_id','selected_name','selected_isActive','selected_race_count','selected_candidate_object_count','all_selected_candidate_values_zero']} for e in p['actual_cache_entries']]} for p in setups],'AP_iframe_sources':len(iframes),'question_workers_launched':False}))
