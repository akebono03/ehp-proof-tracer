# Phase 154-R3 Cross-group Prose Re-audit

Production changes: none.

Conditions:
- Narrative view
- depth 2
- primary: pi6_3, pi10_4, pi11_4
- secondary: pi12_5, pi16_9

## Category totals

- internal_fallback: affected_groups=0, findings=0
- bare_reference_marker: affected_groups=0, findings=0
- transition_repetition: affected_groups=1, findings=1
- semantic_duplication: affected_groups=3, findings=8
- reference_body_linkage_candidate: affected_groups=1, findings=2
- punctuation: affected_groups=5, findings=43

## Per-group counts

| group | tier | internal fallback | bare reference | transition | duplication | reference linkage candidate | punctuation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| $\pi_{6}^{3}$ | primary | 0 | 0 | 0 | 4 | 0 | 15 |
| $\pi_{10}^{4}$ | primary | 0 | 0 | 0 | 2 | 0 | 5 |
| $\pi_{11}^{4}$ | primary | 0 | 0 | 1 | 0 | 2 | 4 |
| $\pi_{12}^{5}$ | secondary | 0 | 0 | 0 | 0 | 0 | 8 |
| $\pi_{16}^{9}$ | secondary | 0 | 0 | 0 | 2 | 0 | 11 |

## Interpretation rule

- internal_fallback / bare_reference_marker: R2 regression candidate.
- transition_repetition: R4 candidate.
- semantic_duplication: R4 candidate.
- reference_body_linkage_candidate: R5 candidate; a hit is not automatically a defect.
- punctuation: R6 candidate.
- This audit does not modify production code.
