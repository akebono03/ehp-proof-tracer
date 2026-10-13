# Phase 165 R14-R3 — Toda (5.1) Source Scope

This package adds an **audit-only** source-scope record for Toda (5.1).
The numbered equation and the immediately adjacent display provided by
the user are associated under the same reference. The adjacent text is
not independently verified against the full adopted TeX source.

## Changed files

- New root module `phase165_r14_r3_source_scope.py`, containing `SourceClause`,
  `CLAUSES`, and `collect_toda51_scope()`.
- New targeted test module `phase165_r14_r3_source_scope/test_phase165_r14_r3_source_scope.py`.
- New audit script and runner within the package.

**Existing files are unchanged.** In particular, the 117-row source manifest,
its hashes and publication positions, `phase165_r14_r2_toda51.py`,
registry eligibility, ProofStep, and Web UI are untouched.

The current two R14-R2 typed claim schemas are retained; the four additional
source clauses are **not yet mathematical typed schemas**. No certification
or ProofStep is generated.

## Run

Extract this archive into the repository root and execute:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r14_r3_source_scope\run.ps1"
```

Only targeted tests are run, not the full suite.

## Completion and subsequent phase boundary

Completion: six source clauses appear under (5.1), the numbered source hash
is validated, missing text fails closed, and the extra three display clauses
are visibly marked user-supplied/unverified. The next step is to verify that
the adjacent text belongs to the canonical file and to implement general
typed mathematical schemas and EHP reasoning, *without special-casing pi_3^2*.
