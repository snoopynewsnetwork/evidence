#!/usr/bin/env python3
import gzip,json,collections,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
fields=[json.loads(s) for s in gzip.decompress((R/'extracts/native-fields.jsonl.gz').read_bytes()).decode().splitlines()];units=collections.defaultdict(list)
for f in fields:
 if f['scope']=='president':units[f['unit_key']].append(f)
counties=collections.defaultdict(lambda:collections.Counter());issues=[]
for key,rows in units.items():
 county=rows[0]['county'];ct=next((r for r in rows if r['kind']=='cast_votes'),None)
 candidates=[r for r in rows if r['kind'] in ('candidate','writein_pool') and not r['label'].startswith('Write-In:')]
 val=lambda r:r['tokens'][-1 if r['format']=='choice' else 0]['value']
 total=sum(val(r) for r in candidates)
 if ct and val(ct)!=total:issues.append({'key':key,'cast':val(ct),'candidate_sum':total,'labels':[r['label'] for r in candidates]})
 if len(candidates)<7:issues.append({'key':key,'candidate_rows':len(candidates),'labels':[r['label'] for r in candidates]})
 counties[county]['units']+=1;counties[county]['raw_total']+=val(ct) if ct else total
 for name,needle in [('trump','TRUMP'),('harris','HARRIS')]:
  matches=[r for r in rows if needle in r['label'].upper()]
  if len(matches)!=1:issues.append({'key':key,'candidate':name,'matches':len(matches)})
  counties[county][name]+=sum(val(r) for r in matches)
cert=json.load(open(R/'extracts/certificate-fields.json'));target=collections.defaultdict(dict)
for r in cert:
 if r['contest']=='2024-president':target[r['county']][r['candidate_column']]=r['value']
target={k.casefold():v for k,v in target.items()}
for c,z in counties.items():z['trump_delta']=z['trump']-target[c.casefold()][1];z['harris_delta']=z['harris']-target[c.casefold()][2];z['total_delta']=z['raw_total']-sum(target[c.casefold()].values())
out={'unit_count':len(units),'counties':dict(sorted(counties.items())),'issues':issues}
(R/'extracts/native-diagnostic.json').write_text(json.dumps(out,indent=2)+'\n')
print('units',len(units),'counties',len(counties),'issues',len(issues));print('major deltas',[(c,z) for c,z in counties.items() if z['trump_delta'] or z['harris_delta']]);print('first issues',issues[:10])
