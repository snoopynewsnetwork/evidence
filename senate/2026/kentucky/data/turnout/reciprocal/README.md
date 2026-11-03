# Captured-final Kentucky source-core verification

This bounded review compares immutable whole captures of the original turnout package and finished baseline `ce1620b8-8df0-406b-bdb1-a8522aeea2f4`. It verifies the shared original source core, original positions, complete parent/child inventories and source-volume orders. Calculator, scenario, target, outcome, root CLI/math review and later peer equality are outside this scope. Captured peer reverse proof concerns historical stable-v1/v2 only.

The [review metadata](review.json), [complete comparison](comparison/summary.json), [source orders](comparison/source-order-summary.json), [statistical hierarchy](comparison/hierarchy-summary.json), [isolated replay](replay/result.json), and [complete corruption fixtures](fixtures/summary.json) define the actual scope. All 88 literal/schema differences remain in the complete difference stream. The peer's 3,150 accepted contexts and turnout's 3,220 raw reported-mark slices remain separate. Equal-vote literal key policies produce different subset crossing labels; neither is normalized. Canonical native order/top15/min80/priority/remainder remain NULL and dispatch keys empty. No current, legal, geographic, feed, forecast or coordinator approval follows.

The [own pre-resume index](own-pre-resume/index.json) preserves every one of 2,735 old bodies, including the old manifest, validation, seal, all three original-first witnesses, histories, failures and scripts. Its SHA256 is `7300ad31726da3bf49babc5ecf6e3d3019405b8c82b4f33368fa9e10220141b9`; the captured old manifest is `9721574f385847d85c2cea99e8704425838138d10e9958a81a2586e9fa9629e2`. The [peer index](peer-final/index.json) captures all 1,972 final peer bodies and complete receipt/original roles. Its SHA256 is `fdd06295b6e741eb146080396ca6a0e945766566f06f35b0027e8a19496f3938`; captured peer manifest `9415e66193d21382abc5bc9f5ab97b3943ce2498c64e33acb3aade7dfdf5b2a4`, seal `57c55633ae06cb3799061f258ebe15fd2246549e5e59547070bab6d7312c4f68`.

Each mutable old body is stored whole, losslessly gzipped by hash. Genuinely immutable originals and prior immutable archive bodies remain once, referenced with individual whole/raw/stored hash, size and complete receipt roles. No mutable peer derivative is read during comparison. To reconstruct every original oldpath byte into a new temporary directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/kentucky/data/turnout/reciprocal/scripts/reconstruct.py own-pre-resume --to /private/tmp/ky-own-reconstruction
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/kentucky/data/turnout/reciprocal/scripts/reconstruct.py peer-final --to /private/tmp/ky-peer-reconstruction
```

The captured original phase was actually rebuilt in isolation: all 293 whole outputs match, all 134 PDFs replay exactly, nine actual denial probes blocked network, mutable aggregates, peer discovery/reads, producer helpers/writers and writes outside temporary outputs. The [replay script](scripts/replay_originals.py) and full run receipts remain reproducible. Review adapters write only to owned review paths; the final audit redirects their complete output exclusively to temporary directories and compares exact whole proof bytes.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 senate/2026/kentucky/data/turnout/reciprocal/scripts/review_audit.py --final
```

That command checks complete captures, every original reference and receipt hop, unchanged originals and explicit metadata exceptions, all source-core/parent/statistical/order proof bodies, 17 complete-context corruption rejections, original full offline audit, links, bounds and complete final manifest. It writes no owned files. The final seal is written before the manifest; the manifest excludes only itself and has no reverse digest cycle. No owned writes follow final PASS.
