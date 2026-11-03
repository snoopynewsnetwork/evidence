"""Meaningful denials use the COMPLETE captured source packet and a full owned inventory.
Input recipes retain exact base bytes and reversible mutations; no toy county-only packets.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import copy,gzip,hashlib,json
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(name,obj):
    b=(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n').encode();p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(b,mtime=0)if name.endswith('.gz')else b)
def canonical(b):return json.dumps(b,ensure_ascii=False,separators=(',',':')).encode()
def check_packet(p,anchor):
    assert set(p)==anchor['top_keys'],'complete source/context companion membership'
    assert p['current_admission']is False and p['primary_contract']['coordinator_acceptance']is False and p['primary_contract']['current_native_dispatch']==[],'current admission'
    assert p['source_controls']==anchor['source_controls'],'complete source headers/tokens/blank/null/candidate context'
    assert p['historical_controls']==anchor['historical_controls'],'complete candidate party/runningmate/control context'
    for y,units in p['native_units'].items():
        expected=anchor['native'][y];ids=[x['key']for x in units];assert len(ids)==len(set(ids))==len(expected),'native membership/duplicate'
        assert set(ids)==set(expected),'complete native source membership'
        for u in units:assert u==expected[u['key']],'exact source vector/null/admin/method/position/companion fields'
    for name,d in p['full_orders'].items():
        rows=d['rows'];s=d['summary'];assert len(rows)==len(anchor['orders'][name]),'full order truncation'
        assert rows==anchor['orders'][name],'full rank/key/count/cumulative/exactweight/source order'
        total=sum(int(x['votes'])for x in rows);cum=0;k=None
        for i,x in enumerate(rows,1):
            before=cum;cum+=int(x['votes']);assert int(x['rank'])==i and int(x['cumulative_votes'])==cum,'rank cumulative'
            assert Fraction(x['share'])==Fraction(int(x['votes']),total),'denominator/weight'
            if k is None and 5*cum>=4*total:k=i;previous=before;cross=cum
        assert (s['denominator'],s['minimum80_count'],s['preceding_votes'],s['priority_votes'])==(total,k,previous,cross),'exact integer80/previous/crossing'
        keys=[x['key']for x in rows];assert s['priority_keys']==keys[:k]and s['remainder_keys']==keys[k:],'priority/remainder'
    assert p['all_parent_arrays']==anchor['parents'],'complete all64 source/rank/priority/remainder/method child arrays per year'
    c=p['primary_contract'];assert c['canonical_native_dispatch']==p['full_orders']['2024-native-votes']['summary']['priority_keys'],'no parish dispatch substitution'
    assert c['full_order']==anchor['contract_order'],'complete contract full order'
    assert set(p['whole_body_position_context'])==anchor['whole_context_keys'],'whole body/position companions required'
    assert len(p['whole_body_position_context']['whole_workbooks'])==3 and len(p['whole_body_position_context']['whole_acquired_json'])==anchor['acquired_json_length'],'whole original position contexts required'
def anchor(p):return {'top_keys':set(p),'source_controls':copy.deepcopy(p['source_controls']),'historical_controls':copy.deepcopy(p['historical_controls']),'native':{y:{x['key']:copy.deepcopy(x)for x in z}for y,z in p['native_units'].items()},'orders':{n:copy.deepcopy(x['rows'])for n,x in p['full_orders'].items()},'parents':copy.deepcopy(p['all_parent_arrays']),'contract_order':copy.deepcopy(p['primary_contract']['full_order']),'whole_context_keys':set(p['whole_body_position_context']),'acquired_json_length':len(p['whole_body_position_context']['whole_acquired_json'])}
def graph_check(g):
    done=set();active=set()
    def walk(n):
        assert n not in active,'cyclic current reverse digest dependency'
        if n in done:return
        active.add(n)
        for x in g.get(n,[]):walk(x)
        active.remove(n);done.add(n)
    for n in g:walk(n)
def inventory_check(manifest,bodies,expected,graph):
    assert manifest['excludes_only']==['asset-manifest.json'],'self-only manifest exclusion'
    pins={x['path']:x for x in manifest['assets']};assert len(pins)==len(manifest['assets']),'unique manifest paths'
    assert set(pins)==set(expected),'exact complete manifest membership includes final audit/seal/history'
    for n,b in bodies.items():
        assert n in pins and len(b)==pins[n]['bytes']and sha(b)==pins[n]['sha256']and len(b)<40000000,'whole body changed/omitted'
    graph_check(graph)
def main():
    b=(R/'repair-proof/complete-source-context-packet.json.gz').read_bytes();p=json.loads(gzip.decompress(b));a=anchor(p);check_packet(p,a);out=[];base={'path':'repair-proof/complete-source-context-packet.json.gz','sha256':sha(b),'bytes':len(b),'scope':'Entire three-year native/candidate/method/null/admin/header/physical-position/source-companion/all27-order/all192-parent packet; each mutation applied to full packet, not a projection'}
    fixtures=['delete-native','truncate-full-order','duplicate-native','wrong80','wrong-cumulative','wrong-order','parish-substitution','current-admission','missing-context-companion','changed-party-header','invented-null-zero','lost-provisional','wrong-method','wrong-source-position','parent-child-loss']
    for name in fixtures:
        restore=[]
        def setv(obj,k,v):restore.append((obj,k,obj[k]));obj[k]=v
        if name=='delete-native':setv(p['native_units'],'2024',p['native_units']['2024'][:-1])
        elif name=='duplicate-native':setv(p['native_units'],'2024',p['native_units']['2024']+[p['native_units']['2024'][-1]])
        elif name=='lost-provisional':setv(p['native_units'],'2024',[u for u in p['native_units']['2024']if not(u['kind']=='provisional_aggregate'and u['parish_id']=='01')])
        elif name=='wrong80':s=p['full_orders']['2024-native-votes']['summary'];setv(s,'minimum80_count',s['minimum80_count']-1)
        elif name=='truncate-full-order':d=p['full_orders']['2024-native-votes'];setv(d,'rows',d['rows'][:-1])
        elif name=='wrong-cumulative':d=p['full_orders']['2024-native-votes']['rows'][1515];setv(d,'cumulative_votes',str(int(d['cumulative_votes'])+1))
        elif name=='wrong-order':d=p['full_orders']['2024-native-votes'];rows=d['rows'][:];rows[0],rows[1]=rows[1],rows[0];setv(d,'rows',rows)
        elif name=='parish-substitution':setv(p['primary_contract'],'canonical_native_dispatch',p['primary_contract']['parish_sensitivity']['priority_keys'])
        elif name=='current-admission':setv(p,'current_admission',True)
        elif name=='missing-context-companion':setv(p['whole_body_position_context'],'whole_workbooks',[])
        elif name=='changed-party-header':d=p['source_controls']['2024']['csv_all_records']['precinct'][0]['values'];setv(d,4,d[4]+' fabricated party')
        elif name=='invented-null-zero':u=next(u for u in p['native_units']['2024']if u['qualified']is None);setv(u,'qualified',0)
        elif name=='wrong-method':u=p['native_units']['2024'][0];setv(u,'kind','early_voting_aggregate')
        elif name=='wrong-source-position':u=p['native_units']['2024'][0];setv(u,'xlsx_physical_row',u['xlsx_physical_row']+1)
        elif name=='parent-child-loss':d=p['all_parent_arrays'][0];setv(d,'source_children',d['source_children'][:-1])
        recipe={'name':name,'base':base,'operation':name,'mutations':[{'key':str(k),'before':old,'after':obj[k]}for obj,k,old in restore],'reconstruction':'load entire exact base gzip JSON, apply named operation in repair_negative.py; no other byte/semantic transformations'};put('repair-fixtures/'+name+'.input.json.gz',recipe)
        try:check_packet(p,a)
        except AssertionError as e:result={'name':name,'status':'correctly_rejected','reason':str(e),'full_source_packet_used':True}
        else:raise AssertionError('Accepted negative '+name)
        for obj,k,old in reversed(restore):obj[k]=old
        put('repair-fixtures/'+name+'.result.json',result);out.append(result)
    check_packet(p,a)
    # Full actual owned candidate-body snapshot with concrete acyclic audit/seal fixtures.
    state=R.parent.parent;files={str(q.relative_to(state)):q.read_bytes()for q in R.rglob('*')if q.is_file() and q.name!='asset-manifest.json'};files['turnout.md']=(state/'turnout.md').read_bytes();files['data/county-turnout.csv']=(state/'data/county-turnout.csv').read_bytes()
    files['data/turnout/final-audit.json']=canonical({'scope':'concrete pre-manifest audit fixture','source_packet':base,'depends_on':['source-proof','validation'],'does_not_pin_future_manifest':True})
    files['data/turnout/final-seal.json']=canonical({'scope':'concrete seal fixture','audit_sha256':sha(files['data/turnout/final-audit.json']),'coordinator_acceptance':False})
    pins=[{'path':n,'bytes':len(z),'sha256':sha(z)}for n,z in sorted(files.items())];mf={'excludes_only':['asset-manifest.json'],'assets':pins};g={'manifest':['seal','audit','history','validation'],'seal':['audit','validation','history'],'audit':['source-proof','validation'],'validation':['source-proof'],'source-proof':['history']};inventory_check(mf,files,files,g)
    put('repair-fixtures/complete-packaging-context.json.gz',{'scope':'Full actual candidate owned bodies via exact inventory; immutable full old bodies in captured archives and current body pins. Concrete audit/seal fixture bodies embedded. No future production digest.','manifest':mf,'graph':g,'audit_body':files['data/turnout/final-audit.json'].decode(),'seal_body':files['data/turnout/final-seal.json'].decode(),'body_roles':pins})
    for name in ['omitted-final-audit','omitted-seal','omitted-history','changed-seal','cyclic-reverse-pin']:
        mm=copy.deepcopy(mf);bb=dict(files);gg=copy.deepcopy(g);removed=None
        if name.startswith('omitted-'):
            removed={'omitted-final-audit':'data/turnout/final-audit.json','omitted-seal':'data/turnout/final-seal.json','omitted-history':next(n for n in files if'/history/'in n)}[name];mm['assets']=[x for x in mm['assets']if x['path']!=removed]
        elif name=='changed-seal':bb['data/turnout/final-seal.json']+=b' '
        else:gg['audit'].append('manifest')
        put('repair-fixtures/'+name+'.input.json.gz',{'name':name,'complete_base':'repair-fixtures/complete-packaging-context.json.gz','removed_path':removed,'manifest':mm,'graph':gg,'changed_seal_complete_body':bb['data/turnout/final-seal.json'].decode()if name=='changed-seal'else None})
        try:inventory_check(mm,bb,files,gg)
        except AssertionError as e:result={'name':name,'status':'correctly_rejected','reason':str(e),'complete_inventory_size':len(files)}
        else:raise AssertionError('Accepted packaging negative '+name)
        put('repair-fixtures/'+name+'.result.json',result);out.append(result)
    put('repair-proof/complete-context-negative-validation.json',{'status':'pass','source_packet':base,'source_positive_packet':'pass','packaging_positive_full_inventory':'pass','source_negative_count':len(fixtures),'packaging_negative_count':5,'fixtures':out,'scope':'Actual complete source packet and full candidate inventory denials, not calculator/scenario/outcome tests'})
    print(json.dumps({'status':'pass','source_negatives':len(fixtures),'packaging_negatives':5,'full_candidate_inventory':len(files)}))
if __name__=='__main__':main()
