# Phase 173 R4-R7R1 — Isolated Pi8 Premise Diagnostic

This read-only package diagnoses the failed isolated Toda Proposition 4.4 proof for `pi_8^4`. It does not change any production code, source bindings, mathematical inference rules, prior-result ordering, or the Web route.

## Reviewed baseline

Branch: `develop`. HEAD: `fc6631c1b791a856b4af08657af2453e3f198474`.

## Scope and contract

The existing `phase173_r4_r7_source_first_rule` provider is used unchanged. The report records the four actual proposal obligations, observed accepted `ProofStep` identities, source-registered direct `GIVEN` steps, strictly admitted database-prior steps, whether the observed steps pass the existing guard, and the true partial-search open goals. Database results are not presented as independently proved literature facts.

## Execution

After extracting the ZIP in the repository root, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r7r1_pi84_premise_diagnostic\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r7r1_pi84_premise_diagnostic\run.ps1"
```

The exact JSON output path is printed as `PHASE173_R4_R7R1_REPORT`. Send the PowerShell log for analysis. A successful diagnostic does not certify the incomplete `pi_8^4` proof. Full-suite pytest is deferred until Phase 173 closeout.
