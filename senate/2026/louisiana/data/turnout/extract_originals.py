"""Offline source-only whole-body/physical-position witness; stdlib OOXML, no prepared data."""
from pathlib import Path
import csv, datetime, gzip, hashlib, io, json, posixpath, xml.etree.ElementTree as ET, zipfile
ROOT=Path(__file__).resolve().parent
M={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
def sha(b): return hashlib.sha256(b).hexdigest()
def put(p,obj):
    b=(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n').encode()
    (ROOT/p).write_bytes(gzip.compress(b,mtime=0))
def originals():
    pins=json.loads((ROOT/'source/original-pins.json').read_bytes())
    result={}
    for p in pins['inputs']:
        rb=(ROOT/p['receipt']).read_bytes(); assert sha(rb)==p['receipt_sha256']
        r=json.loads(rb); b=(ROOT/p['body']).read_bytes()
        assert sha(b)==p['stored_sha256']==r['stored_sha256']
        raw=gzip.decompress(b); assert sha(raw)==p['raw_sha256']==r['raw_sha256'] and len(raw)==p['bytes']
        result[p['id']]=raw
    return result
def main():
    src=originals(); files=[]; controls={}
    for year,contest in [('2024','Presidential Electors'),('2022','U. S. Senator'),('2020','U. S. Senator')]:
        sid=f'sos-{year}-full-results-xlsx'
        z=zipfile.ZipFile(io.BytesIO(src[sid])); assert z.testzip() is None
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        rel={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            shared=[''.join(t.itertext()) for t in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        sheets=[]
        for sh in wb.find('m:sheets',M):
            target=rel[sh.attrib[RID]]
            member=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
            root=ET.fromstring(z.read(member)); rows=[]
            for ri,row in enumerate(root.findall('m:sheetData/m:row',M),1):
                cells=[]
                for ci,c in enumerate(row,1):
                    v=c.find('m:v',M); val=v.text if v is not None else None
                    if c.attrib.get('t')=='inlineStr': val=''.join(c.find('m:is',M).itertext())
                    elif c.attrib.get('t')=='s': val=shared[int(val)]
                    cells.append({'physical_cell_ordinal':ci,'attributes':c.attrib,'value':val,
                                  'formula':c.findtext('m:f',None,M)})
                rows.append({'physical_row_ordinal':ri,'attributes':row.attrib,'cells':cells})
            sheets.append({'sheet_attributes':sh.attrib,'relationship_target_literal':target,'member':member,'rows':rows})
        p=f'extract/{year}-whole-workbook-positions.json.gz'
        put(p,{'source_id':sid,'raw_sha256':sha(src[sid]),'members':[{'name':i.filename,'bytes':i.file_size,'CRC':i.CRC,'sha256':sha(z.read(i))} for i in z.infolist()], 'sheets':sheets});files.append(p)
        selected={}
        for s in sheets[:2]:
            rows=[[c['value'] for c in r['cells']] for r in s['rows']]
            start=rows.index([contest]); header=rows[start+1]; state=rows[start+2]
            end=start+3
            while end<len(rows) and any(v not in (None,'') for v in rows[end]): end+=1
            selected[s['sheet_attributes']['name']]={'member':s['member'],'title_physical_row':start+1,'header':header,'state':state,
                'records':[{'row':i+1,'values':rows[i]} for i in range(start+3,end)]}
        csvs={}
        for level in ['parish','precinct']:
            raw=src[f'sos-{year}-selected-{level}-csv']
            reader=csv.reader(io.StringIO(raw.decode('utf-8-sig'),newline='')); rows=[]
            for i,r in enumerate(reader,1): rows.append({'record_ordinal':i,'ending_physical_line':reader.line_num,'values':r})
            csvs[level]=rows
        meta=json.loads(src[f'sos-{year}-race-metadata'])
        controls[year]={'contest':contest,'worksheets':selected,'csv_all_records':csvs,'complete_race_metadata':meta}
    p='extract/source-only-selected-controls.json.gz';put(p,controls);files.append(p)
    # Complete originals remain the witness for non-tabular pages and every unrelated office.
    witness={'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'phase':'independent source-only whole original, cell positions, complete selected headers/controls/native rows; before peer numerical derivatives',
             'peer_agent_id':None,'source_pins_sha256':sha((ROOT/'source/original-pins.json').read_bytes()),
             'files':[{'path':p,'sha256':sha((ROOT/p).read_bytes()),'bytes':(ROOT/p).stat().st_size} for p in files]}
    p=ROOT/'source/original-first-witness.json'
    if p.exists(): assert json.loads(p.read_bytes())['files']==witness['files']
    else:p.write_text(json.dumps(witness,indent=2)+'\n')
    print(json.dumps({'status':'source-only frozen','files':witness['files']}))
if __name__=='__main__':main()
