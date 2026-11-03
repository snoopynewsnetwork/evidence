"""Read-only original OOXML/CSV reconciliation through the published public client."""
from pathlib import Path
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
import posixpath
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

DATA = Path(__file__).resolve().parent
NEWS = DATA / 'news'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'


def main():
    manifest = json.loads((NEWS / 'manifest.json').read_bytes())
    pins = []

    def raw(sid):
        row = next(x for x in manifest if x['id'] == sid)
        stored = (NEWS / row['asset']).read_bytes()
        b = gzip.decompress(stored)
        assert hashlib.sha256(b).hexdigest() == row['raw_sha256'] and len(b) == row['bytes']
        assert hashlib.sha256(stored).hexdigest() == row['stored_sha256']
        pins.append(dict(row))
        return b

    parent = raw('sos-results-index').decode()
    runtime = raw('sos-public-runtime-script').decode()
    assert 'data-environment=""' in parent
    assert 'return url.replace(".--environment--", "")' in runtime
    assert 'https://voterportal.--environment--.sos.la.gov/graphical' in parent
    page = raw('sos-runtime-resolved-graphical').decode()
    config = raw('sos-graphical-config').decode()
    client = raw('sos-graphical-public-client').decode()
    assert '/ElectionResults/GraphicalConfig' in page
    assert 'dataUrl: \'/ElectionResults/ElectionResults/Data\'' in config
    for fragment in ['ElectionDates.htm', 'RacesCandidates_Multiparish.htm', 'getCsvFilePath:function', 'ByPrecinct', 'ByParish']:
        assert fragment in client
    dates = json.loads(raw('sos-graphical-election-dates'))['Dates']
    mode = json.loads(raw('sos-graphical-election-mode'))
    data_config = json.loads(raw('sos-graphical-data-config'))
    assert mode == {'ElectionMode': None}
    november_metadata = json.loads(raw('sos-2026-november-race-metadata'))['Races']
    november_races = november_metadata['Race']
    assert len(november_races) == len({r['ID'] for r in november_races}) == 97
    november_senate = next(r for r in november_races if r['SpecificTitle'] == 'U. S. Senator')
    assert november_senate['ID'] == '67997' and november_senate['CanHaveRunoff'] == '0'
    assert [(c['ID'], c['Desc']) for c in november_senate['Choice']] == [
        ('124654', '"Jamie" Davis (DEM)'), ('124655', 'Julia Letlow (REP)')]
    calendar = raw('sos-current-2026-calendar')
    current_dates_page = raw('sos-current-election-dates').decode()
    assert 'qualifying for candidates for party primary offices occured in January' in current_dates_page
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / 'calendar.pdf'
        p.write_bytes(calendar)
        calendar_text = subprocess.check_output(['pdftotext', '-layout', str(p), '-']).decode()
    assert 'Revised 07/2026' in calendar_text
    assert re.search(r'U\.S\. Senate General', calendar_text)
    assert 'Per Act 7 of the 2026 Regular Session' in calendar_text
    assert '2/11/2026' in calendar_text and '2/13/2026' in calendar_text
    calendar_preview = json.loads((NEWS / 'current-calendar-preview.json').read_bytes())
    preview = (DATA.parent / calendar_preview['path']).read_bytes()
    assert hashlib.sha256(preview).hexdigest() == calendar_preview['sha256']
    reports = {}
    for year, date, contest in [('2024', '11/05/2024', 'Presidential Electors'),
                                 ('2022', '11/08/2022', 'U. S. Senator'),
                                 ('2020', '11/03/2020', 'U. S. Senator')]:
        election = next(x for x in dates['Date'] if x['ElectionDate'] == date)
        assert election['ResultsOfficial'] == '1'
        z = zipfile.ZipFile(io.BytesIO(raw('sos-' + year + '-full-results-xlsx')))
        assert z.testzip() is None
        wb = ET.fromstring(z.read('xl/workbook.xml'))
        rels = {x.attrib['Id']: x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        names = [x.attrib['name'] for x in wb.find('m:sheets', NS)]
        extracted = {}
        for sheet in list(wb.find('m:sheets', NS))[:2]:
            target = rels[sheet.attrib[RID]]
            member = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            root = ET.fromstring(z.read(member))
            rows = []
            missing_addresses = 0
            for ordinal, row in enumerate(root.findall('m:sheetData/m:row', NS), 1):
                values = []
                for cell in row:
                    missing_addresses += 'r' not in cell.attrib
                    if cell.attrib.get('t') == 'inlineStr':
                        values.append(''.join(cell.find('m:is', NS).itertext()))
                    else:
                        v = cell.find('m:v', NS)
                        assert cell.attrib.get('t') not in ['s', 'e'], cell.attrib
                        values.append(v.text if v is not None else None)
                rows.append((ordinal, values))
            start = next(i for i, (_, row) in enumerate(rows) if row == [contest])
            header = rows[start + 1][1]
            state = rows[start + 2][1]
            assert state[0] == 'Total Votes'
            records = []
            for ordinal, row in rows[start + 3:]:
                if not any(x not in [None, ''] for x in row):
                    break
                records.append({'row_ordinal': ordinal, 'raw_values': row})
            extracted[sheet.attrib['name']] = {
                'source_member': member, 'relationship_target_literal': target,
                'entire_sheet_rows': len(rows), 'cells_without_r_address': missing_addresses,
                'header': header, 'state': state, 'records': records}
        parish = extracted['Multi-Parish(Parish)']
        precinct = extracted['Multi-Parish(Precinct)']
        assert parish['header'] == precinct['header'] and parish['state'] == precinct['state']
        parish_rows = {x['raw_values'][0]: x for x in parish['records']}
        assert len(parish_rows) == len(parish['records']) == 64
        width = len(parish['header'])
        unit_rows = []
        current = None
        for row in precinct['records']:
            values = row['raw_values']
            if len(values) == 1 and values[0] in parish_rows:
                current = values[0]
            else:
                assert current is not None and len(values) == width
                unit_rows.append({'parish_literal': current, 'display_unit_literal': values[0],
                                  'source_sheet_row': row['row_ordinal'],
                                  'candidate_values': list(map(int, values[1:]))})
        assert len(unit_rows) == len({(x['parish_literal'], x['display_unit_literal']) for x in unit_rows})
        assert {x['parish_literal'] for x in unit_rows} == set(parish_rows)
        for name, row in parish_rows.items():
            expected = list(map(int, row['raw_values'][1:]))
            assert [sum(u['candidate_values'][j] for u in unit_rows if u['parish_literal'] == name)
                    for j in range(width - 1)] == expected
        state_votes = list(map(int, parish['state'][1:]))
        for j, expected in enumerate(state_votes):
            assert sum(int(row['raw_values'][j + 1]) for row in parish_rows.values()) == expected
        csv_headers = {}
        csv_count = {}
        for level, start in [('parish', 2), ('precinct', 4)]:
            rows = list(csv.reader(io.StringIO(raw('sos-' + year + '-selected-' + level + '-csv').decode('utf-8-sig'))))
            header = rows[0]
            records = [x for x in rows[1:] if x]
            csv_headers[level] = header
            csv_count[level] = len(records)
            # Preserve each original header. This is only an explicit export spelling alias.
            assert [x.replace(' (OTHER)', ' (OTH)') for x in parish['header'][1:]] == header[start:]
            if level == 'parish':
                assert len(records) == 64
                for row in records:
                    assert row[0] == contest and row[1] in parish_rows
                    assert list(map(int, row[start:])) == list(map(int, parish_rows[row[1]]['raw_values'][1:]))
            else:
                lookup = {(u['parish_literal'], u['display_unit_literal']): u for u in unit_rows}
                assert len(records) == len(unit_rows)
                seen = set()
                for row in records:
                    assert row[0] == contest
                    key = (row[1], row[2] + ' ' + row[3])
                    assert key in lookup and key not in seen
                    seen.add(key)
                    assert list(map(int, row[start:])) == lookup[key]['candidate_values']
        meta = json.loads(raw('sos-' + year + '-race-metadata'))['Races']
        race = next(x for x in meta['Race'] if x['SpecificTitle'] == contest)
        assert len(race['Choice']) == width - 1
        reports[year] = {
            'election_roster_original': election, 'selected_contest_literal': contest,
            'race_metadata_original': race, 'race_metadata_WriteTime': meta.get('WriteTime'),
            'zip_member_count': len(z.infolist()), 'zip_CRC_verified': True,
            'workbook_sheet_names': names, 'selected_worksheets': extracted,
            'parishes': 64, 'native_source_unit_records': len(unit_rows),
            'native_source_units': unit_rows, 'state_candidate_total': sum(state_votes),
            'csv_headers_literal': csv_headers, 'csv_row_counts': csv_count,
            'candidate_source_scope': 'All returned named options; no additional write-in or method pool fabricated.'}
    out = {
        'status': 'pass_original_historical_source_controls_no_priority_or_current_admission',
        'authority_chain': 'Actual SOS results HTML -> linked sosscript.js production placeholder replacement -> public graphical page -> GraphicalConfig/public bundle -> returned election roster -> literal published XLSX and CSV constructors.',
        'original_source_pins': pins, 'historical_contests': reports,
        'current_setup_scope': {'default_election_date': dates['DefaultElectionDate'],
                                'ElectionMode': mode, 'raw_site_configuration': data_config,
                                'complete_race_metadata_count': len(november_races),
                                'race_metadata_WriteTime_literal': november_metadata['WriteTime'],
                                'Senate_source_metadata_original': november_senate,
                                'scope': 'DefaultNovember date, site IsLive flag and published candidate setup are not current vote admission. The anonymous source publishes Senate metadata67997 with two named choices, but no November count file was inspected or admitted. Choice IDs remain source/stage scoped, not a signed final ballot/withdrawal proof or historical join. IsClosedParty0 describes this source general setup, not nomination-stage law. Configured refresh120 is not measured cadence; static UTCoffset-5 is not legal November poll-close authority.'},
        'current_calendar_original': {'revision_literal': 'Revised 07/2026',
                                      'complete_page_rendered_and_visually_read': calendar_preview,
                                      'November3': 'U.S. Senate General/Open U.S. Representative Primary/Open Primary',
                                      'December12': 'Open U.S. Representative General/Open General/Special Primary14thStateSenatorialDistrict',
                                      'scope': 'Office-specific current calendar; not a Senate December runoff assumption or a substitute for subsequent operative statutes/orders.'},
        'retained_source_issues': [
            'Cells and rows can omit OOXML r addresses. Preserve physical XML ordinals; do not collapse blank leading cells.2020 first worksheet member is sheet.xml, not sheet1.xml; resolve relationships.',
            'Parish tabs do not cover all64 if that parish has no separate local race; multi-parish selected tables do. Views overlap and cannot be added together.',
            'CSV preserves Ward/Precinct separately; XLSX display concatenates them with a space, including trailing spaces for administrative rows. No cross-year or physical-map join follows.',
            'OTH versus OTHER is retained as an explicit source export label alias. Running-mate/candidate strings remain literal, including Stein/AjamuBaraka in2024; legal identity needs independent source review.',
            'Historical metadata WriteTime is a2026 republication clock, not election-night cadence or certification chronology.',
            '2026 Senate follows the current closed-party-primary/plurality-general office rule; do not carry historical open-primary/runoff flags into current Senate.',
            'The retained current election-date HTML says party-primary qualifying occurred in January, while the July-revised calendar lists February11–13 for the May16 party primary. Preserve both publications and their clocks; cause, amendment sequence and controlling qualifying chronology are not established by this preparation.'
        ]
    }
    (DATA / 'coordinator-primary-preflight.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'status': out['status'], 'historical_parish_contests': 192,
                      'native_source_units': {k:v['native_source_unit_records'] for k,v in reports.items()},
                      'state_candidate_totals': {k:v['state_candidate_total'] for k,v in reports.items()}}))


if __name__ == '__main__':
    main()
