"""Bounded source/packaging verification from complete captured bodies; no producers imported.
Only this assignment's proof outputs are written. No network, source acquisition or peer writers.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import csv,gzip,hashlib,io,json,posixpath,tarfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent
H=R/'history/packaging-repair'
PP='senate/2026/louisiana/data/baselines/'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,obj):
    b=(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n').encode();p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(b,mtime=0)if name.endswith('.gz')else b)
class Archive:
    def __init__(self,kind):
        self.index=json.loads((H/f'{kind}-prior-inventory.json').read_bytes())
        bs=[]
        for p in self.index['ordered_archive_parts']:
            b=(R/p['path']).read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256'];bs.append(b)
        b=b''.join(bs);assert sha(b)==self.index['archive_sha256']
        self.tar=tarfile.open(fileobj=io.BytesIO(gzip.decompress(b)),mode='r:');self.pins={p['path']:p for p in self.index['members']}
        assert set(self.tar.getnames())==set(self.pins)
        for p in self.index['members']:self.get(p['path'])
    def get(self,path):
        b=self.tar.extractfile(path).read();p=self.pins[path];assert len(b)==p['bytes'] and sha(b)==p['sha256'];return b
    def obj(self,path):
        b=self.get(path);return json.loads(gzip.decompress(b)if path.endswith('.gz')else b)
def own(a,path):return a.get('data/turnout/'+path)
def oj(a,path):
    b=own(a,path);return json.loads(gzip.decompress(b)if path.endswith('.gz')else b)
def archive_sources(a):
    result={};receipts={};failed=[]
    for idx in ['source/original-pins.json','source/acquired-pins.json']:
        for p in oj(a,idx)['inputs']:
            b=own(a,p['receipt']);assert sha(b)==p['receipt_sha256'];rec=json.loads(b);receipts[p['id']]=rec
            if 'body'in p:
                b=own(a,p['body']);raw=gzip.decompress(b);assert sha(b)==p['stored_sha256'] and sha(raw)==p['raw_sha256'] and len(raw)==p['bytes']
                if p.get('status',rec.get('status'))==200:result[p['id']]={'body':raw,'receipt':rec,'pin':p}
            else:failed.append(p)
    return result,receipts,failed
def peer_sources(p):
    result={};receipts={};references=p.obj(PP+'source/receipts.json');roles=json.loads((H/'shared-original-roles.json').read_bytes());ar=roles['archive_parts'][0];b=(R/ar['path']).read_bytes();assert sha(b)==ar['sha256'] and len(b)==ar['bytes'];t=tarfile.open(fileobj=io.BytesIO(gzip.decompress(b)),mode='r:')
    for r in references:
        b=t.extractfile(r['reference_path']).read();raw=gzip.decompress(b);assert sha(b)==r['stored_sha256'] and len(b)==r['stored_bytes'] and sha(raw)==r['raw_sha256'] and len(raw)==r['bytes'];result[r['id']]={'body':raw,'receipt':r};receipts[r['id']]=r
    for path in p.pins:
        if not path.startswith(PP+'source/') or not path.endswith('.receipt.json'):continue
        r=p.obj(path)
        if 'asset'not in r or 'raw_sha256'not in r:continue
        b=p.get(PP+'source/'+r['asset']);raw=gzip.decompress(b);assert sha(b)==r['stored_sha256'] and sha(raw)==r['raw_sha256'] and len(raw)==r['bytes'];assert len(b)==r['stored_bytes']
        assert r['id']not in result
        result[r['id']]={'body':raw,'receipt':r};receipts[r['id']]=r
    return result,receipts
def source_proof():
    a=Archive('own');p=Archive('peer');src,receipts,failed=archive_sources(a);ps,pr=peer_sources(p)
    counts=Counter();differences=[];representation=[]
    def check(ok,field,context=None):
        counts[field]+=1
        if not ok:differences.append({'field':field,'context':context})
    # Original-first source freezes are checked against captured bodies, not their later paths.
    fw=oj(a,'source/original-first-witness.json');check(sha(own(a,'source/original-pins.json'))==fw['source_pins_sha256'],'own_first_source_pins')
    for r in fw['files']:check(sha(own(a,r['path']))==r['sha256'],'own_first_witness_body',r['path'])
    af=oj(a,'source/acquired-original-first-witness.json');check(sha(own(a,'source/acquired-pins.json'))==af['pins_sha256'],'own_acquired_first_pins');check(sha(own(a,af['whole_json_path']))==af['whole_json_sha256'],'own_acquired_whole_json')
    freeze=p.obj(PP+'original-freeze.json');unavailable=[]
    for e in freeze['assets']:
        path=PP+e['path']
        if path in p.pins and p.pins[path]['sha256']==e['sha256'] and p.pins[path]['bytes']==e['bytes']:continue
        matches=[q for q,r in p.pins.items()if r['sha256']==e['sha256'] and r['bytes']==e['bytes']]
        if not matches:
            # Archived script/error bodies may themselves be gzip-wrapped in immutable history.
            for q in p.pins:
                if '/history/'in q and q.endswith('.gz'):
                    try:b=gzip.decompress(p.get(q))
                    except (OSError,EOFError):continue
                    if sha(b)==e['sha256'] and len(b)==e['bytes']:matches=[q+' [one gzip layer]'];break
        if not matches:unavailable.append(e)
        else:representation.append({'role':'earlier_peer_freeze_body_recovered','old_path':e['path'],'sha256':e['sha256'],'captured_role':matches[0]})
    check(not unavailable,'peer_original_freeze_all_earlier_bodies',unavailable)
    for sid in set(src)&set(ps):
        if sid.startswith('sos-')or sid=='governor-house-suspension':
            check(src[sid]['body']==ps[sid]['body'],'shared_original_entire_entity_bytes',sid)
    # Same-body matching uses the precise constructor URL + raw body, never inferred source counts.
    matched=[]
    for sid,x in src.items():
        r=x['receipt'];url=r.get('requested_url',r.get('url'));matches=[(k,z)for k,z in ps.items()if z['receipt'].get('url')==url]
        if len(matches)==1:
            pid,z=matches[0]
            if sid in ['current-closed-primary','current-statistics-index'] and x['body']!=z['body']:
                representation.append({'role':'different_current_authority_HTML_observations','own_id':sid,'peer_id':pid,'own_raw_sha256':sha(x['body']),'peer_raw_sha256':sha(z['body']),'historical_equality_scope':False,'complete_failure_context':'history/packaging-repair/source-check-attempt1-whole-difference-context.json','qualification':'Complete current HTML bodies differ across retrievals; no source normalization, chronology or historical count difference inferred. Both exact observations retained; current semantic scope excluded.'})
            else:check(x['body']==z['body'],'common_original_full_body_bytes',sid)
            matched.append({'own_id':sid,'peer_id':pid,'raw_sha256':sha(x['body']),'own_receipt_role':x['pin']['receipt'],'peer_receipt_role':PP+'source/'+pid+'.receipt.json'if not pid.startswith('sos-')else PP+'source/receipts.json','receipt_equivalence':'whole receipts retained separately; retrieval clocks/headers differ; no normalization'})
    check(len([x for x in matched if 'native-votes'in x['own_id']])==192,'all192_native_json_bodies')
    controls=oj(a,'extract/source-only-selected-controls.json.gz');native={y:oj(a,f'extract/{y}-native.json.gz')for y in ['2024','2022','2020']};parish={y:oj(a,f'extract/{y}-parishes.json')for y in native};hist=oj(a,'historical-controls.json');orders=oj(a,'orders-summary.json');contract=oj(a,'priority-set.json')
    pn=p.obj(PP+'native-results.json.gz');pc=list(csv.DictReader(io.StringIO(p.get(PP+'candidates.csv').decode())));pctrl=p.obj(PP+'controls.json');positions=p.obj(PP+'native-position-links.json.gz');posmap={(z['year'],z['ward_literal'],z['precinct_literal'],json.loads(z['key'])[1]):z for z in positions}
    peer_witness=p.obj(PP+'source/workbook-position-witness.json.gz');peer_rows={(z['year'],z['member'],z['physical_row']):z for z in peer_witness};ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    for y in native:
        w=oj(a,f'extract/{y}-whole-workbook-positions.json.gz')
        for sheet in w['sheets']:
            for row in sheet['rows']:
                z=peer_rows[(y,sheet['member'],row['physical_row_ordinal'])];check(z['row_attributes']==row['attributes'],'whole_OOXML_row_attributes',[y,sheet['member'],row['physical_row_ordinal']]);check(len(z['cells'])==len(row['cells']),'whole_OOXML_cell_membership')
                for c,cc in zip(row['cells'],z['cells']):
                    check(c['physical_cell_ordinal']==cc['physical_cell'] and c['attributes']==cc['attributes'] and c['value']==cc['value'],'whole_OOXML_cell_position_attributes_style_value')
                    xml=ET.fromstring(cc['xml']);check(c['formula']==xml.findtext('m:f',None,ns),'whole_OOXML_formula')
        check(src[f'sos-{y}-full-results-xlsx']['body']==ps[f'sos-{y}-full-results-xlsx']['body'],'whole_ZIP_relationship_member_bytes_styles_formulas',y)
        for level in ['parish','precinct']:
            cw=p.obj(PP+f'source/{y}-{level}-csv-positions.json.gz');ownrows=controls[y]['csv_all_records'][level];check(ownrows[0]['values']==cw['header'],'CSV_entire_header_literals',y+' '+level)
            check(len(ownrows)-1==len(cw['rows']),'CSV_complete_record_count')
            for x,z in zip(ownrows[1:],cw['rows']):check(x['record_ordinal']==z['physical_row'] and x['values']==z['values'],'CSV_all_token_and_record_positions')
        pm={(z['parish_code'],z['ward'],z['precinct']):z for z in pn if z['year']==y};check(len(pm)==len(native[y]),'native_complete_membership',y)
        for u in native[y]:
            z=pm[(u['parish_id'],u['ward_literal'],u['precinct_literal'])];lk=posmap[(y,u['ward_literal'],u['precinct_literal'],u['parish_id'])]
            for field,left,right in [('candidate_vector',u['candidate_votes'],json.loads(z['candidate_votes'])),('native_literal',u['source_native_id'],z['source_native']),('qualified_null',u['qualified'],int(z['qualified'])if z['qualified']not in [None,'']else None),('voted_null',u['voted'],int(z['voted'])if z['voted']not in [None,'']else None),('reported',u['has_reported_literal'],z['has_reported']),('csv_record',u['csv_record_ordinal'],lk['csv_record_ordinal']),('xlsx_member',u['xlsx_member'],lk['xlsx_member']),('xlsx_row',u['xlsx_physical_row'],lk['xlsx_physical_row']),('display_trailing_space',u['workbook_display_literal'],lk['workbook_display_literal']),('api_position',u['native_votes_json_index'],'/Precincts/Precinct/'+str(u['native_votes_json_index'])==lk['api_pointer']and u['native_votes_json_index'])]:check(left==right,'native_'+field,u['key'])
            check(lk['xlsx_candidate_cell_ordinals']==list(range(2,len(u['candidate_votes'])+2)),'native_all_OOXML_candidate_positions',u['key']);check(lk['csv_candidate_column_ordinals']==list(range(5,len(u['candidate_votes'])+5)),'native_all_CSV_candidate_positions',u['key'])
        check(hist[y]['race_source_metadata']==pctrl[y]['metadata'],'entire_candidate_party_runningmate_metadata',y)
        for h in hist[y]['candidate_universe']:
            z=next(z for z in pc if z['year']==y and z['choice_id']==h['choice_id']);literal=h['header_literal'];alias=literal[:-7]+'(OTH)'if literal.endswith('(OTHER)')else literal
            check(alias==z['label'],'explicit_source_export_party_alias',h['choice_id'])
    po=p.obj(PP+'all-source-orders.json.gz');check(set(po)==set(orders)and len(po)==27,'all27_source_orders')
    fullorders={};hierarchies=[];ph=p.obj(PP+'native-hierarchy.json.gz')
    for name,s in orders.items():
        cr=list(csv.DictReader(io.StringIO(own(a,'orders/'+name+'.csv').decode())));prr=po[name];fullorders[name]={'summary':s,'rows':cr}
        check(len(cr)==len(prr['full_order']),'order_all_rows',name)
        for x,z in zip(cr,prr['full_order']):
            check(x['key']==z['key'] and int(x['rank'])==z['rank'] and int(x['votes'])==z['votes'] and int(x['cumulative_votes'])==z['cumulative_votes'] and Fraction(x['share'])==Fraction(z['share_numerator'],z['share_denominator']),'order_every_key_rank_count_cumulative_exactweight',name)
        check((s['denominator'],s['minimum80_count'],s['preceding_votes'],s['priority_votes'])==(prr['total'],prr['minimum80_count'],prr['previous'],prr['crossing']),'order_denominator_integer80_preceding_crossing',name)
        check(s['priority_keys']==[z['key']for z in prr['full_order'][:prr['minimum80_count']]]and s['remainder_keys']==[z['key']for z in prr['full_order'][prr['minimum80_count']:]],'order_full_priority_remainder',name)
    for y,units in native.items():
        priorities=set(orders[y+'-native-votes']['priority_keys']);ranks=[x['key']for x in fullorders[y+'-native-votes']['rows']]
        for par in parish[y]:
            pu=[u for u in units if u['parish_id']==par['parish_id']];z=next(x for x in ph if x['year']==y and x['parish_code']==par['parish_id']);peerkeys=[json.dumps([y,hist[y]['race_id'],*json.loads(k)[1:]],separators=(',',':'))for k in z['native_disjoint_children']];sourcekeys=[u['key']for u in pu]
            check(sourcekeys==peerkeys,'parent_entire_source_order_children',y+' '+par['key'])
            packet={'year':y,'parish_key':par['key'],'source_children':sourcekeys,'rank_children':[k for k in ranks if k in set(sourcekeys)],'priority_children':[k for k in ranks if k in set(sourcekeys)&priorities],'remainder_children':[k for k in ranks if k in set(sourcekeys)-priorities],'method_children':{kind:[u['key']for u in pu if u['kind']==kind]for kind in ['ward_precinct_source_row','early_voting_aggregate','provisional_aggregate']}}
            for kind,peer_kind in [('ward_precinct_source_row','ward-precinct'),('early_voting_aggregate','early-aggregate'),('provisional_aggregate','provisional-aggregate')]:
                pp=[json.dumps([y,hist[y]['race_id'],*json.loads(k)[1:]],separators=(',',':'))for k in z['method_children'][peer_kind]];check(packet['method_children'][kind]==pp,'parent_ordinary_early_provisional_full_arrays',y+' '+par['key'])
            if y=='2024':
                cp=next(x for x in contract['all_parishes']if x['key']==par['key']);check(packet['source_children']==cp['all_native_keys_in_source_order']and packet['rank_children']==cp['all_native_keys_in_descending_order']and packet['priority_children']==cp['ordered_priority_native_keys']and packet['remainder_children']==cp['ordered_remainder_native_keys'],'primary_parent_all_full_arrays',par['key'])
            hierarchies.append(packet)
    reverse=p.obj(PP+'peer-source-agreement.json');reported=sum(reverse['checks'].values());check(reverse['pass_comparison']and not reverse['issues']and reported==146652,'peer_reverse_proof_historical_scope_only',reported)
    # Explicitly retain every representation/source limitation without changing either side.
    representation += [{'role':'OTHER_vs_OTH','scope':'Only terminal export party spelling; complete source literals preserved'},{'role':'key_adapter','scope':'peer native key omits race_id; inserted from independently matching historical metadata'},{'role':'receipt_differences','scope':'independent retrieval clocks/headers and final-only redirect histories remain distinct; no equality claimed'},{'role':'native_stats_scope','scope':'peer has all64 StatsRaceParish contexts; own independently acquired native control JSON covers all64, with only17 StatsRaceParish sample. No extra demographic/control adoption; complete peer bodies retained.'}]
    packet={'scope':'Complete independently frozen historical source context, not calculator/scenario/future outcomes','source_controls':controls,'historical_controls':hist,'native_units':native,'parish_units':parish,'full_orders':fullorders,'all_parent_arrays':hierarchies,'primary_contract':contract,'current_admission':False,'source_role_indexes':{'own':oj(a,'source/original-pins.json'),'acquired':oj(a,'source/acquired-pins.json'),'peer_shared':p.obj(PP+'source/receipts.json')},'whole_body_position_context':{'own_first_witness':fw,'whole_workbooks':[oj(a,f'extract/{y}-whole-workbook-positions.json.gz')for y in native],'whole_acquired_json':oj(a,'extract/acquired-whole-json-witness.json.gz')}}
    save('repair-proof/complete-source-context-packet.json.gz',packet)
    proof={'status':'pass'if not differences else'fail','scope':'Complete captured historical SOURCE evidence only; no scenarios, calculators, outcomes or later/current ballot/native geometry/count/cadence/eligibility approval','own_capture_sha256':sha((H/'own-prior-inventory.json').read_bytes()),'peer_capture_sha256':sha((H/'peer-prior-inventory.json').read_bytes()),'checks':dict(counts),'differences':differences,'representation_qualifications':representation,'common_whole_entity_pairs':matched,'own_failed_acquisition_receipts_preserved':len(failed),'peer_reverse_proof':reverse,'peer_reverse_reported_source_field_checks':reported,'original_first_chronology':{'own_initial_source_freeze':oj(a,'source/original-pins.json')['frozen_at_utc'],'own_position_freeze':fw['frozen_at_utc'],'own_first_freeze_peer_id':fw['peer_agent_id'],'own_prior_peer_capture':oj(a,'peer-capture/capture.json')['captured_at_utc'],'peer_declared_original_only_scope':freeze['scope'],'peer_original_freeze_sha256':sha(p.get(PP+'original-freeze.json')),'peer_priority_original_freeze':p.obj(PP+'priority-original-freeze.json'),'qualification':'Captured source freeze body hashes verified against exact earlier bodies. Wall-clock assertions remain source provenance, not independent forensic creation-time attestation.'},'complete_packet':{'path':'repair-proof/complete-source-context-packet.json.gz','sha256':sha((R/'repair-proof/complete-source-context-packet.json.gz').read_bytes())},'unchanged_counts':{'native':3933,'candidate_votes':2006975,'priority_count':1516,'previous':1605350,'crossing':1605649},'coordinator_acceptance':False,'current_native_dispatch':[]}
    save('repair-proof/captured-final-peer-source-verification.json',proof)
    print(json.dumps({'source_verification':proof['status'],'differences':differences[:5],'checks':sum(counts.values()),'peer_reverse_source_fields':reported}))
    assert not differences
if __name__=='__main__':source_proof()
