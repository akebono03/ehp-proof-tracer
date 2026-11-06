# Phase 174 R3-R7-R3 — Isolated Generic EHP Zero Inference

This package introduces an **isolated**, mathematical inference rule for an exact EHP chain. It is **not installed** in the shared production search provider and does not change the Web renderer, databases, sources, or historical documentation.

## Mathematical rule

If `A --Delta--> B --E--> C --H--> D` is exact at `B` and `C`, `Delta` is surjective, and `D=0`, then `C=0`:

- `im Delta = B = ker E`, so `E=0`.
- `D=0` implies `H=0`.
- `im E = ker H = C` by exactness, so `C=0`.

This is a general group-theoretic inference. Each of its four typed premises must be independently proven, not merely proposed. The source of the EHP exactness is Toda Proposition 4.2, not the desired group assertion.

For the current frontier, the proposed four obligations are:

1. `MapSurjective(Delta: pi_13^13 -> pi_11^6)`.
2. The typed `Delta -> E` exactness window.
3. The typed `E -> H` exactness window.
4. The typed zero-group goal `pi_12^13=0`.

The previous source-screened audit found **no candidate** for obligation 1. Therefore this package must **not** mark `pi_12^7` complete. The separate `pi_11^6` source-first search also remains incomplete.

## Files

- `rule.py`: complete generic rule and backward-expansion functions.
- `audit.py`: source- and lineage-guarded read-only audit of the new isolated branch.
- `tests/test_rule.py`: focused dimensional, inference, non-forgery and generality tests.
- `tests/test_audit.py`: prior-evidence and source-guard contract tests.
- `run.ps1`: Windows-focused pytest and read-only audit, with `-DryRun` support.
- `CODE_FULL_JA.md`: full source of every added Python and PowerShell file.
- `AUDIT_PLAN_JA.md`: scope, verification criteria, and the next-phase boundary.

## Run

Extract the ZIP at the repository root, then run from PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r3_ehp_zero_rule\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r3_ehp_zero_rule\run.ps1"
```

The R3-R7-R2 JSON report must already exist in `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r2\ehp_chain_audit.json`.

The script uses `--import-mode=prepend` to avoid the previously observed pytest collection collision between historical directories and equally named Python modules. It never checks out, resets, stages, or modifies tracked production files. A new report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r3\generic_zero_rule.json`.

## Acceptance criteria

The focused tests and the Source Guard pass; the candidate Root is exactly one; the standard shared provider remains unchanged; the Delta-surjectivity obligation stays unproved; all four child obligations remain explicit. No full pytest is run before the Phase 174 closeout.

## Next boundary

A later R3-R7-R4 must establish a **source-certified, independent** derivation of Delta surjectivity before this isolated rule can be considered for production integration. An isomorphism proposal that already depends on Delta surjectivity is not evidence of that premise. Reuse the common Verified Proof Tree and narrative path; do not create a group-specific proof or renderer.
