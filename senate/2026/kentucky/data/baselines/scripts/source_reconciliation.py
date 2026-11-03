from pathlib import Path
import json,csv,collections
B=Path(__file__).resolve().parents[1];ROOT=B.parents[1]
def main():
 county=[r for r in csv.DictReader((ROOT/'data/county-baselines.csv').open()) if r['year']=='2024']
 units=json.loads((B/'extracted/native-known-pair-units.json').read_text())+json.loads((B/'extracted/elliott-manual.json').read_text());g=collections.defaultdict(list)
 for r in units:g[r['county'].lower()].append(r)
 cov={r['county'].lower():r for r in json.loads((B/'extracted/native-coverage.json').read_text())};rows=[]
 for c in county:
  k=c['county_literal'].lower();rr=g[k];source=cov[k]
  a=sum(r['A'] for r in rr) if rr else None;b=sum(r['B'] for r in rr) if rr else None;t=sum(r['all_candidate_printed_total'] for r in rr) if rr else None
  reason='Source-local known subset only; no full named candidate/native closure'
  if k=='scott':reason='Original10page cumulative county report; no native subdivision'
  if k=='magoffin':reason='Source TOTAL is Mail In-only; other voting methods unavailable in this body'
  if k in ('madison','laurel'):reason='Complete original/raw positioned candidate fields retained; own quantitative context parser does not establish additive full-field control, so no subset volume accepted'
  if k=='elliott':reason='All16pages independently inspected;7native blocks manually transcribed; generic/unassigned write-ins3 differ from named certificate0'
  rows.append(dict(fips=c['fips'],county_literal=c['county_literal'],source_sha256=source['source_sha256'],recap_pages=source['pages'],accepted_pair_contexts=len(rr),source_local_A=a,source_local_B=b,source_local_all=t,certificate_A=c['A'],certificate_B=c['B'],certificate_all=c['all'],A_difference=None if a is None else a-int(c['A']),B_difference=None if b is None else b-int(c['B']),all_difference=None if t is None else t-int(c['all']),reason=reason,canonical_native_complete=False))
 with (B/'source-reconciliation.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 print('county source comparisons',len(rows),'pair closing',sum(r['A_difference']==0 and r['B_difference']==0 for r in rows),'all closing',sum(r['all_difference']==0 for r in rows))
 print('differences',[(r['county_literal'],r['A_difference'],r['B_difference'],r['all_difference']) for r in rows if r['all_difference']!=0 or r['A_difference']!=0 or r['B_difference']!=0])
if __name__=='__main__':main()
