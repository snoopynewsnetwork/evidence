# Louisiana turnout source and replay schema

Only `turnout.md`, `data/county-turnout.csv` and `data/turnout/**` are owned.
The compatibility CSV contains **parishes**. Its rank/share/priority flags are
explicit parish sensitivities; the historical primary contract uses **native
ward/precinct and administrative source units**. No parish rank authorizes
substitution for finer native dispatch.

`original-pins.json` freezes 27 whole original entities recovered by reopening
original gzip bodies and checking raw/stored hashes against individual copied
receipts. It is the only initial replay index. `freeze_originals.py` is a
one-time recovery helper; do not rerun it to replace a freeze. Neither that
helper nor the mutable news ledger/preflight is a final calculation dependency.
Every final replay reads content-addressed owned `.body.gz` and exact individual
receipt pins. Original shared receipts' intermediate redirects are unavailable;
their final entity, URL, status, headers, UTC and source hashes survive.

`acquired-pins.json` freezes 238 complete per-request receipt records, including
15 initial sandbox DNS failures. Successful acquisitions retain original bytes,
all response headers, requested/final URLs, UTC start/end, raw/stored hashes,
bytes and per-hop redirect bodies when encountered. All downloads are finite
anonymous GETs through actual public parent/client constructors. The source
index is immutable; mutable globs are used only by the one-time freeze helper.
There were 223 successful new request receipts, including 213 JSON entities.
Repeated body hashes share one owned body. Failed source advisory 404/empty
content is retained in initial originals and never treated as election data.

Gzip files reconstruct exact uncompressed bytes with `gzip.decompress`.
All stored files are strictly less than 40,000,000 bytes. The complete original
workbooks remain ZIP entities; all member bytes, including unrelated offices,
styles, relationships and blank cells remain lossless. No truncation, clipping,
rescaling, residual allocation, candidate-key deduplication or invented zero.

`original-first-witness.json` pins whole-workbook physical row/cell extracts
for every worksheet and complete selected CSV records, header/footers, native
parent rows and full metadata. XML row/cell `r` attributes are optional: physical
ordinals are authoritative positions, preserved alongside original attributes.
CSV `record_ordinal` is one-based, header=1; `ending_physical_line` preserves
quoted-record line position. `xlsx_physical_row` is one-based physical XML row,
not a guessed Excel address. Resolve relationship targets; 2020 starts at
`sheet.xml`. Blank leading cells remain cells. `acquired-original-first-witness`
pins complete JSON trees and exact bodies. JSON object member order and array
positions survive in whole original bytes and the complete JSON witnesses.

`source/independent-stable-schema.json.gz` is the unchanged first independently
derived control/order/vector freeze. The later scope-corrected
`source/native-primary-stable-schema.json.gz` preserves the same source counts
with explicit native order labels; neither is updated to match a peer.
`history/` retains exact failed scripts/logs/input pins and previous parish-primary
contract/CSV/script before scope correction. Controls missing in a native object
are null; their explicit candidate zeros do not authorize control zeros.

`historical-controls.json` contains source date/election metadata, race IDs,
complete ordered choices, literal labels/parties, source choice IDs, statewide
candidate vectors, general/race qualified/voted controls, source clocks and
actual majority arithmetic. Selected universes: 2024 President race67190,
2022 Senate61897, 2020 Senate59569. Source election roster marks these official;
that does not establish signed certification chronology. `CanHaveRunoff` is
potential historical procedure, not proof of an actual runoff. Party sums are
not named 2026 coalitions.

Native `key` is literal JSON `[year,race_id,parish_id,ward,precinct]`, encoded
without padding/normalization beyond original fields. `source_native_id` is
the API literal ward/precinct string (slash-separated for ordinary records)
or the administrative label. CSV Ward/Precinct survive separately. XLSX uses
Ward + space + Precinct, including trailing administrative spaces. The only
method aliases are `ward_precinct_source_row`, `early_voting_aggregate` and
`provisional_aggregate`. They describe source rows, not legal ballot methods,
polling locations, geometry, current eligibility or cross-year equivalence.
Native IDs require year+contest+parent; bare precinct numbers never join statewide.

Source `OTHER` workbook versus `OTH` CSV is a documented formatting alias only.
All labels, including the 2024 Stein/Baraka ticket string, are retained literally.
Generic/named write-ins, blanks, undervotes, overvotes and ballots cast are null
where absent. SOS's no-write-in-candidates guidance and R.S.18:1319 FWAB ballot
mechanism are kept distinct. No additional candidate pool inferred.

`qualified`/`voted` on parish rows are general Stats All/All_Voted.
`race_qualified`/`race_voted` are selected StatsRace controls. Native fields
are VoterCountQualified/VoterCountVoted. Active/inactive registration scope and
roll cutoff are unspecified. Participation need not equal tabulator ballots or
candidate totals. Whole original demographics remain preserved, with no
separate unrelated demographic analysis. All general and race scopes sum to
their own published controls; differences remain in explicit ledgers. Native
control sums with missing cells remain incomplete, never filled with zeros.

`orders/*.csv` sort counts descending then ascending composite literal key.
Share/cumulative shares are exact fraction strings plus display percentages.
The minimum crossing is the first integer `5*cumulative >= 4*total`. Order
summaries retain top15, preceding count/votes, crossing unit, priority and
remainder. Separate parish sensitivity orders cover candidate votes, general
and race participation/registration, early/provisional/ordinary candidate rows.
Ballot/under/over/blank rankings are explicitly unavailable, not synthesized.

`priority-set.json` v2 uses 3,933 disjoint 2024 native units as historical
primary, all64 parent-child arrays and all available literal constituents.
`canonical_native_dispatch` is the **proposed historical** source-complete
ordered priority; `coordinator_acceptance=false`, and current2026 dispatch=[]
because no legal current identity/geometry equivalence is established. If a
native coverage/membership check fails, the builder fails and no new complete
contract may be emitted. Null/empty dispatch is required for unresolved source
membership. Geometry, missing optional source controls, final ballots and legal
qualifications are separately scoped, not fabricated from parent controls.

`peer-capture/` freezes the actual peer's original-only schema before comparison.
`compare_peer.py` reads only captured source schemas/positions, checks freeze
hashes and compares source candidate/native/method/control fields. It documents
key/header-position aliases and reconstructs complete source orders under the
same explicit tie rule. No peer calculator, future outcome or mutable contract
is a count input. Agreement is one-way; reciprocal signoff/coordinator acceptance
are not implied. The peer's independent full original witness is retained.

`validate_turnout.py` rereads original CSV/native JSON/OOXML state controls,
checks all identities/vectors/hierarchy/order/weights/crossings and rejects nine
saved adversarial fixtures, including balanced candidate transfers that leave
statewide totals unchanged. Fixture input recipes identify immutable base
hashes and exact operations so altered inputs are reproducible without large
duplicate copies. `validation.json` is produced before the manifest.

The packaging repair supersedes the old two-exclusion convention. The exact
prior 645 bodies, including both the old manifest and its unlisted audit, are
retained in `history/packaging-repair/own-prior-complete.tar.gz.part001` with an
exact member inventory. No prior pins point at rewritten current bodies.
`make_manifest.py` now excludes ONLY `data/turnout/asset-manifest.json` itself.
It includes every other current owned file: validation, final audit proof,
final seal, histories, fixtures, captured complete bodies and scripts.

Prepare all proofs, validation, and `final-audit.json` first; this audit proof
has no current/future manifest or seal digest. `seal_repair.py` prepares the
final seal after those bodies exist. The seal pins all current bodies except
itself and the future manifest. Run `make_manifest.py` LAST to pin the seal and
all other bodies. The actual final `final_audit.py` is read-only and prints
stdout only; NEVER redirect it to any owned path after seal. No owned writes
after its passing audit. Old manifest-bearing audits remain exact archived
history, never retroactively repaired.


## Captured final-peer and replay repair proof roles

`history/packaging-repair/own-prior-inventory.json` pins all645 prior whole
bodies, with member paths relative to Louisiana. `peer-prior-inventory.json`
pins the actual final peer1608 complete bodies, with repository-relative member
paths and its exact final manifest/seal. Concatenate ordered archive parts
before gzip/tar reconstruction; no artifact is at or above40,000,000bytes.
`shared-original-roles.json` pins27 individual exact original stored/raw bodies
and their complete receipt roles. Final proof replay reads those captured
individual bodies, not mutable news/coordinator/discovery aggregates.

`repair_verify.py` is an independent read-only source comparator (its `main`
only writes owned proof outputs during preparation). It never imports peer
producers. Complete original entity bytes plus independently extracted physical
OOXML/cell and CSV token positions are checked, preserving blank cells, missing
`r`, styles/formulas, all metadata/header/party/running-mate fields, null/admin
controls and original method scopes. All27 full orders and192 year-parent
arrays are verified. Two differing current authority HTML observations are
retained separately; they are excluded current semantic scope, not normalized
historical agreement. Peer reverse146652 source checks apply only to its
captured historical comparison, not later/future contracts, calculators or
outcomes. Original-first exact freezes and chronology claims remain qualified.

`isolated_replay.py` runs exact captured own original extractor/builder in a
unique temporary directory. Audit hooks actually reject network, mutable or
current external sources/helpers, existing producer import, and outside-temp
writes. All46 generated whole bodies match the captured old originals exactly.
Its stdout/error/context and exact script histories survive. It does not
execute peer scripts or adopt any peer count/model field.

`repair_negative.py` tests the COMPLETE three-year source packet and full owned
candidate inventory, preserving exact base bytes and deterministic reversible
mutation recipes. Fifteen source/context/header/party/null/admin/method/position/
companion/order/parent mutations and five packaging mutations must be rejected.
The actual final read-only audit re-exercises those checks in memory and also
applies omission/altered-seal/reverse-cycle tests to the actual final manifest
and current bodies. An audit hook denies all filesystem mutation and network.

`validation.json`, `final-audit.json`, `final-seal.json` and the current manifest
are packaging proof/status metadata only. The historical contract, CSV, all
numeric/source/order/null/admin context and original-first witness bytes remain
exact. `repair_readonly.py` explicitly enforces the small allowed set of old
report/schema/packaging/proof changes against the full immutable645-body capture.
Coordinator acceptance and every current operational approval remain false or
unknown; current native dispatch is empty. No new public acquisition, peer
contact, Git operation or shared/peer write occurs in this repair.
