"""Independent offline checks against pinned original source bytes and adversarial fixtures."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import copy,csv,gzip,hashlib,io,json,posixpath,re,xml.etree.ElementTree as ET,zipfile
from extract_originals import originals,ROOT
from build_turnout import acquired
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
    b=(ROOT/p).read_bytes();return json.loads(gzip.decompress(b)if p.endswith('.gz')else b)
def identity(u):return (u['parish_id'],u['ward_literal'],u['precinct_literal'])
def native_check(units,expected):
    assert len(units)==len(expected)==len({identity(u)for u in units}),'coverage/uniqueness'
    assert set(map(identity,units))==set(expected),'native membership'
    for u in units:
        v=expected[identity(u)];assert u['candidate_votes']==v['votes'],'raw candidate vector'
        assert u['votes']==sum(v['votes']),'candidate denominator'
        assert u['qualified']==v['qualified'] and u['voted']==v['voted'],'null/control preservation'
def contract_check(c,units,total):
    expected=sorted(units,key=lambda u:(-u['votes'],u['key']));keys=[u['key']for u in expected]
    assert c['primary_reporting_level']=='source_native_ward_precinct_and_administrative_aggregates_disjoint','native primary level'
    assert [r['key']for r in c['full_order']]==keys,'full native order'
    assert c['historical_priority']['denominator']==total,'candidate denominator'
    cum=0;k=None
    for i,u in enumerate(expected,1):
        before=cum;cum+=u['votes'];r=c['full_order'][i-1]
        assert r['rank']==i and r['votes']==u['votes'] and r['cumulative_votes']==cum,'cumulative/rank'
        if k is None and 5*cum>=4*total:k=i;prior=before;at=cum
    assert c['historical_priority']['minimum80_count']==k,'integer minimum80'
    assert c['historical_priority']['preceding_votes']==prior and c['historical_priority']['priority_votes']==at,'preceding/crossing'
    assert c['ordered_priority_keys']==keys[:k] and c['canonical_native_dispatch']==keys[:k],'native dispatch membership'
    assert c['ordered_remainder_keys']==keys[k:],'remainder'
    assert len(c['all_parishes'])==64 and len({p['key']for p in c['all_parishes']})==64,'parent uniqueness'
    child=[]
    for p in c['all_parishes']:
        original=[u['key']for u in units if u['parish_key']==p['key']];ordered=[u['key']for u in expected if u['parish_key']==p['key']]
        assert p['all_native_keys_in_source_order']==original,'source child order'
        assert p['all_native_keys_in_descending_order']==ordered,'ranked child order'
        assert p['ordered_priority_native_keys']==[x for x in ordered if x in set(keys[:k])],'priority child'
        assert p['ordered_remainder_native_keys']==[x for x in ordered if x in set(keys[k:])],'remainder child'
        child+=original
    assert len(child)==len(keys) and set(child)==set(keys),'disjoint hierarchy'
    assert c['current_native_dispatch']==[] and c['coordinator_acceptance']is False,'current/acceptance qualification'
def main():
    src=originals();acq=acquired();c=load('priority-set.json');h=load('historical-controls.json');years={};expecteds={};methods=load('method-candidate-controls.json')
    M={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};rid='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
    for y in ['2024','2022','2020']:
        units=load('extract/'+y+'-native.json.gz');parishes=load('extract/'+y+'-parishes.json');code={p['parish']:p['parish_id']for p in parishes}
        rawcsv=list(csv.reader(io.StringIO(src['sos-'+y+'-selected-precinct-csv'].decode('utf-8-sig'))));expected={}
        apis={}
        for pid in code.values():
            sid=y+'-native-votes-'+pid if pid!='17'else y+'-native-votes-sample'
            rows=json.loads(acq[sid]['raw'])['Precincts']['Precinct'];assert len(rows)==len({r['Precinct']for r in rows})
            apis[pid]={r['Precinct']:r for r in rows}
        for r in rawcsv[1:]:
            if not r:continue
            office,par,ward,prec,*vs=r;pid=code[par];key=(pid,ward,prec);assert key not in expected
            ap=apis[pid][ward+'/'+prec if prec else ward];vv=list(map(int,vs));assert vv==[int(z['VoteTotal'])for z in ap['Choice']]
            expected[key]={'votes':vv,'qualified':int(ap['VoterCountQualified'])if 'VoterCountQualified'in ap else None,'voted':int(ap['VoterCountVoted'])if 'VoterCountVoted'in ap else None}
        native_check(units,expected);expecteds[y]=expected
        z=zipfile.ZipFile(io.BytesIO(src['sos-'+y+'-full-results-xlsx']));assert z.testzip()is None
        wb=ET.fromstring(z.read('xl/workbook.xml'));rels={r.attrib['Id']:r.attrib['Target']for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        footer=[]
        for s in list(wb.find('m:sheets',M))[:2]:
            t=rels[s.attrib[rid]];member=t.lstrip('/')if t.startswith('/')else posixpath.normpath('xl/'+t)
            rs=[]
            for row in ET.fromstring(z.read(member)).findall('m:sheetData/m:row',M):
                vals=[]
                for cell in row:
                    if cell.attrib.get('t')=='inlineStr':v=''.join(cell.find('m:is',M).itertext())
                    else:v=cell.findtext('m:v',None,M)
                    vals.append(v)
                rs.append(vals)
            i=rs.index([h[y]['contest']]);assert rs[i+2][0]=='Total Votes';footer.append(list(map(int,rs[i+2][1:])))
        sums=[sum(u['candidate_votes'][i]for u in units)for i in range(len(footer[0]))]
        assert footer[0]==footer[1]==sums==h[y]['state_candidate_vector']
        mv=methods[y]['method_vectors']
        for kind,vector in mv.items():assert vector==[sum(u['candidate_votes'][i]for u in units if u['kind']==kind)for i in range(len(sums))]
        assert [sum(vector[i]for vector in mv.values())for i in range(len(sums))]==sums
        assert len(parishes)==64 and len(set(p['fips']for p in parishes))==64
        for p in parishes:
            children=[u for u in units if u['parish_key']==p['key']]
            assert [sum(u['candidate_votes'][i]for u in children)for i in range(len(sums))]==p['candidate_votes']
            assert all(u['blank']is None and u['overvotes']is None and u['undervotes']is None and u['ballots_cast']is None for u in children)
        for field in ['votes','voted','qualified','race_voted','race_qualified','early_votes','provisional_votes','ordinary_votes']:
            rows=list(csv.DictReader((ROOT/'orders'/f'{y}-parish-{field}.csv').open()))
            expected_order=sorted(parishes,key=lambda p:(-p[field],p['key']));assert [r['key']for r in rows]==[p['key']for p in expected_order]
            total=sum(p[field]for p in expected_order);cum=0
            for r,p in zip(rows,expected_order):
                cum+=p[field];assert int(r['votes'])==p[field] and int(r['cumulative_votes'])==cum
                assert Fraction(r['share'])==Fraction(p[field],total) and Fraction(r['cumulative_share'])==Fraction(cum,total)
            assert sum(Fraction(r['share'])for r in rows)==1
        ordered=list(csv.DictReader((ROOT/'orders'/f'{y}-native-votes.csv').open()));assert [r['key']for r in ordered]==[u['key']for u in sorted(units,key=lambda u:(-u['votes'],u['key']))]
        years[y]={'parishes':64,'native_rows':len(units),'candidate_columns':len(sums),'state_candidate_total':sum(sums),
                  'missing_ordinary_controls':sum(u['qualified']is None for u in units if u['kind']=='ward_precinct_source_row'),
                  'native_kind_counts':dict(Counter(u['kind']for u in units)),'source_csv_api_xlsx_candidate_reconciliation':'pass'}
    units=load('extract/2024-native.json.gz');contract_check(c,units,sum(h['2024']['state_candidate_vector']))
    assert c['historical_priority']['top15_votes']==sum(u['votes']for u in sorted(units,key=lambda u:(-u['votes'],u['key']))[:15])
    assert load('peer-source-agreement.json')['status']=='pass'
    # Negative fixtures are exact patches against frozen source/contract inputs; saved before execution.
    fixtures=[('missing-unit','native','remove_last'),('duplicate-unit','native','duplicate_last'),('balanced-candidate-transfer','native','transfer'),('invented-null-zero','native','null_zero'),('lost-administrative-aggregate','native','remove_early'),('parish-dispatch-substitution','contract','parish_dispatch'),('wrong-ballot-denominator','contract','denominator'),('minimum80-off-by-one','contract','minimum'),('swapped-native-order','contract','swap')]
    tests=[];fd=ROOT/'qa-fixtures';fd.mkdir(exist_ok=True)
    for name,kind,op in fixtures:
        spec={'name':name,'kind':kind,'operation':op,'base_native_path':'extract/2024-native.json.gz','base_native_sha256':sha((ROOT/'extract/2024-native.json.gz').read_bytes()),'base_contract_sha256':sha((ROOT/'priority-set.json').read_bytes()),'expected':'reject'}
        (fd/(name+'.input.json')).write_text(json.dumps(spec,indent=2)+'\n')
        try:
            if kind=='native':
                u=copy.deepcopy(units)
                if op=='remove_last':u.pop()
                elif op=='duplicate_last':u.append(copy.deepcopy(u[-1]))
                elif op=='remove_early':u.pop(next(i for i,x in enumerate(u)if x['kind']=='early_voting_aggregate'))
                elif op=='null_zero':next(x for x in u if x['qualified']is None)['qualified']=0
                elif op=='transfer':u[0]['candidate_votes'][0]+=1;u[1]['candidate_votes'][0]-=1;u[0]['votes']+=1;u[1]['votes']-=1
                native_check(u,expecteds['2024'])
            else:
                cc=copy.deepcopy(c)
                if op=='parish_dispatch':cc['canonical_native_dispatch']=cc['parish_sensitivity']['priority_keys']
                elif op=='denominator':cc['historical_priority']['denominator']=h['2024']['voted']
                elif op=='minimum':cc['historical_priority']['minimum80_count']-=1
                elif op=='swap':cc['full_order'][0],cc['full_order'][1]=cc['full_order'][1],cc['full_order'][0]
                contract_check(cc,units,h['2024']['state_candidate_total'])
        except AssertionError as e:result={'name':name,'status':'correctly_rejected','reason':str(e)}
        else:raise AssertionError('Mutation accepted: '+name)
        (fd/(name+'.result.json')).write_text(json.dumps(result,indent=2)+'\n');tests.append(result)
    allfiles=[p for p in (ROOT.parent.parent).rglob('*')if p.is_file() and (p==ROOT.parent.parent/'turnout.md' or p==ROOT.parent/'county-turnout.csv' or ROOT in p.parents)]
    assert all(p.stat().st_size<40000000 for p in allfiles),'stored artifact byte bound'
    assert not any('__pycache__'in p.parts for p in allfiles),'retained cache'
    report=(ROOT.parent.parent/'turnout.md').read_text();links=re.findall(r'\]\(([^)]+)\)',report);deferred=[]
    for link in links:
        if '://'in link or link.startswith('#'):continue
        q=ROOT.parent.parent/link.split('#')[0]
        if not q.exists():
            assert link in ['data/turnout/validation.json','data/turnout/asset-manifest.json','data/turnout/final-audit.json'],'broken relative link '+link
            deferred.append(link)
    out={'status':'pass','scope':'Offline independent source-byte checks; historical candidate/native completeness established, source control gaps retained; current legal geometry/ballots remain unavailable',
         'source_pins_verified':27,'acquisition_receipts_verified':len(load('source/acquired-pins.json')['inputs']),
         'historical_years':years,'all_native_rows_compared':sum(y['native_rows']for y in years.values()),
         'primary_native_minimum80':c['historical_priority']['minimum80_count'],'primary_native_preceding_votes':c['historical_priority']['preceding_votes'],'primary_native_priority_votes':c['historical_priority']['priority_votes'],
         'orders_checked':27,'exact_rational_weights':'sum to one','hierarchy':'all64 parents,3933 disjoint children; complete source/descending/priority/remainder arrays',
         'peer_source_schema_comparison':'pass_one_way_not_reciprocal_signoff','negative_fixtures':tests,
         'relative_links':'pass_except_final_manifest_audit_deferred_to_readonly_audit','deferred_links':deferred,
         'source_scope_discrepancies':load('statistics-scope-discrepancies.json'),'native_control_discrepancy_records':len(load('native-control-discrepancies.json')),
         'all_current_stored_assets_below_40000000':True,'coordinator_acceptance':False,'current_native_dispatch':[]}
    (ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'pass','years':years,'negative_fixtures':len(tests)},indent=2))
if __name__=='__main__':main()
