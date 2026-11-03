"""Compare captured stable bodies only. Never repairs owned or peer values."""
from pathlib import Path
import json,csv,gzip,collections
B=Path(__file__).resolve().parents[1]
def main():
 cap=json.loads((B/'peer/capture.json').read_text())['bodies']
 def peer(name):
  r=next(r for r in cap if r['version']=='original-first-v2' and r['peer_path']=='extracts/'+name)
  raw=gzip.decompress((B/r['body']).read_bytes());raw=gzip.decompress(raw) if name.endswith('.gz') else raw
  return [json.loads(x) for x in raw.decode().splitlines()] if name.endswith('.jsonl.gz') else json.loads(raw)
 diff=[];summary={}
 own=list(csv.DictReader((B/'extracted/certificate-fields.csv').open()));pf=peer('certificate-fields.json')+peer('certificate-controls.json')
 om={(r['source_sha256'],int(r['page']),int(r['line']),int(r['column'])):r for r in own}
 pm={(r['source_sha256'],r['page'],r['line'],r['candidate_column']):r for r in pf};assert len(om)==len(own) and len(pm)==len(pf)
 cs={(r['source_sha256'],r['column']):r for r in json.loads((B/'extracted/candidates.json').read_text())}
 for k in sorted(set(om)|set(pm)):
  a=om.get(k);p=pm.get(k)
  if a is None or p is None:diff.append(dict(kind='certificate coverage',key=k,own=a,peer=p));continue
  for af,pfkey in [('votes','value'),('raw_token','raw_token'),('char_start','character_start'),('raw_line','raw_line')]:
   av=int(a[af]) if af in ('votes','char_start') else a[af]
   if av!=p[pfkey]:diff.append(dict(kind='certificate field',key=k,field=af,own=av,peer=p[pfkey]))
  c=cs[(k[0],k[3])]
  for af,pfkey in [('name','candidate'),('party','party_or_ballot_label'),('running_mate','running_mate')]:
   if c[af]!=p[pfkey]:diff.append(dict(kind='certificate identity display',key=k,field=af,own=c[af],peer=p[pfkey]))
 summary['certificate']=dict(own_positions=len(om),peer_positions=len(pm),differences=len(diff),whole_county_order=[]) 
 # All120 county descending order and exact integer80 recomputed independently from captured peer cells.
 g=collections.defaultdict(int)
 for r in peer('certificate-fields.json'):
  if r['contest']=='2024-president':g[r['county']]+=r['value']
 order=sorted(g,key=lambda c:(-g[c],c));ownorder=list(csv.DictReader((B/'county-order.csv').open()));ownnames=[r['county_literal'] for r in ownorder]
 total=sum(g.values());cum=0;cross=None
 for i,c in enumerate(order,1):
  cum+=g[c]
  if cross is None and 5*cum>=4*total:cross=i;crossvotes=cum;prior=cum-g[c]
 summary['county_order80']=dict(equal_full120_order=order==ownnames,peer_order=order,own_order=ownnames,total=total,top15=sum(g[c] for c in order[:15]),minimum80=cross,crossing=crossvotes,previous=prior,canonical_native_contract='NULL/EMPTY; no complete native priority in either captured original-first witness; final peer priority not captured or assumed')
 oh={(r['source_sha256'],r['page']):r['raw_header_lines'] for r in json.loads((B/'extracted/certificate-headers.json').read_text())}
 ph={(r['source_sha256'],r['page']):r['raw_lines'] for r in peer('certificate-headers.json')}
 hd=[]
 for k in sorted(set(oh)|set(ph)):
  if oh.get(k)!=ph.get(k):hd.append(dict(key=k,own=oh.get(k),peer=ph.get(k)))
 summary['headers']=dict(pages=len(oh),differences=len(hd));diff.extend(dict(kind='header',**r) for r in hd)
 ownnative=[json.loads(x) for x in gzip.decompress((B/'extracted/native-observations.jsonl.gz').read_bytes()).decode().splitlines()]
 on={(r['source_sha256'],r['page'],r['line']):r for r in ownnative};pn=peer('native-fields.jsonl.gz');pm={(r['source_sha256'],r['page'],r['line']):r for r in pn}
 nd=collections.Counter();matched=0
 for k in sorted(set(on)|set(pm)):
  a=on.get(k);p=pm.get(k)
  if a is None or p is None:
   kind='peer-only native row' if a is None else 'own-only native context row';nd[kind]+=1;diff.append(dict(kind=kind,key=k,own=a,peer=p));continue
  matched+=1
  if a['raw']!=p['raw_line']:nd['raw line difference']+=1;diff.append(dict(kind='native raw line',key=k,own=a['raw'],peer=p['raw_line']))
  if a['unit_literal']!=p['native_label']:nd['unit label difference']+=1;diff.append(dict(kind='native literal unit',key=k,own=a['unit_literal'],peer=p['native_label']))
  for t in p['tokens']:
   exact=any(x['raw']==t['raw_token'] and x['start']==t['start'] and x['end']==t['end'] for x in a['tokens'])
   if not exact:nd['token selection/position difference']+=1;diff.append(dict(kind='native token',key=k,peer=t,own_tokens=a['tokens']))
 summary['native']=dict(own_observation_rows=len(on),peer_field_rows=len(pm),common_source_positions=matched,differences=dict(nd),comparison='Exact hash/page/line/raw text/literal label/count-token byte positions; schemas differ in inclusion of context/admin/header/percentage tokens. Full differences retained, no adoption.')
 # Independently hand-read Elliott candidates, total, registration and ballots.
 em=json.loads((B/'extracted/elliott-manual.json').read_text());pe=peer('elliott-manual-fields.json');ed=[];n=0
 for r in em:
  rs=[z for z in pe if z['page']==r['page']]
  for name,v in zip(r['candidate_source_order'],r['source_values']):
   # labels may differ in manual case/continuation; compare source order for eight president rows.
   pass
  president=[z for z in rs if z['scope']=='president' and z['kind'] in ('candidate','writein_pool','writein_unassigned','writein_named')]
  actual=[z['tokens'][0]['value'] for z in president]
  if actual!=r['source_values']:ed.append(dict(page=r['page'],own=r['source_values'],peer=actual))
  for kind,field in [('cast_votes','all_candidate_printed_total'),('registration','registered'),('ballots','ballots_cast'),('blank','blank_ballots')]:
   val=[z['tokens'][0]['value'] for z in rs if z['kind']==kind]
   if val!=[r[field]]:ed.append(dict(page=r['page'],field=field,own=r[field],peer=val))
  n+=len(r['source_values'])
 summary['elliott']=dict(compared_presidential_candidate_pool_child_positions=n,differences=ed,source_generic_pool='Never equated to named write-ins; native generic3 versus certificate named0 remains source-scoped')
 # Complete source-position statistics compare raw rows (not inferred candidate choices).
 stats=peer('statistics-fields.json');ownstats=[json.loads(x) for x in gzip.decompress((B/'extracted/turnout-registration-positioned-controls.jsonl.gz').read_bytes()).decode().splitlines()];sm={(r['source_sha256'],r['page'],r['line']):r for r in ownstats};sc=collections.Counter()
 for p in stats:
  k=(p['source_sha256'],p['page'],p['line']);a=sm.get(k)
  if a is None:sc['peer source-position not in own selected controls']+=1
  elif a['raw']!=p['raw_line']:sc['raw row difference']+=1;diff.append(dict(kind='statistics raw row',key=k,own=a['raw'],peer=p['raw_line']))
  else:sc['exact complete raw row']+=1
 summary['statistics']=dict(sc)
 summary['limitations']='Captured only original-first/v2 stable scope, not future final equality. Peer handwriting/Jefferson-alternative bodies retained for scope comparison but not numerical input or owned repairs. Full historical candidate-native coverage unclosed; county agreement never authorizes native dispatch.'
 (B/'peer/comparison.json').write_text(json.dumps(summary,indent=2)+'\n');(B/'peer/differences.jsonl.gz').write_bytes(gzip.compress(''.join(json.dumps(x)+'\n' for x in diff).encode(),mtime=0));print(json.dumps({k:v for k,v in summary.items() if k!='county_order80'},indent=2)[:4500])
if __name__=='__main__':main()
