#!/usr/bin/env python3
"""Full parent/admin/statistical child arrays from literal original source county headers; no native joins."""
import collections,re,json,gzip
from captured_core import Capture,ROOT
O=Capture('own-pre-resume');P=Capture('peer-final');stats=O.json('data/turnout/extracts/statistics-fields.json');peer=P.jsonl('data/baselines/extracted/turnout-registration-positioned-controls.jsonl.gz');coverage=O.json('data/turnout/coverage.json');code={}
for q in stats:
 if q.get('source_county_code') and q.get('county'):
  k=q['source_county_code'];v=q['county'].casefold()
  if k in code:assert code[k]==v
  code[k]=v
own=collections.defaultdict(list);other=collections.defaultdict(list);global_admin=[];sources=collections.defaultdict(list)
for q in stats:
 if q['county']:own[q['county'].casefold()].append(q)
for q in peer:sources[q['source_sha256']].append(q)
for h,rows in sources.items():
 context=None
 for q in sorted(rows,key=lambda z:(z['page'],z['line'])):
  m=re.match(r'^\s*(\d{3})\s+([A-Z][A-Z ]+?)(?:\s{2,}|\s*$)',q['raw'])
  if m and m[1] in code:context={'source_county_code':m[1],'literal_county_header':m[2].strip(),'header_page':q['page'],'header_line':q['line'],'raw_header_line':q['raw'],'association':'same original table section only; no source-native geography join'}
  if re.match(r'^\s*(Statewide totals|Totals)\s{2,}\d',q['raw']):context=None
  record={'complete_peer_original_row':q,'literal_source_parent_context':context}
  if context is None:global_admin.append(record)
  else:other[code[context['source_county_code']]].append(record)
out=[]
for c in coverage:
 n=c['county'].casefold();out.append({'county':c['county'],'county_fips':c['fips'],'own_full_statistical_children':own[n],'peer_full_raw_statistical_children':other[n],'scope':'Original same-document county table sections. Repeated page headers inherit section context and remain administrative text, not additional counts. Raw records retained unchanged.'})
assert len(out)==120 and sum(len(z['peer_full_raw_statistical_children']) for z in out)+len(global_admin)==len(peer)
D=ROOT/'comparison'
for n,rows in [('all120-statistical-child-arrays.jsonl.gz',out),('global-statistical-administrative-rows.jsonl.gz',global_admin)]:
 b=gzip.compress(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in rows).encode(),mtime=0);assert len(b)<40000000;(D/n).write_bytes(b)
(D/'hierarchy-summary.json').write_text(json.dumps({'all120parents':len(out),'own_complete_parented_statistics':sum(len(z['own_full_statistical_children']) for z in out),'peer_complete_parented_raw_statistics':sum(len(z['peer_full_raw_statistical_children']) for z in out),'peer_global_administrative_rows':len(global_admin),'peer_full_total':len(peer),'source_native_cross_year_join':False},indent=2)+'\n');print('Full120 statistical child arrays and global admin preserved')
