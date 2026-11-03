# Kentucky newsroom and NYT backstops

Research observed **2026-10-18 UTC / 2026-10-17 Central**. This is coordinator preparation; four state question assignments and integration remain pending. [Retained responses](data/news/manifest.json) preserve UTC retrieval, URLs, HTTP status/headers and exact compressed/raw hashes. No November live collector or complete state package is claimed.

| Region/product | Primary source | Actual observation |
| --- | --- | --- |
| Statewide public television — KET | [Election hub](https://ket.org/election/) and [Primary 2026 release](https://ket.org/pressroom/release/primary-2026-on-ket-offers-live-results-and-analysis-on-primary-election/) | Both HTTP 200. Hub embeds AP layouts under organization 73761, including 28480; inspected first layout returned 403. The release schedules May 19 primary coverage and also retains an old 2024 reference. Preserve exact election/date and distinguish analysis from counted votes. November product and publication cadence remain unverified. |
| Lexington / eastern Kentucky — WKYT | [Actual results page](https://www.wkyt.com/politics/election-results/) | HTTP 200, inactive **2361, Primary 2026**, with194races/648choices, including two U.S.Senate primary objects. Its backend request excludes testresults and listed/race isTest flags are false; a separate frontend displayTestData=true does not prove those returned primary counts are tests. Positive primary counts and Estimated99% are not November returns or exact remaining votes. |
| Louisville / northern Kentucky — WDRB | [Homepage](https://www.wdrb.com/) | HTTP 200 establishes active reporting; no actual November complete numeric channel, supplier or cadence verified from this landing page. Ohio/Indiana cross-border records require state identity checks. |
| Paducah / western Kentucky — WPSD | [Homepage](https://www.wpsdlocal6.com/) | HTTP 200 confirms regional newsroom access only. Resolve actual November data product and geographic scope before using a count; neighboring-state races are separate. |

The [state 2026 archive](https://elect.ky.gov/results/2020-2029/Pages/2026.aspx) and actual [SOS primary ENR link](https://vrsws.sos.ky.gov/liveresults/?id=2026) returned direct 403; research-browser text identifies **2026 Primary**, not November general. Access limitations remain retained rather than guessed around. The official-results question must inventory every county/election authority, actual native precinct and counting method, state/counties overlap and current November availability. Kentucky's time-zone split also requires locality-level operational timing and exact source timezone checks, not one assumed statewide closing instant.

Treat common upstream suppliers, official reprints and shared newsroom reporting as overlapping evidence. Compare identical election/contest/candidate/unit/method/stage at compatible timestamps. Never add cumulative snapshots, a statewide total and its local components, or two suppliers' views of the same votes. Preserve corrections and decreases. Calls, estimated vote completion and probability forecasts remain separately attributed fields.

[NYT's election hub](https://www.nytimes.com/section/politics/elections) returned direct HTTP 403. Discover the actual November Senate product from current navigation; geographic detail, supplier attribution, automated access and cadence remain unverified. A timestamped manual comparison is the fallback. The [state strategy](live-polling-strategy.md) distinguishes proposed checks from observed publication behavior.


## Southern and eastern publisher originals

The separate [four-request review](data/news/coordinator-oct20-regional/review.json)
retains complete southern/eastern homepage and publisher-linked result bodies.
[WBKO's results](https://www.wbko.com/politics/election-results/) was reached
through the homepage's literal public config; [WYMT's results](https://www.wymt.com/politics/election-results)
through its actual Election Results anchor. All four requests returned200.
The complete embedded election/featured objects preserve every race, candidate,
control, status, null and clock.

The selected products are inactive primary2403(WBKO,173races) and2078(WYMT,
135races), each with two U.S.Senate primary contests. Both retain frontend
`displayTestData:true` and backend`includeTestResults:false`; the listed
`isTest:false` flag does not override the other source qualifications. The
publisher update value June9,18:45:12Z and October20 transformation clocks
remain separate. Homepage refresh/carousel settings are literal config values,
not measured cadence or a verified unit interpretation. SharedGray products
do not constitute independent statewide totals. No currentNovember returns,
roster completeness, exact eligible remainder or geographic match is approved.
The retained checker-history note discloses an initial overescaped local
string assertion and the corrected original-literal check; no source bytes
were changed.


The [independent retained-source audit](data/coordinator-newsroom-original-review.json)
verifies all35legacy complete entities/individual receipts and preserves WKYT's
entire embedded cache, including unrelated races, flags/nulls and raw character
spans. Its updatedDateJune9,19:17:42Z and October18transformation clock are
separate. KET's actual AP73761/layout28480 iframe returned403; November setup,
actual supplier independence and measured update cadence remain unverified.

Complete official historical originals recovered through actual Wayback links
are retained alongside direct403s, CDX discovery and all archived versions.
They are source leads for the future question workers' independent original-first
extraction, not coordinator numerical input or a claim of complete native/current
geography. Legacy final-response entity/status/URL/headers/UTC are retained;
unobserved intermediate redirect bodies/headers or wire/TLS metadata are not
claimed. The regional WBKO/WYMT originals have separate full-hop receipts.
No new acquisition, browser execution, November admission or collector occurred
in this retained-byte review; no state question worker has launched yet.
