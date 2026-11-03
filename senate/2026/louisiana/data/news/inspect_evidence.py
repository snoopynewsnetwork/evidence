#!/usr/bin/env python3
"""Verify captured response bytes and source-specific preflight observations."""
from pathlib import Path
import gzip,hashlib,json,re
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'manifest.json').read_text())
for row in rows:
 if 'asset' not in row:continue
 b=(ROOT/row['asset']).read_bytes();assert hashlib.sha256(b).hexdigest()==row['stored_sha256'],row['id']
 raw_bytes=gzip.decompress(b);assert hashlib.sha256(raw_bytes).hexdigest()==row['raw_sha256'],row['id']
def raw(name):
 row=next(r for r in rows if r['id']==name)
 return gzip.decompress((ROOT/row['asset']).read_bytes()).decode(errors='replace')
s=raw('wbrz-2026-data');decoder=json.JSONDecoder();pos=0;records=[]
while pos<len(s):
 while pos<len(s) and s[pos].isspace():pos+=1
 if pos==len(s):break
 value,end=decoder.raw_decode(s,pos);records.append(value);pos=end
assert pos==len(s) and len(records)==187
assert len({r['parish'] for r in records})==13
assert all(c['votes']==0 for r in records for c in r['candidates'])
assert len([r for r in records if r['race']=='U.S. Senator'])==1
page=raw('wbrz-election-info');assert 'https://weather.wbrz.com/2026race.json' in page and 'parseRaceFeed' in page
start=page.rfind('<script',0,page.index('var sourceUrl'));end=page.index('</script>',page.index('var sourceUrl'));script=page[start:end]
assert 'response.text()' in script and 'setInterval' not in script and 'setTimeout' not in script
assert '--environment--' in raw('sos-results-index')
assert 'greatest number of votes' in raw('sos-closed-primary')
result={'wbrz_stream_records':187,'parish_labels_including_multi':13,'all_setup_votes_zero':True,'client_timed_refresh_observed':False,'official_placeholder_links_retained':True,'usable_november_counts_established':False}
assert next(r for r in rows if r['id']=='nyt-elections')['status']==403
result.update(status='pass',retained_assets=sum('asset' in r for r in rows))
(ROOT/'inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
