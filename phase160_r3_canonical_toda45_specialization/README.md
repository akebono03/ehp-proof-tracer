# Phase 160-R3

Canonical Toda (4.5) specialization from the Phase 160-R2 stable-target semantics.

Scope:

- Add `toda_stable_transport.py`.
- Build the canonical stable transport map from the canonical base to a stable target.
- Build the concrete Toda (4.5) isomorphism proof step with the existing theorem rule.
- Preserve the three theorem premises as proof provenance.
- Do not transport group structure yet.
- Do not normalize generator families.
- Do not change public Narrative.
- Do not run the full test suite.

Prerequisite:

- Phase 160-R2 must already be applied.

Run from the repository root:

```powershell
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase160_r3_canonical_toda45_specialization\run_phase160_r3.ps1"
```
