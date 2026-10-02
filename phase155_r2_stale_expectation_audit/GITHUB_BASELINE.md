# Phase 155-R2 GitHub baseline

Checked before implementation:

```text
repository: akebono03/ehp-proof-tracer
branch: main
baseline commit observed during Phase 155-R1: 8301520a7434f3836b1dbc7e8fa08a60c024225a
```

Relevant current-contract tests inspected from GitHub include:

```text
tests/test_phase154_r6_1_repair3_ascii_period_policy.py
tests/test_phase154_r6_2_ascii_comma_normalization.py
tests/test_phase154_r4_semantic_duplication_transition_refinement.py
tests/test_phase153_r10_used_reference_filtering.py
tests/test_phase153_r12_root_reference_exclusion.py
tests/test_phase144_6_pi6_generic_production_route.py
```

Current contract evidence:

```text
Phase 154:
- prose comma = ", "
- prose period = "."
- internal fallback leakage = 0
- semantic duplication = 0
- Reference linkage violations = 0

Phase 153:
- unused References are filtered
- external References are renumbered
- root theorem is excluded from the external Reference section
- Reference granularity/reuse is presentation-side and provenance-backed
```

R2 is an expectation-level static audit only. It does not repair or delete tests.
