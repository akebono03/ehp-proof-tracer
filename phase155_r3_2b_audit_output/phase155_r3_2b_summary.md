# Phase 155-R3-2B — candidate verification failure audit

## Boundary

This step audits the two focused candidate-test failures and the seven R3-2 `needs_review` pairs.
It changes no production code and no existing test.

- Repository root: `C:\Users\oomae\Dropbox\Python\fitz\ehp_proof`
- Git HEAD: `9e985588f66f8f5ec80eb49aecd8177e61afd66a`
- Failing tests audited: 2
- Failing tests supported as stale expectation: 2
- R3-2 needs-review pairs audited: 7

## `pi6` occurrence classification in generic renderer

| AST classification | occurrences |
| --- | ---: |
| `attribute_field` | 3 |
| `identifier` | 0 |
| `string_literal` | 0 |
| `control_flow_condition` | 0 |
| `other` | 0 |

A `pi6` substring in a statement-field name is not by itself evidence of a pi6-specific renderer branch.
The relevant distinction is whether the occurrence participates in control-flow selection or is merely data access.

## Failing-test audit

| test | stale expectation supported | control-flow pi6 | attribute-field pi6 |
| --- | --- | ---: | ---: |
| `tests/test_phase143_1_generic_proof_order.py::test_phase143_1_generic_order_has_no_pi6_specific_hardcoding` | true | 0 | 3 |
| `tests/test_phase143_1b_semantic_proof_order.py::test_phase143_1b_generic_order_has_no_pi6_specific_hardcoding` | true | 0 | 3 |

## `needs_review` decomposition

| review class | pairs |
| --- | ---: |
| `failure_linked` | 1 |
| `source_evidence_issue` | 6 |
| `other_review_reason` | 0 |

## Completion interpretation

R3-2B is an audit-only step.
If both failing tests are supported as stale expectations and every `needs_review` pair is failure-linked, the next step can repair those two expectations and re-run the candidate-focused verification.
If any `needs_review` pair has another cause, that cause must be resolved before R3-3 consolidation.

Repository-wide pytest remains deferred until Phase 155 closure.
