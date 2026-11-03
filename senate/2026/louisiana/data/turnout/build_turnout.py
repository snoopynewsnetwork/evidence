"""Rebuild only from exact individual original-body/receipt pins. Python standard library."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,io,json,re
from fractions import Fraction
from extract_originals import originals,ROOT

def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    (ROOT/p).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/p).write_bytes(gzip.compress(b,mtime=0) if p.endswith('.gz') else b)
def csvout(p,rows):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',newline='')as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def acquired():
    idx=json.loads((ROOT/'source/acquired-pins.json').read_bytes());result={}
    for p in idx['inputs']:
        rb=(ROOT/p['receipt']).read_bytes();assert sha(rb)==p['receipt_sha256'];r=json.loads(rb)
        if p['status']!=200:continue
        sb=(ROOT/p['body']).read_bytes();raw=gzip.decompress(sb)
        assert sha(sb)==p['stored_sha256'] and sha(raw)==p['raw_sha256'] and len(raw)==p['bytes']
        assert p['id'] not in result,'Repeated success requires explicit vintage selection'
        result[p['id']]={'raw':raw,'receipt':p['receipt'],'pin':p}
    return result
def order(rows,field):
    a=sorted(rows,key=lambda x:(-x[field],x['key']));total=sum(x[field] for x in a);cum=0;out=[]
    assert total>0
    for i,r in enumerate(a,1):
        before=cum;cum+=r[field]
        out.append({'rank':i,'key':r['key'],'name':r.get('source_native_id',r.get('parish')),
                    **({'parish':r['parish'],'parish_key':r['parish_key']} if 'source_native_id' in r else {}),'votes':r[field],
                    'cumulative_votes':cum,'share':str(Fraction(r[field],total)),
                    'cumulative_share':str(Fraction(cum,total)),'share_percent':100*r[field]/total,
                    'cumulative_percent':100*cum/total})
    k=next(i for i,x in enumerate(out,1) if 5*x['cumulative_votes']>=4*total)
    return {'denominator':total,'top15_votes':sum(x['votes'] for x in out[:15]),'top15_share':str(Fraction(sum(x['votes'] for x in out[:15]),total)),
            'minimum80_count':k,'preceding_count':k-1,'preceding_votes':out[k-2]['cumulative_votes'] if k>1 else 0,
            'crossing_key':out[k-1]['key'],'crossing_name':out[k-1]['name'],'crossing_votes':out[k-1]['votes'],
            'priority_votes':out[k-1]['cumulative_votes'],'priority_keys':[x['key'] for x in out[:k]],
            'remainder_votes':total-out[k-1]['cumulative_votes'],'remainder_keys':[x['key'] for x in out[k:]],'order':out}
def main():
    src=originals();acq=acquired()
    # Assert unchanged original-first source position witness before using its selected rows.
    witness=json.loads((ROOT/'source/original-first-witness.json').read_bytes())
    for p in witness['files']:assert sha((ROOT/p['path']).read_bytes())==p['sha256']
    original=json.loads(gzip.decompress((ROOT/'extract/source-only-selected-controls.json.gz').read_bytes()))
    client=src['sos-graphical-public-client'].decode()
    literal=client.split('parishList:[',1)[1].split(']',1)[0]
    codes={name:code for code,name in re.findall(r'\{id:"(\d\d)",name:"([^"]+)"\}',literal)}
    assert len(codes)==64
    cen=list(csv.DictReader(io.StringIO(acq['census-county-codes']['raw'].decode()),delimiter='|'))
    fips={r['COUNTYNAME'].removesuffix(' Parish').lower():r['STATEFP']+r['COUNTYFP'] for r in cen if r['STATE']=='LA'}
    assert len(fips)==64
    dates=json.loads(src['sos-graphical-election-dates'])['Dates']['Date']
    summary={};parishes_by={};natives_by={};candidate_rows=[];allorders={};allstats={};reconciliations={}
    native_control_discrepancies=[];statistics_discrepancies=[]
    for year,date in [('2024','11/05/2024'),('2022','11/08/2022'),('2020','11/03/2020')]:
        d=original[year];sw=d['worksheets'];ps=sw['Multi-Parish(Parish)'];ns=sw['Multi-Parish(Precinct)']
        assert ps['header']==ns['header'] and ps['state']==ns['state']
        meta=d['complete_race_metadata']['Races'];race=next(r for r in meta['Race'] if r['SpecificTitle']==d['contest'])
        headers=ps['header'][1:];cids=[c['ID'] for c in race['Choice']];assert len(headers)==len(cids)==len(set(cids))
        for h,c in zip(headers,race['Choice']):assert h==c['Desc'] or h.startswith(c['Desc']+' (')
        universe=[{'source_column':i+2,'choice_id':cid,'header_literal':h,'party_literal':re.search(r'\(([^()]+)\)$',h)[1]} for i,(cid,h) in enumerate(zip(cids,headers))]
        state=list(map(int,ps['state'][1:]));parishes=[]
        for r in ps['records']:
            name,*vs=r['values'];vs=list(map(int,vs));code=codes[name]
            assert name.lower() in fips
            parishes.append({'key':'LA:'+code,'parish':name,'parish_id':code,'fips':fips[name.lower()],
                'votes':sum(vs),'candidate_votes':vs,'source_row':r['row'],'source_member':ps['member'],
                'ballots_cast':None,'blank':None,'undervotes':None,'overvotes':None,'generic_writeins':None,'named_writeins':None})
        pmap={p['parish']:p for p in parishes};assert len(pmap)==len(parishes)==64
        xlookup={};parent=None
        for row in ns['records']:
            v=row['values']
            if len(v)==1 and v[0] in pmap:parent=v[0];continue
            assert parent is not None and len(v)==len(headers)+1
            k=(parent,v[0]);assert k not in xlookup;xlookup[k]=row
        csvp=[r for r in d['csv_all_records']['parish'] if r['values']];csvn=[r for r in d['csv_all_records']['precinct'] if r['values']]
        for rows,start in [(csvp,2),(csvn,4)]:assert [h.replace(' (OTHER)',' (OTH)') for h in headers]==rows[0]['values'][start:]
        assert len(csvp)-1==64
        for row in csvp[1:]:assert list(map(int,row['values'][2:]))==pmap[row['values'][1]]['candidate_votes']
        natives=[]
        for row in csvn[1:]:
            office,pname,ward,prec,*vs=row['values'];assert office==d['contest'];p=pmap[pname]
            xr=xlookup[(pname,ward+' '+prec)];vs=list(map(int,vs));assert vs==list(map(int,xr['values'][1:]))
            native=ward+'/'+prec if prec else ward
            kind={'Early Voting':'early_voting_aggregate','Provisional Votes':'provisional_aggregate'}.get(native,'ward_precinct_source_row')
            key=json.dumps([year,race['ID'],p['parish_id'],ward,prec],ensure_ascii=False,separators=(',',':'))
            natives.append({'key':key,'parish':pname,'parish_key':p['key'],'parish_id':p['parish_id'],'fips':p['fips'],
                'source_native_id':native,'ward_literal':ward,'precinct_literal':prec,'workbook_display_literal':ward+' '+prec,
                'kind':kind,'geometry_status':'unverified_historical_reporting_identity' if kind=='ward_precinct_source_row' else 'administrative_no_polygon_assigned',
                'candidate_votes':vs,'votes':sum(vs),'csv_record_ordinal':row['record_ordinal'],'csv_ending_line':row['ending_physical_line'],
                'xlsx_member':ns['member'],'xlsx_physical_row':xr['row'],
                'qualified':None,'voted':None,'blank':None,'undervotes':None,'overvotes':None,'ballots_cast':None,
                'generic_writeins':None,'named_writeins':None})
        assert len(natives)==len(xlookup)==len({u['key'] for u in natives})
        roster=json.loads(acq[year+'-ParishesInElection']['raw'])['ParishesInElection']
        rmap={r['ParishValue']:r for r in roster['Parish']};assert set(rmap)==set(codes.values())
        early=json.loads(acq[year+'-early-votes']['raw'])['EarlyVoting']
        emap={r['ParishValue']:r for r in early['Parish']};assert set(emap)==set(codes.values())
        stats=json.loads(acq[year+'-StatsParish']['raw'])['Stats'];state_stats=json.loads(acq[year+'-StatsStatewide']['raw'])['Stats']
        smap={r['Option']:r for r in stats['Parish']};assert set(smap)==set(codes.values())
        race_stats=json.loads(acq[year+'-race-stats']['raw'])['Stats'];rsmap={r['ParishValue']:r for r in race_stats['ParishLevel']['Parish']}
        for field in ['All','All_Voted']:
            assert sum(int(s[field]) for s in smap.values())==int(state_stats[field])
            assert sum(int(s[field]) for s in rsmap.values())==int(race_stats['HighLevel'][field])
        for p in parishes:
            units=[u for u in natives if u['parish_id']==p['parish_id']];assert [sum(u['candidate_votes'][j] for u in units)for j in range(len(cids))]==p['candidate_votes']
            sid=year+'-native-votes-'+p['parish_id'] if p['parish_id']!='17' else year+'-native-votes-sample'
            nr=json.loads(acq[sid]['raw'])['Precincts'];nmap={r['Precinct']:r for r in nr['Precinct']}
            assert len(nmap)==len(nr['Precinct'])==len(units)
            assert set(nmap)=={u['source_native_id']for u in units}
            for u in units:
                r=nmap[u['source_native_id']];assert [c['ID'] for c in r['Choice']]==cids
                assert list(map(lambda c:int(c['VoteTotal']),r['Choice']))==u['candidate_votes']
                u.update(native_votes_source_id=sid,native_votes_json_index=nr['Precinct'].index(r),
                         native_version_clock_literal=nr['VersionDateTime'],has_reported_literal=r.get('HasReported'),
                         qualified=int(r['VoterCountQualified']) if 'VoterCountQualified'in r else None,
                         voted=int(r['VoterCountVoted']) if 'VoterCountVoted'in r else None)
            normal=[u for u in units if u['kind']=='ward_precinct_source_row']
            assert len(normal)==int(rmap[p['parish_id']]['Precincts'])
            for field in ['All','All_Voted']:
                if smap[p['parish_id']][field]!=rsmap[p['parish_id']][field]:
                    statistics_discrepancies.append({'year':year,'parish_key':p['key'],'field':field,'general_statistics':int(smap[p['parish_id']][field]),'selected_race_statistics':int(rsmap[p['parish_id']][field]),'race_minus_general':int(rsmap[p['parish_id']][field])-int(smap[p['parish_id']][field])})
            p.update(qualified=int(smap[p['parish_id']]['All']),voted=int(smap[p['parish_id']]['All_Voted']),
                     race_qualified=int(rsmap[p['parish_id']]['All']),race_voted=int(rsmap[p['parish_id']]['All_Voted']),
                     registration_status='source All / VoterCountQualified; active-inactive and roll cutoff unspecified',
                     stats_write_time_literal=stats['WriteTime'],ordinary_source_rows=len(normal),administrative_source_rows=len(units)-len(normal),
                     source_precincts_literal=rmap[p['parish_id']]['Precincts'],source_precincts_reported_literal=rmap[p['parish_id']]['PrecinctsReported'],
                     source_complete_with_absentee_literal=rmap[p['parish_id']]['CompleteWithAbsentee'])
            for srcfield,ufield in [('All','qualified'),('All_Voted','voted')]:
                vals=[u[ufield] for u in normal]
                if any(v is None for v in vals):
                    native_control_discrepancies.append({'year':year,'parish_key':p['key'],'field':ufield,'missing_native_keys':[u['key'] for u in normal if u[ufield] is None],'native_sum':None,'parish_control':int(smap[p['parish_id']][srcfield]),'difference':None})
                    continue
                diff=sum(vals)-int(smap[p['parish_id']][srcfield])
                if diff:native_control_discrepancies.append({'year':year,'parish_key':p['key'],'field':ufield,'native_sum':sum(vals),'parish_control':int(smap[p['parish_id']][srcfield]),'difference':diff})
            for k,kind in [('early_votes','early_voting_aggregate'),('provisional_votes','provisional_aggregate'),('ordinary_votes','ward_precinct_source_row')]:p[k]=sum(u['votes']for u in units if u['kind']==kind)
            er=emap[p['parish_id']];assert [c['ID']for c in er['Choice']]==cids
            ev=next(u['candidate_votes']for u in units if u['kind']=='early_voting_aggregate')
            assert [int(c['VoteTotal']) for c in er['Choice']]==ev
        assert [sum(p['candidate_votes'][j]for p in parishes)for j in range(len(cids))]==state
        e=next(e for e in dates if e['ElectionDate']==date);assert e['ResultsOfficial']=='1'
        total=sum(state)
        for i,c in enumerate(universe):candidate_rows.append({'year':year,'contest':d['contest'],'race_id':race['ID'],**c,'state_votes':state[i],
            'sum_parish_votes':sum(p['candidate_votes'][i]for p in parishes),'sum_native_votes':sum(u['candidate_votes'][i]for u in natives)})
        for field in ['votes','voted','qualified','race_voted','race_qualified','early_votes','provisional_votes','ordinary_votes']:allorders[year+'-parish-'+field]=order(parishes,field)
        allorders[year+'-native-votes']=order(natives,'votes')
        summary[year]={'contest':d['contest'],'date':date,'election_source_metadata':e,'race_id':race['ID'],'race_source_metadata':race,
            'race_metadata_WriteTime':meta['WriteTime'],'candidate_universe':universe,'state_candidate_vector':state,'state_candidate_total':total,
            'parishes':len(parishes),'native_rows':len(natives),'native_kinds':dict(Counter(u['kind']for u in natives)),
            'qualified':int(state_stats['All']),'voted':int(state_stats['All_Voted']),
            'race_qualified':int(race_stats['HighLevel']['All']),'race_voted':int(race_stats['HighLevel']['All_Voted']),
            'voted_minus_candidate_votes':int(state_stats['All_Voted'])-total,
            'stats_state_WriteTime':state_stats['WriteTime'],'stats_parish_WriteTime':stats['WriteTime'],
            'winner_header':headers[state.index(max(state))],'winner_votes':max(state),'winner_share':str(Fraction(max(state),total)),
            'historical_majority_no_runoff':year in ['2020','2022'] and 2*max(state)>total,
            'ballots_cast':None,'blank':None,'undervotes':None,'overvotes':None,'generic_writeins':None,'named_writeins':None}
        parishes_by[year]=parishes;natives_by[year]=natives
        allstats[year]={'state':state_stats,'parish':stats,'race':race_stats,'early':early,'native_stats_sample':json.loads(acq[year+'-native-stats-sample']['raw']),
            'scope':'Whole source JSON retained. Demographic cells not a separate analytical assignment; VoterCountQualified/VoterCountVoted are distinct source controls, not candidate votes.'}
        write('extract/'+year+'-parishes.json',parishes);write('extract/'+year+'-native.json.gz',natives)
    write('historical-controls.json',summary);write('source-statistics-controls.json.gz',allstats)
    write('method-candidate-controls.json',{
        y:{'race_id':summary[y]['race_id'],'choice_ids':[u['choice_id']for u in summary[y]['candidate_universe']],
           'source_scope':'Disjoint candidate vectors by literal reporting row kind; early composition/ballot methods not inferred',
           'method_vectors':{kind:[sum(u['candidate_votes'][j] for u in natives_by[y] if u['kind']==kind)for j in range(len(summary[y]['candidate_universe']))]for kind in ['ward_precinct_source_row','early_voting_aggregate','provisional_aggregate']}}
        for y in summary})
    write('native-control-discrepancies.json',native_control_discrepancies);write('statistics-scope-discrepancies.json',statistics_discrepancies);csvout('candidate-controls.csv',candidate_rows)
    for name,o in allorders.items():csvout('orders/'+name+'.csv',o['order'])
    write('orders-summary.json',{k:{a:b for a,b in v.items()if a!='order'}for k,v in allorders.items()})
    primary=allorders['2024-parish-votes'];priority=set(primary['priority_keys']);rows=[]
    for r in primary['order']:
        p=next(p for p in parishes_by['2024']if p['key']==r['key']);row={**{k:v for k,v in r.items()if k!='name'},'parish':p['parish'],'parish_id':p['parish_id'],'fips':p['fips'],'parish_sensitivity_top15':r['rank']<=15,'parish_sensitivity_priority80':p['key']in priority}
        native_priority=set(allorders['2024-native-votes']['priority_keys'])
        selected=[u for u in natives_by['2024'] if u['parish_key']==p['key'] and u['key']in native_priority]
        row.update(native_primary_priority_child_count=len(selected),native_primary_priority_child_votes=sum(u['votes'] for u in selected))
        for y in ['2024','2022','2020']:
            q=next(q for q in parishes_by[y]if q['key']==p['key'])
            for field in ['votes','qualified','voted','race_qualified','race_voted','early_votes','provisional_votes','ordinary_votes','ballots_cast','blank','undervotes','overvotes','generic_writeins','named_writeins']:row[y+'_'+field]=q[field]
        rows.append(row)
    csvout('../county-turnout.csv',rows)
    # This witness freezes independently derived source controls and all-unit order before peer comparison.
    stable={'historical_controls':summary,'all_orders':allorders,'parish_vectors':parishes_by,'native_vectors':natives_by}
    raw=(json.dumps(stable,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode();sp=ROOT/'source/native-primary-stable-schema.json.gz'
    if sp.exists():assert gzip.decompress(sp.read_bytes())==raw
    else:sp.write_bytes(gzip.compress(raw,mtime=0))
    parish_sensitivity=primary;primary=allorders['2024-native-votes'];native_priority=set(primary['priority_keys'])
    unitmap={u['key']:u for u in natives_by['2024']}
    parents=[]
    for p in parishes_by['2024']:
        children=[u['key'] for u in natives_by['2024'] if u['parish_key']==p['key']]
        ordered=[r['key'] for r in primary['order'] if r['key'] in set(children)]
        parents.append({**p,'all_native_keys_in_source_order':children,'all_native_keys_in_descending_order':ordered,
                       'ordered_priority_native_keys':[k for k in ordered if k in native_priority],
                       'ordered_remainder_native_keys':[k for k in ordered if k not in native_priority]})
    contract={'schema_version':2,'state':'LA','primary_election':'2024-11-05','primary_contest':'Presidential Electors','primary_race_id':'67190',
        'primary_reporting_level':'source_native_ward_precinct_and_administrative_aggregates_disjoint',
        'denominator_scope':'all returned named candidate choices; no additional write-in pool inferred',
        'historical_completeness':'64/64 parishes and all selected native candidate rows independently reconciled across XLSX/CSV/JSON',
        'peer_agent_id':'4f625056-8184-4b03-97fb-4152b00397e3',
        'peer_agreement':{'status':'one_way_independent_original_source_schema_match' if (ROOT/'peer-source-agreement.json').exists() and json.loads((ROOT/'peer-source-agreement.json').read_bytes())['status']=='pass' else 'pending',
                          'evidence':'peer-source-agreement.json','reciprocal_peer_audit':'not_claimed'},
        'coordinator_acceptance':False,'dispatch_status':'historical_source_universe_complete_pending_peer_and_coordinator_acceptance',
        'canonical_native_dispatch':primary['priority_keys'],'canonical_parish_dispatch':None,
        'current_native_dispatch':[],'current_native_scope':'No approved November2026 reporting identity/geometry equivalence established.',
        'historical_priority':primary,'ordered_priority_keys':primary['priority_keys'],'ordered_remainder_keys':primary['remainder_keys'],
        'full_order':primary['order'],'all_parishes':parents,'historical_native_constituents':natives_by['2024'],
        'priority_native_constituents':[unitmap[k] for k in primary['priority_keys']],
        'remainder_native_constituents':[unitmap[k] for k in primary['remainder_keys']],
        'parish_sensitivity':parish_sensitivity,
        'historical_native_full_order':allorders['2024-native-votes'],'all_year_native_inventory':{y:'extract/'+y+'-native.json.gz'for y in summary},
        'availability':{'ordinary_precincts':'source-native ward/precinct literal, historical only','early':'one source administrative aggregate per parish; mail/in-person composition unavailable',
            'provisional':'one source administrative aggregate per parish; no polygon or eligible remainder inferred','ballots_cast':None,'blank':None,'undervotes':None,'overvotes':None,
            'writeins':'No separate pool in selected exports. SOS disallows write-in candidates; R.S.18:1319 Federal Write-In Absentee Ballot is a separate ballot mechanism. No unknown residual allocated.',
            'current_legal_geometry':'unverified','native_registration_admin_cells':'omitted by source, retained null'},
        'stable_source_schema':{'path':'source/native-primary-stable-schema.json.gz','sha256':sha(sp.read_bytes())},
        'prior_original_first_schema_unchanged':{'path':'source/independent-stable-schema.json.gz','sha256':sha((ROOT/'source/independent-stable-schema.json.gz').read_bytes())}}
    write('priority-set.json',contract)
    print(json.dumps({'status':'built_from_individual_original_pins','primary':{k:v for k,v in primary.items()if k!='order'},'native_control_discrepancies':len(native_control_discrepancies)},indent=2))
if __name__=='__main__':main()
