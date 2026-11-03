# Kentucky historical partisanship and conditional paths

Research observed 2026-10-20. All 120 county parents and all candidates close independently to the three complete SBE certificate originals. The primary baseline is 2024 president; Kentucky had no 2024 Senate general election. The 2020 McConnell–McGrath contest is the same Class II seat, while 2022 Paul–Booker is the other Class III seat and midterm comparison. The [current SBE 2024 page](https://elect.ky.gov/results/2020-2029/Pages/2024.aspx) labels its certificate amended December 9, 2024. Original bytes, individual receipts, exact archive observations and hashes remain in the [source pins](data/baselines/source/pins.json).

**Full-state native priority remains unavailable:** canonical order/top 15/minimum 80 are NULL and dispatch keys EMPTY in [priority.json](data/baselines/priority.json). County controls and known native subsets cannot supply missing full-native units, methods or named-write-in allocations. This is a bounded, reproducible historical/conditional package with precise source gaps, not current geographic/legal approval or a calibrated 2026 forecast.

## Complete historical outcomes

| Contest | A, Democratic | B, Republican | Other candidates | All-candidate votes | A pair share | A-minus-B pair margin | Tie A-share shift | A+1 shift |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [2024 president](https://web.archive.org/web/20241223120817id_/https://elect.ky.gov/results/2020-2029/Documents/2024%20General%20Election%20Certification%20as%20Amended%20on%20December%209th%202024.pdf) | 704,043 | 1,337,494 | 32,993 | 2,074,530 | 34.485929% | -31.028142 pp | +15.514071 pp | +16.014071 pp |
| [2020 same-seat Senate](https://web.archive.org/web/20201120170339id_/https://elect.ky.gov/results/2020-2029/Documents/2020%20General%20Election%20Results.pdf) | 816,257 | 1,233,315 | 85,485 | 2,135,057 | 39.825729% | -20.348541 pp | +10.174271 pp | +10.674271 pp |
| [2022 other-seat Senate](https://web.archive.org/web/20221223031129id_/https://elect.ky.gov/results/2020-2029/Documents/2022%20General%20Election%20results.pdf) | 564,311 | 913,326 | 193 | 1,477,830 | 38.190097% | -23.619806 pp | +11.809903 pp | +12.309903 pp |

A is Harris/Walz in 2024, McGrath in 2020 and Booker in 2022. B is Trump/Vance, McConnell and Paul respectively. These pairs are historical named candidates; third parties and independents are retained as their own identities. A won 2 county parents in 2024 and 3 in each Senate comparison; all 360 county outcomes, margins, source positions and vectors are in [county-baselines.csv](data/county-baselines.csv). These are election-specific results, not permanent county labels.

The following is the complete 29-column statewide candidate control, read from the linked original certificates above; each of its 120 county sums equals its own printed footer. A presidential running mate is part of one ticket/vote column. Write-In is a source ballot label, not an inferred present eligibility ruling.

| Year/source column | Candidate / ticket | Source party/ballot label | Printed statewide votes |
| --- | --- | --- | ---: |
| 2024/1 | Donald J. TRUMP / J. D. VANCE | Republican Party | 1,337,494 |
| 2024/2 | Kamala D. HARRIS / Tim WALZ | Democratic Party | 704,043 |
| 2024/3 | Robert F. KENNEDY JR. / Nicole SHANAHAN | Independent | 16,769 |
| 2024/4 | Jill STEIN / Samson KPADENOU | Kentucky Party | 7,566 |
| 2024/5 | Chase OLIVER / Mike TER MAAT | Libertarian Party | 6,422 |
| 2024/6 | Shiva AYYADURAI / Crystal ELLIS | Independent | 1,015 |
| 2024/7 | Peter SONSKI / Lauren ONAK | Write-In | 611 |
| 2024/8 | Claudia DE LA CRUZ / Karina GARCIA | Write-In | 391 |
| 2024/9 | Cornel WEST / Melina ABDULLAH | Write-In | 177 |
| 2024/10 | James D. SODERNA / Matthew J. TREWHELLA | Write-In | 14 |
| 2024/11 | Jay J. BOWMAN / De BOWMAN | Write-In | 10 |
| 2024/12 | Joseph KISHORE / Jerry WHITE | Write-In | 8 |
| 2024/13 | John CHENG / Wayne WALIGORSKI | Write-In | 5 |
| 2024/14 | Billy KELLEY JR. / Jason HOLDEMAN | Write-In | 4 |
| 2024/15 | Cherunda FOX / Harlan McVAY JR. | Write-In | 1 |
| 2024/16 | Andre Ramon McNEIL SR. / Roschelle McNEIL | Write-In | 0 |
| 2024/17 | Future Madam POTUS / Jessica KENNEDY | Write-In | 0 |
| 2020/1 | Mitch McCONNELL | Republican Party | 1,233,315 |
| 2020/2 | Amy McGRATH | Democratic Party | 816,257 |
| 2020/3 | Brad BARRON | Libertarian Party | 85,386 |
| 2020/4 | Paul John FRANGEDAKIS | Write-In | 70 |
| 2020/5 | Daniel COBBLE | Write-In | 18 |
| 2020/6 | Randall Lee TEEGARDEN | Write-In | 9 |
| 2020/7 | Harold H. FITZPATRICK | Write-In | 1 |
| 2020/8 | Demetra WYSINGER | Write-In | 1 |
| 2022/1 | Rand PAUL | Republican Party | 913,326 |
| 2022/2 | Charles BOOKER | Democratic Party | 564,311 |
| 2022/3 | Charles Lee THOMASON | Write-In | 145 |
| 2022/4 | Billy Ray WILSON | Write-In | 48 |

Raw header spacing/case defects survive in [headers](data/baselines/extracted/certificate-headers.json); names above are explicitly manual display transcriptions. [All 3,509 candidate positions](data/baselines/extracted/certificate-fields.csv) retain original hash/page/line/column/token/character locators. Ballots, blank ballots, undervotes, overvotes, registration and methods are not printed in those certificate contest tables and remain unknown there.

## County volume sensitivity and every-unit targets

At the 2024 certificate **county** denominator of 2,074,530 contest votes, the top 15 supply 1,094,747(52.770844%). The smallest county set reaching 80% has 50 counties: 1,660,226/2,074,530; the preceding 49 have 1,650,178. The integer comparison is 5*cumulative>=4*total. The [full 120 county descending order](data/baselines/county-order.csv) includes every nonpriority parent. These are county sensitivities only; the [120 county native-recap index](https://elect.ky.gov/results/2020-2029/Pages/2024General-Recap-Sheets.aspx) does not establish a complete additive native universe.

All-state and every-county tie/A+1 targets are in [2,160 county target rows](data/baselines/county-targets.csv). Low/base/high **historical** volume and county mix settings use 2022/2024/2020 all-candidate contest counts, respectively. Each of the three preference anchors independently supplies its own county pair share and pair participation. Thus pair volume equals volume-year all-candidate votes times preference-year pair participation. No 2026 volume, candidate effect or crossyear native match is inferred. Changing total volume alone leaves a fractional pair target unchanged; changing county mix changes weights.

| Preference anchor | Historical volume/mix | Final pair volume | Final all-candidate volume | Tie share shift | A+1 share shift |
| --- | --- | ---: | ---: | ---: | ---: |
| 2024 | low-midterm (2022) | 1,454,247.849 | 1,477,830 | +14.881394 pp | +15.381394 pp |
| 2024 | base-presidential (2024) | 2,041,537.000 | 2,074,530 | +15.514071 pp | +16.014071 pp |
| 2024 | high-presidential (2020) | 2,101,027.361 | 2,135,057 | +15.127898 pp | +15.627898 pp |
| 2020 | low-midterm (2022) | 1,418,801.932 | 1,477,830 | +9.934474 pp | +10.434474 pp |
| 2020 | base-presidential (2024) | 1,991,010.103 | 2,074,530 | +10.536982 pp | +11.036982 pp |
| 2020 | high-presidential (2020) | 2,049,572.000 | 2,135,057 | +10.174271 pp | +10.674271 pp |
| 2022 | low-midterm (2022) | 1,477,637.000 | 1,477,830 | +11.809903 pp | +12.309903 pp |
| 2022 | base-presidential (2024) | 2,074,258.952 | 2,074,530 | +12.420106 pp | +12.920106 pp |
| 2022 | high-presidential (2020) | 2,134,778.112 | 2,135,057 | +12.059217 pp | +12.559217 pp |

For fixed two-candidate weights, the unbounded tie shift is `(B-A)/(2*(A+B))`. An illustrative A+1 pair margin uses target m=.01, adding 0.5A-share percentage points. One A-share point adds two pair-margin points and `.02*pair_volume`net votes. Share points, margin points, net votes and the full-candidate denominator are reported separately. The feasible solver clips each unit share to[0,1] and solves the common shift; unbounded algebra and bounded roots remain separate. None of these 18 county scenarios clips, while a saved synthetic endpoint case does. All candidates/nonpriority units remain in statewide denominators and other allocations.

At unchanged 2024 pair weights, the baseline A-minus-B net is−633,451. Tie requires that net improvement; A+1 requires a further 20,415.37 expected net votes on the 2,041,537 pair denominator. For example, one A-share point in Jefferson is 6,952.46 net votes, versus 2,814.68 in Fayette. These are arithmetic contributions, not mandatory local thresholds. With **every other county fixed at its unshifted 2024 preferences and volume**, no single county can reach the statewide tie even at 100%A. Jefferson alone would require 149.5285%A pair share; Fayette 284.3041%. Raw impossible selected-only requirements remain in the CSV, not silently clipped into feasible claims. Alternatives can combine gains across counties.

The separate [known-native subset targets](data/baselines/native-known-subset-targets.csv) provide tie/A+1 weights, contributions, gains and selected-only requirements for 3,127 positive-pair source contexts, including the 7 independently transcribed Elliott blocks. Their unallocated-other denominator retains the generic/named scope distinction. The [subset scope](data/baselines/native-subset-scope.json) also preserves 23 zero-pair contexts with undefined preference, unresolved contexts and the absent full-state universe. Holding other known-subset units fixed is not a full-state break-even requirement. No statewide native priority or 2026 boundary join follows.

## Native/method/admin evidence and source disagreements

All 120 individual recap HTTP 200 originals/receipts are pinned once by exact hash and reused read-only. Full originals and positioned layouts preserve 16,246 recap pages, including Jefferson 2,736 and Fayette 1,716; all 133 pinned PDFs total 17,073 pages. [Document inventory](data/baselines/extracted/document-inventory.json), [complete source/page contexts](data/baselines/extracted/native-page-contexts.jsonl.gz), [raw native observations](data/baselines/extracted/native-observations.jsonl.gz) and [positional selected fields](data/baselines/extracted/native-positional-fields.jsonl.gz) retain literal labels, method orders, controls, clock/status/header/footer and overlapping write-in relationships. Raw names/numbers do not establish precinct/split/central-group equivalence or polygon identity.

Choice reports generally put TOTAL last, with mail/walk-in/early/Election Day columns; Electionware summaries put TOTAL first and vary their method order/scope. Generic Write-In Totals is a parent of named/unassigned rows, not another candidate to add to them. Original zeros remain zeros; unavailable/private cells remain unknown and unmodeled. No deduplication, residual allocation, percentage reconstruction or source rescaling is used. These observations are directly inspectable through the [actual county originals](https://elect.ky.gov/results/2020-2029/Pages/2024General-Recap-Sheets.aspx) and exact receipt/body pins.

- **Scott:** its actual 10 page [county PDF](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Scott.pdf) is a cumulative county report, not native units. No native priority substitute is made.
- **Magoffin:** the [30 page source](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Magoffin.pdf) explicitly has TOTAL/Mail In only. It cannot represent the full county/method universe.
- **Elliott:** all 16 image-only [pages](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Elliott.pdf) were independently inspected. Seven selected presidential/native/admin blocks are [manually transcribed](data/baselines/extracted/elliott-manual.json); their A 532/B 2,335 match the certificate, while generic/unassigned 3 marks make 2,914 native cast votes versus 2,911 named certificate votes. The 3 marks are not distributed among named write-ins.
- **Fayette/Whitley:** own accepted source-local recap contexts give Fayette Trump 3 below its certificate, and Whitley Harris 1 below. The [full 120 parent reconciliation](data/baselines/source-reconciliation.csv) retains those and every other candidate-total difference. It closes A/B in 114 parents and all-candidate totals in 93, which does not prove complete named/native closure in those parents. Generic versus named write-in scope, candidate-universe differences and source vintages stay separate; no common cause is invented.
- **Laurel/Madison:** complete original/raw fields survive, but own quantitative grouping does not establish an accepted additive full-field control. Their 70 contexts remain [unresolved](data/baselines/extracted/native-unresolved-pair-contexts.json), not missing zeros.
- **2020/2022 native history:** the full 120 county certificates close both Senate contests. Complete statewide Senate native/method candidate coverage is not established. Direct historic navigation requests returned 403; actual 2020 Estill/Lyon archived originals are retained as 3/2 scanned pages with overlapping handwritten method/scan fields and blanks. All 5 pages were inspected and OCR separately retained; uncertain cells are unaccepted. The old Jefferson 2020 request redirected to generic HTML and supplies no historical native PDF. No 2020/2022 native crossyear join is inferred.

Poppler bounding-box extraction aborted on some rotated-text PDFs; all complete layout extracts and whole original bytes still passed page/hash checks. Failed/partial bounding-box output, stderr and checker history are retained and not called complete coordinates. This does not authorize reconstruction of image-only cells.

All 120 county administrative turnout rows for each of 2020/2022/2024 and 2024 registration independently close their own printed state controls. SBE [turnout guidance](https://elect.ky.gov/Resources/Pages/Turnout.aspx) qualifies its post-roll-reopening voter-history statistics as unofficial and explains why they may differ from election returns. Registration party counts are not candidate votes. The administrative total registration/Number voting controls are 2020:3,565,428/2,149,444;2022:3,590,227/1,502,626;2024:3,548,136/2,086,320. Their Number voting minus certificate-contest differences are 14,387/24,796/11,790, respectively; none is an estimated remaining pool. [All county controls](data/baselines/extracted/county-admin-turnout.csv) and [native/admin positioned rows](data/baselines/extracted/turnout-registration-positioned-controls.jsonl.gz) preserve definitions and overlaps. The [2024 registration PDF](https://elect.ky.gov/Resources/Documents/voterstatscounty-November%20General%202024.pdf) prints September 2024 despite the November General filename; that discrepancy is retained. These totals do not establish eligible 2026 turnout or certified ballots.

## Offline live-remainder calculator and validation

The [calculator contract](data/baselines/CALCULATOR.md) and [CLI](data/baselines/scripts/calculator.py) keep counted A/B/other votes fixed and forecast only a stated remaining all-candidate pool, with explicit participation/preference/other allocations. Final pair and full-candidate denominators include counted+remaining votes. Null positive-pool preference remains unknown; no-pool, secured/impossible, clipping and selected-only cases remain distinct. A pair leader can lose the complete supplied candidate field. Final official ballot/write-in mapping and applicable legal outcome rules remain external qualifications; old IDs, primary nominees, pair ties or pair A+1 cannot certify a result.

The 47 saved actual CLI cases exercise valid and invalid paths, global key uniqueness before unknown/no-pool branches, finite/bounded targets/counts/shares/allocations, duplicate object/candidate fields, unsupported settings, overflow, counted-fixed final denominators, raw negative/>1 selected requirements, unknown other units, clipping, undefined zero pair and pair leader losing full field. Expected invalid inputs return 2/strict JSON/empty stderr. Independent Fraction-based piecewise arithmetic verifies 20 historical roots and every unit contribution, gain and normalized weight. See [meaningful checks](data/baselines/proof/calculator-validation.json) and [fixtures](data/baselines/fixtures/). No probabilities or calibrated candidate/method effects are inferred.

## Independent peer comparison and handoff limits

Own [original-first freeze](data/baselines/proof/original-first-freeze.json) and [addendum](data/baselines/proof/original-first-freeze-v2.json) precede any coordinator numerical diagnostics or turnout numerical/parser/ranking derivatives. Only afterward were the actual turnout worker’s complete original-first/v2 witness bodies and individual receipts captured read-only. The [capture ledger](data/baselines/peer/capture.json) pins 373 stable body roles, including witness a101f4693c6cbf1ab0f1f0a5872a26037bbe24eb43f2d30760f3861d63afdafe and addendum 04944536c174c7eef726789370114aabb7d553bc5b96784921b8a7cd42a8d747. It does not depend on unfinished mutable peer builds.

The [bounded comparison](data/baselines/peer/comparison.json) finds all 3,509 certificate numeric/identity/party/ticket/raw-position fields,14 headers, full descending 120 county order and exact integer 80 crossing equal. All 58,543 captured peer native field positions have identical raw lines/count token positions in own 148,527 observations; own 89,984 additional rows retain context/admin/header detail. Twenty unit-label differences are Scott null versus a peer explicit cumulative sentinel. All 17,052 captured statistics raw rows and 56 Elliott candidate/pool/child positions plus their totals/admin match. All differences remain in a complete [difference ledger](data/baselines/peer/differences.jsonl.gz). Checker adapter errors were preserved before correcting schema handling; no source values or models were adopted. Handwritten/Jefferson alternative peer bodies are captured for scope audit, not imported as owned numeric evidence.

This comparison is limited to those frozen bodies and source positions. It makes no future final-output equality or coordinator acceptance claim. Full historical native candidate/method closure, final official 2026 ballot/current IDs, eligible write-ins, boundary crosswalks, legal result determination, remaining-vote pools, actual feed cadence and calibration remain explicitly unavailable. They are not replaced with neutral assumptions. The [schema](data/baselines/source/SCHEMA.md), [reproduction](data/baselines/REPRODUCE.md), [validation](data/baselines/validation.json) and [complete owned asset manifest](data/baselines/asset-manifest.json) make this bounded handoff reviewable. No Git operations, delegation or edits outside the assigned report/baseline paths were used.
