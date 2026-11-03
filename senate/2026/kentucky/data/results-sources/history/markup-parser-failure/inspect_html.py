import gzip,json,pathlib,html.parser,urllib.parse
BASE=pathlib.Path(__file__).resolve().parents[1]
class HTML(html.parser.HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.links=[];self.nodes=[];self.active=[];self.text=[];self.scripts=[];self.script=None;self.selects=[];self.select=None
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a':self.active.append({'tag':tag,'attrs':a,'text':''})
  if tag=='script':self.script={'attrs':a,'text':''}
  if tag=='select':self.select={'attrs':a,'options':[]}
  if tag=='option' and self.select is not None:self.select['options'].append({'attrs':a,'text':''})
  if tag in ['iframe','form','input']:self.nodes.append({'tag':tag,'attrs':a})
 def handle_endtag(self,tag):
  if tag=='a' and self.active:self.links.append(self.active.pop())
  if tag=='script' and self.script is not None:self.scripts.append(self.script);self.script=None
  if tag=='select' and self.select is not None:self.selects.append(self.select);self.select=None
 def handle_data(self,data):
  self.text.append(data)
  for a in self.active:a['text']+=data
  if self.script is not None:self.script['text']+=data
  if self.select is not None and self.select['options']:self.select['options'][-1]['text']+=data

def load(label):
 r=json.loads((BASE/'receipts'/f'{label}.json').read_bytes());h=r['hops'][-1];b=gzip.decompress((BASE/h['response_body']['path']).read_bytes());s=HTML();s.feed(b.decode('utf-8','replace'));return r,s
if __name__=='__main__':
 for name in ['state-results-public','clerk-directory-public','general-roster-public']:
  r,s=load(name);print('\n'+name)
  if name=='state-results-public':
   for t in s.scripts:
    if t['attrs'].get('src') or any(q in t['text'].lower() for q in ['ajax','result','vrsws']):print(json.dumps(t))
  elif name=='clerk-directory-public':
   for t in s.links:
    if any(q in (t['text']+' '+t['attrs'].get('href','')).lower() for q in ['clerk','directory','contactlist']):print(json.dumps(t))
  else:print(' '.join(s.text)[-6500:]);print(json.dumps(s.selects))
