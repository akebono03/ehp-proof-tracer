# EHP Proof Tracer — Phase 174 R3-R3: Injective Suspension / Delta-zero Bridge

This package adds an **isolated general inference rule** for a standard EHP consequence:

- A separately proved suspension map `E` is injective.
- An independently proved, well-indexed Toda Proposition 4.2 window states `im(Delta) = ker(E)`.
- Therefore, `Delta` is the zero map.

The rule contains no hard-coded group coordinates, generators or narrative. Both
premises must be `ProofRule.INFERENCE` and must match the same exact EHP window.
The live capability audit reconstructs the two prerequisites from the same
citation-screened context as the public `pi_8^5` query, inspects their source
ancestry, and attempts to derive a Delta-zero ProofStep **in memory**.

The new rule is **not connected** to the public `shared_expansion_provider`.
The report must not be interpreted as a completed group proof or a verified
public narrative. It does not change production modules or project documents.

## Files

- `rule.py`: full new general rule and backward expansion, no trusted facts.
- `audit.py`: source and provenance checks, live source-backed trial.
- `tests/test_rule.py`: seven focused rule and failure-contract tests.
- `run.ps1`: guarded DryRun and audit with existing related focused tests.
- `AUDIT_PLAN_JA.md`: Japanese mathematical scope and Phase boundary.

## Windows execution

Extract this ZIP to the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r3_injective_delta_zero\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r3_injective_delta_zero\run.ps1"
```

All reports are written outside the repository under
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r3\audit.json`.
The script does not reset, clean, commit, push, or pull any Git changes.
No full-suite pytest is run; defer that until the end of Phase 174.
