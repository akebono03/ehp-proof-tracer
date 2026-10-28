# Phase 169 R10ET-R2 — Shadow Definition Comparison

This package runs a **read-only, in-process comparison** of the existing
citation-first inference provider and a proposed common-Definition-first
provider. It does **not** modify repository production files, tests, or
proof records. The provider factory is restored before the audit process exits.

It requires a working EHP Proof Tracer repository on `develop`, at either
`36e4dc41427ec4437009c96b01cacb07dc165bf6` or
`a5892721436effaf7be759ff17afd3bd427814ed`, with the exact previously
reviewed production provider Git blob. The R10ET-R1 JSON output must be
present at its original recorded path.

Run from the repository root after expanding the ZIP into the root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r2_shadow_common_definition_comparison\run.ps1"
```

Use `-Cases core` to compare the six principal groups without low-stem and
other historical projection cases. All cases use verified current Proof Trees.

The output includes `audit.json`, `audit.md`, and per-group `proof_steps.json`
and `narrative.md` files. `READY_FOR_IMPLEMENTATION=False` flags comparison
failures or lost projection behavior; it is not an exception and never means
that tracked source files were changed. The R2 preview should be reviewed
before any implementation ZIP is generated.

The runner executes a focused pytest selection; it does not run the full suite.
