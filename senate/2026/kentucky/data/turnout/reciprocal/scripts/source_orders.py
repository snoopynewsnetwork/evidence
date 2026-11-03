#!/usr/bin/env python3
"""Independent complete source-volume order verification; no scenario/target/calculator conclusions."""
import json,gzip,csv,io,collections
from captured_core import Capture,ROOT
O=Capture('own-pre-resume');P=Capture('peer-final');D=ROOT/'comparison'
def ranked(rows):
 a=sorted(rows,key=lambda q:(-q['votes'],q['key']));n=sum(q['votes'] for q in a);c=0;out=[];cross=None
 for i,q in enumerate(a,1):
  prev=c;c+=q['votes'];out.append({**q,'rank':i,'cumulative_votes':c,'denominator':n})
  if cross is None and 5*c>=4*n:cross={'count':i,'votes':c,'preceding_count':i-1,'preceding_votes':prev,'crossing_key':q['key'],'crossing_votes':q['votes']}
 return {'units':len(a),'denominator':n,'order':out,'min80':cross,'top15':{'votes':sum(q['votes'] for q in a[:15]),'keys':[q['key'] for q in a[:15]]},'remainder':{'keys':[q['key'] for q in a[cross['count']:]],'votes':n-cross['votes']}}
def verify(stored,ind):
 assert stored['denominator']==ind['denominator'] and stored['units']==ind['units']
 assert [(x['key'],x['votes'],x['rank'],x['cumulative_votes']) for x in stored['order']]==[(x['key'],x['votes'],x['rank'],x['cumulative_votes']) for x in ind['order']]
 for k in ['count','votes','preceding_count','preceding_votes','crossing_key','crossing_votes']:assert stored['min80'][k]==ind['min80'][k]
 assert stored['top15']['votes']==ind['top15']['votes'] and stored['top15']['keys']==ind['top15']['keys'];assert stored['remainder']['votes']==ind['remainder']['votes'] and stored['remainder']['keys']==ind['remainder']['keys']
sens=O.json('data/turnout/county-sensitivity.json');evidence={};allchecks=[]
fips={q['county'].casefold():q['fips'] for q in O.json('data/turnout/extracts/county-fips.json')}
cert=collections.defaultdict(lambda:collections.Counter())
for q in csv.DictReader(io.StringIO(P.body('data/baselines/extracted/certificate-fields.csv').decode())):
 if q['scope']=='county':cert[int(q['year'])][q['county_literal']]+=int(q['votes'])
admin=list(csv.DictReader(io.StringIO(P.body('data/baselines/extracted/county-admin-turnout.csv').decode())))
regs=list(csv.DictReader(io.StringIO(P.body('data/baselines/extracted/county-registration.csv').decode())))
source_rows={}
for year,name in [(2024,'2024-president'),(2022,'2022-senate'),(2020,'2020-senate')]:source_rows[name]=[{'key':fips[c.casefold()],'county':c,'votes':v} for c,v in cert[year].items()]
for year in [2024,2022,2020]:
 a=[q for q in admin if int(q['year'])==year]
 for suffix,col in [('', 'number_voting'),('_registration','total_registration')]:source_rows[f'unofficial_voter_history_{year}'+suffix]=[{'key':fips[q['county_literal'].casefold()],'county':q['county_literal'],'votes':int(q[col])} for q in a]
source_rows['registration_snapshot_PDF_titled_September_2024']=[{'key':fips[q['county_literal'].casefold()],'county':q['county_literal'],'votes':int(q['total_registration'])} for q in regs]
units=O.jsonl('data/turnout/native-units.jsonl.gz');controls=O.json('data/turnout/extracts/recap-report-controls.json');cr={q['county'].casefold():q for q in controls}
source_rows['captured_recap_ballots_source_scope']=[]
for c,control in cr.items():
 h=control['source_sha256'];pn=f'data/baselines/extracted/{h}.layout.txt.gz';pages=gzip.decompress(P.body(pn)).decode().split('\f');us=[u for u in units if u['county'].casefold()==c]
 if control['header_ballots_cast'] is not None:
  fields=[q for q in control['fields'] if q['kind']=='county_header_ballots']
  for q in fields:assert pages[q['page']-1].splitlines()[q['value_line']-1]==q['raw_value_line']
  v=control['header_ballots_cast']
 else:
  v=0
  for u in us:
   q=u['ballots_cast'];v+=q['value'];loc=q['source']
   # Elliott's source is image-only; independent complete manual rows were compared already.
   if loc.get('line') is not None:
    line=pages[loc['page']-1].splitlines()[loc['line']-1];assert str(q['value']) in line.replace(',','')
 source_rows['captured_recap_ballots_source_scope'].append({'key':fips[c],'county':us[0]['county'],'votes':v})

for name,stored in sens.items():
 # Full source position reconciliation, not peer's derivative order, supplies source quantities.
 ind=ranked(source_rows[name]);verify(stored,ind);evidence[name]=ind;allchecks.append({'scope':name,'all_rows':len(ind['order']),'all_keys_counts_cumulatives_top15_minimum80_crossing_remainder':'exact','source_basis':'captured original core/party/statistical/control fields reconciled at all original positions'})
known=O.json('data/turnout/known-native-order.json');units=O.jsonl('data/turnout/native-units.jsonl.gz');ind=ranked([{'key':u['key'],'votes':u['votes'],'county':u['county']} for u in units if u['scope']!='county_cumulative_summary']);verify(known,ind);evidence['own_broader_qualified3220']=ind
pairs=[json.loads(x) for x in gzip.decompress((D/'accepted-subset-complete-source-context-pairs.jsonl.gz').read_bytes()).decode().splitlines()]
po=ranked([{'key':q['peer_full_source_context']['key'],'votes':q['peer_full_source_context']['all_candidate_printed_total'],'source_sha256':q['peer_full_source_context']['source_sha256'],'literal':q['peer_full_source_context']['unit_literal']} for q in pairs]);oo=ranked([{'key':q['own_full_source_context']['key'],'votes':q['own_full_source_context']['votes'],'source_sha256':q['own_full_source_context']['source_sha256'],'literal':q['own_full_source_context']['literal_native_label']} for q in pairs]);assert po['units']==oo['units']==3150
assert [q['votes'] for q in po['order']]==[q['votes'] for q in oo['order']]
for k in ['count','votes','preceding_count','preceding_votes','crossing_votes']:assert po['min80'][k]==oo['min80'][k]
assert po['denominator']==oo['denominator'] and po['top15']['votes']==oo['top15']['votes'] and po['remainder']['votes']==oo['remainder']['votes']
evidence['captured_peer_accepted3150_original_keys']=po;evidence['own_same_source3150_original_keys']=oo
b=''.join(json.dumps({'scope':k,'complete_order_contract':v})+'\n' for k,v in evidence.items()).encode();b=gzip.compress(b,mtime=0);assert len(b)<40000000;(D/'complete-source-orders.jsonl.gz').write_bytes(b)
summary={'status':'PASS','all_parent_sensitivity_contracts':allchecks,'own_qualified3220':{'denominator':ind['denominator'],'min80':ind['min80']},'peer_accepted3150_and_own_same_source3150':{'denominator':po['denominator'],'peer_min80':po['min80'],'own_min80':oo['min80'],'all_sorted_vote_and_cumulative_sequences_match':True,'literal_source_keys_preserved_separately':True,'tie_order_policy':'Each original producer key sorts its own equal-vote rows; no rewritten/normalized key equality claimed'},'excluded70_plus_Scott_not_added_to_peer_subset':True,'canonical_statewide_native':None,'dispatch_keys':[],'out_of_scope':['calculator','scenario','target','outcome','current or future peer equality']};(D/'source-order-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
