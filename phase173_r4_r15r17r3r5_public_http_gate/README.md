# EHP Proof Tracer — Phase 173 R15R17-R3R5 Public HTTP Gate

This package is a **read-only focused audit** of the canonical Web Narrative following R15R17-R1, R2, R3R3 and R3R4. It does not change proof search, mathematical objects, production Python files, tests from earlier phases, the Web template, or the Git index.

## Scope and provenance

Reviewed GitHub `develop` baseline: `a3baa7f2d5fa94983bbe1b795bd1883d57680b5b` (`173-15-17-3-3`). The PowerShell runner fetches `origin/develop`, accepts later descendants of the reviewed baseline, and stops if any relevant production source has changed relative to that baseline or is modified locally. Existing changes to the ten historical regression test files are preserved.

The tests use the **real Flask application, actual typed group-proof search, the canonical ProofNarrativeModel, common Renderer, Web adapter, and Jinja template**. Only the unrelated group-structure query is replaced with a known NOT_FOUND result, preventing an extra database search and exercising the existing public result-banner logic. No mathematical proof is mocked or promoted.

Four group cases are checked: `(n,k)=(4,8)` (certified abstract, named incomplete), `(4,9)` (certified abstract direct sum, named incomplete), `(5,3)` (uncertified incomplete), and `(4,4)` (named complete). The HTML gate checks a single Reference heading, absence of a separate abstract/tree appendix in the canonical route, named-proof status, pending-goal display counts, verified abstract math, and no internal Python type-name leak.

**This is HTTP/template verification, not visual browser verification.** Mathematical proof correctness and the historical compatibility API are covered by earlier focused tests. The full pytest suite is reserved for the Phase 173 closeout.

## How to run on Windows PowerShell

Extract the ZIP at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r17r3r5_public_http_gate\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r17r3r5_public_http_gate\run.ps1"
```

DryRun executes four fast, isolated parser tests. Normal execution adds four real Flask HTTP tests. Both modes verify Git branch, ancestry, production source changes, and index preservation. Use `git --no-pager status -sb` after the run.

## Success conditions

The normal run reports `R15R17R3R5_SOURCE_GUARD=PASS`, four `R15R17R3R5_HTTP_CASE` records, `R15R17R3R5_HTTP_GATE=PASS`, `R15R17R3R5_GIT_INDEX_PRESERVED=PASS`, and `R15R17R3R5_AUDIT_COMPLETE=PASS`.

Follow the Japanese `MANUAL_BROWSER_CHECK.md` to verify interactive browser rendering separately. No source files are modified by this package, and no full pytest run is performed.
