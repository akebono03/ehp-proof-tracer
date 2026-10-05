Phase 158-R5-5 closure / focused verification
==============================================

Purpose
-------

Close R5-5 by re-verifying the generic public ordering and sequence contracts
established across R5-5a through R5-5d.

This package changes no production code and no existing tests.

Files
-----

- audit_phase158_r5_5_closure.py
- test_phase158_r5_5_closure.py
- run_phase158_r5_5_closure.ps1
- README.txt

Focused verification
--------------------

The runner executes:

1. Existing R5-5a depth=2 audit-contract tests.
2. Existing R5-5b generic-order and Web verification tests.
3. Lightweight closure-harness tests.
4. A current-corpus Web Narrative depth=2 closure cross-check.

Closure invariants
------------------

The cross-check verifies that:

- Web public Narrative is generated at depth=2.
- Every numbered connector refers only to already-visible equation tags.
- Every numbered connector has an immediate visible target.
- The target itself does not require a tag unless later prose needs to refer
  to it.
- The public root target is immediately before one terminal QED marker "□".

The current n=2..15, k=0..7 window is only the historical audit corpus.  It
is not an architectural fixed-group-count contract.

Completion condition
--------------------

R5-5 closure is PASS when:

- all focused pytest invocations pass;
- 112 current audit coordinates render;
- exceptions = 0;
- wrong Web mode/depth = 0;
- connector findings = 0;
- root/QED findings = 0.

Boundary
--------

Repository-wide pytest is intentionally NOT run here.  Whole-repository
pytest remains reserved for the end of Phase 158.

Production code changes: none.
Existing test changes: none.
