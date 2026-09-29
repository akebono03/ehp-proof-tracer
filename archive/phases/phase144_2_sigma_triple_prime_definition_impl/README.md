# Phase 144-2 Sigma Triple-Prime Definition Structure

This package makes the minimal Phase 144-2 production change needed to recognize `TodaLemma513Statement` as a generic Narrative Definition statement.

Changes:

1. Add `TodaLemma513Statement` to `DEFINITION_STATEMENT_TYPES`.
2. Add a small generic definition-subject extractor in `toda_group_proof_narrative_arguments.py`.
3. Preserve the existing `.element` convention for nu/sigma family definitions.
4. Use `.sigma_triple_prime` for `TodaLemma513Statement`.
5. Add focused tests for pi_12^5 and regression checks for pi_8^5 / pi_16^9.

This package intentionally does not:

- change the generic statement renderer;
- suppress the unrelated nu_n definition from pi_12^5;
- add pi_12^5-specific Narrative code;
- change scalar-condition rendering;
- run the full regression suite.

The post-implementation audit prints the resulting pi_12^5 Argument ordering and discourse. Its result determines the next minimal Phase 144-2 step.
