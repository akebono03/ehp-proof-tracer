# Phase 173 R4-R15R1 — Unbounded Abstract Prior Frontier

This narrowly scoped patch separates the abstract group-shape prerequisite for Toda Proposition 4.4 from the stronger, independently verified named-generator correspondence. It is not a new proof rule and does not mark the high-stem group as proved.

The reviewed target is `phase173_r4_r10_general_toda56_core/core.py`. Its existing `checked_general_inputs` contract remains strict: only previously certified generator correspondences qualify for the existing public proof route. The newly inserted `checked_abstract_inputs` has no hard-coded upper stem limit. For `n=4, k=31` it checks the three actual registered database statements, both earlier-source admission guards, and the cyclic-order multiset. It makes no database claim into a literature fact.

The ZIP contains a source and Git-blob guard, a full-source preview, a reversible one-file installer, focused unit and repository tests, and a read-only frontier report. It does not change the proof-search connection, central renderer, citation model, or database. As before, an abstract structural match alone never permits `generic-complete-proof` for the eight specified generators.

## Run

Extract this ZIP at the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r1_unbounded_abstract_frontier\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r1_unbounded_abstract_frontier\run.ps1"
```

Only focused pytest tests are executed; the full suite remains reserved for Phase 173 closeout. If a repository-backed test fails after applying the new core helper, the runner requests a guarded rollback. Existing unrelated uncommitted changes are not overwritten.

### Acceptance and next boundary

The source guard and focused tests must pass; the `k=31` structural row must have two real prior statements and eight target cyclic components. The report shows which source-generator suspension images are still unsupported. The next substep must supply proof-backed suspension and composition identities for those symbols before connecting a public complete proof. This ZIP intentionally does not solve that future obligation.
