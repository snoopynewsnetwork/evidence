"""Exact reviewed first-pair publication guard; current legal/live scope remains separate."""
from pathlib import Path
import json,hashlib,re,urllib.parse,sys
S=Path(__file__).resolve().parents[1];D=S/'data';N=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def ck(v,label=''):
 global N
 N+=1
 assert v,(N,label)
def read(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)}
KY=S.name=='kentucky';seals=[]
for role,num,extra in [('turnout',5008 if KY else 733,['turnout.md','data/county-turnout.csv']),('baselines',1971 if KY else 1607,['county-partisanship.md','data/county-baselines.csv'])]:
 root=D/role;m=read(root/'asset-manifest.json');rows=m['files' if KY else 'assets']
 def norm(path):return str(Path(path).relative_to('senate/2026/'+S.name)) if path.startswith('senate/2026/') else path
 ck(len(rows)==num and len({norm(r['path']) for r in rows})==num)
 ck({norm(r['path']) for r in rows}=={str(p.relative_to(S)) for p in root.rglob('*') if p.is_file() and p!=root/'asset-manifest.json'}|set(extra),'manifest-only-self exact ownership')
 for r in rows:
  p=S/norm(r['path']);b=p.read_bytes();ck(len(b)==r['bytes']<40000000 and sha(b)==r['sha256'] and not p.is_symlink(),'sealed body')
 seals.append({'role':role,'manifest':pin(root/'asset-manifest.json'),'targets':num})
reviews=['coordinator-first-pair-original-review.json','coordinator-baseline-math-review.json','coordinator-baseline-cli-review.json','coordinator-turnout-reciprocal-final-review.json','coordinator-source-acceptance-validation.json','coordinator-first-pair-command-review.json']
if KY:reviews.append('coordinator-first-pair-history-and-visual-review.json')
else:reviews.append('coordinator-turnout-isolated-replay-review.json')
for name in reviews:ck(str(read(D/name)['status']).lower().startswith('pass'),name)
c=read(D/'turnout/priority-set.json')
if KY:ck(c['dispatch_keys']==[] and all(c[k] is None for k in ['order','top15','min80','priority','remainder']) and len(c['coverage'])==120)
else:ck(len(c['historical_native_constituents'])==3933 and len(c['ordered_priority_keys'])==1516 and len(c['ordered_remainder_keys'])==2417 and c['current_native_dispatch']==[] and c['coordinator_acceptance'] is False)
links=0
for p in [S/n for n in ['README.md','research-review.md','research-dispatch.md','local-news-results.md','live-polling-strategy.md','turnout.md','county-partisanship.md']]:
 for u in re.findall(r'\[[^\]\n]*\]\(([^\n)]+)\)',p.read_text()):
  u=u.split(' "')[0].strip('<>');v=urllib.parse.urlsplit(u)
  if v.scheme or v.netloc or not v.path:continue
  ck((p.parent/urllib.parse.unquote(v.path)).exists(),(p,u));links+=1
out={'status':'pass_reviewed_first_pair_historical_sources_and_conditional_arithmetic','whole_four_question_state_complete':False,'checks':N,'producer_seals':seals,'root_reviews':[pin(D/n) for n in reviews],'current_document_links':links,'historical_native_units':None if KY else 3933,'historical_native_priority':None if KY else 1516,'current_dispatch':[],'producer_flags_untouched':True,'all_current_legal_geographic_eligible_WI_live_probability_admissions':False,'next':'Actual original questions3and4 and full state integration remain required; first-pair component publication only.'}
p=D/'coordinator-first-pair-validation.json';b=(json.dumps(out,indent=2)+'\n').encode()
if '--check' in sys.argv:ck(p.read_bytes()==b)
else:p.write_bytes(b)
print(json.dumps({'status':out['status'],'checks':N,'proof':pin(p)}))
