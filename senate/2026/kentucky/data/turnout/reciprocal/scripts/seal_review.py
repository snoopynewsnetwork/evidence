#!/usr/bin/env python3
"""Seal reviewed metadata first, complete owned manifest LAST. Run read-only audit next."""
import json,datetime
from captured_core import ROOT,STATE,sha
R=ROOT.parent
def h(p):return sha(p.read_bytes())
assert json.loads((R/'validation.json').read_bytes())['status']=='preseal_checks_satisfied'
assert json.loads((ROOT/'validation.json').read_bytes())['status']=='PASS'
seal={'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owned_scope':['turnout.md','data/county-turnout.csv','data/turnout/**'],'bounded_original_research_complete':True,'bounded_captured_final_source_core_review_complete':True,'worker_released_after_final_readonly_audit':True,'canonical_native_order':None,'canonical_native_top15':None,'canonical_native_min80':None,'canonical_native_priority':None,'canonical_native_remainder':None,'dispatch_keys':[],'all120_county_candidate_controls_reconciled':True,'peer_agent_id':'ce1620b8-8df0-406b-bdb1-a8522aeea2f4','source_core_agreement':'captured final only;88 literal/schema representations retained;distinct3150/3220source universes','independent_peer_agreement':False,'coordinator_accepted':False,'validation_sha256':h(R/'validation.json'),'reciprocal_validation_sha256':h(ROOT/'validation.json'),'review_metadata_sha256':h(ROOT/'review.json'),'original_first_witnesses':{str(p.relative_to(R)):h(p) for p in sorted((R/'history').glob('original-first*/witness.json'))},'old_body_indexes':{str(p.relative_to(R)):h(p) for p in [ROOT/'own-pre-resume/index.json',ROOT/'peer-final/index.json']},'final_audit_command':'PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/kentucky/data/turnout/reciprocal/scripts/review_audit.py --final','manifest_rule':'asset-manifest.json is written last and excludes ONLY itself; no current manifest digest is included in this seal','no_owned_writes_after_final_PASS':True,'external_qualifications':['Scott no native allocation;Magoffin Mail In only','167unresolved literal associations and source-vintage gaps retained','no statewide canonical native universe or dispatch','current/legal/geographic/eligible write-in/November IDs/cadence/pool/collector/forecast/calibration false or unknown','coordinator review/acceptance/publication separate']}
(R/'finalseal.json').write_text(json.dumps(seal,indent=2)+'\n')
mf=R/'asset-manifest.json';files=sorted([STATE/'turnout.md',STATE/'data/county-turnout.csv']+[p for p in R.rglob('*') if p.is_file() and p!=mf]);entries=[]
for p in files:
 assert not p.is_symlink() and p.stat().st_size<40000000
 assert not any(x in p.parts for x in ('__pycache__','node_modules','.cache','.venv'))
 entries.append({'path':str(p.relative_to(STATE)),'bytes':p.stat().st_size,'sha256':h(p)})
mf.write_text(json.dumps({'schema':'complete owned membership v1','excludes_only':'data/turnout/asset-manifest.json','all_artifacts_strictly_less_than_bytes':40000000,'source_entities':'data/turnout/source/entities.json','shared_original_pins':'data/turnout/source/refs.json','files':entries},indent=2)+'\n')
print(json.dumps({'targets':len(entries),'members_including_manifest':len(entries)+1,'manifest_sha256':h(mf),'finalseal_sha256':h(R/'finalseal.json'),'contract_sha256':h(R/'priority-set.json'),'review_sha256':h(ROOT/'review.json'),'largest_bytes':max(z['bytes'] for z in entries)},indent=2))
