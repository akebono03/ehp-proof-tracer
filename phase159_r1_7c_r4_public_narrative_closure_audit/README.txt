Phase 159 R1-7c R4 public Narrative closure audit

Purpose
-------
Cross-check the public Narrative contract after the R4 repair sequence.

This audit verifies, over the reproducible sample n=2..15, k=0..7:

- no public target text contains the stale "を示す." phrase;
- no proof-body map property uses "は単射である." or "は全射である.";
- no equation-number reference points forward;
- every visible injective+surjective+isomorphism trio is fully numbered and
  the isomorphism conclusion appears after both numbered premises;
- injective+surjective pairs without an isomorphism conclusion remain
  non-isomorphism pairs.

The runner also executes the focused regression files for:
- equation-reference ordering;
- numbered map-property reasoning;
- concise map-property prose;
- exact-sequence suppression;
- pi6^3 exactness display;
- generator canonicalization.

This is not the full test suite.

Expected current cross-audit
----------------------------
- rendered: 112
- failed: 0
- target "を示す." findings: 0
- map-property dearu findings: 0
- forward equation references: 0
- fully numbered trios: 4
- defective numbered trios: 0
- injective+surjective pairs without isomorphism: 2

Scope
-----
Audit only.

Production code changes: none.
Test code changes: none.
No full pytest.
