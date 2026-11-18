# Phase 175 R4R12R10R1 — Cited Toda (5.11) source wiring

This phase admits equation (5.11) as an explicitly cited mathematical premise without re-proving it. The citation carries **only** the typed map equality; it does **not** assert the target group structure.

The adopted Japanese transcription `sources/toda/Toda_05_2.tex` and the existing publication-order manifest are checked before registration. The original printed edition is not independently verified. A `CitedToda511` source statement is a registered GIVEN. Its exact map equality is produced by a separate reference-preserving INFERENCE, suitable for the existing R9 `GeneratorImage` bridge. No new mathematical inference law or final group GIVEN is introduced.

Install from the repository root on `develop` with the reviewed HEAD `3ec001a59044aeb056ec7190c43c6066eaf5abae`. The existing R9 patch must already be installed.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r10r1_cited_511_public\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r10r1_cited_511_public\run.ps1
```

Only `build_shared_typed_bridge()` and `shared_expansion_provider()` of `phase165_r52_r9_shared_math.py` are edited. Full post-edit function bodies and the complete module are exported to `output/`. The source and provider modules are new. Tests are focused; the whole suite must wait until Phase 175 closeout.

Gate: `PASS_R4R12R10R1_CITED_511_CONNECTED_PROOF_PENDING` (not group completion). The next task is a real public proof-search audit and the still-open E-generator image.

## R4R12R10R1R1 focused-test correction

The only correction is the complete `test_only_two_entire_functions_are_replaced()` test function. Its synthetic bridge fixture now puts the eight-space source anchor inside a valid `if True:` block. The test checks full-function replacement for both shared functions and idempotence. Production code, mathematical rules, and cited facts are unchanged.


## R4R12R10R1R2 — Reviewed R9 commit lineage correction

The R9 bridge was committed to `develop` as `bf0d7be3081c61f2feec075a3c82c2004c29bbf2`, one commit after the earlier reviewed HEAD. The installer now accepts the two independently reviewed committed production blob SHAs. The audit checks the exact reviewed R9 commit change-set, ancestry, and commit count rather than broadly trusting any descendant. Only audit/installer guards and the focused tests were changed; Toda (5.11), proof rules, and the production provider are unchanged by this correction.

Run the same `run.ps1` first with `-DryRun`, then without it. The script runs nine focused tests. Do not run the full test suite until Phase 175 closeout. A passing gate confirms wiring, not the final group proof.
