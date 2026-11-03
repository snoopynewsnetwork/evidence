"""Reconstruct whole native JSON features; affine preview derivatives only."""
from common import *
import math,struct,collections,sys,html
from shapely.geometry import Polygon,MultiPolygon
from shapely.validation import explain_validity
from shapely.strtree import STRtree
import shapely

def load_features():
 idx=strict((ROOT/'source/sbe-city-overlay-complete-index.json').read_bytes());fs=[];sr=None
 metadata=strict(body(ROOT/idx['controls']['before']['layer']['hops'][-1]['entity']['path']))
 fields={x['name'] for x in metadata['fields']};allids=[]
 for batch in idx['batches']:
  x=strict(body(ROOT/batch['response']['hops'][-1]['entity']['path']));assert 'error' not in x
  assert len(batch['requested_ids'])<=50
  ids=[f['attributes'][idx['object_id_field']] for f in x['features']];assert ids==batch['returned_ids_in_source_order'] and set(ids)==set(batch['requested_ids'])
  assert not set(ids)&set(allids);allids+=ids
  if sr is None:sr=x['spatialReference']
  assert x['spatialReference']==sr
  for f in x['features']:assert set(f['attributes'])==fields
  fs+=x['features']
 assert len(fs)==idx['total_features']==len(set(allids))
 before=strict(body(ROOT/idx['controls']['before']['ids']['hops'][-1]['entity']['path']))
 after=strict(body(ROOT/idx['controls']['after']['ids']['hops'][-1]['entity']['path']))
 assert set(allids)==set(before['objectIds'])==set(after['objectIds'])
 return idx,metadata,sr,fs

def classify(f):
 g=f.get('geometry');d={'object_id':f['attributes']['OBJECTID'],'geometry_kind':'null' if g is None else 'native_json','preview_eligible':False,'linear_topology_eligible':False,'ring_diagnostics':[]}
 if g is None:return d,None
 d['native_geometry_complete_semantic_sha256']=sem(g)
 if 'curveRings' in g or 'curvePaths' in g:d['geometry_kind']='native_truecurves';return d,None
 rings=g.get('rings')
 if not rings:d['geometry_kind']='empty_or_other';return d,None
 d['coordinate_positions']=sum(len(r) for r in rings);d['coordinate_values']=sum(len(p) for r in rings for p in r)
 bitstream=b''.join(struct.pack('>d',float(v)) for r in rings for p in r for v in p);d['all_ordered_coordinate_ieee754_sha256']=sha(bitstream)
 allfinite=all(len(p)>=2 and all(math.isfinite(v) for v in p) for r in rings for p in r)
 d['all_coordinates_finite']=allfinite
 if not allfinite:return d,None
 d['preview_eligible']=True
 linearok=all(len(r)>=4 and r[0]==r[-1] for r in rings);d['linear_topology_eligible']=linearok
 shells=[];holes=[]
 for i,r in enumerate(rings):
  rd={'ring':i,'positions':len(r),'coordinate_dimensions':sorted(set(len(p) for p in r)),'closed_full_coordinate':bool(r) and r[0]==r[-1]};d['ring_diagnostics'].append(rd)
  if len(r)<4 or r[0]!=r[-1]:rd['validity']='Excluded: short or open ring. No closure added.';continue
  poly=Polygon([p[:2] for p in r]);rd['validity']=explain_validity(poly);rd['valid']=bool(poly.is_valid)
  area=sum(r[j][0]*r[j+1][1]-r[j+1][0]*r[j][1] for j in range(len(r)-1))/2
  rd['signed_area_diagnostic']=area
  (shells if area<0 else holes).append((r,poly))
 if not linearok:return d,None
 # Diagnostic adapter uses Esri ring orientation. No source coordinates reordered or repaired.
 assignments=[[] for _ in shells];unassigned=0
 for r,p in holes:
  candidates=[(s.area,i) for i,(_,s) in enumerate(shells) if s.is_valid and p.is_valid and s.covers(p)]
  if not candidates:unassigned+=1
  else:assignments[min(candidates)[1]].append([x[:2] for x in r])
 d['unassigned_orientation_holes']=unassigned
 if unassigned or not shells:return d,None
 polys=[Polygon([x[:2] for x in r],assignments[i]) for i,(r,_) in enumerate(shells)]
 geom=polys[0] if len(polys)==1 else MultiPolygon(polys);d['feature_validity_diagnostic']=explain_validity(geom);d['feature_valid']=bool(geom.is_valid)
 return d,geom if geom.is_valid and not geom.is_empty else None

def svg(fs,title):
 visible=[f for f in fs if classify_preview(f)]
 pts=[p for f in visible for r in f['geometry']['rings'] for p in r]
 if not pts:return '<svg xmlns="http://www.w3.org/2000/svg"><text y="20">No supported linear geometry</text></svg>'
 lo=[min(p[k] for p in pts) for k in [0,1]];hi=[max(p[k] for p in pts) for k in [0,1]];scale=min(920/max(hi[0]-lo[0],1),680/max(hi[1]-lo[1],1))
 out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 780"><rect width="1000" height="780" fill="white"/>',f'<text x="20" y="24" font-size="18">{html.escape(title)}</text><text x="20" y="48" font-size="12">Native source polygons · affine preview · no legal/results match approved</text>']
 for f in visible:
  g=f['geometry'];rings=g['rings'];commands=[]
  for r in rings:
   if not r:continue
   commands.append('M '+' L '.join(repr(40+(p[0]-lo[0])*scale)+' '+repr(740-(p[1]-lo[1])*scale) for p in r))
  closed=all(r and r[0]==r[-1] for r in rings)
  color=['#bfdbe2','#d5e4c6','#f0dbaf','#d4cde6','#e7cbd0'][f['attributes']['OBJECTID']%5]
  out.append('<path d="'+' '.join(commands)+'" fill="'+(color if closed else 'none')+'" fill-rule="evenodd" stroke="#485b60" stroke-width="0.45"><title>'+html.escape(str(f['attributes']))+'</title></path>')
 out.append('</svg>');return '\n'.join(out)
def classify_preview(f):
 g=f.get('geometry')
 return g is not None and not any(k in g for k in ['curveRings','curvePaths']) and bool(g.get('rings')) and all(len(p)>=2 and all(math.isfinite(v) for v in p) for r in g['rings'] for p in r)

def main(out):
 idx,metadata,sr,fs=load_features();groups=collections.defaultdict(list)
 known={r['fips']:r['county'] for r in structured(STATE/'data/turnout/extracts/county-fips.json')}
 diagnostics=[];geoms=[];geo_ids=[]
 for f in fs:
  fips=str(f['attributes']['F_State_County_FIPS']);groups[fips].append(f)
  d,geom=classify(f);diagnostics.append(d)
  if geom is not None:geoms.append(geom);geo_ids.append(d['object_id'])
 assert set(known)<=set(groups)
 for unknown in set(groups)-set(known):known[unknown]='Unassigned source county '+unknown
 overlaps=[]
 if geoms:
  tree=STRtree(geoms)
  for i,g in enumerate(geoms):
   for j in tree.query(g):
    j=int(j)
    if j<=i:continue
    area=g.intersection(geoms[j]).area
    if area>0:overlaps.append({'object_ids':[geo_ids[i],geo_ids[j]],'intersection_area_in_native_crs_units_squared':area})
 for fips,county in known.items():
  path=out/'native'/f'{fips}.json.gz';path.parent.mkdir(parents=True,exist_ok=True)
  b=canonical({'dataset':'sbe_vtd_cities_260827','scope':'Whole returned features assigned by literal source county FIPS; city-overlay records can split precincts. Not a native-result crosswalk.','spatialReference':sr,'metadata':metadata,'features':groups[fips]});z=gzip.compress(b,mtime=0);assert len(z)<40000000;path.write_bytes(z)
  p=out/'previews'/f'{fips}.svg';p.parent.mkdir(parents=True,exist_ok=True);b=svg(groups[fips],county+' · SBE/DGI compiled precinct/city layer').encode();assert len(b)<40000000;p.write_bytes(b)
 summary={'features':len(fs),'county_or_unassigned_groups':len(groups),'qualified_counties':120,'unassigned_source_features':sum(len(v) for k,v in groups.items() if k not in {r['fips'] for r in structured(STATE/'data/turnout/extracts/county-fips.json')}),'spatialReference':sr,'coordinate_positions':sum(d.get('coordinate_positions',0) for d in diagnostics),'truecurve_features':sum(d['geometry_kind']=='native_truecurves' for d in diagnostics),'null_geometry':sum(d['geometry_kind']=='null' for d in diagnostics),'empty_or_other_geometry':sum(d['geometry_kind']=='empty_or_other' for d in diagnostics),'linear_preview_features':sum(d['preview_eligible'] for d in diagnostics),'invalid_feature_geometries':sum(d.get('feature_valid') is False for d in diagnostics),'overlap_pairs':len(overlaps),'shapely_version':shapely.__version__,'binary_shapefile_audit':None,'binary_audit_scope':'No ZIP/SHP acquired. JSON-only sources; no binary audit claimed.','diagnostic_adapter':'Native Esri clockwise-shell/counterclockwise-hole convention; no ring reversal, closure, coordinate reduction or repair. XY-only diagnostic geometry excludes whole curve/null/open/unsupported features. All source ordinates/order remain in originals and native packets.','county_counts':{k:{'features':len(v),'distinct_source_precinct_ids':len(set(f['attributes']['F_Precinct_ID'] for f in v)),'county':known[k]} for k,v in groups.items()}}
 save(out/'geometry/summary.json',summary);save(out/'geometry/feature-diagnostics.json',diagnostics);save(out/'geometry/overlap-diagnostics.json',overlaps);print(summary)
if __name__=='__main__':main(pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT)
