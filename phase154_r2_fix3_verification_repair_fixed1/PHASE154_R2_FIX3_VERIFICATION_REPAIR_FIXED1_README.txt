Phase 154-R2 Fix3 — Verification Repair Fixed1

Production changes
------------------
none

Cause
-----
The previous verification repair used a long inline:

  python -c "..."

command containing Japanese strings.

On Windows PowerShell, those Japanese characters were corrupted before Python
parsed the command, producing:

  SyntaxError: invalid non-printable character U+0080

The focused pytest run had already completed successfully:

  26 passed

Therefore this is a verification-script encoding issue, not a Phase 154-R2
production-code regression.

Repair
------
Move the representative Narrative assertions into a UTF-8 encoded Python file:

  check_phase154_r2_fix3_representative_narrative.py

The PowerShell runner now invokes that file directly.

Production files changed
------------------------
none

Tests
-----
The same current-contract focused tests are rerun:

- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r7_proof_body_relevance.py
- tests/test_phase153_r8_reference_use_prose_normalization.py
- tests/test_phase153_closure_repair_r13.py

Representative conditions
-------------------------
pi_11^4 must contain:

  まず、[R2]を用いる。
  $\nu_{4}$ の分解写像は同型写像である.
  \pi_{11}^{4} = 0

and must not contain:

  まず、[R2]        as an incomplete line
  Toda Proposition 5.15を用いる。
  \text{ is injective}
  \text{ is exact}
  である.を用いる。

Full suite
----------
not run; reserved for the end of Phase 154.

Completion boundary
-------------------
If this verification passes, Phase 154-R2 is complete and the next step is
Phase 154-R3 cross-group re-audit.
