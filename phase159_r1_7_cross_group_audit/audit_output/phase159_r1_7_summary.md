# Phase 159-R1-7 Cross-group Display Audit

Production code changes: none.
Existing test changes: none.
Repository-wide pytest: intentionally not run.

Representative groups:
- $\pi_6^3$
- $\pi_8^5$
- $\pi_{10}^4$
- $\pi_{11}^4$

## Result matrix

| group | exact-seq candidates | tags | map property lines | defect flags | review candidates |
| --- | ---: | --- | ---: | --- | --- |
| $\pi_{6}^{3}$ | 2 | (1, 2) | 6 | exact_sequence_not_display_math, equation_tag_outside_display_math | multiple_exact_sequence_candidates, exactness_reason_style_variation, reference_connector_style_candidate |
| $\pi_{8}^{5}$ | 0 | - | 1 | none | exactness_reason_style_variation, group_generator_brace_candidate |
| $\pi_{10}^{4}$ | 0 | - | 0 | none | reference_connector_style_candidate |
| $\pi_{11}^{4}$ | 0 | - | 3 | exact_sequence_not_display_math | map_property_dearu_style_candidate, reference_connector_style_candidate |

## Classification rule for the next step

- A: generic display rule itself is defective.
- B: generic rule exists but is not applied on a route.
- C: proof data / semantic classification is the source.
- D: group-specific mathematical circumstance; do not generalize blindly.

R1-7 is audit-only. Do not repair findings in this package.
If a finding is confirmed, split it into R1-7a, R1-7b, ... by root cause.
