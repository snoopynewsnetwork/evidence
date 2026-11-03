# Louisiana reported vote volume and historical native priority

Research: **2026-10-20 UTC**. The primary is **November 5, 2024 Presidential Electors**, all **2,006,975 reported votes for the 11 source choices**, at the finest complete disjoint reporting level: **3,933 source units in all 64 parishes**. Louisiana had no 2024 Senate contest. These are candidate votes, not ballots cast, eligible voters or a 2026 turnout forecast. The originals are the SOS [complete workbook][xlsx24], [native CSV][csv24] and all 64 original native JSON responses pinned in the [individual acquired source index](data/turnout/source/acquired-pins.json), through the official [results authority][results].

**Native top 15: 689,455/2,006,975 = 34.35294411%. Minimum descending native set: 1,516 units, 1,605,649 votes = 80.00343801%.** The preceding 1,515 units contain 1,605,350 votes (79.98853997%). **Bienville parish (native code 07), ward 06 / precinct 03, contributes 299 votes and crosses 80%.** The remaining 2,417 units contain 401,326 votes (19.99656199%). Integer proof: `5*1605350=8026750 < 4*2006975=8027900 <= 5*1605649=8028245`. A descending set of only 1,515 cannot reach the threshold. Ties use ascending literal JSON composite key `[year,race_id,parish_id,ward,precinct]`; the chosen membership among equal-volume units follows that documented rule.

The [exact historical contract](data/turnout/priority-set.json) contains all 3,933 native rows, full order, ordered 1,516-unit priority and 2,417-unit remainder, and all 64 parent arrays with source order, descending order, priority and remainder children. [Full native order](data/turnout/orders/2024-native-votes.csv) preserves each literal key; [native details](data/turnout/extract/2024-native.json.gz) retain original CSV/API/OOXML positions. **The 24-parish/Washington set is a parish sensitivity, not the native dispatch.** Every parish contributes at least one native priority child. The priority has 1,452 ward/precinct source rows plus all 64 Early Voting aggregates; it contains no Provisional Votes aggregate. No polygon is assigned to administrative aggregates.

The complete historical source universe reconciles independently, so the contract carries its proposed historical native dispatch. **Coordinator acceptance is false.** One-way comparison with the actual peer's already-frozen independent original source schema passed; reciprocal peer signoff is not claimed. November 2026 native dispatch remains empty and no current legal geometry is approved. Historical source identity and current map approval are separate questions.

## Native top 15

All 15 are the source's **Early Voting** administrative row, not wards, polling sites or separately geolocated vote centers. Source CSV represents each as `Ward="Early Voting", Precinct=""`; XLSX concatenates a trailing space. The original source does not split their composition into early in-person and absentee mail. Their votes are disjoint from the separately published ordinary and provisional candidate rows. Sources: [native CSV][csv24], [workbook][xlsx24], [sample original native JSON][native24]; all parish originals and receipts are pinned, not just the sample.

| Rank | Parish/native parent | Native source label | Candidate votes | State share | Cumulative share |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | East Baton Rouge | Early Voting | 93,940 | 4.68067614% | 4.68067614% |
| 2 | Jefferson | Early Voting | 89,694 | 4.46911397% | 9.14979011% |
| 3 | St. Tammany | Early Voting | 79,796 | 3.97593393% | 13.12572404% |
| 4 | Orleans | Early Voting | 79,157 | 3.94409497% | 17.06981901% |
| 5 | Lafayette | Early Voting | 55,227 | 2.75175326% | 19.82157227% |
| 6 | Caddo | Early Voting | 40,325 | 2.00924277% | 21.83081503% |
| 7 | Calcasieu | Early Voting | 38,422 | 1.91442345% | 23.74523848% |
| 8 | Ascension | Early Voting | 35,014 | 1.74461565% | 25.48985413% |
| 9 | Ouachita | Early Voting | 34,486 | 1.71830740% | 27.20816154% |
| 10 | Livingston | Early Voting | 32,654 | 1.62702575% | 28.83518728% |
| 11 | Bossier | Early Voting | 27,317 | 1.36110315% | 30.19629044% |
| 12 | Tangipahoa | Early Voting | 22,644 | 1.12826518% | 31.32455561% |
| 13 | Rapides | Early Voting | 22,642 | 1.12816552% | 32.45272114% |
| 14 | Lafourche | Early Voting | 20,430 | 1.01794990% | 33.47067103% |
| 15 | Terrebonne | Early Voting | 17,707 | 0.88227307% | 34.35294411% |

## Source identity, universe and hierarchy

The official results parent publishes environment placeholders. Its explicitly linked [production runtime script][runtime] removes `.--environment--` when `data-environment` is empty, yielding the actual [public graphical app][app]. That app links [GraphicalConfig][config] and the [complete public client][client]. Its published date-folder constructors produce XLSX, CSV, `StatsParish`, `StatsStatewide`, `StatsRace`, `VotesEarly` and `VotesRaceByPrecinct` sources used here. No authentication, personal lookup, media credentials or November count request was used. [Original pins](data/turnout/source/original-pins.json) and [acquired pins](data/turnout/source/acquired-pins.json) preserve exact bodies, individual receipts, requested/final URLs, UTC, status, headers, stored/raw hashes and sizes. New acquisitions retain each redirect entity; legacy receipts establish final entities only, with intermediate-hop evidence unavailable.

For 2024 there are **3,805 ward/precinct rows + 64 Early Voting + 64 Provisional Votes = 3,933 disjoint candidate rows**. The corresponding counts are 3,937+64+64=4,065 in 2022 and 3,934+64+64=4,062 in 2020. Each candidate vector matches native CSV to workbook and independently downloaded native JSON; each native sum matches its parish and every parish sum the two workbook statewide control rows. The views overlap and are never added. Parish tabs do not cover the whole state in every workbook; the multi-parish tables do. [Election roster][dates] marks all three historical elections `ResultsOfficial=1`; this is the publisher's status, not an independently obtained signed certificate or certification chronology.

The actual two-character parish IDs come from the literal public-client parish list, crosschecked against all returned parish inventories. Parish FIPS come from the complete [Census official code file][fips], using explicit case-insensitive parish-name matching with the ` Parish` suffix removed; source `Lasalle` matches `LaSalle`. FIPS describe parents, not a fabricated precinct code or map crosswalk. A native key includes year, source race ID, parish ID, literal Ward and Precinct. Leading zeros, letters, embedded spaces, empty fields, source order and explicit zero counts survive. No native ID or boundary equivalence across years or to November 2026 is asserted. These rows are reporting identities; split-like suffixes do not establish ballot style, physical precinct or polling-place membership.

The [whole-workbook source witness](data/turnout/source/original-first-witness.json) preserves every sheet's physical row/cell ordinal, original attributes and blank leading cells. OOXML `r` addresses are sometimes omitted; 2020's first member is `sheet.xml`, resolved through workbook relationships. Every ZIP member's exact bytes remain reconstructible from the original workbook, with CRC, size and member hashes. Unrelated offices and demographic fields survive whole in original bytes and witnesses; they are not silently discarded or promoted into extra turnout analysis. No prepared totals were imported.

## All candidates and historical outcomes

These are complete **11/13/15-choice** first-election source fields. `OTHER` (workbook) versus `OTH` (CSV) is an explicit formatting alias, not candidate deduplication. The 2024 source's `Jill Stein, Ajamu Baraka Green` running-mate string is preserved literally, as are all other ballot/party labels; this package does not substitute national ticket labels or establish their legal ballot identity. Sources: [2024 workbook][xlsx24], [2022 workbook][xlsx22], [2020 workbook][xlsx20] and independently read metadata through the [official app][app]. [Candidate controls](data/turnout/candidate-controls.csv) retain source choice IDs, party labels and separate state/parish/native sums, with zero differences for every candidate.

| Year/contest | Literal candidate or ticket | Choice ID | State = parish sum = native sum |
| --- | --- | --- | ---: |
| 2024 President | Kamala D. Harris, Tim Walz Democratic (DEM) | 123574 | 766,870 |
| 2024 President | Jill Stein, Ajamu Baraka Green (GRN) | 123573 | 7,138 |
| 2024 President | Chase Oliver, Mike ter Maat Libertarian (LBT) | 123239 | 6,835 |
| 2024 President | Donald J. Trump, "JD" Vance Republican (REP) | 123572 | 1,208,505 |
| 2024 President | Peter Sonski, Lauren Onak American Solidarity Party (OTHER) | 123575 | 2,240 |
| 2024 President | Randall Terry, Stephen Broden Constitution Party (OTHER) | 123576 | 1,424 |
| 2024 President | Mattie Preston, Shannel Conner Godliness, Truth, Justice (OTHER) | 123578 | 2,857 |
| 2024 President | Cornel West, Melina Abdullah Justice For All (OTHER) | 123577 | 2,623 |
| 2024 President | Claudia de la Cruz, Karina Garcia Socialism and Liberation (OTHER) | 123570 | 1,481 |
| 2024 President | Rachele Fruit, Dennis Richter Socialist Workers Party (OTHER) | 123571 | 361 |
| 2024 President | Robert F. Kennedy, Jr., Nicole Shanahan We The People (OTHER) | 123569 | 6,641 |
| 2022 Senate | Beryl A. Billiot (NOPTY) | 116035 | 9,378 |
| 2022 Senate | Gary Chambers, Jr. (DEM) | 115136 | 246,933 |
| 2022 Senate | Devin Lance Graham (REP) | 117227 | 25,275 |
| 2022 Senate | "Xan" John (OTHER) | 114911 | 2,753 |
| 2022 Senate | John Kennedy (REP) | 114861 | 851,568 |
| 2022 Senate | W. Thomas La Fontaine Olson (NOPTY) | 115670 | 1,676 |
| 2022 Senate | Bradley McMorris (IND) | 116755 | 5,388 |
| 2022 Senate | MV "Vinny" Mendoza (DEM) | 116132 | 11,910 |
| 2022 Senate | "Luke" Mixon (DEM) | 115416 | 182,887 |
| 2022 Senate | Salvador P. Rodriguez (DEM) | 116412 | 7,767 |
| 2022 Senate | Aaron C. Sigler (LBT) | 117198 | 4,865 |
| 2022 Senate | Syrita Steib (DEM) | 115414 | 31,568 |
| 2022 Senate | Thomas Wenn (OTHER) | 115636 | 1,322 |
| 2020 Senate | Beryl Billiot (NOPTY) | 112789 | 17,362 |
| 2020 Senate | John Paul Bourgeois (NOPTY) | 111401 | 16,518 |
| 2020 Senate | "Bill" Cassidy (REP) | 112841 | 1,228,908 |
| 2020 Senate | Reno Jean Daret III (NOPTY) | 112620 | 3,954 |
| 2020 Senate | Derrick "Champ" Edwards (DEM) | 112172 | 229,814 |
| 2020 Senate | "Xan" John (OTHER) | 112662 | 2,813 |
| 2020 Senate | David Drew Knight (DEM) | 112138 | 36,962 |
| 2020 Senate | M.V. "Vinny" Mendoza (IND) | 113149 | 7,811 |
| 2020 Senate | Jamar Montgomery (NOPTY) | 113121 | 5,804 |
| 2020 Senate | Dustin Murphy (REP) | 112998 | 38,383 |
| 2020 Senate | Adrian Perkins (DEM) | 112580 | 394,049 |
| 2020 Senate | Antoine Pierce (DEM) | 111893 | 55,710 |
| 2020 Senate | Melinda Mary Price (OTHER) | 112892 | 7,680 |
| 2020 Senate | Aaron C. Sigler (LBT) | 112599 | 11,321 |
| 2020 Senate | Peter Wenstrup (DEM) | 112549 | 14,454 |

2020 is Cassidy's **Class II same-seat** Senate election; 2022 is Kennedy's **Class III other-seat midterm**, not a second Class II observation and not a governor election. Cassidy received 1,228,908/2,071,543 (59.32331600%); Kennedy received 851,568/1,383,290 (61.56106095%). Each exceeded half the complete field at the first election and therefore needed no Senate runoff. Historical metadata's `CanHaveRunoff=1` describes potential procedure, not an actual second round. The historical majority rule is reflected in [R.S.18:511][law511]; the raw historical fields and exact majority arithmetic are retained in [historical controls](data/turnout/historical-controls.json).

Current rules were independently inspected on October 20: the [SOS closed-party explanation][closed] describes spring majority nomination and a plurality general; its [qualifying page][qualify] expressly keeps Senate in that system while describing the Act 7 House exception. [R.S.18:512][law512] states the most-votes general rule. Historical runoff flags and the U.S. House exception are not applied to the 2026 Senate general. The retained [July-revised calendar][calendar] says Senate general November 3, while December's House stage is separately labeled. A retained [election-date HTML][electiondates] says party qualifying occurred in January; the July calendar says February 11–13. Their cause/amendment chronology is not established here.

The complete retained [November setup metadata][nov26] has Senate race 67997 with choices 124654 `"Jamie" Davis (DEM)` and 124655 `Julia Letlow (REP)`, and literal WriteTime `2026-10-18T05:00:06.330` (timezone unspecified). These are published setup identities, not genuine counts, signed final ballot/withdrawal proof or a historical candidate join. No November count file was requested. Final candidate legal identities, later statutes/orders and approved current reporting units remain precise external qualifications.

## Candidate votes, participation, registration and unavailable ballots

The exports have no separate generic/named write-in, blank, under- or overvote pools. Those fields remain **null**, not invented zeros. [SOS qualifying guidance][qualify] says Louisiana does not allow write-in candidates. [R.S.18:1319][fwab] separately permits the Federal Write-In Absentee Ballot mechanism for specified voters; that is not evidence of an additional generic candidate pool or a measured method count in these exports. The ranking therefore uses all reported named choice counts, with no allocated residual.

`All` and `All_Voted` are the public statistics' registration/participation fields; native results expose `VoterCountQualified` and `VoterCountVoted`. The app labels these registered/voted controls. This package preserves the source names, scope and republication clocks; it does not assert active-only registration, a specific roll cutoff or equivalence to tabulated ballots cast. **Exact ballots-cast and blank/under/over sensitivities are unavailable.** Differences between participation and candidate votes are not classified as undervotes. General-election statistics and selected-race statistics are retained separately. Sources: [2024 general statewide statistics][stats24], [2024 race statistics][race24], and the corresponding independently downloaded 2022/2020 originals in the [source index](data/turnout/source/acquired-pins.json).

| Year | Named candidate votes | General All_Voted | Race All_Voted | General All | Race All | General voted − candidate votes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2024 | 2,006,975 | 2,021,164 | 2,021,164 | 3,046,376 | 3,046,376 | 14,189 |
| 2022 | 1,383,290 | 1,410,476 | 1,410,466 | 3,018,815 | 3,018,815 | 27,186 |
| 2020 | 2,071,543 | 2,169,400 | 2,169,413 | 3,093,003 | 3,092,988 | 97,857 |

General parish sums exactly match their general state controls; selected-race parish sums exactly match their selected-race controls. In 2022, East Baton Rouge race participation is 10 below general participation. In 2020, race participation is 4 higher in Caddo and 9 higher in East Baton Rouge; race registration is 4 lower in Calcasieu, 2 in Lincoln, 4 in Orleans and 5 in Webster. No reconciliation adjustment or cause is inferred. [Full source-scope discrepancy ledger](data/turnout/statistics-scope-discrepancies.json).

The native result objects omit qualified/voted cells on 5 ordinary rows in 2024, 11 in 2022 and 13 in 2020, plus all administrative rows. Their explicit candidate zeros remain valid zeros while their omitted controls remain null. Native control sums are not called complete where a cell is missing; differences in complete sums against general parish controls also remain visible. The [native discrepancy ledger](data/turnout/native-control-discrepancies.json) retains keys, source totals and missing-cell lists. Every candidate/native membership still reconciles independently. Neither registration minus participation nor precincts reported supplies exact remaining eligible votes.

## Historical and method sensitivities

The native primary and its actual recent midterm comparator use complete source-native rows at each year's own vintage; they do not assert cross-year precinct equivalence. Sources: original [2024][xlsx24], [2022][xlsx22] and [2020][xlsx20] workbooks/CSV/native originals. All full orders and remainder sets are in [orders summary](data/turnout/orders-summary.json) and the [2024](data/turnout/orders/2024-native-votes.csv), [2022](data/turnout/orders/2022-native-votes.csv), [2020](data/turnout/orders/2020-native-votes.csv) native order files.

| Native field | Total votes | Top-15 votes/share | Minimum80 units | Preceding votes | Crossing unit | Crossing cumulative votes/share |
| --- | ---: | --- | ---: | ---: | --- | --- |
| 2024 President | 2,006,975 | 689,455 / 34.35294411% | 1,516 | 1,605,350 | parish 07 ward 06 precinct 03 | 1,605,649 / 80.00343801% |
| 2022 Senate | 1,383,290 | 248,636 / 17.97424980% | 1,907 | 1,106,608 | parish 56 ward 00 precinct 19 | 1,106,852 / 80.01590411% |
| 2020 Senate | 2,071,543 | 667,617 / 32.22800589% | 1,552 | 1,657,026 | parish 26 ward 00 precinct K011 | 1,657,333 / 80.00475974% |

The [method candidate controls](data/turnout/method-candidate-controls.json) retain every candidate vector in each disjoint reporting-row method group. The following are **parish-level sensitivity rankings**, each independently sorted by its own stated field. Registration and participation are separate source measures, not a forecast of candidate votes. Method totals are source candidate votes: Early Voting's internal mail/in-person composition is unknown; ordinary rows are a source category, not a proven election-day-only ballot definition. Provisional volume is counted candidate votes, not eligibility or outstanding ballots. [All complete orders](data/turnout/orders-summary.json) retain exact priority/remainder membership for every field. Sources: the same original candidate exports, [VotesEarly][early24] and the source-scoped general/race statistics above.

| Year/field | Denominator | Top15 votes/share | Minimum80 parishes | Preceding votes | Crossing parish | Cumulative votes/share |
| --- | ---: | --- | ---: | ---: | --- | --- |
| 2024 votes | 2,006,975 | 1,391,066 / 69.31157588% | 24 | 1,602,004 | Washington | 1,620,459 / 80.74136449% |
| 2024 voted | 2,021,164 | 1,400,925 / 69.31278214% | 24 | 1,613,236 | Washington | 1,631,811 / 80.73619954% |
| 2024 qualified | 3,046,376 | 2,129,415 / 69.89994013% | 23 | 2,416,784 | St. John The Baptist | 2,446,188 / 80.29829542% |
| 2024 race_voted | 2,021,164 | 1,400,925 / 69.31278214% | 24 | 1,613,236 | Washington | 1,631,811 / 80.73619954% |
| 2024 race_qualified | 3,046,376 | 2,129,415 / 69.89994013% | 23 | 2,416,784 | St. John The Baptist | 2,446,188 / 80.29829542% |
| 2024 early_votes | 967,415 | 689,455 / 71.26775996% | 22 | 764,568 | Acadia | 774,290 / 80.03700584% |
| 2024 provisional_votes | 584 | 563 / 96.40410959% | 6 | 466 | Calcasieu | 491 / 84.07534247% |
| 2024 ordinary_votes | 1,038,976 | 701,062 / 67.47624584% | 25 | 829,805 | Washington | 839,554 / 80.80590889% |
| 2022 votes | 1,383,290 | 943,759 / 68.22567936% | 25 | 1,103,308 | Iberville | 1,115,462 / 80.63833325% |
| 2022 voted | 1,410,476 | 960,146 / 68.07248050% | 25 | 1,122,872 | Iberville | 1,135,583 / 80.51062195% |
| 2022 qualified | 3,018,815 | 2,102,321 / 69.64060401% | 23 | 2,389,743 | St. John The Baptist | 2,419,280 / 80.14005496% |
| 2022 race_voted | 1,410,466 | 960,136 / 68.07225413% | 25 | 1,122,862 | Iberville | 1,135,573 / 80.51048377% |
| 2022 race_qualified | 3,018,815 | 2,102,321 / 69.64060401% | 23 | 2,389,743 | St. John The Baptist | 2,419,280 / 80.14005496% |
| 2022 early_votes | 371,766 | 248,636 / 66.87970390% | 26 | 294,145 | St. Mary | 297,723 / 80.08343958% |
| 2022 provisional_votes | 201 | 192 / 95.52238806% | 6 | 160 | Ouachita | 166 / 82.58706468% |
| 2022 ordinary_votes | 1,011,323 | 694,990 / 68.72087355% | 24 | 804,074 | Washington | 813,013 / 80.39103234% |
| 2020 votes | 2,071,543 | 1,433,562 / 69.20261853% | 24 | 1,653,160 | Washington | 1,672,018 / 80.71365161% |
| 2020 voted | 2,169,400 | 1,495,655 / 68.94325620% | 24 | 1,727,748 | Washington | 1,747,456 / 80.55019821% |
| 2020 qualified | 3,093,003 | 2,149,211 / 69.48622423% | 23 | 2,444,284 | St. John The Baptist | 2,474,990 / 80.01899772% |
| 2020 race_voted | 2,169,413 | 1,495,668 / 68.94344230% | 24 | 1,727,761 | Washington | 1,747,469 / 80.55031476% |
| 2020 race_qualified | 3,092,988 | 2,149,203 / 69.48630257% | 23 | 2,444,276 | St. John The Baptist | 2,474,982 / 80.01912714% |
| 2020 early_votes | 956,850 | 667,617 / 69.77237812% | 24 | 763,686 | Acadia | 773,005 / 80.78643466% |
| 2020 provisional_votes | 583 | 562 / 96.39794168% | 4 | 414 | East Baton Rouge | 483 / 82.84734134% |
| 2020 ordinary_votes | 1,114,110 | 767,810 / 68.91689330% | 24 | 890,398 | Lincoln | 900,196 / 80.79956198% |

For parish candidate volume alone, the top 15 contribute **1,391,066/2,006,975 = 69.31157588%**. The first 24 contribute **1,620,459 (80.74136449%)**; the first 23 contribute 1,602,004 (79.82182140%), and Washington crosses. This is not the finer native primary. The remaining 40 parishes contribute 386,516 votes. Full all-parish order follows; none is excluded from state arithmetic. The compatibility filename [county-turnout.csv](data/county-turnout.csv) contains **parishes**, with explicitly named parish sensitivity flags and each parent's native priority-child count/votes.

## All 64 parishes: volume sensitivity and native priority coverage

Source: [2024 original parish CSV][parish24], native originals and workbook; [full source positions](data/turnout/source/original-first-witness.json). This parent table does not add to its native children in any calculation.

| Parish rank | Parish (SOS ID/FIPS) | Candidate votes | Cumulative % | Native priority children / all children | Priority child votes |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | East Baton Rouge (17/22033) | 190,643 | 9.49902216 | 146 / 333 | 148,283 |
| 2 | Jefferson (26/22051) | 178,205 | 18.37830566 | 147 / 273 | 150,953 |
| 3 | Orleans (36/22071) | 159,130 | 26.30715380 | 61 / 351 | 100,994 |
| 4 | St. Tammany (52/22103) | 138,384 | 33.20230695 | 105 / 172 | 124,852 |
| 5 | Lafayette (28/22055) | 111,086 | 38.73730365 | 95 / 136 | 102,660 |
| 6 | Caddo (09/22017) | 94,699 | 43.45579790 | 97 / 130 | 87,721 |
| 7 | Calcasieu (10/22019) | 81,201 | 47.50173769 | 71 / 125 | 70,499 |
| 8 | Livingston (32/22063) | 65,906 | 50.78558527 | 57 / 82 | 61,079 |
| 9 | Ouachita (37/22073) | 64,436 | 53.99618829 | 42 / 87 | 54,589 |
| 10 | Ascension (03/22005) | 62,473 | 57.10898242 | 47 / 74 | 56,801 |
| 11 | Tangipahoa (53/22105) | 55,104 | 59.85460706 | 56 / 76 | 51,094 |
| 12 | Rapides (40/22079) | 53,395 | 62.51507866 | 42 / 115 | 40,021 |
| 13 | Bossier (08/22015) | 52,232 | 65.11760236 | 40 / 87 | 42,508 |
| 14 | Lafourche (29/22057) | 42,845 | 67.25240723 | 34 / 74 | 34,849 |
| 15 | Terrebonne (55/22109) | 41,327 | 69.31157588 | 39 / 73 | 35,189 |
| 16 | St. Landry (49/22097) | 37,043 | 71.15728895 | 29 / 93 | 27,326 |
| 17 | Iberia (23/22045) | 29,331 | 72.61874214 | 26 / 57 | 24,689 |
| 18 | Acadia (01/22001) | 26,720 | 73.95009903 | 29 / 49 | 23,169 |
| 19 | St. Charles (45/22089) | 26,685 | 75.27971200 | 25 / 46 | 22,806 |
| 20 | Vermilion (57/22113) | 26,429 | 76.59656946 | 20 / 68 | 19,710 |
| 21 | St. Martin (50/22099) | 25,006 | 77.84252420 | 21 / 45 | 21,944 |
| 22 | St. Mary (51/22101) | 20,897 | 78.88374295 | 14 / 48 | 14,064 |
| 23 | St. John The Baptist (48/22095) | 18,827 | 79.82182140 | 16 / 38 | 15,848 |
| 24 | Washington (59/22117) | 18,455 | 80.74136449 | 8 / 43 | 12,175 |
| 25 | Lincoln (31/22061) | 18,157 | 81.64605937 | 12 / 52 | 13,632 |
| 26 | St. Bernard (44/22087) | 17,292 | 82.50765455 | 13 / 33 | 13,319 |
| 27 | Webster (60/22119) | 16,205 | 83.31508863 | 10 / 42 | 11,526 |
| 28 | Vernon (58/22115) | 16,149 | 84.11973243 | 6 / 62 | 9,440 |
| 29 | Avoyelles (05/22009) | 16,037 | 84.91879570 | 18 / 43 | 12,009 |
| 30 | Beauregard (06/22011) | 15,874 | 85.70973729 | 10 / 39 | 11,250 |
| 31 | Iberville (24/22047) | 15,354 | 86.47476924 | 20 / 35 | 13,339 |
| 32 | Natchitoches (35/22069) | 15,040 | 87.22415576 | 7 / 52 | 9,035 |
| 33 | Jefferson Davis (27/22053) | 14,358 | 87.93956078 | 10 / 30 | 11,529 |
| 34 | Evangeline (20/22039) | 14,176 | 88.64589743 | 10 / 57 | 7,689 |
| 35 | De Soto (16/22031) | 13,913 | 89.33912978 | 5 / 59 | 9,109 |
| 36 | West Baton Rouge (61/22121) | 13,836 | 90.02852552 | 7 / 32 | 10,295 |
| 37 | St. James (47/22093) | 11,789 | 90.61592695 | 9 / 22 | 9,570 |
| 38 | Pointe Coupee (39/22077) | 11,570 | 91.19241645 | 10 / 27 | 8,998 |
| 39 | Union (56/22111) | 10,475 | 91.71434622 | 6 / 33 | 6,462 |
| 40 | Assumption (04/22007) | 10,367 | 92.23089475 | 8 / 32 | 6,756 |
| 41 | Sabine (43/22085) | 10,170 | 92.73762752 | 5 / 34 | 5,406 |
| 42 | Morehouse (34/22067) | 10,097 | 93.24072298 | 2 / 42 | 6,563 |
| 43 | East Feliciana (19/22037) | 9,947 | 93.73634450 | 7 / 25 | 7,951 |
| 44 | Plaquemines (38/22075) | 9,945 | 94.23186637 | 7 / 19 | 8,263 |
| 45 | Richland (42/22083) | 9,193 | 94.68991891 | 7 / 25 | 6,405 |
| 46 | Grant (22/22043) | 9,018 | 95.13925186 | 9 / 33 | 5,877 |
| 47 | Franklin (21/22041) | 8,798 | 95.57762304 | 4 / 27 | 5,605 |
| 48 | Allen (02/22003) | 8,751 | 96.01365239 | 8 / 20 | 6,588 |
| 49 | Concordia (15/22029) | 7,755 | 96.40005481 | 7 / 20 | 5,451 |
| 50 | Jackson (25/22049) | 7,226 | 96.76009915 | 3 / 33 | 3,888 |
| 51 | Lasalle (30/22059) | 6,620 | 97.08994880 | 2 / 23 | 3,573 |
| 52 | Bienville (07/22013) | 6,256 | 97.40166170 | 4 / 37 | 3,007 |
| 53 | West Feliciana (63/22125) | 6,008 | 97.70101770 | 2 / 29 | 3,757 |
| 54 | Claiborne (14/22027) | 5,816 | 97.99080706 | 3 / 27 | 3,667 |
| 55 | Winn (64/22127) | 5,781 | 98.27885250 | 1 / 28 | 2,741 |
| 56 | St. Helena (46/22091) | 5,745 | 98.56510420 | 7 / 13 | 5,228 |
| 57 | West Carroll (62/22123) | 4,603 | 98.79445434 | 1 / 25 | 2,529 |
| 58 | Catahoula (13/22025) | 4,348 | 99.01109879 | 2 / 30 | 2,051 |
| 59 | Caldwell (11/22021) | 4,334 | 99.22704568 | 1 / 21 | 2,070 |
| 60 | Madison (33/22065) | 3,992 | 99.42595199 | 1 / 28 | 1,670 |
| 61 | Red River (41/22081) | 3,725 | 99.61155470 | 1 / 20 | 1,526 |
| 62 | Cameron (12/22023) | 3,362 | 99.77907049 | 2 / 13 | 1,925 |
| 63 | East Carroll (18/22035) | 2,306 | 99.89396978 | 1 / 19 | 1,011 |
| 64 | Tensas (54/22107) | 2,128 | 100.00000000 | 1 / 17 | 1,116 |

## Reproduction, review and limits

Run from the repository root, offline, using Python's standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/extract_originals.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/build_turnout.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/compare_peer.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/render_report.py
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/validate_turnout.py
```

[SCHEMA and evidence semantics](data/turnout/source/SCHEMA.md), [validation](data/turnout/validation.json), [peer source agreement](data/turnout/peer-source-agreement.json), [all-owned exact asset manifest](data/turnout/asset-manifest.json) and [pre-manifest audit proof](data/turnout/final-audit.json) describe the checks and their limits. The repaired current manifest excludes only itself and includes the current validation, pre-manifest audit proof, final seal, histories and fixtures. The exact former two-exclusion manifest and its unlisted audit remain whole in immutable history. It includes original bodies, receipts, scripts, extraction, reports and failed histories; every stored artifact is strictly below 40,000,000 bytes. Gzip is lossless; no original is truncated or simplified. Final replay uses owned immutable individual body/receipt pins, never the mutable news ledger, discovery files or coordinator preflight outputs.

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


## Bounded immutable packaging repair and captured final-peer source verification

The repair first independently verified **all 645 prior whole owned files**: all 643 old manifest targets, the 135,869-byte manifest (`d95ab6f276e4feeea3662671d03c62328ed4ffebc850197fcca34b0919e382dc`) and its excluded 656-byte audit (`031acefbd77ec716d2080091213ca7de16f3f05703c3f9e4dc990d2bb3ec4b91`). Before editing, every complete prior body was frozen at its exact old path/size/SHA in a lossless archive. This includes all original-first freezes, raw witnesses, failed inputs/scripts/claims and both the earlier parish and native contracts. [Own prior inventory and reconstruction parts](data/turnout/history/packaging-repair/own-prior-inventory.json) pin the complete archive. No old hash is checked against a rewritten current body.

The actual final baseline peer's **1,607 manifest targets plus manifest = 1,608 whole files** were captured before comparison, with exact final manifest `22aa501bcbcf9a6b99849e41859cf14a7d3216191e22d0f6dd68eced41fe897d` and seal `7e3c2305515037ef32169d18af91b331bf8724bdf023e5550957e5339d2ba8c8`. [Complete peer inventory](data/turnout/history/packaging-repair/peer-prior-inventory.json) includes all source/input/receipt/history/archive/original-first roles, including peer files excluded from semantic scope. Shared originals are preserved once by [individual exact stored/raw body pins and complete receipt roles](data/turnout/history/packaging-repair/shared-original-roles.json). No peer acquisition, builder, replay, calculator or writer was executed or imported; no peer or shared path was changed.

[Captured final-peer source proof](data/turnout/repair-proof/captured-final-peer-source-verification.json) records **1,806,692 historical source/context checks**, with no historical source differences: whole workbook/member/relationship bytes, all physical OOXML rows/cells/styles/values/formulas, complete CSV headers/records/tokens/positions, all native/candidate/party/running-mate/null/admin/method context, all 27 full orders, ranks/denominators/cumulatives/integer crossings/priority/remainder, and all 192 year-parent source/rank/method child arrays. The captured reverse proof's **146,652 source checks** concern the earlier independently frozen historical source schema only; they do not establish equality of this later package, future outcomes, scenario calculators or current operational geography. Key and export label adapters remain explicit and source-scoped. Missing cells and source zeros retain their separate meaning.

Two independently retrieved **current authority HTML bodies differ** from the peer's older observations. Both whole bodies, receipts and the actual initially failed checker are preserved under `history/packaging-repair/`; they are explicitly outside historical equality scope. Their difference is not normalized into agreement or used to infer a correction chronology. The first peer-capture path-root failure, exact checker/error/context, full source-check failure and subsequent narrow scope qualification are also retained. Original-first witness wall clocks and scope attestations are preserved and checked against exact captured bodies; this does not claim a separate forensic file-creation-time attestation.

[Isolated original replay](data/turnout/repair-proof/isolated-original-replay.json) executes only the exact captured own original extraction/build scripts with fixed individual body/receipt pins in temporary outputs. **All 46 generated whole files match the old captured bytes exactly**, with no metadata exception and no count/key/order/null/admin drift. Actual audit-hook probes deny network, mutable news and coordinator helpers, current/peer discovery reads, an existing producer-module import and writes outside the temporary tree: seven denials in each of two runs. The contract remains byte-exact at 15,320,920 bytes / `69f0244082d967c671fad29bf15bda5941f819271f63c0654366b3202c87337b`; the parish sensitivity CSV remains byte-exact.

[Complete-context negative validation](data/turnout/repair-proof/complete-context-negative-validation.json) rejects 15 source mutations using the entire three-year source/native/candidate/method/null/admin/header/position/companion/order/parent packet, and five full-inventory packaging mutations: omitted audit, omitted seal, omitted history, altered seal and a cyclic reverse manifest pin. Exact base packets and reversible input recipes preserve complete failing inputs without truncation. These are historical-source and packaging tests, not election-outcome/calculator tests.

The acyclic construction is **proofs → validation → pre-manifest audit proof → final seal → manifest LAST**. The current audit proof does not contain a current/future manifest or seal digest. The [final seal](data/turnout/final-seal.json) pins all prepared bodies except itself and the future manifest; the manifest then pins every current owned body including the seal, excluding only the manifest itself. Old manifest-bearing audits remain exact archived history. All ordered archive parts are strictly below 40,000,000 bytes and concatenate to reconstruct exact gzip/tar bytes.

The final command is read-only and prints **stdout only**; no owned file is written after it passes:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/louisiana/data/turnout/final_audit.py
```

Run the original extraction/build reproduction only through the captured temporary replay described above. Rebuilding proof files or resealing is a new preparation operation; it must precede manifest-last and a new stdout-only final audit. Source/native/candidate/numeric/coverage/order/null/admin fields and the original-first witnesses remain unchanged. Coordinator acceptance remains false; November/current native dispatch remains empty. Current ballot, legal orders, geometry, eligible write-in and provisional remainder, early aggregate composition, roll cutoff, true ballots/blank/under/over counts, live votes/cadence/pools, collector, forecast and probability approval remain unavailable or unapproved. No new source or numerical model was adopted.
