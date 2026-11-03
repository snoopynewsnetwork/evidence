"""Run LAST after validation, acyclic audit proof and final seal exist."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R.parent.parent;SELF='data/turnout/asset-manifest.json'
def main():
    assert(R/'final-seal.json').is_file()and(R/'final-audit.json').is_file()
    files={str(p.relative_to(S)):p for p in R.rglob('*')if p.is_file()}|{'turnout.md':S/'turnout.md','data/county-turnout.csv':S/'data/county-turnout.csv'}
    rows=[]
    for name,p in sorted(files.items()):
        if name==SELF:continue
        b=p.read_bytes();assert len(b)<40000000 and '__pycache__'not in p.parts
        rows.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    (R/'asset-manifest.json').write_text(json.dumps({'scope':'All current exclusively owned bodies, including validation/final audit/final seal/history/proofs/fixtures. Self only excluded; no current reverse digest dependency.','excludes_only':[SELF],'assets':rows,'count':len(rows),'total_bytes':sum(x['bytes']for x in rows)},indent=2)+'\n')
    print(json.dumps({'manifest_targets':len(rows),'manifest_sha256':hashlib.sha256((R/'asset-manifest.json').read_bytes()).hexdigest()}))
if __name__=='__main__':main()
