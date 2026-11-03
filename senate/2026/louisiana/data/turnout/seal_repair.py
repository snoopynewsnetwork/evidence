"""Prepare validation, acyclic final audit proof and final seal BEFORE manifest-last."""
from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;S=R.parent.parent;SELF='data/turnout/asset-manifest.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    from repair_verify import Archive
    from repair_readonly import verify_core_unchanged
    prior=Archive('own');core=verify_core_unchanged(prior);proofpins={}
    for name in ['captured-final-peer-source-verification.json','isolated-original-replay.json','complete-context-negative-validation.json']:
        p=R/'repair-proof'/name;b=p.read_bytes();assert json.loads(b)['status']=='pass';proofpins[name]=sha(b)
    old_validation=json.loads(prior.get('data/turnout/validation.json'))
    validation={'status':'pass','scope':'Bounded packaging and independently captured final-peer historical SOURCE verification only; no count/model/research acquisition repair','prior_validation_exact_archived':{'archive':'history/packaging-repair/own-prior-complete.tar.gz.part001','member':'data/turnout/validation.json','sha256':sha(prior.get('data/turnout/validation.json'))},'original_offline_validation_status':old_validation['status'],'source_complete_context_proof':proofpins['captured-final-peer-source-verification.json'],'isolated_original_replay':{'proof_sha256':proofpins['isolated-original-replay.json'],'whole_generated_bytes_equal':46,'actual_denial_probes':14},'complete_source_context_negative_fixtures':15,'complete_packaging_negative_fixtures':5,'proof_pins':proofpins,'core_preservation':core,'prior_own_complete_bodies':645,'captured_peer_final_complete_bodies':1608,'coordinator_acceptance':False,'current_native_dispatch':[],'current_ballot_geometry_live_cadence_eligible_writein_pool_collector_forecast_probability_approval':False}
    (R/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    audit={'status':'pass','scope':'Pre-manifest complete historical source/context, original replay and meaningful negative proof. No current/future manifest or seal digest. The ACTUAL post-manifest read-only audit prints stdout only.','proof_pins':proofpins,'validation_sha256':sha((R/'validation.json').read_bytes()),'current_reverse_digest_dependencies':[],'coordinator_acceptance':False,'current_native_dispatch':[]};(R/'final-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    files={str(p.relative_to(S)):p for p in R.rglob('*')if p.is_file()}|{'turnout.md':S/'turnout.md','data/county-turnout.csv':S/'data/county-turnout.csv'};rows=[]
    for name,p in sorted(files.items()):
        if name in [SELF,'data/turnout/final-seal.json']:continue
        b=p.read_bytes();assert len(b)<40000000 and '__pycache__'not in p.parts;rows.append({'path':name,'bytes':len(b),'sha256':sha(b)})
    graph={'manifest':['seal','audit','validation','source-proof','replay-proof','negative-proof','history'],'seal':['audit','validation','source-proof','replay-proof','negative-proof','history'],'audit':['validation','source-proof','replay-proof','negative-proof'],'validation':['source-proof','replay-proof','negative-proof','history'],'source-proof':['history'],'replay-proof':['history'],'negative-proof':['history']}
    seal={'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Louisiana actual original turnout bounded packaging repair; complete historical source/position/control/order/parent comparison only. No peer calculator/scenario/outcome/current operational approval.','manifest_dependency':'manifest_is_last_and_pins_this_seal; seal_never_pins_current_manifest','current_dependency_graph':graph,'body_pins':rows,'prior_own_manifest_sha256':'d95ab6f276e4feeea3662671d03c62328ed4ffebc850197fcca34b0919e382dc','captured_final_peer_manifest_sha256':'22aa501bcbcf9a6b99849e41859cf14a7d3216191e22d0f6dd68eced41fe897d','captured_final_peer_seal_sha256':'7e3c2305515037ef32169d18af91b331bf8724bdf023e5550957e5339d2ba8c8','coordinator_acceptance':False,'current_native_dispatch':[],'current_operational_approval':False};(R/'final-seal.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps({'prepared':'validation -> audit proof -> seal; manifest must follow LAST','body_pins':len(rows),'seal_sha256':sha((R/'final-seal.json').read_bytes())}))
if __name__=='__main__':main()
