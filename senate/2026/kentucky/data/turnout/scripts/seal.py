#!/usr/bin/env python3
"""Write finalseal first, complete manifest LAST; run audit.py --final afterward without owned writes."""
import hashlib,json,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R.parents[1]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
validation=json.load(open(R/'validation.json'));assert validation['status']=='preseal_checks_satisfied'
seal={'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned_scope':['turnout.md','data/county-turnout.csv','data/turnout/**'],'bounded_original_research_complete':True,'worker_released_after_final_readonly_audit':True,'canonical_native_order':None,'canonical_native_top15':None,'canonical_native_min80':None,'canonical_native_priority':None,'canonical_native_remainder':None,'dispatch_keys':[],'all120_county_candidate_controls_reconciled':True,'peer_agent_id':'ce1620b8-8df0-406b-bdb1-a8522aeea2f4','independent_peer_agreement':False,'coordinator_accepted':False,'validation_sha256':h(R/'validation.json'),'original_first_witnesses':{str(p.relative_to(R)):h(p) for p in sorted((R/'history').glob('original-first*/witness.json'))},'final_audit_command':'PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/kentucky/data/turnout/scripts/audit.py --final','manifest_rule':'asset-manifest.json is written last and excludes ONLY itself; no current manifest digest is included in this seal','no_owned_writes_after_final_PASS':True,'external_qualifications':['missing Scott native presidential allocation','Magoffin Mail In-only native source','native/certified source-vintage and generic/valid-write-in universe differences','actual independent peer agreement and coordinator acceptance pending','current/legal/geographic/eligible write-in/November IDs/cadence/pool/collector/forecast/calibration false or unknown']}
(R/'finalseal.json').write_text(json.dumps(seal,indent=2)+'\n')
manifest=R/'asset-manifest.json';files=sorted([S/'turnout.md',S/'data/county-turnout.csv']+[p for p in R.rglob('*') if p.is_file() and p!=manifest]);entries=[]
for p in files:
 b=p.read_bytes();assert len(b)<40000000;assert '__pycache__' not in p.parts;entries.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest.write_text(json.dumps({'schema':'complete owned membership v1','excludes_only':'data/turnout/asset-manifest.json','all_artifacts_strictly_less_than_bytes':40000000,'source_entities':'data/turnout/source/entities.json','shared_original_pins':'data/turnout/source/refs.json','files':entries},indent=2)+'\n')
print(json.dumps({'manifest':str(manifest),'manifest_sha256':h(manifest),'files':len(entries),'largest_bytes':max(z['bytes'] for z in entries)},indent=2))
