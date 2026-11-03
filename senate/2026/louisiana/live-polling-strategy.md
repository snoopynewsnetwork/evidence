# Louisiana collection and remaining-vote strategy

Prepared **2026-10-18 UTC / 2026-10-17 Central**. Four question assignments and integration remain pending. Read the [news survey](local-news-results.md); this is proposed operation, not live collection.

## Louisiana-specific preflight

The [current SOS explanation](https://www.sos.la.gov/elections-voting/closed-party-primary-elections) describes closed-party primaries for Senate beginning in 2026 and a **plurality** general-election winner without a majority requirement. The [April 30 Governor notice](https://gov.louisiana.gov/news/5093) suspends U.S. House primaries, a distinct office scope. The official-results worker must verify controlling current statutes, actual Senate ballot/stage, subsequent orders and any later changes. Do not apply the historical jungle-primary general/runoff model to November Senate merely because it applies to an older dataset or another office.

Retain all 64 parishes and native precinct/method keys, with multi-parish and statewide views explicitly overlapping. County-oriented filenames are compatibility names for parish reporting. The exact 80% set and actual map approval/crosswalk remain pending state questions. Louisiana had no 2024 Senate election: label 2024 president, 2022 Senate midterm/other seat and 2020 same-seat Senate separately. Historical multi-candidate party aggregations are not interchangeable with a named 2026 opposition coalition or new plurality rules. Preserve every candidate and stage; a D/R tie alone does not establish plurality against another candidate.

WBRZ's actual November-named product links a stream of 187 complete JSON race objects with all votes zero and 13 parish labels including Multi-Parish. A single-document JSON parse fails because the publisher uses consecutive objects; its client intentionally parses the stream. Retain that framing and complete-consumption validation. This setup snapshot does not establish complete Senate ballot identity, all-parish detail, source timestamps or live update cadence. Its client fetches on load without an observed timer. Regional TV homepages are accessible but actual November numeric products remain to inspect; northern/northeastern coverage gaps stay explicit.

The modern SOS results landing contains environment placeholders, but its linked public script supplies an explicit production rewrite. The [source preflight](data/coordinator-source-preflight.md) now reproduces that authority chain and recovers complete historical XLSX/CSV originals through the public graphical app. The default November date, site IsLive flag, configured120-second refresh and static offset are not admitted counts, measured cadence or legal poll-close authority. The results assignment must still verify current hours/timezone, mail return/eligibility, cure/provisional processing, canvass and certification deadlines.

## Proposed collection and revision handling

Start with 2-minute checks of a verified official release index/version around an announced election-night publication, fetching details only after a change. Use 5-minute checks for verified newsroom backstops and manual NYT observation where automated access fails. Outside announced windows, back off to 15 minutes or hourly during counting and daily through canvass/certification. These are implementation proposals, not observed publisher cadence. Use timeouts, bounded concurrency, jitter, conditional requests where supported and exponential backoff. A quiet source is not automatically an outage.

Resolve actual November navigation and verify election date, Senate title, complete candidate identities, zero/test status, unit/method coverage and source status before importing counts. HTTP 200, a current pathname, an old widget ID or visible candidate numbers is insufficient. Store original bytes, URL, UTC retrieval, HTTP/cache headers, hash, parser version, publisher timestamp/timezone and native election/contest/unit IDs. Reject challenge HTML and app shells. Keep a source-health ledger with last successful fetch, last genuine vote change, expected versus observed units, and manual-fallback reason.

Replace cumulative snapshots; derive compatible changes afterward and retain decreases, corrections and status changes. State, county, municipality/authority, precinct and method views may overlap. Pick a consistent authoritative scope rather than summing every product or averaging disagreements. External calls, estimated completion and probabilities remain separately attributed fields. Multiple AP products or shared newsroom reports are one upstream chain. Preserve a conflicting observation until scope/time/status explains it.

For a failed primary channel, capture the same official election page or linked PDF/export manually with URL, observation time, source status and original file/screenshot. Use newsroom figures only as an explicit temporary substitution for the same unit/method. Reconcile and replace with official counts once available; never silently combine different vintages. NYT access and actual November Senate product remain unverified in this preparation.

## Remaining votes and scenario readiness

Counted votes remain fixed. Estimate only uncounted ballots using documented unit/method inventories and explicit low/base/high ranges, with source/time and acceptance/counting status. Issued minus returned, registration minus turnout and reporting-precinct percentages do not equal remaining candidate votes. If accepted-unprocessed detail is absent, uncertainty remains unknown or bounded by stated assumptions; do not manufacture an exact total. Processed ballots, eligibility review, published candidate counts and certification are different stages.

Compare partial returns with the same historical geography/method and boundary vintage. No allocation through an unvalidated map crosswalk. Historical turnout volumes are sensitivity anchors, not 2026 projections. Tie/+1 conditional scenarios require complete statewide weights and candidate/other-vote reconciliation; distinguish share-point shifts from margin-point shifts. Do not substitute an independent candidate into a D/R coalition without explicit identity and assumptions.

Before live use, replay genuine dated releases and test idempotent retries, missing units, corrections/decreases, overlapping aggregates, candidate identity and manual recovery. Keep original counts and derivatives auditable. A calibrated win probability additionally requires a dated prior, genuine historical release sequences, remaining-ballot assumptions and held-out calibration under the [root plan](../../../ELECTION_NIGHT_PLAN.md). No live collector or calibrated Needle is implemented here. Final integration must insert the measured priority set, complete official inventory, downloaded map compatibility and verified current rules from the four state question assignments.


## Source replay before collection

The [retained-source audit](data/coordinator-newsroom-original-review.json)
and [newsroom survey](local-news-results.md#retained-source-replay) preserve
whole source entities, literal test/status settings and empty products. A null
selected election or empty candidate list is unavailable count evidence, not
an observed zero return. A configured refresh timer is not measured publication
cadence. Independently verify a current election, contest, candidate universe,
reporting scope and genuine dated release before admitting any value, including
a positive value in a pre-election product. Keep original source clocks,
retrieval clocks and transformations separate; no correction chronology follows
from differently dated cached and fresh representations alone.

## Reviewed historical scope

The full historical source universe is 3,933 disjoint native rows across all 64 parishes. Its minimum 80% set contains 1,516 rows (1,605,649 of 2,006,975 votes), including every Early Voting parish aggregate. Retain all 2,417 remainder rows. The 24-parish sensitivity is not native dispatch. Ordinary, early and provisional identities remain source-specific; no administrative polygon or current boundary join is inferred. The [coordinator review](research-review.md) links independent source, arithmetic, CLI, capture and seal evidence. These measurements do not establish current ballot/choice IDs, eligible write-in coverage, true physical ballots, remaining-vote pools or measured publication cadence. All current admission gates remain false or unknown pending the original official and maps questions.
