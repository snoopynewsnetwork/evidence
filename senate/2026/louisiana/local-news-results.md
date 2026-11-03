# Louisiana newsroom and NYT backstops

Research observed **2026-10-18 UTC / 2026-10-17 Central**. This is coordinator preparation; four state question assignments and integration remain pending. [Retained responses](data/news/manifest.json) preserve UTC retrieval, URLs, HTTP status/headers and exact compressed/raw hashes. No November live collector or complete state package is claimed.

| Region/product | Primary source | Verified state and use |
| --- | --- | --- |
| Baton Rouge / capital region — WBRZ | [Actual results page](https://www.wbrz.com/election-information) and [linked data](https://weather.wbrz.com/2026race.json) | Both HTTP 200. Page names November 3; its client parses a stream of consecutive JSON objects, not one JSON document. Independent complete parsing consumed all 290,018 bytes: **187 race objects, 13 parish labels including Multi-Parish, all candidate votes zero**. Senate setup lists Jamie Davis/Julia Letlow; this is no substitute for a verified complete official ballot. No source count timestamp or guaranteed cadence established. Client fetches once on load and offers refresh on failure; zero setup is not election returns. |
| Baton Rouge — WAFB | [Homepage](https://www.wafb.com/) | HTTP 200 establishes active regional reporting. Actual November result configuration, supplier and full count coverage remain to inspect. |
| New Orleans / southeast — WWL and WDSU | [WWL](https://www.wwltv.com/), [WDSU](https://www.wdsu.com/) | Both HTTP 200 homepages. No complete November Senate numeric channel established from these captures; original counting reports/manual context are separately attributed. Local state-senate runoffs are not the U.S. Senate general election. |
| Lake Charles / southwest — KPLC | [Homepage](https://www.kplctv.com/) | HTTP 200; regional reporting access only. Exact November scoreboard, supplier and cadence remain unverified. Northern/northeastern regional numeric coverage is also a preparation gap. |

The [SOS current closed-party explanation](https://www.sos.la.gov/elections-voting/closed-party-primary-elections), retained 200, includes U.S. Senate and explains a plurality general-election winner without a majority requirement. The [Governor's April 30 notice](https://gov.louisiana.gov/news/5093) suspended **U.S. House** primaries, a distinct scope. These are leads for the official-results worker to verify against current controlling law/ballot and later changes; do not reuse historical jungle-primary assumptions for November Senate. The [modern results index](https://www.sos.la.gov/elections-voting/election-results-statistics) retrieved 200 but its raw links contain `--environment--` placeholders. Preserve that observation rather than silently repairing a hostname into a supposed verified API. A May data-advisory PDF route returned 404 and is retained as a failed request.

Parish, multi-parish statewide and precinct views overlap. WBRZ's 13 labels are its inspected product scope, not proof of all-64-parish detail. Complete authority/native geography and exact research priority still await the question workers.

Treat common upstream suppliers, official reprints and shared newsroom reporting as overlapping evidence. Compare identical election/contest/candidate/unit/method/stage at compatible timestamps. Never add cumulative snapshots, a statewide total and its local components, or two suppliers' views of the same votes. Preserve corrections and decreases. Calls, estimated vote completion and probability forecasts remain separately attributed fields.

[NYT's election hub](https://www.nytimes.com/section/politics/elections) returned direct HTTP 403. Discover the actual November Senate product from current navigation; geographic detail, supplier attribution, automated access and cadence remain unverified. A timestamped manual comparison is the fallback. The [state strategy](live-polling-strategy.md) distinguishes proposed checks from observed publication behavior.


Additional **October 20 UTC** [bounded regional observations](data/news/coordinator-oct20-regional/review.json)
retain five complete primary-publisher responses with their original bodies,
headers and clocks. They leave the earlier newsroom ledger unchanged.

- Northeast — KNOE's actual homepage links its [November ArkLaMiss guide](https://www.knoe.com/2026/10/19/november-2026-arklamiss-election-guide/)
  and [results page](https://www.knoe.com/politics/election-results). The current
  complete embedded results response has a null selected election ID and an
  empty election list. The guide points readers to that product; future numeric
  availability remains unproved. A separate [June 24 test notice](https://www.knoe.com/2026/06/24/knoe-test-election-systems-june-27-election/)
  explicitly describes mock June results, with that historical scope retained.
- Central Louisiana — [KALB's complete results product](https://www.kalb.com/politics/election-results/)
  retains inactive election 2519, **June 27 Election**, with 40 races and two
  party-specific Senate contests. Its June source update and October data
  transformation clocks are distinct. The frontend display-test flag, backend
  include-test parameter and election-list test flag are preserved separately.
  None establishes admitted November returns or a measured update cadence.

Both use Gray infrastructure. Their pages and the other inspected products
remain overlapping publisher evidence rather than independent statewide vote
counts. The November guide is newsroom context; operative rules still require
primary legal verification. Northern November numeric coverage remains a gap.


## Retained-source replay

The [independent retained-source audit](data/coordinator-newsroom-original-review.json)
reopens every complete source body and checks its individual receipt, raw hash,
stored hash, final status, URL, headers and UTC retrieval time. It preserves
complete embedded cache objects and actual iframe attributes where present.

The 36 retained complete entities include the actual WBRZ stream and its client. This audit found no embedded GSync election cache in those legacy responses; that absence does not establish the supplier or future availability of another product. The later KNOE/KALB full-hop observations remain separate evidence.

Legacy receipts establish the final response entity and metadata. They do not
claim unretained intermediate redirect bodies, headers or wire/TLS framing.
Original official PDF/CSV/workbook/archive bodies in the ledger are source leads
for future independent original-first extraction, not coordinator numerical
inputs. No state question worker has launched. This audit performs no network
request or browser execution and admits no November returns, current IDs, legal
geometry, measured cadence, exact eligible remainder, collector or probability.
