# Snoopy News Network evidence

Archived election research sources, map originals, extracted data, and review artifacts moved out of [snn](https://github.com/snoopynewsnetwork/snn). Paths under `senate/2026/` preserve the original layout and file bytes. Lightweight race notes are included for context; the application and maintained race summaries live in `snn`.

This repository is large. Normal application development does not require it. For selected states, use a partial sparse clone:

```sh
git clone --filter=blob:none --sparse https://github.com/snoopynewsnetwork/evidence.git
git -C evidence sparse-checkout set senate/2026/massachusetts
```

The migration preserves the working-tree evidence as of November 3, 2026, including research that had not yet been committed in `snn`.
