# Reproduce and audit

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python senate/2026/kentucky/data/baselines/scripts/reproduce.py
PYTHONDONTWRITEBYTECODE=1 python senate/2026/kentucky/data/baselines/scripts/audit.py --final
```

`reproduce.py` verifies every exact individual original pin, freshly extracts all 133 complete PDF text bodies with Poppler, and replays extraction/build/calculator verification in a temporary isolated Kentucky directory. It reads source assets by pinned hash, preserves all pages, and compares exact output bytes with the owned package. No unfinished peer output, coordinator parser/table, acquisition aggregate or external package install is a build dependency. The temporary replay tree is removed. Its proof is [reproduction.json](proof/reproduction.json). Run reproduction before sealing; after sealing, the final auditor is read-only. To repeat reproduction after sealing, copy this owned package to a temporary review location and retain its exact source pins rather than overwriting sealed proofs.

Python standard library and system `pdftotext`/`pdfinfo` suffice for extraction/build/calculation; source-image proof additionally used `pdftoppm`, Tesseract and Pillow. No dependency/cache trees are retained. All original bodies and lossless gzip artifacts are strictly below 40,000,000 stored bytes. Large raw originals are retained once under read-only exact body pins, not copied into this package. No split reconstruction is needed for the actual stored files.

Scripts have distinct roles: `pin_sources.py` is a one-time individual original/receipt capture; `extract_originals.py` preserves complete layouts and bounding-box attempts; `extract_certificates.py`, `extract_native.py`, `native_quantities.py` and `extract_admin.py` are independent original-source transformations. `ocr_scans.py` retains qualified OCR and full-page contact sheets. The Elliott manual file is an explicitly independent visual reading, not OCR/certificate allocation. `build.py` writes the all-county and separate native-subset assumptions/results; `source_reconciliation.py` preserves source differences. `calculator.py` is an offline actual CLI; `validate_calculator.py` exercises it and independently checks piecewise roots. `report.py` generates the report from owned controls. None should be run in place over a sealed package.

`capture_peer.py` and `compare_peer.py` record the bounded post-freeze comparison of exact stable witness bodies. They are not production build inputs. Repeated captures fail instead of silently substituting future peer bodies. The comparison scope is the captured original-first/v2, not a promise about later final outputs. No source/model values were repaired using the peer.

`audit.py` validates source/receipt/body hashes, original-first witness files, historical candidate balances, county/state denominators and exact integer 80% crossing, source/native keys and coverage, scenario weights/contributions/targets/selected-only assumptions, strict CLI proofs, relative Markdown links and asset bounds. `--prepare` writes validation before the final seal; `--seal` creates the final seal first and current manifest last. `--final` then checks exact complete membership, bytes and hashes without writing. The manifest excludes only itself, including every owned report/CSV/source/history/script/proof/validation/finalseal. The final seal never references the current manifest digest, avoiding a reverse digest cycle.

Acquisition receipts retain initial DNS errors and subsequent direct 403 responses; browser inspection independently confirmed actual published authority navigation. Current live/candidate/legal/geographic/feed/pool/calibration unknowns remain qualifications. Reproduction confirms the retained historical arithmetic and explicit scopes, not a calibrated forecast or legal/current-geography approval.
