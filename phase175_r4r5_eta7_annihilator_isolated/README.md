# Phase 175 R4R5R2 — Order annihilation for finite-cyclic direct summands

This revision extends the previously isolated order-to-zero inference from a single finite cyclic group to **every typed finite-cyclic component** of a direct sum. In a proved presentation `G = A ⊕ Z/m{g} ⊕ B`, the rule concludes `m*g = 0`. The rule also handles nested direct sums and continues to support the existing single-cyclic-group case. A zero goal may use either `RelationType.EQUALITY` or `RelationType.ZERO`.

The presentation must first be established through a screened source proof or an authenticated earlier database result. A candidate presentation in a backward expansion is a proof obligation, **not evidence**. The inference cannot mark an unproved presentation true.

## Changes and boundaries

The self-contained ZIP replaces the complete `phase175_r4r5_eta7_annihilator_isolated/` package from R4R5R1. No production modules, registry, shared backward-search provider, Web renderer, data files, or root-level project documents are changed.

- `rule.py`: extend `typed_endpoints`, `order_zero_premise`, `finite_cyclic_order_zero_rule`, `expand_finite_cyclic_order_zero`; add `_finite_cyclic_components` immediately after `typed_endpoints`. With concrete `presentations=(relation_1, relation_2, ...)`, backward search proposes only matching entire group presentations. With no candidate, the previous single-cyclic proposal is preserved.
- `audit.py`: add `direct_sum_prior_and_isolated_zero` immediately after `eta7_prior_and_isolated_zero`; update `run`, report and isolated gates. The real audit authenticates both previously registered `pi_8^7` (single cyclic) and `pi_8^4` (two finite-cyclic summands) as prior DB results relative to `(n,k)=(5,4)`. It checks separate inference steps without replaying either group proof.
- `tests/test_rule.py`, `tests/test_audit.py`: add focused acceptance and rejection checks for each summand, nested sums, free summands, mismatched generators/orders/dimensions, unsupported inputs, and checked prior API failures. Existing tests remain.
- `run.ps1`: run only the focused tests and the read-only isolated audit.
- `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `TEST_RESULTS_JA.md`: complete documentation, with import-complete executable code in `CODE_FULL_JA.md`.

There is one **isolated general inference rule**, zero new literature GIVEN facts, and zero public proof-search connections. In particular, this package does **not yet make the rule available to every public query**; that requires a separately reviewed shared-provider wiring step. Proposition 2.5 and Toda (5.8) are outside this revision. `pi_9^5` remains unproved by the public engine.

## Windows PowerShell

Extract the complete ZIP into the repository root and run:

```powershell
$script = '.\phase175_r4r5_eta7_annihilator_isolated\run.ps1'
$r4r4Report = 'C:\Users\oomae\AppData\Local\EHPProofTracerAudit\phase175_r4r4_pi95_premise_frontier\20261117T055000_247161Z\report.json'
powershell -NoProfile -ExecutionPolicy Bypass -File $script -R4R4Report $r4r4Report -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File $script -R4R4Report $r4r4Report
```

Expected gates: `PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_DRYRUN` and `PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_ISOLATED_NOT_PUBLIC`.

The real success indicators are `PHASE175_R4R5_2ETA7_ZERO_STEP=True`, `PHASE175_R4R5R2_DIRECT_SUM_ZERO_STEPS=2`, `PHASE175_R4R5_PI87_PROOF_SEARCH_EXECUTED=False`, and `PHASE175_R4R5_PI84_PROOF_SEARCH_EXECUTED=False`. These are isolated results, not a completed public proof.

Full pytest is reserved for the end of Phase 175.
