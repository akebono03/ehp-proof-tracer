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

## R4R12R10R1R4 — Registered source-to-DB notation correspondence

The R3 diagnostic found the exact difference: eta-9 display names and
`Suspension(nu-prime)` versus `IteratedSuspension(nu-prime, 1)` with the
registered historical nu-prime ID. This revision uses the **existing**
`phase168_r2_8_3_generator_identity.identity` registered-factor resolution,
including endpoint checks, to accept the cited (5.11) equality in the DB's
verified presentation. It does not equate nu-4 to suspended nu-prime.

Only the new phase provider (`same_registered_cited_511`,
`expand_cited_511`), its audit (`inspect`) and focused tests change;
production installation still replaces only the two complete shared functions.
`CitedToda511` remains the sole (5.11) GIVEN; the DB spelling is supplied
by a reference-preserving INFERENCE. No new mathematical relation or group
conclusion is GIVEN. The source is the adopted Toda TeX transcription, not a
separately verified print edition. Run `run.ps1 -DryRun` followed by `run.ps1`.

## R4R12R10R1R5 — reviewed R10/R3 commit lineage

GitHub confirms commit `12d2116bc23e96c879d97b043dbc104b31030091` is one commit after reviewed R9 commit `bf0d7be3081c61f2feec075a3c82c2004c29bbf2`. Its changes are confined to the checked-in R10R1 audit package, R3 diagnostic package and pytest cache metadata. The committed production blob remains `83f278ec98512a763cdfba2552c70f972b169eac`.

The audit accepts this exact commit only when the reviewed ancestor, the two-commit count from the original reviewed base, and the exact cumulative path set all match. This is a lineage-only correction: no source, provider, rule, installer, or production module changes. The revised focused suite contains 13 tests. Run the same `run.ps1` using `-DryRun` and then without it; full-suite pytest is reserved for Phase 175 closeout.

## R4R12R10R1R6 — Reviewed tracked overlay guard

A reviewed, checked-in R10/R3 package was overlaid by the subsequent R4/R5 ZIP revisions. Git correctly reports eight tracked package paths as locally modified, including a previously written `output/preflight.json`. The audit now accepts exactly these explicit tracked paths plus the existing production target and pytest-cache exception. Changes to `source.py`, `installer.py`, `run.ps1`, any unrelated code, and unexpected output paths are still rejected. The production module is independently constrained by `installer.plan()`. No source registration, proof rule, or mathematical statement is changed. Three focused guard tests are added; run the same DryRun and actual commands.
