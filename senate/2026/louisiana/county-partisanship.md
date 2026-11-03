# Louisiana historical partisanship and conditional paths

Research completed October 20, 2026. **All 64 parishes and every 3,933/4065/4062 original native result row are included.** Louisiana had no 2024 Senate contest. The primary volume basis is2024 president;2020 Cassidy is the same Class II seat, and 2022 Kennedy is the other Class III seat/midterm. These are historical outcomes and conditional arithmetic, with no 2026 turnout forecast or calibrated probability.

The complete [parish baselines](data/county-baselines.csv), [native baselines](data/baselines/native-baselines.json.gz), [candidate field](data/baselines/candidates.csv), [original-first freeze](data/baselines/original-freeze.json) and [schema](data/baselines/source/SCHEMA.md) support this report. Native source rows include ward/precinct, Early Voting and Provisional Votes identities; source-native completeness does not establish current polygons or a November crosswalk.

## Original sources and complete candidate fields

The [SOS results authority](https://www.sos.la.gov/elections-voting/election-results-statistics) publishes the script transformation leading to the [graphical application](https://voterportal.sos.la.gov/graphical). Its public client supplies the actual historical metadata/download constructors. Individually pinned [full receipts](data/baselines/source/receipts.json) retain requested/final URLs, UTC, status, headers, source clocks and raw/stored hashes. Final replay depends on those exact originals, not a mutable newsroom ledger or another worker’s parser. Complete workbooks, unrelated-office bytes and all physical row/cell positions survive; only the three required contests receive substantive analyses.

**2024:** [official parish CSV](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/csv/ByParish_67190.csv), [complete native CSV](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/csv/ByPrecinct_67190.csv), [complete original workbook](https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/20241105/Election+Results+(11-05-2024).xlsx). Every candidate’s native sum equals its parish sum and workbook statewide control; totals below use the complete named-candidate field.

| Candidate / source ballot label | Votes | % all named candidates |
| --- | --- | --- |
| Kamala D. Harris, Tim Walz Democratic (DEM) | 766,870 | 38.210 |
| Jill Stein, Ajamu Baraka Green (GRN) | 7,138 | 0.356 |
| Chase Oliver, Mike ter Maat Libertarian (LBT) | 6,835 | 0.341 |
| Donald J. Trump, "JD" Vance Republican (REP) | 1,208,505 | 60.215 |
| Peter Sonski, Lauren Onak American Solidarity Party (OTH) | 2,240 | 0.112 |
| Randall Terry, Stephen Broden Constitution Party (OTH) | 1,424 | 0.071 |
| Mattie Preston, Shannel Conner Godliness, Truth, Justice (OTH) | 2,857 | 0.142 |
| Cornel West, Melina Abdullah Justice For All (OTH) | 2,623 | 0.131 |
| Claudia de la Cruz, Karina Garcia Socialism and Liberation (OTH) | 1,481 | 0.074 |
| Rachele Fruit, Dennis Richter Socialist Workers Party (OTH) | 361 | 0.018 |
| Robert F. Kennedy, Jr., Nicole Shanahan We The People (OTH) | 6,641 | 0.331 |

**2022:** [official parish CSV](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20221108/csv/ByParish_61897.csv), [complete native CSV](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20221108/csv/ByPrecinct_61897.csv), [complete original workbook](https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/20221108/Election+Results+(11-08-2022).xlsx). Every candidate’s native sum equals its parish sum and workbook statewide control; totals below use the complete named-candidate field.

| Candidate / source ballot label | Votes | % all named candidates |
| --- | --- | --- |
| Beryl A. Billiot (NOPTY) | 9,378 | 0.678 |
| Gary Chambers, Jr. (DEM) | 246,933 | 17.851 |
| Devin Lance Graham (REP) | 25,275 | 1.827 |
| "Xan" John (OTH) | 2,753 | 0.199 |
| John Kennedy (REP) | 851,568 | 61.561 |
| W. Thomas La Fontaine Olson (NOPTY) | 1,676 | 0.121 |
| Bradley McMorris (IND) | 5,388 | 0.390 |
| MV "Vinny" Mendoza (DEM) | 11,910 | 0.861 |
| "Luke" Mixon (DEM) | 182,887 | 13.221 |
| Salvador P. Rodriguez (DEM) | 7,767 | 0.561 |
| Aaron C. Sigler (LBT) | 4,865 | 0.352 |
| Syrita Steib (DEM) | 31,568 | 2.282 |
| Thomas Wenn (OTH) | 1,322 | 0.096 |

**2020:** [official parish CSV](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20201103/csv/ByParish_59569.csv), [complete native CSV](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20201103/csv/ByPrecinct_59569.csv), [complete original workbook](https://s3-us-west-2.amazonaws.com/mediaresults.sos.la.gov/HumanReadableElectionResults/20201103/Election+Results+(11-03-2020).xlsx). Every candidate’s native sum equals its parish sum and workbook statewide control; totals below use the complete named-candidate field.

| Candidate / source ballot label | Votes | % all named candidates |
| --- | --- | --- |
| Beryl Billiot (NOPTY) | 17,362 | 0.838 |
| John Paul Bourgeois (NOPTY) | 16,518 | 0.797 |
| "Bill" Cassidy (REP) | 1,228,908 | 59.323 |
| Reno Jean Daret III (NOPTY) | 3,954 | 0.191 |
| Derrick "Champ" Edwards (DEM) | 229,814 | 11.094 |
| "Xan" John (OTH) | 2,813 | 0.136 |
| David Drew Knight (DEM) | 36,962 | 1.784 |
| M.V. "Vinny" Mendoza (IND) | 7,811 | 0.377 |
| Jamar Montgomery (NOPTY) | 5,804 | 0.280 |
| Dustin Murphy (REP) | 38,383 | 1.853 |
| Adrian Perkins (DEM) | 394,049 | 19.022 |
| Antoine Pierce (DEM) | 55,710 | 2.689 |
| Melinda Mary Price (OTH) | 7,680 | 0.371 |
| Aaron C. Sigler (LBT) | 11,321 | 0.547 |
| Peter Wenstrup (DEM) | 14,454 | 0.698 |

Independent, Libertarian, No Party, Green and Other candidates remain distinct. The CSV abbreviation OTH and workbook/metadata OTHER survive literally with an explicit comparison alias. The 2024 source names Stein/Ajamu Baraka; this report does not silently repair that running-mate label into a legal identity. Party totals in the data are descriptive historical sums, not named coalitions or2026 nominees.

Cassidy received 1,228,908/2,071,543 (59.323%) and Kennedy 851,568/1,383,290 (61.561%): each won an actual majority in the historical first election, so no runoff was needed. Their majority thresholds were 1,035,772 and 691,646 named votes, respectively. The complete multi-candidate field and electorate remain distinct from any deterministic pair scenario. The [primary majority rule](https://www.legis.la.gov/legis/Law.aspx?d=81616), source metadata and elected outcome objects are separately retained.

## Native coverage, turnout controls and priority

The original-source [hierarchy](data/baselines/native-hierarchy.json.gz), [coverage](data/baselines/native-coverage.json), [position links](data/baselines/native-position-links.json.gz), [whole-workbook witness](data/baselines/source/workbook-position-witness.json.gz) and [scope controls](data/baselines/scope-controls.json) retain parent/child arrays, candidate/method/null objects and exact source locations. CSV ward and precinct are separate literal fields; workbook display concatenates them with a space, including administrative trailing spaces. Local workbook tabs are overlapping views and incomplete tab coverage does not imply missing statewide multi-parish records.

| Historical contest | All named votes | Native source rows | General qualified | General voted | Selected-race qualified | Selected-race voted |
| --- | --- | --- | --- | --- | --- | --- |
| 2024 | 2,006,975 | 3933 | 3,046,376 | 2,021,164 | 3,046,376 | 2,021,164 |
| 2022 | 1,383,290 | 4065 | 3,018,815 | 1,410,476 | 3,018,815 | 1,410,466 |
| 2020 | 2,071,543 | 4062 | 3,093,003 | 2,169,400 | 3,092,988 | 2,169,413 |

Controls above come from each official client’s [2024 StatsStatewide](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/StatsStatewide.htm), [2022 StatsStatewide](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20221108/StatsStatewide.htm), [2020 StatsStatewide](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20201103/StatsStatewide.htm), [2024 RaceStats](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20241105/StatsRace/Stats_67190.htm), [2022 RaceStats](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20221108/StatsRace/Stats_61897.htm), [2020 RaceStats](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20201103/StatsRace/Stats_59569.htm), and all 64 native StatsRaceParish/VotesRaceByPrecinct objects, preserved as complete [own acquisitions and receipts](data/baselines/source/) and extracted in scope-controls. The 2022 selected-race voted total is 10 below general Stats, entirely in East Baton Rouge. In 2020 selected-race qualified is 15 below general Stats (Calcasieu4, Lincoln2, Orleans4, Webster5), while voted is 13 above (Caddo4, East Baton Rouge9). No rescaling, residual allocation or correction chronology is inferred.

Qualified is the source All/VoterCountQualified; active/inactive registration scope and roll cutoff remain unspecified. Voted is the published voter statistic, not an asserted physical-ballot count. Blank, under/over votes, generic/named write-in allocation and voting-eligible turnout are unknown here. The differences from candidate votes cannot be assigned to one of those categories. Native known qualified/voted sums reproduce selected RaceStats; early/provisional controls remain null, together with5/11/13 additional ordinary-looking zero-vote rows in 2024/2022/2020. Those rows remain in the source universe and arithmetic.

| Year | Ward/precinct votes | Early Voting aggregate | Provisional Votes |
| --- | --- | --- | --- |
| 2024 | 1,038,976 | 967,415 | 584 |
| 2022 | 1,011,323 | 371,766 | 201 |
| 2020 | 1,114,110 | 956,850 | 583 |

These are source-method sums of the cited complete native CSVs/API, not ballots or separate geographic polygons. Early Voting aggregate composition is unproved; no early-in-person/mail split is inferred. Statistics rows overlap voter controls, rather than adding a second vote pool. Reporting/expected precinct and absentee flags, HasReported and literal clocks are retained without converting percent precincts into percent votes counted.

The [complete historical priority contract](data/baselines/historical-priority-contract.json.gz) and [all 27 full source orders](data/baselines/all-source-orders.json.gz) retain every unit and parent, including zero-vote and outside-priority contexts. Descending vote order uses literal source-key tie breaking; exact minimum80 uses5*cumulative≥4*total.

| Year / historical scope | Universe | Minimum80 rows | Before crossing | At crossing | Crossing identity |
| --- | --- | --- | --- | --- | --- |
| 2024 native | 3933 | 1516 | 1,605,350 | 1,605,649 | ["2024","07","06","03"] |
| 2024 parish | 64 | 24 | 1,602,004 | 1,620,459 | Washington |
| 2022 native | 4065 | 1907 | 1,106,608 | 1,106,852 | ["2022","56","00","19"] |
| 2022 parish | 64 | 25 | 1,103,308 | 1,115,462 | Iberville |
| 2020 native | 4062 | 1552 | 1,657,026 | 1,657,333 | ["2020","26","00","K011"] |
| 2020 parish | 64 | 24 | 1,653,160 | 1,672,018 | Washington |

For2024 native priority, the1,516th row is Bienville06/03 with 299 votes; previous1,605,350 and crossing1,605,649 bracket the exact threshold1,605,580. The top 15 native rows contribute689,455 votes. For the separate64-parish sensitivity, top 15 contribute1,391,066/2,006,975=69.312%, and the first 24 cross at Washington. The historical24-parish set is: East Baton Rouge, Jefferson, Orleans, St. Tammany, Lafayette, Caddo, Calcasieu, Livingston, Ouachita, Ascension, Tangipahoa, Rapides, Bossier, Lafourche, Terrebonne, St. Landry, Iberia, Acadia, St. Charles, Vermilion, St. Martin, St. Mary, St. John The Baptist, Washington.

**Current canonical dispatch is null/empty.** Historical source completeness is recorded; coordinator acceptance and actual November native-ID/geometry closure are unverified. Parish priority is never substituted for finer dispatch.

## Named pairs and conditional targets

A/B means Harris/Trump2024, Chambers/Kennedy2022, and Perkins/Cassidy2020. These pairs preserve all other named candidates; Chambers and Perkins do not absorb other Democrats. The [full-field constraints](data/baselines/full-field-constraints.json) keep plurality and majority thresholds separate. A pair tie, or pair A+1, does not guarantee a full-field win or historical majority.

At fixed two-candidate weights, tie shift=(B−A)/(2(A+B)). An illustrative A+1 **pair-margin** target adds0.5 A-share points to the unbounded tie shift. One A-share point is two pair-margin points and0.02*pair-volume net votes. Net votes, share points, pair-margin points and complete-field margin points are separately reported. Values below are percentage-point shifts; native bounded shifts clip each share to[0,1] and solve the feasible common root, so clipping may change both the required shift and tie-to-cushion gap.

| Anchor | Pair votes | All named votes | A−B net | Tie unbounded pp | Tie native clipped pp | A+1 unbounded pp | A+1 native clipped pp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2024 | 1,975,375 | 2,006,975 | -441,635 | 11.179 | 11.429 | 11.679 | 11.957 |
| 2022 | 1,098,501 | 1,383,290 | -604,635 | 27.521 | 28.691 | 28.021 | 29.235 |
| 2020 | 1,622,957 | 2,071,543 | -834,859 | 25.720 | 26.445 | 26.220 | 26.987 |

Every [scenario input/output](data/baselines/scenarios/), [state result](data/baselines/state-scenarios.csv) and [all-unit contribution/selected threshold](data/baselines/all-unit-scenarios.json.gz) is saved. Each unit supplies source-based volume, pair participation/share, pair/all weights, baseline/target net, gain and+1 share-point net-vote value. Positive-pool unknown preference stays unknown; zero-pair preference stays undefined. Impossible/already-secured/no-pool cases remain explicit.

The following primary2024 native partitions show why outside-priority units remain necessary. These are computed over all 3,933 source rows at their own2024 volumes, with fixed participation and the common clipped shift.

| Pair target | Partition | Rows | Pair votes | Pair weight % | Baseline net | Target net | Net gain |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | priority | 1516 | 1,582,438.000 | 80.108 | -416,598.000 | -58,523.590 | 358,074.410 |
| 0.0 | outside-priority | 2417 | 392,937.000 | 19.892 | -25,037.000 | 58,523.590 | 83,560.590 |
| 0.01 | priority | 1516 | 1,582,438.000 | 80.108 | -416,598.000 | -42,237.107 | 374,360.893 |
| 0.01 | outside-priority | 2417 | 392,937.000 | 19.892 | -25,037.000 | 61,990.857 | 87,027.857 |

### All 64-parish historical comparison and selected-only sensitivity

This table is a parish scenario, retaining all 64 in every state calculation.2024 counts come from the cited original presidential CSV;2022/2020 are the cited named Senate pair shares, not Democratic party sums. Tie target applies the common2024 **parish** bounded shift at2024 parish volume/participation. Selected-only holds every other parish at its original2024 pair preference, preserving the whole-state1,975,375 pair denominator. Raw requirements outside[0,100]% are impossible/already-secured and remain untrimmed; they are not individual necessary conditions.

| Rank | Parish | 2024 all | Harris | Trump | Harris pair % | Chambers pair % | Perkins pair % | 2024 tie target % | Selected-only tie % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | East Baton Rouge | 190,643 | 103,820 | 82,720 | 55.656 | 39.590 | 38.559 | 66.834 | 174.03 (impossible) |
| 2 | Jefferson | 178,205 | 75,731 | 98,810 | 43.389 | 22.226 | 26.622 | 54.567 | 169.90 (impossible) |
| 3 | Orleans | 159,130 | 130,749 | 24,119 | 84.426 | 71.826 | 72.203 | 95.605 | 227.01 (impossible) |
| 4 | St. Tammany | 138,384 | 37,777 | 98,377 | 27.746 | 11.034 | 13.865 | 38.924 | 189.93 (impossible) |
| 5 | Lafayette | 111,086 | 37,170 | 72,007 | 34.046 | 19.812 | 19.930 | 45.224 | 236.30 (impossible) |
| 6 | Caddo | 94,699 | 48,864 | 44,471 | 52.353 | 32.068 | 43.045 | 63.532 | 288.94 (impossible) |
| 7 | Calcasieu | 81,201 | 23,918 | 56,064 | 29.904 | 16.719 | 10.051 | 41.083 | 305.99 (impossible) |
| 8 | Livingston | 65,906 | 9,965 | 55,101 | 15.315 | 6.552 | 6.677 | 26.494 | 354.69 (impossible) |
| 9 | Ouachita | 64,436 | 22,845 | 40,808 | 35.890 | 17.843 | 19.977 | 47.068 | 382.80 (impossible) |
| 10 | Ascension | 62,473 | 20,113 | 41,319 | 32.740 | 19.004 | 17.541 | 43.919 | 392.19 (impossible) |
| 11 | Tangipahoa | 55,104 | 16,886 | 37,500 | 31.048 | 15.098 | 17.794 | 42.227 | 437.07 (impossible) |
| 12 | Rapides | 53,395 | 16,537 | 36,171 | 31.375 | 16.569 | 14.825 | 42.553 | 450.32 (impossible) |
| 13 | Bossier | 52,232 | 14,467 | 37,105 | 28.052 | 13.561 | 21.029 | 39.231 | 456.23 (impossible) |
| 14 | Lafourche | 42,845 | 7,864 | 34,461 | 18.580 | 7.801 | 7.709 | 29.759 | 540.30 (impossible) |
| 15 | Terrebonne | 41,327 | 9,702 | 31,115 | 23.770 | 10.228 | 11.513 | 34.948 | 564.76 (impossible) |
| 16 | St. Landry | 37,043 | 14,833 | 21,812 | 40.478 | 25.350 | 24.118 | 51.656 | 643.06 (impossible) |
| 17 | Iberia | 29,331 | 9,504 | 19,511 | 32.755 | 17.409 | 17.390 | 43.934 | 793.80 (impossible) |
| 18 | Acadia | 26,720 | 4,695 | 21,783 | 17.732 | 9.612 | 9.392 | 28.910 | 851.70 (impossible) |
| 19 | St. Charles | 26,685 | 8,812 | 17,443 | 33.563 | 18.316 | 17.161 | 44.742 | 874.61 (impossible) |
| 20 | Vermilion | 26,429 | 4,637 | 21,510 | 17.734 | 8.311 | 8.135 | 28.913 | 862.26 (impossible) |
| 21 | St. Martin | 25,006 | 7,284 | 17,466 | 29.430 | 17.024 | 15.703 | 40.609 | 921.62 (impossible) |
| 22 | St. Mary | 20,897 | 7,011 | 13,671 | 33.899 | 19.005 | 20.410 | 45.078 | 1101.58 (impossible) |
| 23 | St. John The Baptist | 18,827 | 12,043 | 6,557 | 64.747 | 43.810 | 39.042 | 75.926 | 1251.94 (impossible) |
| 24 | Washington | 18,455 | 5,411 | 12,846 | 29.638 | 18.401 | 15.767 | 40.816 | 1239.13 (impossible) |
| 25 | Lincoln | 18,157 | 6,627 | 11,248 | 37.074 | 18.645 | 21.255 | 48.253 | 1272.42 (impossible) |
| 26 | St. Bernard | 17,292 | 5,967 | 11,033 | 35.100 | 19.727 | 15.866 | 46.279 | 1334.03 (impossible) |
| 27 | Webster | 16,205 | 5,053 | 10,965 | 31.546 | 19.083 | 26.513 | 42.724 | 1410.10 (impossible) |
| 28 | Vernon | 16,149 | 2,513 | 13,474 | 15.719 | 6.534 | 5.777 | 26.898 | 1396.95 (impossible) |
| 29 | Avoyelles | 16,037 | 4,460 | 11,379 | 28.158 | 10.356 | 12.041 | 39.337 | 1422.30 (impossible) |
| 30 | Beauregard | 15,874 | 2,192 | 13,504 | 13.965 | 6.478 | 4.636 | 25.144 | 1420.80 (impossible) |
| 31 | Iberville | 15,354 | 7,503 | 7,616 | 49.626 | 37.364 | 30.622 | 60.805 | 1510.16 (impossible) |
| 32 | Natchitoches | 15,040 | 5,740 | 9,100 | 38.679 | 19.581 | 28.160 | 49.858 | 1526.67 (impossible) |
| 33 | Jefferson Davis | 14,358 | 2,699 | 11,478 | 19.038 | 10.000 | 9.768 | 30.216 | 1576.61 (impossible) |
| 34 | Evangeline | 14,176 | 3,526 | 10,483 | 25.170 | 16.273 | 12.025 | 36.348 | 1601.42 (impossible) |
| 35 | De Soto | 13,913 | 4,426 | 9,359 | 32.107 | 16.436 | 29.966 | 43.286 | 1633.98 (impossible) |
| 36 | West Baton Rouge | 13,836 | 6,008 | 7,627 | 44.063 | 30.955 | 26.592 | 55.242 | 1663.55 (impossible) |
| 37 | St. James | 11,789 | 5,792 | 5,902 | 49.530 | 23.663 | 31.717 | 60.708 | 1937.83 (impossible) |
| 38 | Pointe Coupee | 11,570 | 4,132 | 7,319 | 36.084 | 22.238 | 20.468 | 47.263 | 1964.45 (impossible) |
| 39 | Union | 10,475 | 2,206 | 8,176 | 21.248 | 8.639 | 10.614 | 32.427 | 2148.17 (impossible) |
| 40 | Assumption | 10,367 | 3,273 | 6,963 | 31.975 | 19.680 | 17.418 | 43.154 | 2189.24 (impossible) |
| 41 | Sabine | 10,170 | 1,488 | 8,613 | 14.731 | 6.568 | 10.772 | 25.910 | 2200.83 (impossible) |
| 42 | Morehouse | 10,097 | 4,008 | 5,961 | 40.205 | 23.070 | 22.676 | 51.383 | 2255.25 (impossible) |
| 43 | East Feliciana | 9,947 | 3,809 | 6,020 | 38.753 | 26.333 | 22.802 | 49.931 | 2285.34 (impossible) |
| 44 | Plaquemines | 9,945 | 3,023 | 6,803 | 30.765 | 16.941 | 14.836 | 41.944 | 2278.04 (impossible) |
| 45 | Richland | 9,193 | 2,732 | 6,354 | 30.068 | 16.386 | 13.901 | 41.247 | 2460.37 (impossible) |
| 46 | Grant | 9,018 | 996 | 7,925 | 11.165 | 4.310 | 4.002 | 22.343 | 2486.42 (impossible) |
| 47 | Franklin | 8,798 | 2,196 | 6,524 | 25.183 | 10.673 | 11.034 | 36.362 | 2557.49 (impossible) |
| 48 | Allen | 8,751 | 1,661 | 7,003 | 19.171 | 9.706 | 6.389 | 30.350 | 2567.85 (impossible) |
| 49 | Concordia | 7,755 | 2,698 | 4,974 | 35.167 | 16.642 | 18.667 | 46.345 | 2913.39 (impossible) |
| 50 | Jackson | 7,226 | 1,852 | 5,291 | 25.927 | 13.936 | 16.129 | 37.106 | 3117.31 (impossible) |
| 51 | Lasalle | 6,620 | 546 | 6,023 | 8.312 | 3.047 | 3.088 | 19.490 | 3369.82 (impossible) |
| 52 | Bienville | 6,256 | 2,531 | 3,660 | 40.882 | 26.140 | 35.674 | 52.060 | 3607.63 (impossible) |
| 53 | West Feliciana | 6,008 | 2,004 | 3,923 | 33.811 | 13.313 | 20.662 | 44.990 | 3759.43 (impossible) |
| 54 | Claiborne | 5,816 | 2,239 | 3,522 | 38.865 | 21.866 | 30.130 | 50.043 | 3871.84 (impossible) |
| 55 | Winn | 5,781 | 1,292 | 4,437 | 22.552 | 11.183 | 11.331 | 33.730 | 3876.93 (impossible) |
| 56 | St. Helena | 5,745 | 2,848 | 2,804 | 50.389 | 31.261 | 34.366 | 61.568 | 3957.28 (impossible) |
| 57 | West Carroll | 4,603 | 578 | 3,986 | 12.664 | 5.273 | 6.412 | 23.843 | 4850.91 (impossible) |
| 58 | Catahoula | 4,348 | 1,060 | 3,258 | 24.548 | 13.695 | 13.996 | 35.727 | 5138.43 (impossible) |
| 59 | Caldwell | 4,334 | 580 | 3,724 | 13.476 | 5.227 | 5.725 | 24.654 | 5143.99 (impossible) |
| 60 | Madison | 3,992 | 2,094 | 1,846 | 53.147 | 32.940 | 31.826 | 64.326 | 5657.65 (impossible) |
| 61 | Red River | 3,725 | 1,321 | 2,337 | 36.113 | 18.108 | 34.261 | 47.291 | 6072.68 (impossible) |
| 62 | Cameron | 3,362 | 219 | 3,120 | 6.559 | 2.353 | 2.011 | 17.737 | 6619.84 (impossible) |
| 63 | East Carroll | 2,306 | 1,338 | 931 | 58.969 | 43.062 | 37.938 | 70.147 | 9790.90 (impossible) |
| 64 | Tensas | 2,128 | 1,002 | 1,093 | 47.828 | 29.688 | 21.378 | 59.007 | 10588.04 (impossible) |

The same selected-only formula is saved for every native source row under every applicable historical sensitivity; other units stay at their explicit scenario baseline. Requirement=(target*final_pair_denominator−fixed_other_net+selected_pair_volume)/(2*selected_pair_volume). A selected zero-pair unit cannot move the state target.

### Historical volume/mix and preference sensitivity

Parish low/base/high uses the complete2022 Senate/2024 president/2020 Senate candidate-vote volume and mix, respectively, crossed separately with2024/2022/2020 preference and pair-participation anchors. Every volume/participation combination is explicit: scenario pair volume=mix-year complete-field volume*preference-year pair participation in each parish. The low/base/high ordering labels total historical anchors, not2026 bounds. Different Senate candidates and electorates are not exchangeable forecasts.

Native low/base/high stays within each year’s literal identities:0.8/1.0/1.2 times source volume, with an additional1.25 Early Voting aggregate multiplier only in high. These are stated illustrative stress assumptions around historical observed volumes, not measured likely ranges. No cross-year native join, lower-preference inference or candidate-effect estimate occurs. Source zero-pair/unknown contexts remain present.

| Preference / scope / mix | All scenario votes | Pair scenario votes | Tie clipped pp | A+1 clipped pp |
| --- | --- | --- | --- | --- |
| 2024-parish-low-2022-volume-mix | 1,383,290.000 | 1,361,544.543 | 11.035 | 11.535 |
| 2024-parish-base-2024-volume-mix | 2,006,975.000 | 1,975,375.000 | 11.179 | 11.679 |
| 2024-parish-high-2020-volume-mix | 2,071,543.000 | 2,038,855.001 | 10.869 | 11.369 |
| 2024-native-low-0.8-native-volume | 1,605,580.000 | 1,580,300.000 | 11.429 | 11.957 |
| 2024-native-base-native-volume | 2,006,975.000 | 1,975,375.000 | 11.429 | 11.957 |
| 2024-native-high-1.2-native-volume-early1.25 | 2,698,594.500 | 2,657,399.100 | 11.462 | 11.987 |
| 2022-parish-low-2022-volume-mix | 1,383,290.000 | 1,098,501.000 | 27.521 | 28.021 |
| 2022-parish-base-2024-volume-mix | 2,006,975.000 | 1,594,543.846 | 27.686 | 28.187 |
| 2022-parish-high-2020-volume-mix | 2,071,543.000 | 1,643,504.755 | 27.438 | 27.938 |
| 2022-native-low-0.8-native-volume | 1,106,632.000 | 878,800.800 | 28.691 | 29.235 |
| 2022-native-base-native-volume | 1,383,290.000 | 1,098,501.000 | 28.691 | 29.235 |
| 2022-native-high-1.2-native-volume-early1.25 | 1,771,477.800 | 1,402,418.700 | 28.746 | 29.288 |
| 2020-parish-low-2022-volume-mix | 1,383,290.000 | 1,084,315.739 | 25.876 | 26.376 |
| 2020-parish-base-2024-volume-mix | 2,006,975.000 | 1,573,899.846 | 26.012 | 26.512 |
| 2020-parish-high-2020-volume-mix | 2,071,543.000 | 1,622,957.000 | 25.720 | 26.220 |
| 2020-native-low-0.8-native-volume | 1,657,234.400 | 1,298,365.600 | 26.445 | 26.987 |
| 2020-native-base-native-volume | 2,071,543.000 | 1,622,957.000 | 26.445 | 26.987 |
| 2020-native-high-1.2-native-volume-early1.25 | 2,772,906.600 | 2,170,390.200 | 25.890 | 26.432 |

## Counted-plus-remainder calculator

The offline [calculator](data/baselines/calculator.py) and [complete JSON contract](data/baselines/source/SCHEMA.md#offline-calculator-json-contract) keep counted A/B/every-other votes fixed. Only explicitly supplied remaining volume receives preferences and other allocations. Final pair denominator=counted pair+remaining pair; final complete-field denominator=all counted+all remaining. Inputs are arithmetic assumptions, not remaining-ballot estimates or calibrated probabilities.

Example [saved input](data/baselines/fixtures/counted-fixed-final-denominator.input.json) has counted A 10/B 20/C 5 and 100 remaining with 80% pair participation,50% A pair share and all nonpair remainder to C. Final A 50/B 60/C 25, pair denominator 110 and full denominator 135; the tie requires A 56.25% of the 80 remaining pair votes. Counted votes never swing. [Unknown](data/baselines/fixtures/unknown-positive-pool.stdout.json), [no-pool](data/baselines/fixtures/no-pool-below.stdout.json), [impossible](data/baselines/fixtures/negative-lead.stdout.json), [secured](data/baselines/fixtures/secured-even-zero-share.stdout.json), [clipping](data/baselines/fixtures/clipping-root-distinct.stdout.json) and [pair-leader/full-field-loss](data/baselines/fixtures/pair-leader-loses-fullfield.stdout.json) cases are retained. Negative/invalid inputs return strict JSON and nonzero exit without stderr/traceback.

## Current law, setup identities and limits

Independently inspected primary authority distinguishes Senate nomination from general election: [R.S.18:2](https://www.legis.la.gov/legis/Law.aspx?d=81529) includes U.S.Senate as a party-primary office; [R.S.18:410.7](https://www.legis.la.gov/legis/Law.aspx?d=1341864) requires a party-primary majority and, when necessary, a second party primary; [R.S.18:512](https://www.legis.la.gov/legis/Law.aspx?d=81617) elects the general-election candidate receiving the most votes. The [current SOS explanation](https://www.sos.la.gov/elections-voting/closed-party-primary-elections) independently describes plurality at the general stage. Complete legal bodies and receipts are retained under source/law-*. The separate [House suspension](https://gov.louisiana.gov/news/5093) does not transfer House’s2026 exception to Senate. Historical CanHaveRunoff flags do not establish current nomination or general rules.

The retained [official November setup metadata](https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob=20261103/RacesCandidates_Multiparish.htm) lists race67997, choice124654 “Jamie” Davis(DEM),124655 Julia Letlow(REP), CanHaveRunoff0 and IsClosedParty0, WriteTime2026-10-18T05:00:06.330 with unspecified timezone. This is complete published setup metadata, not genuine counts or signed final-ballot/withdrawal proof; **actual current ballot mapping remains unknown**. No primary nominee or old ID is promoted into a confirmed general ballot. The retained current election-date HTML and July-revised calendar disagree on qualifying chronology; no amendment/cause is inferred. Configured120-second refresh, IsLive=True, static offset−5 and null ElectionMode are observations, not demonstrated cadence, poll-close law or current returns.

Later roster/legal changes, eligible write-in allocation, current geometry/IDs, method compatibility, actual remaining pools and calibration remain precise external qualifications. They do not prevent finishing this historical research package. No implemented live collector, approved map, legal election call or calibrated Needle is claimed.

## Independent comparison, reproduction and checks

The original-only extraction/control/hierarchy/full-order/position witness was frozen before peer numerical files were opened. Complete [peer inputs and receipts](data/baselines/peer-capture/capture.json) were captured before comparisons. The [source agreement](data/baselines/peer-source-agreement.json) checks146,652 historical source-field comparisons with zero remaining discrepancies, including all 39 candidate columns,192 parish vectors,12,060 native vectors/positions/controls, methods/nulls and all 27 descending orders/integer80 crossings. Proof is limited to captured historical source fields, not future/final outcomes or calculator equality. Adapter spellings, column bases and explicit key mapping are recorded; no peer values repaired originals.

Meaningful [offline validation](data/baselines/validation.json) passes61 saved synthetic actual-CLI fixtures, two [complete historical CLI fixtures](data/baselines/fixtures/historical-cli-results.json),36 independent piecewise clipping/whole-state residual checks and73,512 selected-threshold substitution checks. [Original-only reproduction](data/baselines/reproduction.json) reproduces72 artifacts byte-for-byte in a temporary isolated mirror. The [audit](data/baselines/audit.py) verifies original/owned hashes, candidate/method balances, identity/hierarchy coverage, exact rank/80, links/schema and strict<40,000,000-byte file bounds.

Exact failed scripts/checkers/inputs/outputs/claims are preserved in [history](data/baselines/history/) before bounded repairs: absent native voter-field extractor assumption; omitted optional native method multiplier in build; peer field/kind adapters; float-dictionary checker tolerance; and inclusion of an in-progress stdout log in the first freeze inventory. The original freeze itself is unchanged: completed stdout was preserved and its known exact empty frozen state restored. All source/count/model data remained unchanged. The final [seal](data/baselines/final-seal.json) precedes the [manifest](data/baselines/asset-manifest.json); the manifest includes every owned file except itself, including histories, proofs, validation and seal. Final audit is read-only after both.

Reproduce offline from the repository root:

```sh
python3 -B senate/2026/louisiana/data/baselines/reproduce.py
python3 -B senate/2026/louisiana/data/baselines/qa.py
python3 -B senate/2026/louisiana/data/baselines/source_cli.py
python3 -B senate/2026/louisiana/data/baselines/audit.py
```

The first command leaves final artifacts read-only; QA commands intentionally regenerate their owned validation/fixture outputs. After any authorized change, preserve prior failures/seal/manifest as applicable, regenerate the seal and manifest last, then run the final audit read-only. No Git commands or peer/shared-file writes were used.
