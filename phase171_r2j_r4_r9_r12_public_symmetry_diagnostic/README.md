# EHP Proof Tracer — Phase 171 R2J-R4-R9-R12

This is a **read-only diagnostic release**. It does not patch project source,
create mathematical axioms, insert GIVEN proof steps, or replay finished trees.

## Prerequisite

The `develop` branch must contain the committed R11 equality-symmetry hook.
The reviewed SHA-1 Git blob of `phase165_r52_r9_shared_math.py` is
`10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac`.

The R10 commit `40fccc4d` is not sufficient; R11 was subsequently committed
as `e941ac47`. GitHub's develop branch was checked with the R11 hook in place.
A different source blob fails closed rather than being silently overwritten.

## Run on Windows PowerShell

Unpack the archive into the root of the EHP Proof Tracer checkout, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass `
  -File '.\phase171_r2j_r4_r9_r12_public_symmetry_diagnostic\run.ps1' `
  -DryRun
powershell -NoProfile -ExecutionPolicy Bypass `
  -File '.\phase171_r2j_r4_r9_r12_public_symmetry_diagnostic\run.ps1'
```

The detailed structured report will be written to
`phase171_r2j_r4_r9_r12_public_symmetry_diagnostic/output/audit.json`.
Only focused tests are executed. No full test suite is run.

## Diagnosis

The audit verifies the registered public-search context, then compares R11's
exact reverse-equality route at four points: direct rule output, deduplication,
root ordering gate, and the actual shared provider. It also reconstructs the
forward and reverse equalities *independently* through the canonical recursive
searcher, collecting accepted steps and unresolved subgoals as observations.

A proposed `GoalExpansion` is never counted as a proved `ProofStep`. A completed
Web proof is never declared merely because the candidate exists. All outputs
are recorded read-only, and no source changes are made automatically.

The next patch must be selected based on this report, not on a guessed search
failure. No implementation for a future phase is included.
