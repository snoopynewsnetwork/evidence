"""Render the owned report from independently extracted historical originals."""
import csv,gzip,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def pct(a,b):return f'{100*a/b:.8f}%'
def n(v):return f'{v:,}'
def main():
    c=json.loads((ROOT/'priority-set.json').read_bytes());h=json.loads((ROOT/'historical-controls.json').read_bytes());os=json.loads((ROOT/'orders-summary.json').read_bytes());p=c['historical_priority'];par=c['parish_sensitivity']
    s=f'''# Louisiana reported vote volume and historical native priority

Research: **2026-10-20 UTC**. The primary is **November 5, 2024 Presidential Electors**, all **{n(p['denominator'])} reported votes for the 11 source choices**, at the finest complete disjoint reporting level: **3,933 source units in all 64 parishes**. Louisiana had no 2024 Senate contest. These are candidate votes, not ballots cast, eligible voters or a 2026 turnout forecast. The originals are the SOS [complete workbook][xlsx24], [native CSV][csv24] and all 64 original native JSON responses pinned in the [individual acquired source index](data/turnout/source/acquired-pins.json), through the official [results authority][results].

**Native top 15: {n(p['top15_votes'])}/{n(p['denominator'])} = {pct(p['top15_votes'],p['denominator'])}. Minimum descending native set: {n(p['minimum80_count'])} units, {n(p['priority_votes'])} votes = {pct(p['priority_votes'],p['denominator'])}.** The preceding {n(p['preceding_count'])} units contain {n(p['preceding_votes'])} votes ({pct(p['preceding_votes'],p['denominator'])}). **Bienville parish (native code 07), ward 06 / precinct 03, contributes 299 votes and crosses 80%.** The remaining 2,417 units contain 401,326 votes ({pct(401326,p['denominator'])}). Integer proof: `5*1605350=8026750 < 4*2006975=8027900 <= 5*1605649=8028245`. A descending set of only 1,515 cannot reach the threshold. Ties use ascending literal JSON composite key `[year,race_id,parish_id,ward,precinct]`; the chosen membership among equal-volume units follows that documented rule.

The [exact historical contract](data/turnout/priority-set.json) contains all 3,933 native rows, full order, ordered 1,516-unit priority and 2,417-unit remainder, and all 64 parent arrays with source order, descending order, priority and remainder children. [Full native order](data/turnout/orders/2024-native-votes.csv) preserves each literal key; [native details](data/turnout/extract/2024-native.json.gz) retain original CSV/API/OOXML positions. **The 24-parish/Washington set is a parish sensitivity, not the native dispatch.** Every parish contributes at least one native priority child. The priority has 1,452 ward/precinct source rows plus all 64 Early Voting aggregates; it contains no Provisional Votes aggregate. No polygon is assigned to administrative aggregates.

The complete historical source universe reconciles independently, so the contract carries its proposed historical native dispatch. **Coordinator acceptance is false.** One-way comparison with the actual peer's already-frozen independent original source schema passed; reciprocal peer signoff is not claimed. November 2026 native dispatch remains empty and no current legal geometry is approved. Historical source identity and current map approval are separate questions.

## Native top 15

All 15 are the source's **Early Voting** administrative row, not wards, polling sites or separately geolocated vote centers. Source CSV represents each as `Ward="Early Voting", Precinct=""`; XLSX concatenates a trailing space. The original source does not split their composition into early in-person and absentee mail. Their votes are disjoint from the separately published ordinary and provisional candidate rows. Sources: [native CSV][csv24], [workbook][xlsx24], [sample original native JSON][native24]; all parish originals and receipts are pinned, not just the sample.

| Rank | Parish/native parent | Native source label | Candidate votes | State share | Cumulative share |
| ---: | --- | --- | ---: | ---: | ---: |
'''
    for r in p['order'][:15]:s+=f"| {r['rank']} | {r['parish']} | {r['name']} | {n(r['votes'])} | {r['share_percent']:.8f}% | {r['cumulative_percent']:.8f}% |\n"
    s+='''
## Source identity, universe and hierarchy

The official results parent publishes environment placeholders. Its explicitly linked [production runtime script][runtime] removes `.--environment--` when `data-environment` is empty, yielding the actual [public graphical app][app]. That app links [GraphicalConfig][config] and the [complete public client][client]. Its published date-folder constructors produce XLSX, CSV, `StatsParish`, `StatsStatewide`, `StatsRace`, `VotesEarly` and `VotesRaceByPrecinct` sources used here. No authentication, personal lookup, media credentials or November count request was used. [Original pins](data/turnout/source/original-pins.json) and [acquired pins](data/turnout/source/acquired-pins.json) preserve exact bodies, individual receipts, requested/final URLs, UTC, status, headers, stored/raw hashes and sizes. New acquisitions retain each redirect entity; legacy receipts establish final entities only, with intermediate-hop evidence unavailable.

For 2024 there are **3,805 ward/precinct rows + 64 Early Voting + 64 Provisional Votes = 3,933 disjoint candidate rows**. The corresponding counts are 3,937+64+64=4,065 in 2022 and 3,934+64+64=4,062 in 2020. Each candidate vector matches native CSV to workbook and independently downloaded native JSON; each native sum matches its parish and every parish sum the two workbook statewide control rows. The views overlap and are never added. Parish tabs do not cover the whole state in every workbook; the multi-parish tables do. [Election roster][dates] marks all three historical elections `ResultsOfficial=1`; this is the publisher's status, not an independently obtained signed certificate or certification chronology.

The actual two-character parish IDs come from the literal public-client parish list, crosschecked against all returned parish inventories. Parish FIPS come from the complete [Census official code file][fips], using explicit case-insensitive parish-name matching with the ` Parish` suffix removed; source `Lasalle` matches `LaSalle`. FIPS describe parents, not a fabricated precinct code or map crosswalk. A native key includes year, source race ID, parish ID, literal Ward and Precinct. Leading zeros, letters, embedded spaces, empty fields, source order and explicit zero counts survive. No native ID or boundary equivalence across years or to November 2026 is asserted. These rows are reporting identities; split-like suffixes do not establish ballot style, physical precinct or polling-place membership.

The [whole-workbook source witness](data/turnout/source/original-first-witness.json) preserves every sheet's physical row/cell ordinal, original attributes and blank leading cells. OOXML `r` addresses are sometimes omitted; 2020's first member is `sheet.xml`, resolved through workbook relationships. Every ZIP member's exact bytes remain reconstructible from the original workbook, with CRC, size and member hashes. Unrelated offices and demographic fields survive whole in original bytes and witnesses; they are not silently discarded or promoted into extra turnout analysis. No prepared totals were imported.

## All candidates and historical outcomes

These are complete **11/13/15-choice** first-election source fields. `OTHER` (workbook) versus `OTH` (CSV) is an explicit formatting alias, not candidate deduplication. The 2024 source's `Jill Stein, Ajamu Baraka Green` running-mate string is preserved literally, as are all other ballot/party labels; this package does not substitute national ticket labels or establish their legal ballot identity. Sources: [2024 workbook][xlsx24], [2022 workbook][xlsx22], [2020 workbook][xlsx20] and independently read metadata through the [official app][app]. [Candidate controls](data/turnout/candidate-controls.csv) retain source choice IDs, party labels and separate state/parish/native sums, with zero differences for every candidate.

| Year/contest | Literal candidate or ticket | Choice ID | State = parish sum = native sum |
| --- | --- | --- | ---: |
'''
    for y in ['2024','2022','2020']:
        d=h[y]
        for u,v in zip(d['candidate_universe'],d['state_candidate_vector']):s+=f"| {y} {'President'if y=='2024'else'Senate'} | {u['header_literal']} | {u['choice_id']} | {n(v)} |\n"
    s+='''
2020 is Cassidy's **Class II same-seat** Senate election; 2022 is Kennedy's **Class III other-seat midterm**, not a second Class II observation and not a governor election. Cassidy received 1,228,908/2,071,543 (59.32331501%); Kennedy received 851,568/1,383,290 (61.56098726%). Each exceeded half the complete field at the first election and therefore needed no Senate runoff. Historical metadata's `CanHaveRunoff=1` describes potential procedure, not an actual second round. The historical majority rule is reflected in [R.S.18:511][law511]; the raw historical fields and exact majority arithmetic are retained in [historical controls](data/turnout/historical-controls.json).

Current rules were independently inspected on October 20: the [SOS closed-party explanation][closed] describes spring majority nomination and a plurality general; its [qualifying page][qualify] expressly keeps Senate in that system while describing the Act 7 House exception. [R.S.18:512][law512] states the most-votes general rule. Historical runoff flags and the U.S. House exception are not applied to the 2026 Senate general. The retained [July-revised calendar][calendar] says Senate general November 3, while December's House stage is separately labeled. A retained [election-date HTML][electiondates] says party qualifying occurred in January; the July calendar says February 11–13. Their cause/amendment chronology is not established here.

The complete retained [November setup metadata][nov26] has Senate race 67997 with choices 124654 `"Jamie" Davis (DEM)` and 124655 `Julia Letlow (REP)`, and literal WriteTime `2026-10-18T05:00:06.330` (timezone unspecified). These are published setup identities, not genuine counts, signed final ballot/withdrawal proof or a historical candidate join. No November count file was requested. Final candidate legal identities, later statutes/orders and approved current reporting units remain precise external qualifications.

## Candidate votes, participation, registration and unavailable ballots

The exports have no separate generic/named write-in, blank, under- or overvote pools. Those fields remain **null**, not invented zeros. [SOS qualifying guidance][qualify] says Louisiana does not allow write-in candidates. [R.S.18:1319][fwab] separately permits the Federal Write-In Absentee Ballot mechanism for specified voters; that is not evidence of an additional generic candidate pool or a measured method count in these exports. The ranking therefore uses all reported named choice counts, with no allocated residual.

`All` and `All_Voted` are the public statistics' registration/participation fields; native results expose `VoterCountQualified` and `VoterCountVoted`. The app labels these registered/voted controls. This package preserves the source names, scope and republication clocks; it does not assert active-only registration, a specific roll cutoff or equivalence to tabulated ballots cast. **Exact ballots-cast and blank/under/over sensitivities are unavailable.** Differences between participation and candidate votes are not classified as undervotes. General-election statistics and selected-race statistics are retained separately. Sources: [2024 general statewide statistics][stats24], [2024 race statistics][race24], and the corresponding independently downloaded 2022/2020 originals in the [source index](data/turnout/source/acquired-pins.json).

| Year | Named candidate votes | General All_Voted | Race All_Voted | General All | Race All | General voted − candidate votes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
'''
    for y,d in h.items():s+=f"| {y} | {n(d['state_candidate_total'])} | {n(d['voted'])} | {n(d['race_voted'])} | {n(d['qualified'])} | {n(d['race_qualified'])} | {n(d['voted_minus_candidate_votes'])} |\n"
    s+='''
General parish sums exactly match their general state controls; selected-race parish sums exactly match their selected-race controls. In 2022, East Baton Rouge race participation is 10 below general participation. In 2020, race participation is 4 higher in Caddo and 9 higher in East Baton Rouge; race registration is 4 lower in Calcasieu, 2 in Lincoln, 4 in Orleans and 5 in Webster. No reconciliation adjustment or cause is inferred. [Full source-scope discrepancy ledger](data/turnout/statistics-scope-discrepancies.json).

The native result objects omit qualified/voted cells on 5 ordinary rows in 2024, 11 in 2022 and 13 in 2020, plus all administrative rows. Their explicit candidate zeros remain valid zeros while their omitted controls remain null. Native control sums are not called complete where a cell is missing; differences in complete sums against general parish controls also remain visible. The [native discrepancy ledger](data/turnout/native-control-discrepancies.json) retains keys, source totals and missing-cell lists. Every candidate/native membership still reconciles independently. Neither registration minus participation nor precincts reported supplies exact remaining eligible votes.

## Historical and method sensitivities

The native primary and its actual recent midterm comparator use complete source-native rows at each year's own vintage; they do not assert cross-year precinct equivalence. Sources: original [2024][xlsx24], [2022][xlsx22] and [2020][xlsx20] workbooks/CSV/native originals. All full orders and remainder sets are in [orders summary](data/turnout/orders-summary.json) and the [2024](data/turnout/orders/2024-native-votes.csv), [2022](data/turnout/orders/2022-native-votes.csv), [2020](data/turnout/orders/2020-native-votes.csv) native order files.

| Native field | Total votes | Top-15 votes/share | Minimum80 units | Preceding votes | Crossing unit | Crossing cumulative votes/share |
| --- | ---: | --- | ---: | ---: | --- | --- |
'''
    for y in ['2024','2022','2020']:
        q=os[y+'-native-votes'];k=json.loads(q['crossing_key']);s+=f"| {y} {'President'if y=='2024'else'Senate'} | {n(q['denominator'])} | {n(q['top15_votes'])} / {pct(q['top15_votes'],q['denominator'])} | {n(q['minimum80_count'])} | {n(q['preceding_votes'])} | parish {k[2]} ward {k[3]} precinct {k[4]} | {n(q['priority_votes'])} / {pct(q['priority_votes'],q['denominator'])} |\n"
    s+='''
The [method candidate controls](data/turnout/method-candidate-controls.json) retain every candidate vector in each disjoint reporting-row method group. The following are **parish-level sensitivity rankings**, each independently sorted by its own stated field. Registration and participation are separate source measures, not a forecast of candidate votes. Method totals are source candidate votes: Early Voting's internal mail/in-person composition is unknown; ordinary rows are a source category, not a proven election-day-only ballot definition. Provisional volume is counted candidate votes, not eligibility or outstanding ballots. [All complete orders](data/turnout/orders-summary.json) retain exact priority/remainder membership for every field. Sources: the same original candidate exports, [VotesEarly][early24] and the source-scoped general/race statistics above.

| Year/field | Denominator | Top15 votes/share | Minimum80 parishes | Preceding votes | Crossing parish | Cumulative votes/share |
| --- | ---: | --- | ---: | ---: | --- | --- |
'''
    for y in ['2024','2022','2020']:
        for f in ['votes','voted','qualified','race_voted','race_qualified','early_votes','provisional_votes','ordinary_votes']:
            q=os[y+'-parish-'+f];s+=f"| {y} {f} | {n(q['denominator'])} | {n(q['top15_votes'])} / {pct(q['top15_votes'],q['denominator'])} | {q['minimum80_count']} | {n(q['preceding_votes'])} | {q['crossing_name']} | {n(q['priority_votes'])} / {pct(q['priority_votes'],q['denominator'])} |\n"
    s+=f'''
For parish candidate volume alone, the top 15 contribute **{n(par['top15_votes'])}/{n(par['denominator'])} = {pct(par['top15_votes'],par['denominator'])}**. The first 24 contribute **1,620,459 ({pct(1620459,par['denominator'])})**; the first 23 contribute 1,602,004 ({pct(1602004,par['denominator'])}), and Washington crosses. This is not the finer native primary. The remaining 40 parishes contribute 386,516 votes. Full all-parish order follows; none is excluded from state arithmetic. The compatibility filename [county-turnout.csv](data/county-turnout.csv) contains **parishes**, with explicitly named parish sensitivity flags and each parent's native priority-child count/votes.

## All 64 parishes: volume sensitivity and native priority coverage

Source: [2024 original parish CSV][parish24], native originals and workbook; [full source positions](data/turnout/source/original-first-witness.json). This parent table does not add to its native children in any calculation.

| Parish rank | Parish (SOS ID/FIPS) | Candidate votes | Cumulative % | Native priority children / all children | Priority child votes |
| ---: | --- | ---: | ---: | ---: | ---: |
'''
    pm={x['key']:x for x in c['all_parishes']};um={u['key']:u for u in c['historical_native_constituents']}
    for r in par['order']:
        x=pm[r['key']];keys=x['ordered_priority_native_keys'];s+=f"| {r['rank']} | {x['parish']} ({x['parish_id']}/{x['fips']}) | {n(r['votes'])} | {r['cumulative_percent']:.8f} | {len(keys)} / {len(x['all_native_keys_in_source_order'])} | {n(sum(um[k]['votes']for k in keys))} |\n"
    s+='''
## Reproduction, review and limits

Run from the repository root, offline, using Python's standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/extract_originals.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/build_turnout.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/compare_peer.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/render_report.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/validate_turnout.py
```

[SCHEMA and evidence semantics](data/turnout/source/SCHEMA.md), [validation](data/turnout/validation.json), [peer source agreement](data/turnout/peer-source-agreement.json), [all-owned exact asset manifest](data/turnout/asset-manifest.json) and [final read-only audit](data/turnout/final-audit.json) describe the checks and their limits. The manifest excludes only itself and final audit. It includes original bodies, receipts, scripts, extraction, reports and failed histories; every stored artifact is strictly below 40,000,000 bytes. Gzip is lossless; no original is truncated or simplified. Final replay uses owned immutable individual body/receipt pins, never the mutable news ledger, discovery files or coordinator preflight outputs.

The first native-control assertion and the later general-versus-race equality assertion failed. Their complete input source pins, exact scripts, error logs and later correction history survive under `data/turnout/history/`; source discrepancies were retained instead of repaired by allocation. The previous parish-primary contract/CSV/script also survive before the necessary native-primary scope correction. Original-first source/control/position freezes remain unchanged. Mutation QA tests missing/duplicate units, balanced candidate transfers, administrative loss, invented zeros, wrong denominator, incorrect order/crossing and parish-dispatch substitution.

The actual peer is `4f625056-8184-4b03-97fb-4152b00397e3`. Exact copies of its already-frozen source schemas, freeze manifest and position witnesses are retained under `peer-capture/`. Comparison checked all 12,060 native rows, 192 parish vectors, 39 candidate columns, method classes, source positions, literal IDs, null qualified/voted fields, complete native orders and integer crossings derived from independently captured original source vectors. Different composite-key and one-based header-position conventions are documented aliases; no peer file was edited and no future scenario/outcome calculator was compared or adopted. Coordinator acceptance remains separate.

Material external limits: no signed ballot/withdrawal proof, complete subsequent legal/order review, November native identity/map approval or cross-year precinct crosswalk; no true ballot-cast or blank/under/over controls; registration status/cutoff unspecified; incomplete native registration/participation cells and explicit general/race differences; no eligible/outstanding write-in or provisional remainder measurement. Source configuration `IsLive=True`, refresh 120 and static offset −5, historical January 2026 WriteTime and `1900-01-01` version sentinels do not establish legal time, election-night cadence or certification sequencing. No live collector, calibrated Needle, genuine November returns or 2026 turnout projection is claimed. These limits qualify current operational use without preventing completion of the historical research.

[results]: https://www.sos.la.gov/elections-voting/election-results-statistics
[runtime]: https://www.sos.la.gov/scripts/sosscript.js
[app]: https://voterportal.sos.la.gov/graphical
[config]: https://voterportal.sos.la.gov/ElectionResults/GraphicalConfig
[client]: https://voterportal.sos.la.gov/bundles/graphicalresults?v=cIm8yGz__OufYjw9EhdZgZBxy8qhq7TaHRR_ZKepPws1
[dates]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=ElectionDates.htm
[xlsx24]: https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/20241105/Election+Results+(11-05-2024).xlsx
[xlsx22]: https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/20221108/Election+Results+(11-08-2022).xlsx
[xlsx20]: https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/20201103/Election+Results+(11-03-2020).xlsx
[csv24]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/csv/ByPrecinct_67190.csv
[parish24]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/csv/ByParish_67190.csv
[native24]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/VotesRaceByPrecinct/Votes_67190_17.htm
[early24]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/VotesEarly/Votes_67190.htm
[stats24]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/StatsStatewide.htm
[race24]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/StatsRace/Stats_67190.htm
[fips]: https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt
[closed]: https://www.sos.la.gov/elections-voting/closed-party-primary-elections
[qualify]: https://www.sos.la.gov/elections-voting/qualify-for-an-election
[law511]: https://www.legis.la.gov/legis/Law.aspx?d=81616
[law512]: https://www.legis.la.gov/legis/Law.aspx?d=81617
[fwab]: https://www.legis.la.gov/legis/Law.aspx?d=726711
[nov26]: https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20261103/RacesCandidates_Multiparish.htm
[calendar]: https://www.sos.la.gov/media/p31j4zkc/elections-calendar-2026.pdf
[electiondates]: https://www.sos.la.gov/elections-voting/election-dates
'''
    # Historical percentages are derived, never remembered constants.
    s=s.replace('59.32331501%',pct(1228908,2071543)).replace('61.56098726%',pct(851568,1383290))
    (ROOT.parent.parent/'turnout.md').write_text(s)
    print('turnout.md',len(s.encode()),'bytes')
if __name__=='__main__':main()
