# Kentucky turnout and source-native reporting geography

Research completed from public original evidence captured through **2026-10-20 UTC**. **A complete statewide native presidential ordering is unavailable.** The [dispatch contract](data/turnout/priority-set.json) keeps canonical native total/order/top15/min80/priority/remainder **null** and ordered priority/dispatch keys **empty**. The complete120-county calculation below is a **county sensitivity**, with its own denominator; it does not substitute for precincts, wards, combined groups, ballot styles, or central administrative/method units. Peer existence is verified by the coordinator's session message; independent numerical agreement and coordinator acceptance remain pending.

The primary historical contest is **2024 President and Vice President**, because Kentucky had no2024 Senate general election. **2020 McConnell–McGrath** is the same ClassII Senate seat; **2022 Paul–Booker** is the separate ClassIII Senate midterm comparator. Each uses all reported candidate/named-write-in columns. Candidate votes, ballots cast, voter-history participation, and dated registration are separate measurements. The sources are [2024 state certificate](https://elect.ky.gov/results/2020-2029/Documents/2024%20General%20Election%20Certification%20as%20Amended%20on%20December%209th%202024.pdf) ([exact archived original](https://web.archive.org/web/20241223120817id_/https://elect.ky.gov/results/2020-2029/Documents/2024%20General%20Election%20Certification%20as%20Amended%20on%20December%209th%202024.pdf)), [2022 state certificate](https://elect.ky.gov/results/2020-2029/Documents/2022%20General%20Election%20results.pdf) ([exact archived original](https://web.archive.org/web/20221223031129id_/https://elect.ky.gov/results/2020-2029/Documents/2022%20General%20Election%20results.pdf)), and [2020 state certificate](https://elect.ky.gov/results/2020-2029/Documents/2020%20General%20Election%20Results.pdf) ([exact archived original](https://web.archive.org/web/20201120170339id_/https://elect.ky.gov/results/2020-2029/Documents/2020%20General%20Election%20Results.pdf)); full individual receipts and exact raw/stored byte pins are in the [source registry](data/turnout/source/entities.json).

**Original-first evidence.** Before opening any coordinator numerical diagnostic/parser/table or peer derivative, this worker independently read original certificate bodies, extracted every120-county candidate position and printed footer, captured every linked2024 county recap, and retained native/method/admin/null/source-position contexts. [First immutable witness](data/turnout/history/original-first/witness.json), SHA256 `a101f4693c6cbf1ab0f1f0a5872a26037bbe24eb43f2d30760f3861d63afdafe`, and [complete addendum](data/turnout/history/original-first-v2/witness.json), SHA256 `04944536c174c7eef726789370114aabb7d553bc5b96784921b8a7cd42a8d747`, contain immutable script/extraction/receipt bodies and exact raw-source references. [Third original-first witness](data/turnout/history/original-first-v3/witness.json), SHA256 `cf42c9f312acbab43f7f4d3c52a68a47daa1648b7470e0f3406ecc978f7f4b45`, freezes the source-only correction after the offline checker found Madison's wrapped Kennedy numeric row. The [complete prior owned body witness](data/turnout/history/before-native-continuation-repair/witness.json) precedes that narrow repair. The qualified captured-native total increased by436 from restoring the full original row; no certificate or source byte changed. No peer count was used to repair an original source. Failed parsers, full prior output bodies, source-linked inputs and errors are retained in [history](data/turnout/history/). Later additions are owned original-source calculation/control/report work, not external numerical imports.

**County sensitivity result.** The descending top15 are **Jefferson, Fayette, Kenton, Boone, Warren, Campbell, Hardin, Daviess, Madison, Bullitt, Oldham, McCracken, Pulaski, Scott, Laurel**. They supply **1,094,747/2,074,530 = 52.7708444804%**. The minimum descending county set reaching80% contains **50 counties**, **1,660,226 votes = 80.0290186211%**. The preceding49 contain **1,650,178 = 79.5446679489%**; **Breckinridge (10,048)** crosses. The remaining70 contain **414,304** votes. Integer comparisons use `5*cumulative >= 4*denominator`; descending largest-first proves49 cannot reach80%. Ties use the complete source key/FIPS. These are computed directly from the [2024 state certificate](https://elect.ky.gov/results/2020-2029/Documents/2024%20General%20Election%20Certification%20as%20Amended%20on%20December%209th%202024.pdf) ([exact archived original](https://web.archive.org/web/20241223120817id_/https://elect.ky.gov/results/2020-2029/Documents/2024%20General%20Election%20Certification%20as%20Amended%20on%20December%209th%202024.pdf)); every county outside the sensitivity priority remains in the denominator.

The ordered county sensitivity50 is: **Jefferson, Fayette, Kenton, Boone, Warren, Campbell, Hardin, Daviess, Madison, Bullitt, Oldham, McCracken, Pulaski, Scott, Laurel, Jessamine, Franklin, Shelby, Pike, Nelson, Christian, Boyd, Hopkins, Barren, Henderson, Clark, Marshall, Greenup, Calloway, Graves, Floyd, Whitley, Woodford, Boyle, Meade, Muhlenberg, Knox, Anderson, Montgomery, Logan, Taylor, Grayson, Mercer, Spencer, Grant, Carter, Lincoln, Ohio, Harlan, Breckinridge**. The [complete county sensitivity JSON](data/turnout/county-sensitivity.json) retains every full order, ordered priority and remainder for all three contests and each separate volume/registration measure. The compatibility [county-turnout.csv](data/county-turnout.csv) has120 county-parent rows, all29 candidate columns, source scopes, exact shares/cumulatives and explicit canonical nulls. Its filename does not authorize any native-unit substitution.

**Candidate controls and tickets.** Every county sum equals its independently extracted printed statewide candidate footer:3,480 county candidate cells and29 controls. Presidential running mates share one vote column and are not counted again. Named Write-In labels are source ballot identities, not ordinary party affiliations; no generic pool is manufactured from missing named columns. Complete raw positioned headers, including spacing/case defects, and explicitly marked display transcriptions are retained in [headers](data/turnout/extracts/certificate-headers.json); every raw token has page, line, character span and full source row in [fields](data/turnout/extracts/certificate-fields.json). All selected first/final table pages were rendered and visually inspected; other county glyphs use the original text layer, not a claim of manual reading of every cell. Poppler's flate warnings are retained without modifying original PDFs.

| Contest / candidate (running mate where applicable) | Party / source label | County sum = printed footer |
| --- | --- | ---: |
| 2024-president: Donald J. TRUMP / J. D. VANCE | Republican Party | 1,337,494 |
| 2024-president: Kamala D. HARRIS / Tim WALZ | Democratic Party | 704,043 |
| 2024-president: Robert F. KENNEDY JR. / Nicole SHANAHAN | Independent | 16,769 |
| 2024-president: Jill STEIN / Samson KPADENOU | Kentucky Party | 7,566 |
| 2024-president: Chase OLIVER / Mike TER MAAT | Libertarian Party | 6,422 |
| 2024-president: Shiva AYYADURAI / Crystal ELLIS | Independent | 1,015 |
| 2024-president: Peter SONSKI / Lauren ONAK | Write-In | 611 |
| 2024-president: Claudia DE LA CRUZ / Karina GARCIA | Write-In | 391 |
| 2024-president: Cornel WEST / Melina ABDULLAH | Write-In | 177 |
| 2024-president: James D. SODERNA / Matthew J. TREWHELLA | Write-In | 14 |
| 2024-president: Jay J. BOWMAN / De BOWMAN | Write-In | 10 |
| 2024-president: Joseph KISHORE / Jerry WHITE | Write-In | 8 |
| 2024-president: John CHENG / Wayne WALIGORSKI | Write-In | 5 |
| 2024-president: Billy KELLEY JR. / Jason HOLDEMAN | Write-In | 4 |
| 2024-president: Cherunda FOX / Harlan McVAY JR. | Write-In | 1 |
| 2024-president: Andre Ramon McNEIL SR. / Roschelle McNEIL | Write-In | 0 |
| 2024-president: Future Madam POTUS / Jessica KENNEDY | Write-In | 0 |
| **2024-president all columns** | **Sum, not ballots** | **2,074,530** |
| 2022-senate: Rand PAUL | Republican Party | 913,326 |
| 2022-senate: Charles BOOKER | Democratic Party | 564,311 |
| 2022-senate: Charles Lee THOMASON | Write-In | 145 |
| 2022-senate: Billy Ray WILSON | Write-In | 48 |
| **2022-senate all columns** | **Sum, not ballots** | **1,477,830** |
| 2020-senate: Mitch McCONNELL | Republican Party | 1,233,315 |
| 2020-senate: Amy McGRATH | Democratic Party | 816,257 |
| 2020-senate: Brad BARRON | Libertarian Party | 85,386 |
| 2020-senate: Paul John FRANGEDAKIS | Write-In | 70 |
| 2020-senate: Daniel COBBLE | Write-In | 18 |
| 2020-senate: Randall Lee TEEGARDEN | Write-In | 9 |
| 2020-senate: Harold H. FITZPATRICK | Write-In | 1 |
| 2020-senate: Demetra WYSINGER | Write-In | 1 |
| **2020-senate all columns** | **Sum, not ballots** | **2,135,057** |

**Full native inventory and bounded recovery.** The actual [SBE2024 recap parent](https://elect.ky.gov/results/2020-2029/Pages/2024General-Recap-Sheets.aspx) supplied120 individual county PDF links. All120 complete originals downloadedHTTP200, totaling16,246 PDF pages, with exact requested/final URLs, UTC, HTTP headers/hops, byte sizes/hashes and full text bodies. [All120 coverage records](data/turnout/coverage.json) retain every county/FIPS, every captured recap constituent, explicit unavailable cases and source method/header positions. [Native raw rows](data/turnout/extracts/native-fields.jsonl.gz), [every source-page identity](data/turnout/extracts/native-page-identities.jsonl.gz), [manual Elliott rows](data/turnout/extracts/elliott-manual-fields.json), and [source-native unit vectors](data/turnout/native-units.jsonl.gz) preserve candidate, method, administrative and statistical fields. All source-native participation/registration/district-summary identities from2020/2022/2024 are separately retained in [statistics identities](data/turnout/source-native-statistics-identities.jsonl.gz), with no name/count-based precinct equivalence or cross-year/current join.

The inventory contains3,221 recap source entities:3,220 captured native slices across119 county parents plus Scott's county cumulative summary. A label/ID can denote a precinct, ward, split style, combined polling group or central method; the package preserves literal labels and publisher IDs where present and uses an owned hash-scoped key. Reporting locations, registered precinct counts and source reporting groups are not silently equated. County FIPS comes from the [2024 Census county identity table](https://tigerweb.geo.census.gov/tigerwebmain/Files/bas25/tigerweb_bas25_county_2024_acs24_ky.html); this establishes parent identifiers only.

Material original-source limits are precise:

- [Scott2024](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Scott.pdf) is a10-page **Cumulative Results Report**, not a native precinct report. The exact single observed CDX-listed archive returned the same raw original scope. The current clerk election authority page and a bounded public official search did not expose a historical native download. Scott's29,769 certificate votes remain in county statewide arithmetic; no finer allocation is reconstructed.
- [Magoffin2024](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Magoffin.pdf) has14 literal native units with **TOTAL / Mail In** columns. Their509 reported presidential votes are that captured method slice, not the county's5,274 valid certificate votes. Non-Mail-In native counts remain unknown; no residual is allocated.
- [Fayette2024 recap](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Fayette.pdf) totals57,344 Trump votes, three below the certificate's57,347; [Whitley2024 recap](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Whitley.pdf) totals2,236 Harris votes, one below the certificate's2,237. These source/vintage differences stay unchanged. All120×17 column comparisons, including unavailable cells and scope qualifiers, are in [native–certificate comparisons](data/turnout/native-certificate-comparisons.json).
- [Elliott2024](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Elliott.pdf) is16 image-only pages. Seven precinct presidential/statistical blocks were independently visually read, including explicit zero versus unavailable named write-ins. Complete16-page renders and uncorrected OCR survive; OCR mistakes were not promoted to counts. The printed source clock is03/12/2025 9:07AM, timezone unstated, separate from election/certification/retrieval dates.
- Generic write-in totals, named subrows and Not Assigned may overlap. Some Choice reports omit named write-in columns; those cells stay null rather than becoming zeros. Each raw candidate row and all reported methods remain source scoped. Source numerical closure within a captured slice does not establish a complete statewide valid-write-in native universe.

**Qualified known-native order.** Across the3,220 captured native slices, the reported candidate/write-in denominator is **2,042,278**, including generic/unassigned write-ins where the source includes them and Magoffin's Mail In slice; Scott's county summary is excluded. The top15 contribute **52,777 = 2.5842221284%**. A descending minimum **1,817** slices reaches **1,633,888 = 80.0032120994%**; preceding1,816 have **1,633,414**, and **Washington / D102 (474)** crosses. The remaining1,403 slices contain408,390 votes. This is a sensitivity within the captured source universe; it is not the unknown canonical statewide native ranking. [All3,220 ordered keys/integers/cumulatives and remainder](data/turnout/known-native-order.json) are complete for that qualified universe.

| Captured-slice rank | County / literal native label | Source reported candidate/write-in votes |
| ---: | --- | ---: |
| 1 | Montgomery / C101 | 4,350 |
| 2 | Montgomery / A101 | 4,258 |
| 3 | Montgomery / B101 | 4,213 |
| 4 | Pulaski / E101 | 3,946 |
| 5 | Grant / B102 | 3,909 |
| 6 | Grant / A101 | 3,814 |
| 7 | Grant / C103 | 3,746 |
| 8 | Franklin / C102 | 3,740 |
| 9 | Pulaski / D101 | 3,470 |
| 10 | Franklin / F101 | 3,088 |
| 11 | Warren / A102 | 2,921 |
| 12 | Warren / C107 | 2,921 |
| 13 | Graves / C110 | 2,902 |
| 14 | Graves / A101 | 2,759 |
| 15 | Kenton / B208 IND 1 IND-SB2 | 2,740 |

**Jefferson alternatives and historical handwritten originals.** The state-linked [Jefferson2024 native report](https://elect.ky.gov/results/2020-2029/2024ElectionReports/GeneralRecaps/Jefferson.pdf) is2,736 pages, with TOTAL, Election Day, Mail, Walk-in Excuse, Walk-in Early and Provisional fields. The [county alternative summary](https://elections.jeffersoncountyclerk.org/Gen24_Results.pdf) was direct403 and was recovered through its exact listed [archived original](https://web.archive.org/web/20250603004433id_/https://elections.jeffersoncountyclerk.org/Gen24_Results.pdf),34 complete image pages. Its11/08/2024 3:35PM clock is a different source view from the native report's12/05/2024 4:47PM, both timezone unstated. The alternative reports355,722 presidential cast votes and357,876 ballots; its2,113 generic write-ins include1,628 Not Assigned plus485 named write-ins. Thus its generic universe is not the certificate's named-valid universe. All six ballot candidates, six named write-in rows, generic/unassigned rows, method integers and ballot controls are retained in [alternative image readings](data/turnout/extracts/jefferson-alternative-fields.json), separately from state certificate/native data. No overlapping views are added together. The nominal2020 `Gen20SOVC.pdf` redirected to current generic Voting HTML; that fullHTTP200 HTML and original receipt remain a failure to acquire the2020 precinct PDF, not a PDF success. The current county historical parent returned403; no unobserved40MB link body is claimed captured.

The complete archived [Estill2020 recap](https://web.archive.org/web/20210116034430id_/https://elect.ky.gov/results/2020-2029/PublishingImages/2020General/61657_20201211_RECAP.pdf) (three pages) and [Lyon2020 recap](https://web.archive.org/web/20210116042754id_/https://elect.ky.gov/results/2020-2029/PublishingImages/2020General/61002_20201118_RECAP.pdf) (two pages) remain exact raw originals with all five full-page images. Estill PDF2 is sideways and PDF3 is a distinct local-office write-in sheet. All printed native/method/template columns, overlapping Mail-In/Walk-In/Total and scan/eSlate/eScan identities and selected presidential/Senate cell readings are in [hierarchy](data/turnout/extracts/historical-handwritten-hierarchy.json) and [cell witness](data/turnout/extracts/historical-handwritten-fields.json). Uncertain handwriting is explicitly null and excluded from arithmetic; template blanks differ from written zeros. These local handwritten views do not close historical statewide native coverage. Lyon's handwritten Votes Cast4,251 / Reg Voters6,691 is a source-specific control, not candidate votes or an eligible-voter denominator. The broader originals retain every unrelated office without requiring another numerical table for those offices.

**Midterm, volume, ballots and registration sensitivities.** The following rows use complete county vectors for each stated source scope. No turnout rate or ballot count is inferred from candidate votes. The2022 Senate comparator is the actual recent midterm statewide contest; no2024 Senate or invented governor contest is substituted. The [SBE turnout authority](https://elect.ky.gov/Resources/Pages/Turnout.aspx) labels its reports unofficial and warns that reopening registration rolls, moves and purges prevent exact comparison with election results. The [registration authority](https://elect.ky.gov/Resources/Pages/Registration-Statistics.aspx) describes monthly statistical timing; the selected November-General2024 PDF URL actually prints September2024. That mismatch, and the complete linked XLS original, are preserved rather than relabeled. Active/inactive eligibility breakdown and true voting-eligible population remain unknown. Native registration/turnout units have separate source identities and are not joined to recap units merely by names.

| County sensitivity denominator / scope | Total | Top15 share | Minimum80% count | Preceding votes | Crossing county | Crossing cumulative votes |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| 2024-president | 2,074,530 | 52.7708444804% | 50 | 1,650,178 | Breckinridge | 1,660,226 |
| 2022-senate | 1,477,830 | 53.0839135760% | 51 | 1,181,183 | Ohio | 1,188,461 |
| 2020-senate | 2,135,057 | 53.3095837722% | 50 | 1,702,981 | Perry | 1,713,534 |
| registration_snapshot_PDF_titled_September_2024 | 3,548,136 | 53.4919743775% | 49 | 2,819,891 | Lincoln | 2,838,687 |
| unofficial_voter_history_2022 | 1,502,626 | 52.8085498321% | 51 | 1,197,843 | Ohio | 1,205,269 |
| unofficial_voter_history_2022_registration | 3,590,227 | 53.2251024796% | 50 | 2,864,311 | Johnson | 2,882,576 |
| unofficial_voter_history_2020 | 2,149,444 | 53.2254852883% | 50 | 1,713,500 | Perry | 1,724,254 |
| unofficial_voter_history_2020_registration | 3,565,428 | 52.8264769335% | 50 | 2,837,740 | Johnson | 2,856,257 |
| unofficial_voter_history_2024 | 2,086,320 | 52.6479638790% | 51 | 1,668,579 | Perry | 1,678,693 |
| unofficial_voter_history_2024_registration | 3,548,136 | 53.4919743775% | 49 | 2,819,891 | Lincoln | 2,838,687 |
| captured_recap_ballots_source_scope | 2,088,041 | 52.9221887884% | 50 | 1,665,060 | Breckinridge | 1,675,189 |

Direct original turnout controls: [2024 county](https://elect.ky.gov/Resources/Documents/2024G%20Voter%20Turnout%20by%20County.pdf), [2022 county](https://elect.ky.gov/Resources/Documents/voterturnoutcounty-2022G-20221227-014248.pdf), [2020 county](https://elect.ky.gov/Resources/Documents/2020G%20Turnout%20by%20County.pdf), and [registration PDF](https://elect.ky.gov/Resources/Documents/voterstatscounty-November%20General%202024.pdf). The reported Number voting totals2,086,320 /1,502,626 /2,149,444 have different definitions/clocks from candidate votes. The captured recap ballot sum2,088,041 is explicitly a **source-scope sensitivity including Mail-In-only Magoffin**; it is not a reconciled statewide certified ballot total. A fully certified all120-county ballot denominator remains unavailable. Under/overvotes are retained only where explicitly printed; no ballots-minus-votes subtraction is assigned to an unobserved category. Ballot blank counts, contest undervotes, contest overvotes, generic invalid/unassigned write-ins and registration are never conflated.

**Complete county order, source-scoped sensitivity only.** Full primary denominator2,074,530 includes every row. All source candidate sums are exact integers; display percentages round only after calculation. The80% sensitivity set is ranks1–50 and the full remainder ranks51–120. Sources: the amended2024 certificate and separate2022/2020 certificates cited above; party/count/locator details are in the linked field witnesses.

| Rank | County | FIPS | President2024 candidate votes | State share | Cumulative votes | Cumulative share | Senate2022 | Senate2020 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Jefferson | 21111 | 354,094 | 17.068637% | 354,094 | 17.068637% | 277,888 | 387,090 |
| 2 | Fayette | 21067 | 143,935 | 6.938198% | 498,029 | 24.006835% | 106,550 | 153,214 |
| 3 | Kenton | 21117 | 80,948 | 3.901992% | 578,977 | 27.908828% | 51,158 | 82,197 |
| 4 | Boone | 21015 | 67,421 | 3.249941% | 646,398 | 31.158768% | 45,318 | 66,957 |
| 5 | Warren | 21227 | 56,891 | 2.742356% | 703,289 | 33.901125% | 38,358 | 55,434 |
| 6 | Campbell | 21037 | 48,334 | 2.329877% | 751,623 | 36.231002% | 35,664 | 48,882 |
| 7 | Hardin | 21093 | 48,082 | 2.317730% | 799,705 | 38.548732% | 30,886 | 48,952 |
| 8 | Daviess | 21059 | 47,097 | 2.270249% | 846,802 | 40.818981% | 32,906 | 49,289 |
| 9 | Madison | 21151 | 45,188 | 2.178228% | 891,990 | 42.997209% | 30,019 | 44,026 |
| 10 | Bullitt | 21029 | 43,209 | 2.082833% | 935,199 | 45.080042% | 24,842 | 41,882 |
| 11 | Oldham | 21185 | 38,210 | 1.841863% | 973,409 | 46.921905% | 26,297 | 38,070 |
| 12 | McCracken | 21145 | 31,947 | 1.539963% | 1,005,356 | 48.461868% | 22,762 | 33,562 |
| 13 | Pulaski | 21199 | 31,735 | 1.529744% | 1,037,091 | 49.991613% | 21,177 | 31,518 |
| 14 | Scott | 21209 | 29,769 | 1.434976% | 1,066,860 | 51.426588% | 20,503 | 28,977 |
| 15 | Laurel | 21125 | 27,887 | 1.344256% | 1,094,747 | 52.770844% | 17,571 | 28,140 |
| 16 | Jessamine | 21113 | 26,685 | 1.286315% | 1,121,432 | 54.057160% | 17,301 | 26,344 |
| 17 | Franklin | 21073 | 25,763 | 1.241872% | 1,147,195 | 55.299032% | 20,162 | 26,116 |
| 18 | Shelby | 21211 | 24,620 | 1.186775% | 1,171,815 | 56.485806% | 17,806 | 23,594 |
| 19 | Pike | 21195 | 23,950 | 1.154478% | 1,195,765 | 57.640285% | 15,735 | 25,266 |
| 20 | Nelson | 21179 | 22,852 | 1.101551% | 1,218,617 | 58.741836% | 16,993 | 23,204 |
| 21 | Christian | 21047 | 21,671 | 1.044622% | 1,240,288 | 59.786458% | 15,465 | 23,790 |
| 22 | Boyd | 21019 | 20,951 | 1.009915% | 1,261,239 | 60.796373% | 14,169 | 21,755 |
| 23 | Hopkins | 21107 | 20,537 | 0.989959% | 1,281,776 | 61.786332% | 14,796 | 21,468 |
| 24 | Barren | 21009 | 19,802 | 0.954529% | 1,301,578 | 62.740862% | 14,143 | 20,022 |
| 25 | Henderson | 21101 | 19,688 | 0.949034% | 1,321,266 | 63.689896% | 13,998 | 20,683 |
| 26 | Clark | 21049 | 17,885 | 0.862123% | 1,339,151 | 64.552019% | 12,805 | 18,128 |
| 27 | Marshall | 21157 | 17,602 | 0.848481% | 1,356,753 | 65.400500% | 12,930 | 17,607 |
| 28 | Greenup | 21089 | 17,374 | 0.837491% | 1,374,127 | 66.237991% | 12,634 | 18,138 |
| 29 | Calloway | 21035 | 16,945 | 0.816812% | 1,391,072 | 67.054803% | 11,841 | 17,479 |
| 30 | Graves | 21083 | 16,678 | 0.803941% | 1,407,750 | 67.858744% | 12,093 | 16,963 |
| 31 | Floyd | 21071 | 15,652 | 0.754484% | 1,423,402 | 68.613228% | 11,637 | 16,284 |
| 32 | Whitley | 21235 | 15,075 | 0.726671% | 1,438,477 | 69.339899% | 10,043 | 15,298 |
| 33 | Woodford | 21239 | 14,993 | 0.722718% | 1,453,470 | 70.062617% | 11,251 | 15,249 |
| 34 | Boyle | 21021 | 14,373 | 0.692832% | 1,467,843 | 70.755448% | 10,326 | 14,466 |
| 35 | Meade | 21163 | 14,123 | 0.680781% | 1,481,966 | 71.436229% | 9,555 | 14,066 |
| 36 | Muhlenberg | 21177 | 13,692 | 0.660005% | 1,495,658 | 72.096234% | 10,200 | 14,160 |
| 37 | Knox | 21121 | 13,156 | 0.634168% | 1,508,814 | 72.730402% | 7,977 | 13,240 |
| 38 | Anderson | 21005 | 13,095 | 0.631227% | 1,521,909 | 73.361629% | 9,378 | 13,235 |
| 39 | Montgomery | 21173 | 12,821 | 0.618020% | 1,534,730 | 73.979648% | 8,986 | 12,816 |
| 40 | Logan | 21141 | 12,511 | 0.603076% | 1,547,241 | 74.582725% | 8,508 | 12,323 |
| 41 | Taylor | 21217 | 12,261 | 0.591025% | 1,559,502 | 75.173750% | 8,996 | 12,498 |
| 42 | Grayson | 21085 | 12,095 | 0.583024% | 1,571,597 | 75.756774% | 7,917 | 11,963 |
| 43 | Mercer | 21167 | 11,851 | 0.571262% | 1,583,448 | 76.328036% | 8,288 | 11,704 |
| 44 | Spencer | 21215 | 11,480 | 0.553378% | 1,594,928 | 76.881414% | 7,734 | 11,407 |
| 45 | Grant | 21081 | 11,469 | 0.552848% | 1,606,397 | 77.434262% | 7,441 | 11,084 |
| 46 | Carter | 21043 | 11,422 | 0.550583% | 1,617,819 | 77.984845% | 8,176 | 11,548 |
| 47 | Lincoln | 21137 | 11,034 | 0.531880% | 1,628,853 | 78.516724% | 7,403 | 10,893 |
| 48 | Ohio | 21183 | 10,937 | 0.527204% | 1,639,790 | 79.043928% | 7,278 | 11,078 |
| 49 | Harlan | 21095 | 10,388 | 0.500740% | 1,650,178 | 79.544668% | 7,719 | 10,922 |
| 50 | Breckinridge | 21027 | 10,048 | 0.484351% | 1,660,226 | 80.029019% | 6,799 | 10,199 |
| 51 | Perry | 21193 | 9,992 | 0.481651% | 1,670,218 | 80.510670% | 7,462 | 10,553 |
| 52 | Rowan | 21205 | 9,873 | 0.475915% | 1,680,091 | 80.986585% | 7,416 | 10,043 |
| 53 | Johnson | 21115 | 9,622 | 0.463816% | 1,689,713 | 81.450401% | 5,643 | 10,152 |
| 54 | Bourbon | 21017 | 9,537 | 0.459719% | 1,699,250 | 81.910119% | 6,818 | 9,648 |
| 55 | Allen | 21003 | 9,418 | 0.453982% | 1,708,668 | 82.364102% | 6,102 | 9,301 |
| 56 | Bell | 21013 | 9,340 | 0.450222% | 1,718,008 | 82.814324% | 6,795 | 9,947 |
| 57 | Marion | 21155 | 9,102 | 0.438750% | 1,727,110 | 83.253074% | 5,896 | 8,892 |
| 58 | Harrison | 21097 | 9,018 | 0.434701% | 1,736,128 | 83.687775% | 6,659 | 8,844 |
| 59 | Adair | 21001 | 8,974 | 0.432580% | 1,745,102 | 84.120355% | 6,324 | 8,724 |
| 60 | Garrard | 21079 | 8,917 | 0.429832% | 1,754,019 | 84.550187% | 5,907 | 8,694 |
| 61 | Russell | 21207 | 8,893 | 0.428675% | 1,762,912 | 84.978863% | 6,407 | 8,932 |
| 62 | Simpson | 21213 | 8,776 | 0.423036% | 1,771,688 | 85.401898% | 5,738 | 8,699 |
| 63 | Wayne | 21231 | 8,733 | 0.420963% | 1,780,421 | 85.822861% | 6,331 | 9,150 |
| 64 | Letcher | 21133 | 8,431 | 0.406405% | 1,788,852 | 86.229266% | 5,727 | 9,077 |
| 65 | Hart | 21099 | 8,409 | 0.405345% | 1,797,261 | 86.634611% | 6,226 | 8,350 |
| 66 | Henry | 21103 | 8,074 | 0.389197% | 1,805,335 | 87.023808% | 6,039 | 8,092 |
| 67 | Mason | 21161 | 7,901 | 0.380857% | 1,813,236 | 87.404665% | 5,806 | 7,929 |
| 68 | Rockcastle | 21203 | 7,724 | 0.372325% | 1,820,960 | 87.776990% | 4,781 | 7,755 |
| 69 | Clay | 21051 | 7,517 | 0.362347% | 1,828,477 | 88.139338% | 4,925 | 7,568 |
| 70 | Larue | 21123 | 7,259 | 0.349911% | 1,835,736 | 88.489248% | 5,205 | 7,291 |
| 71 | Trigg | 21221 | 7,196 | 0.346874% | 1,842,932 | 88.836122% | 5,455 | 7,368 |
| 72 | Casey | 21045 | 7,080 | 0.341282% | 1,850,012 | 89.177404% | 5,148 | 7,152 |
| 73 | Fleming | 21069 | 7,000 | 0.337426% | 1,857,012 | 89.514830% | 5,057 | 7,039 |
| 74 | Pendleton | 21191 | 6,900 | 0.332605% | 1,863,912 | 89.847435% | 4,892 | 6,913 |
| 75 | Lawrence | 21127 | 6,574 | 0.316891% | 1,870,486 | 90.164326% | 4,127 | 6,922 |
| 76 | Washington | 21229 | 6,341 | 0.305660% | 1,876,827 | 90.469986% | 4,956 | 6,193 |
| 77 | Estill | 21065 | 6,290 | 0.303201% | 1,883,117 | 90.773187% | 4,621 | 6,537 |
| 78 | Edmonson | 21061 | 6,247 | 0.301128% | 1,889,364 | 91.074316% | 4,266 | 6,123 |
| 79 | McCreary | 21147 | 6,212 | 0.299441% | 1,895,576 | 91.373757% | 4,367 | 6,390 |
| 80 | Caldwell | 21033 | 6,188 | 0.298284% | 1,901,764 | 91.672041% | 4,684 | 6,425 |
| 81 | Union | 21225 | 6,058 | 0.292018% | 1,907,822 | 91.964059% | 4,881 | 6,553 |
| 82 | Knott | 21119 | 6,003 | 0.289367% | 1,913,825 | 92.253426% | 4,792 | 6,201 |
| 83 | Butler | 21031 | 5,943 | 0.286475% | 1,919,768 | 92.539901% | 4,195 | 6,123 |
| 84 | Jackson | 21109 | 5,934 | 0.286041% | 1,925,702 | 92.825941% | 3,668 | 6,086 |
| 85 | Green | 21087 | 5,857 | 0.282329% | 1,931,559 | 93.108270% | 4,313 | 5,798 |
| 86 | Lewis | 21135 | 5,721 | 0.275773% | 1,937,280 | 93.384044% | 3,831 | 5,857 |
| 87 | Webster | 21233 | 5,556 | 0.267820% | 1,942,836 | 93.651863% | 4,212 | 5,976 |
| 88 | Owen | 21187 | 5,500 | 0.265120% | 1,948,336 | 93.916984% | 3,895 | 5,446 |
| 89 | Bath | 21011 | 5,389 | 0.259770% | 1,953,725 | 94.176753% | 4,233 | 5,610 |
| 90 | Morgan | 21175 | 5,373 | 0.258998% | 1,959,098 | 94.435752% | 4,021 | 5,525 |
| 91 | Powell | 21197 | 5,360 | 0.258372% | 1,964,458 | 94.694123% | 3,592 | 5,493 |
| 92 | Monroe | 21171 | 5,308 | 0.255865% | 1,969,766 | 94.949989% | 3,807 | 5,274 |
| 93 | Magoffin | 21153 | 5,274 | 0.254226% | 1,975,040 | 95.204215% | 4,876 | 5,427 |
| 94 | Metcalfe | 21169 | 5,127 | 0.247140% | 1,980,167 | 95.451355% | 3,999 | 4,969 |
| 95 | Breathitt | 21025 | 5,113 | 0.246465% | 1,985,280 | 95.697821% | 3,552 | 5,613 |
| 96 | Todd | 21219 | 5,112 | 0.246417% | 1,990,392 | 95.944238% | 3,495 | 5,339 |
| 97 | Livingston | 21139 | 4,972 | 0.239669% | 1,995,364 | 96.183907% | 3,216 | 4,997 |
| 98 | Clinton | 21053 | 4,880 | 0.235234% | 2,000,244 | 96.419141% | 3,425 | 4,902 |
| 99 | McLean | 21149 | 4,634 | 0.223376% | 2,004,878 | 96.642517% | 3,634 | 4,775 |
| 100 | Hancock | 21091 | 4,633 | 0.223328% | 2,009,511 | 96.865844% | 3,257 | 4,578 |
| 101 | Leslie | 21131 | 4,357 | 0.210023% | 2,013,868 | 97.075868% | 2,881 | 4,792 |
| 102 | Trimble | 21223 | 4,249 | 0.204817% | 2,018,117 | 97.280685% | 3,190 | 4,302 |
| 103 | Lyon | 21143 | 4,187 | 0.201829% | 2,022,304 | 97.482514% | 3,230 | 4,229 |
| 104 | Bracken | 21023 | 4,153 | 0.200190% | 2,026,457 | 97.682704% | 3,234 | 4,232 |
| 105 | Ballard | 21007 | 4,088 | 0.197057% | 2,030,545 | 97.879761% | 3,127 | 4,227 |
| 106 | Carroll | 21041 | 4,025 | 0.194020% | 2,034,570 | 98.073781% | 2,878 | 4,115 |
| 107 | Crittenden | 21055 | 4,010 | 0.193297% | 2,038,580 | 98.267077% | 3,074 | 4,236 |
| 108 | Gallatin | 21077 | 3,917 | 0.188814% | 2,042,497 | 98.455891% | 3,012 | 3,844 |
| 109 | Martin | 21159 | 3,655 | 0.176184% | 2,046,152 | 98.632076% | 2,599 | 3,925 |
| 110 | Cumberland | 21057 | 3,442 | 0.165917% | 2,049,594 | 98.797993% | 2,478 | 3,277 |
| 111 | Nicholas | 21181 | 3,319 | 0.159988% | 2,052,913 | 98.957981% | 2,473 | 3,388 |
| 112 | Menifee | 21165 | 3,294 | 0.158783% | 2,056,207 | 99.116764% | 2,265 | 3,076 |
| 113 | Wolfe | 21237 | 2,915 | 0.140514% | 2,059,122 | 99.257278% | 2,253 | 2,981 |
| 114 | Elliott | 21063 | 2,911 | 0.140321% | 2,062,033 | 99.397598% | 2,064 | 2,966 |
| 115 | Lee | 21129 | 2,690 | 0.129668% | 2,064,723 | 99.527266% | 2,071 | 2,783 |
| 116 | Carlisle | 21039 | 2,610 | 0.125812% | 2,067,333 | 99.653078% | 2,128 | 2,642 |
| 117 | Fulton | 21075 | 2,145 | 0.103397% | 2,069,478 | 99.756475% | 1,532 | 2,409 |
| 118 | Hickman | 21105 | 2,069 | 0.099733% | 2,071,547 | 99.856208% | 1,547 | 2,192 |
| 119 | Owsley | 21189 | 1,839 | 0.088647% | 2,073,386 | 99.944855% | 1,759 | 1,877 |
| 120 | Robertson | 21201 | 1,144 | 0.055145% | 2,074,530 | 100.000000% | 979 | 1,139 |

**Reproduction and finish boundary.** [Schema](data/turnout/source/SCHEMA.md), [acquisition plan](data/turnout/source/acquisition-plan.json), individual source receipts, exact shared immutable source pins, full original bodies, source positions, prior-error histories, [deterministic build](data/turnout/scripts/build_turnout.py), [offline audit](data/turnout/scripts/audit.py), [validation record](data/turnout/validation.json), [final seal](data/turnout/finalseal.json) and [complete asset manifest](data/turnout/asset-manifest.json) are part of this package. Every owned file except the manifest itself is included in that manifest; shared originals are separately pinned and audited. Each stored artifact is strictly below40,000,000 bytes; no dependency/cache directories are retained. Gzip decompression exactly reconstructs stored original entities. There is no manifest-to-current-manifest digest cycle.

Run `PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/kentucky/data/turnout/scripts/audit.py --final` for the final **read-only** audit. It checks full owned membership/hashes/sizes, all raw source pins, offline original-to-text replay, token/source-row positions, all120 coverage/FIPS/identities, all candidate balances, source-method/count/denominator bounds, negative/null cases, every full descending order and integer80% crossing, links and all nonapproval flags. Build/extraction scripts are preserved for reproduction; use an owned isolated replay copy rather than writing over the sealed package. The final manifest is written last, then the complete read-only audit is run; no owned writes follow a PASS.

Substantive bounded research and offline QA finish this worker's assignment with the stated native gaps. Actual peer agreement and coordinator acceptance are external qualifications, not an indefinite worker finish gate. Current/legal/geographic/eligible-write-in/November IDs/cadence/exact remaining pool/collector/forecast/calibration approval remain false or unknown. This is historical source research, not a live collector, current precinct approval or a calibrated2026 turnout forecast.


**Bounded captured-final-peer verification addendum.** The earlier pending-peer statements describe the preserved original phase. The exact pre-resume package (manifest `9721574f385847d85c2cea99e8704425838138d10e9958a81a2586e9fa9629e2`,2,734targets plus itself) was independently verified and every whole old body preserved before edits. The finished original baseline's exact final package (manifest `9415e66193d21382abc5bc9f5ab97b3943ce2498c64e33acb3aade7dfdf5b2a4`,1,971targets plus itself; finalseal `57c55633ae06cb3799061f258ebe15fd2246549e5e59547070bab6d7312c4f68`) was completely verified/captured before comparison. All comparison reads use those complete immutable captures or individually pinned whole original entities, never current peer derivatives. See the [standalone capture/reconstruction and review instructions](data/turnout/reciprocal/README.md), [review metadata](data/turnout/reciprocal/review.json), and [complete comparison evidence](data/turnout/reciprocal/comparison/summary.json).

All3,509certificate positions, full headers/party/running-mate fields and shared original body/receipt roles reconcile. Every58,543turnout raw native row and17,052statistical row has a matching peer original-position observation; all148,527peer raw native observations and18,645raw statistical observations were checked against complete original layouts. Complete all120parent/native/admin/statistical child arrays and full ordered source-volume contracts are retained. Eighty-eight literal/schema differences remain unchanged:29footer scope strings,29footer county/null representations,20native-label appearances and10page-label appearances, including Scott's typed county-summary label versus peer null. These are disclosed representations, never normalized count agreement. The167unresolved literal associations, generic/named/NotAssigned overlap, FayetteTrump-3/WhitleyHarris-1 and original handwritten unknowns remain exact.

The peer's accepted3,150contexts (3,127positive and23zero-pair) contain1,969,011reported marks and exclude70unresolvedLaurel/Madison contexts plusScott. This is distinct from turnout's broader3,220slices/2,042,278marks. Within the matching accepted subset, both complete descending vote/cumulative sequences agree; minimum1,782 reaches1,575,315 after1,781/1,574,848. The467-vote crossing labels differ under original literal tie keys (peer CrittendenF101; turnout ToddB101) and both full orders/remainders survive unchanged. No key was rewritten to manufacture agreement. Turnout's original broader minimum1,817/1,633,888 after1,816/1,633,414/WashingtonD102474 and county minimum50/1,660,226 after49/1,650,178/Breckinridge10,048 remain unchanged. Neither native source universe authorizes canonical dispatch.

The isolated replay executed captured own original scripts only, reproduced293whole historical outputs exactly and replayed134complete PDFs. Nine actual denial probes blocked network/DNS, mutable newsroom/coordinator aggregates, peer discovery/current reads, producer helper reads/writer execution, acquisition-helper execution and writes outside the isolated temporary root. Seventeen corruption fixtures used complete actual source/context/order/companion/null/admin/candidate/party/method/position packets, with full immutable source companions; all were rejected. The failed initial reciprocal adapter and complete prior outputs/errors were preserved before the narrow footer-representation classification correction; no source/count/key/order/null/admin value changed. Calculator/scenario/target/outcome/full-field conclusions and root CLI/math review are outside this reciprocal source-core scope. Captured peer reverse proof remains historical stable-v1/v2 evidence only, never later/current/future equality. Current/coordinator/legal/native/geometry/feed/cadence/pool/forecast/probability approvals stay false or unknown; canonical native fields stay null and dispatch keys empty.
