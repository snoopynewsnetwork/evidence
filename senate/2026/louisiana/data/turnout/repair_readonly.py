"""Final actual read-only body/membership/source/history/order/offline/negative audit."""
from pathlib import Path
import contextlib,gzip,hashlib,io,json,os,re,sys
R=Path(__file__).resolve().parent;STATE=R.parent.parent
SELF='data/turnout/asset-manifest.json'
ALLOWED_OLD_CHANGES={'turnout.md','data/turnout/source/SCHEMA.md','data/turnout/make_manifest.py','data/turnout/final_audit.py','data/turnout/final-audit.json','data/turnout/validation.json',SELF}
def sha(b):return hashlib.sha256(b).hexdigest()
def current_owned():return {str(p.relative_to(STATE)):p for p in R.rglob('*')if p.is_file()}|{'turnout.md':STATE/'turnout.md','data/county-turnout.csv':STATE/'data/county-turnout.csv'}
def deny_mutation(event,args):
    if event=='open':
        mode=args[1];flags=args[2]if len(args)>2 else 0
        if(isinstance(mode,str)and any(x in mode for x in 'wax+'))or(isinstance(flags,int)and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):raise PermissionError('Final audit denies file writes')
    if event in ['os.mkdir','os.remove','os.rmdir','os.rename','os.replace','subprocess.Popen','os.system','os.posix_spawn']or event.startswith('socket.'):raise PermissionError('Final audit denies mutation/network/process')
def verify_core_unchanged(archive):
    changed=[];unchanged=0
    for name,pin in archive.pins.items():
        q=STATE/name;assert q.is_file(),'prior owned body disappeared '+name;b=q.read_bytes()
        if sha(b)!=pin['sha256']or len(b)!=pin['bytes']:
            assert name in ALLOWED_OLD_CHANGES,'Unapproved old body/semantic change '+name;changed.append(name)
        else:unchanged+=1
    assert sha((R/'priority-set.json').read_bytes())=='69f0244082d967c671fad29bf15bda5941f819271f63c0654366b3202c87337b'
    assert sha((STATE/'data/county-turnout.csv').read_bytes())=='8df56f50cb5f6a0595693a7c2c1e3b9b8465547276e91320ff4dcba04acc6df2'
    return {'unchanged_old_whole_bodies':unchanged,'explicit_packaging_report_proof_changes_only':changed,'all645_prior_complete_bodies_preserved':True}
def main():
    sys.dont_write_bytecode=True;sys.addaudithook(deny_mutation)
    from repair_verify import Archive,archive_sources,peer_sources
    import repair_negative as neg
    own=Archive('own');peer=Archive('peer');src,recs,failed=archive_sources(own);ps,prs=peer_sources(peer);core=verify_core_unchanged(own)
    assert own.index['whole_file_count']==645 and peer.index['whole_file_count']==1608
    assert own.index['manifest_sha256']=='d95ab6f276e4feeea3662671d03c62328ed4ffebc850197fcca34b0919e382dc'
    assert peer.index['manifest_sha256']=='22aa501bcbcf9a6b99849e41859cf14a7d3216191e22d0f6dd68eced41fe897d'
    manifest=json.loads((R/'asset-manifest.json').read_bytes());assert manifest['excludes_only']==[SELF]
    found=current_owned();pins={x['path']:x for x in manifest['assets']};assert len(pins)==len(manifest['assets'])and set(pins)==set(found)-{SELF},'exact current membership; self only'
    bodies={}
    for name,pin in pins.items():
        b=found[name].read_bytes();assert len(b)==pin['bytes']<40000000 and sha(b)==pin['sha256'],name;bodies[name]=b
        assert '__pycache__'not in found[name].parts and 'node_modules'not in found[name].parts
    assert(R/'asset-manifest.json').stat().st_size<40000000
    seal=json.loads(bodies['data/turnout/final-seal.json']);sp={x['path']:x for x in seal['body_pins']};assert set(sp)==set(pins)-{'data/turnout/final-seal.json'}
    for name,x in sp.items():assert x==pins[name],'seal/current MF body disagreement '+name
    assert seal['manifest_dependency']=='manifest_is_last_and_pins_this_seal; seal_never_pins_current_manifest'
    audit=json.loads(bodies['data/turnout/final-audit.json']);assert 'manifest_sha256'not in audit and 'final_seal_sha256'not in audit and audit['status']=='pass'
    neg.graph_check(seal['current_dependency_graph']);validation=json.loads(bodies['data/turnout/validation.json']);assert validation['status']=='pass'
    for name in ['captured-final-peer-source-verification.json','isolated-original-replay.json','complete-context-negative-validation.json']:
        proof=json.loads(bodies['data/turnout/repair-proof/'+name]);assert proof['status']=='pass';assert audit['proof_pins'][name]==sha(bodies['data/turnout/repair-proof/'+name])
    source=json.loads(bodies['data/turnout/repair-proof/captured-final-peer-source-verification.json']);assert not source['differences'] and source['peer_reverse_reported_source_field_checks']==146652
    replay=json.loads(bodies['data/turnout/repair-proof/isolated-original-replay.json']);assert len(replay['whole_byte_comparison'])==46 and all(x['whole_bytes_equal']for x in replay['whole_byte_comparison'])and all(len(x['denials'])==7 for x in replay['runs'])
    packetbytes=bodies['data/turnout/repair-proof/complete-source-context-packet.json.gz'];assert sha(packetbytes)==source['complete_packet']['sha256']
    packet=json.loads(gzip.decompress(packetbytes));assert packet['source_controls']==json.loads(gzip.decompress(own.get('data/turnout/extract/source-only-selected-controls.json.gz')))
    for y in ['2024','2022','2020']:assert packet['native_units'][y]==json.loads(gzip.decompress(own.get('data/turnout/extract/'+y+'-native.json.gz')))
    anchor=neg.anchor(packet);neg.check_packet(packet,anchor)
    # Re-exercise complete-context negatives in memory: put is replaced with a no-write sink.
    captured=[];neg.put=lambda name,obj:captured.append((name,obj.get('status')if isinstance(obj,dict)else None));output=io.StringIO()
    with contextlib.redirect_stdout(output):neg.main()
    negative_summary=json.loads(output.getvalue());assert negative_summary['source_negatives']==15 and negative_summary['packaging_negatives']==5
    # Apply packaging denials to the ACTUAL final current body packet as well.
    canonical={'excludes_only':['asset-manifest.json'],'assets':manifest['assets']};graph=seal['current_dependency_graph'];neg.inventory_check(canonical,bodies,bodies,graph);current_neg=[]
    for name,target in [('omitted-finalaudit','data/turnout/final-audit.json'),('omitted-finalseal','data/turnout/final-seal.json'),('omitted-history',next(k for k in bodies if'/history/'in k))]:
        bad={'excludes_only':['asset-manifest.json'],'assets':[x for x in manifest['assets']if x['path']!=target]}
        try:neg.inventory_check(bad,bodies,bodies,graph)
        except AssertionError:current_neg.append(name)
        else:raise AssertionError('Accepted actual current omission '+name)
    bad=dict(bodies);bad['data/turnout/final-seal.json']+=b' '
    try:neg.inventory_check(canonical,bad,bodies,graph)
    except AssertionError:current_neg.append('changed-current-seal')
    else:raise AssertionError('Accepted changed actual seal')
    graphbad=json.loads(json.dumps(graph));graphbad['audit'].append('manifest')
    try:neg.inventory_check(canonical,bodies,bodies,graphbad)
    except AssertionError:current_neg.append('cyclic-current-reverse-pin')
    else:raise AssertionError('Accepted current reverse digest cycle')
    links=0
    for name,path in found.items():
        if not name.endswith('.md'):continue
        for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if'://'in link or link.startswith('#'):continue
            assert(path.parent/link.split('#')[0]).resolve().exists(),'broken relative link '+name+' '+link;links+=1
    contract=json.loads(bodies['data/turnout/priority-set.json']);assert contract['coordinator_acceptance']is False and contract['current_native_dispatch']==[]
    print(json.dumps({'status':'PASS_FINAL_READONLY','no_owned_writes':True,'manifest_sha256':sha((R/'asset-manifest.json').read_bytes()),'final_seal_sha256':sha(bodies['data/turnout/final-seal.json']),'whole_current_owned_files':len(found),'manifest_targets':len(pins),'excludes_only':[SELF],'all_stored_bytes_strictly_below_40000000':True,'prior_archived_bodies_verified':645,'peer_final_archived_bodies_verified':1608,'individual_source_body_receipts_verified':len(src)+len(ps),'source_complete_context_checks':sum(source['checks'].values()),'peer_reverse_scope':'146652 historical source checks only; no later/future outcome/contract/calculator/current approval','isolated_original_replay_exact_files':46,'actual_denial_probes':14,'complete_context_negative_rejections':20,'actual_current_packaging_negative_rejections':current_neg,'relative_links':links,'core_preservation':core,'historical_native_primary':{'units':3933,'candidate_votes':2006975,'top15':689455,'minimum80':1516,'previous':1605350,'crossing':1605649,'crossing_unit':'Bienville06/03','remainder_units':2417,'remainder_votes':401326},'coordinator_acceptance':False,'current_native_dispatch':[]},indent=2))
if __name__=='__main__':main()
