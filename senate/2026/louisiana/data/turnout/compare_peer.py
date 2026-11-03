"""Read-only semantic comparison of two already frozen independent original source schemas.
Does not read peer scenario outputs, current contracts, calculators or future results.
"""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,io,json
ROOT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def peer(name):
    cap=json.loads((ROOT/'peer-capture/capture.json').read_bytes())
    pin=next(p for p in cap['inputs']if p['peer_source_path'].endswith('/baselines/'+name))
    b=(ROOT/pin['captured_path']).read_bytes();assert sha(b)==pin['stored_sha256']
    if pin['compression']=='gzip_of_exact_bytes':b=gzip.decompress(b)
    assert sha(b)==pin['raw_sha256'] and len(b)==pin['raw_bytes']
    return b
def main():
    freeze=json.loads(peer('original-freeze.json'));assets={p['path']:p for p in freeze['assets']}
    for f in ['controls.json','native-results.json.gz','parish-controls.csv','candidates.csv','native-coverage.json','full-orders.json.gz']:
        b=peer(f);assert sha(b)==assets[f]['sha256'] and len(b)==assets[f]['bytes']
    a=json.loads(gzip.decompress((ROOT/'source/native-primary-stable-schema.json.gz').read_bytes()))
    b=json.loads(gzip.decompress(peer('native-results.json.gz')));bc=json.loads(peer('controls.json'));frozen_orders=json.loads(gzip.decompress(peer('full-orders.json.gz')))
    p=list(csv.DictReader(io.StringIO(peer('parish-controls.csv').decode())));c=list(csv.DictReader(io.StringIO(peer('candidates.csv').decode())))
    aliases={'ward_precinct_source_row':'ward-precinct','early_voting_aggregate':'early-aggregate','provisional_aggregate':'provisional-aggregate'}
    out={'scope':'Historical independently frozen original-source candidate/native/method/null/control comparison only; no future calculator or scenario equality',
         'peer_agent_id':'4f625056-8184-4b03-97fb-4152b00397e3','own_stable_sha256':sha((ROOT/'source/native-primary-stable-schema.json.gz').read_bytes()),
         'peer_freeze_sha256':sha(peer('original-freeze.json')),'years':{},'differences':[],'not_compared':['current2026 identities/geometry','future election outcomes','scenario calculators','peer later native priority contract'],
         'aliases':{'candidate_party':'OTHER workbook = OTH CSV, preserved on both sides','native_key':'own includes race_id; peer key excludes race_id; semantic join uses year,parish_code,ward,precinct','source_column':'own XLSX one-based physical column = peer parish CSV one-based column - 1'}}
    def check(ok,label,detail=None):
        if not ok:out['differences'].append({'field':label,'detail':detail})
    for y in ['2024','2022','2020']:
        own=a['native_vectors'][y];other=[r for r in b if r['year']==y]
        om={(r['parish_id'],r['ward_literal'],r['precinct_literal']):r for r in own}
        pm={(r['parish_code'],r['ward'],r['precinct']):r for r in other}
        check(len(pm)==len(other)==len(own)==len(om),'native uniqueness '+y)
        check(set(om)==set(pm),'native coverage '+y)
        for k in set(om)&set(pm):
            x=om[k];z=pm[k]
            for field,got,want in [('candidate_votes',x['candidate_votes'],json.loads(z['candidate_votes'])),('votes',x['votes'],z['all_candidate_votes']),('source_native_id',x['source_native_id'],z['source_native']),('kind',aliases[x['kind']],z['type']),('csv_record',x['csv_record_ordinal'],z['csv_row']),('api_position',x['native_votes_json_index']+1,z['api_ordinal']),('qualified',x['qualified'],int(z['qualified'])if z['qualified']not in [None,'']else None),('voted',x['voted'],int(z['voted'])if z['voted']not in [None,'']else None),('has_reported',x['has_reported_literal'],z['has_reported'])]:check(got==want,y+' '+field,list(k))
        for x in a['parish_vectors'][y]:
            z=next(r for r in p if r['year']==y and r['parish_code']==x['parish_id'])
            for field,got,want in [('candidate_votes',x['candidate_votes'],json.loads(z['candidate_votes'])),('race_qualified',x['race_qualified'],int(z['qualified'])),('race_voted',x['race_voted'],int(z['voted'])),('general_qualified',x['qualified'],int(z['stats_qualified'])),('general_voted',x['voted'],int(z['stats_voted']))]:check(got==want,y+' parish '+field,x['key'])
        h=a['historical_controls'][y];check(h['state_candidate_vector']==bc[y]['candidate_totals'],y+' state candidates');check(h['race_source_metadata']==bc[y]['metadata'],y+' race literal metadata')
        for i,x in enumerate(h['candidate_universe']):
            z=next(r for r in c if r['year']==y and r['choice_id']==x['choice_id'])
            check(x['header_literal'].replace(' (OTHER)',' (OTH)')==z['label'],y+' candidate literal',x['choice_id'])
            check(x['source_column']+1==int(z['source_column']),y+' header position convention',x['choice_id'])
            check(int(z['votes'])==h['state_candidate_vector'][i],y+' candidate state count',x['choice_id'])
        # Derive order only from the captured independent native source vectors, using this project's explicit tie rule.
        def key(z):return json.dumps([y,z['race_id'],z['parish_code'],z['ward'],z['precinct']],ensure_ascii=False,separators=(',',':'))
        sorted_peer=sorted(other,key=lambda z:(-z['all_candidate_votes'],key(z)))
        expected=a['all_orders'][y+'-native-votes'];check([key(z)for z in sorted_peer]==[z['key']for z in expected['order']],y+' complete native order')
        frozen_native=[json.loads(r['key'])for r in frozen_orders[y]['native_order']]
        own_semantic=[[y,z['parish_id'],z['ward_literal'],z['precinct_literal']]for z in sorted(own,key=lambda z:(-z['votes'],z['key']))]
        check(frozen_native==own_semantic,y+' exact independently frozen native source order')
        check([r['votes']for r in frozen_orders[y]['native_order']]==[r['votes']for r in expected['order']],y+' frozen native order values')
        check([r['code']for r in frozen_orders[y]['order']]==[r['key'].split(':')[1]for r in a['all_orders'][y+'-parish-votes']['order']],y+' frozen parish source order')
        for ownkind,peerkind in aliases.items():
            vector=[sum(z['candidate_votes'][i]for z in own if z['kind']==ownkind)for i in range(len(h['candidate_universe']))]
            check(vector==bc[y]['method_candidate_totals'][peerkind],y+' method candidate control '+ownkind)
        cum=0;cross=None
        for i,z in enumerate(sorted_peer,1):
            prev=cum;cum+=z['all_candidate_votes']
            if cross is None and 5*cum>=4*h['state_candidate_total']:cross={'count':i,'before':prev,'at':cum,'key':key(z)}
        check(cross['count']==expected['minimum80_count'] and cross['before']==expected['preceding_votes'] and cross['at']==expected['priority_votes'] and cross['key']==expected['crossing_key'],y+' source-vector integer crossing')
        out['years'][y]={'native_rows_compared':len(own),'parishes_compared':len(a['parish_vectors'][y]),'candidate_columns_compared':len(h['candidate_universe']),'exact_frozen_native_and_parish_source_orders':'compared','method_candidate_controls':'compared','source_order_and_crossing_from_independent_vectors':cross,'native_method_counts':dict(Counter(r['kind']for r in own))}
    out['status']='pass'if not out['differences']else'fail'
    (ROOT/'peer-source-agreement.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'differences':out['differences'][:5],'years':out['years']},indent=2))
    assert out['status']=='pass'
if __name__=='__main__':main()
