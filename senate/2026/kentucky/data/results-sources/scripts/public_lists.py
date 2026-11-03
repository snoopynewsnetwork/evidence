import gzip,json,xml.etree.ElementTree as ET
from inspect_html import BASE,load
NS={'a':'http://www.w3.org/2005/Atom','m':'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata','d':'http://schemas.microsoft.com/ado/2007/08/dataservices'}
def element(x):return {'tag':x.tag,'attributes':dict(x.attrib),'text':x.text,'tail':x.tail,'children':[element(v) for v in x]}
def atom(label):
 r,_=load(label);b=gzip.decompress((BASE/r['hops'][-1]['response_body']['path']).read_bytes());root=ET.fromstring(b)
 return root,[{x.tag.rsplit('}',1)[-1]:(None if x.get('{'+NS['m']+'}null')=='true' else x.text if not list(x) else element(x)) for x in e.findall('./a:content/m:properties/*',NS)} for e in root.findall('a:entry',NS)]
if __name__=='__main__':
 for label in ['directory-roles','reports-2026']:
  root,rows=atom(label);print(label,'rows',len(rows),'next',[(x.get('rel'),x.get('href')) for x in root.findall('a:link',NS)]);print(json.dumps(rows[0],indent=2));
  if label=='directory-roles':print('counties',len(set(x.get('County') for x in rows)),'websites',len(set(x.get('OData__x0067_295') for x in rows)));print('fields',list(rows[0]))
