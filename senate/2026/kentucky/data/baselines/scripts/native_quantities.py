from pathlib import Path
import json,gzip,re,collections
ROOT=Path(__file__).resolve().parents[3];B=ROOT/'data/baselines'
def main():
 obs=[json.loads(x) for x in gzip.decompress((B/'extracted/native-observations.jsonl.gz').read_bytes()).decode().splitlines()]
 fields=[];groups=collections.defaultdict(list)
 for o in obs:
  if not o['presidential_context']:continue
  nums=[x for x in o['tokens'] if re.fullmatch(r'\d[\d,]*',x['raw'])]
  # These remain source row positions; pools and their children never added.
  if nums and o['kind'] not in ('context',):
   o=dict(o,integer_fields=[dict(position=i+1,value=int(t['raw'].replace(',','')),raw=t['raw'],char_start=t['start']) for i,t in enumerate(nums)])
   fields.append(o)
   if o['unit_literal'] is not None:groups[(o['source_sha256'],o['county'],o['unit_literal'])].append(o)
 units=[];unresolved=[]
 for (h,c,u),rs in groups.items():
  a=[r for r in rs if 'HARRIS' in r['raw'] and 'DEM' in r['raw']];bb=[r for r in rs if 'TRUMP' in r['raw'] and 'REP' in r['raw']]
  total=[r for r in rs if re.match(r'^\s*(Cast Votes:|Total Votes Cast)',r['raw'])]
  if len(a)!=1 or len(bb)!=1 or len(total)>1:
   unresolved.append(dict(source_sha256=h,county=c,unit_literal=u,A_rows=len(a),B_rows=len(bb),total_rows=len(total)));continue
  choice='%' in a[0]['raw'];idx=-1 if choice else 0
  av=a[0]['integer_fields'][idx]['value'];bv=bb[0]['integer_fields'][idx]['value']
  total_basis='printed Total Votes Cast / Cast Votes'
  if total:tv=total[0]['integer_fields'][idx]['value']
  else:
   tops=[r for r in rs if r['kind']=='candidate'];pool=[r for r in rs if r['kind']=='overlapping write-in parent']
   if len(tops)!=6 or len(pool)!=1:
    unresolved.append(dict(source_sha256=h,county=c,unit_literal=u,reason='No printed candidate-total and complete six-choice plus write-in-parent field not established'));continue
   tv=sum(r['integer_fields'][idx]['value'] for r in tops+pool);total_basis='sum of six printed regular choices plus printed generic write-in parent; named children overlap'
  if tv<av+bv:unresolved.append(dict(source_sha256=h,county=c,unit_literal=u,reason='printed contest total smaller than pair'));continue
  units.append(dict(key=h+':literal:'+u,source_sha256=h,county=c,unit_literal=u,A=av,B=bv,all_candidate_printed_total=tv,
    pair=av+bv,pair_participation=(av+bv)/tv if tv else None,A_pair_share=av/(av+bv) if av+bv else None,
    A_row=a[0]['observation_key'],B_row=bb[0]['observation_key'],total_row=total[0]['observation_key'] if total else None,total_basis=total_basis,
    native_geographic_equivalence_2026=None,full_named_field_closure=False))
 raw=''.join(json.dumps(r)+'\n' for r in fields).encode();(B/'extracted/native-positional-fields.jsonl.gz').write_bytes(gzip.compress(raw,mtime=0))
 (B/'extracted/native-known-pair-units.json').write_text(json.dumps(units,indent=2)+'\n')
 (B/'extracted/native-unresolved-pair-contexts.json').write_text(json.dumps(unresolved,indent=2)+'\n')
 print('known source-local pair/control contexts',len(units),'unresolved',len(unresolved),'positional rows',len(fields))
if __name__=='__main__':main()
