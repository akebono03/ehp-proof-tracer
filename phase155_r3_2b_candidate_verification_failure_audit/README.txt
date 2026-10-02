Phase 155-R3-2B — candidate verification failure audit

Purpose
-------
Audit the two focused test failures found by R3-2 and decompose all seven
`needs_review` candidate pairs before any duplicate-test removal.

This step does not modify production code or existing tests.

Failure audit
-------------
The two failing tests both inspect the complete source of
`toda_group_proof_generic_narrative_renderer.py` and prohibit the substring
`pi6`.

R3-2B classifies every AST-level `pi6` occurrence in that module as:
- attribute_field
- identifier
- string_literal
- control_flow_condition

A field name such as `statement.pi6_4_group_relation` is data access and is
not by itself evidence of a pi6-specific rendering branch.

The old global substring ban can be classified as stale only when:
- the failing test really contains that global ban,
- current `pi6` occurrences exist,
- none of those occurrences participate in control flow, and
- all current occurrences are attribute-field accesses.

Needs-review audit
------------------
Every R3-2 `needs_review` pair is classified as:
- failure_linked
- source_evidence_issue
- other_review_reason

This determines whether repairing the two stale hardcoding expectations is
sufficient to close R3-2, or whether another issue must be handled first.

Boundary
--------
- production code changes: none
- existing test changes: none
- deleted tests: none
- repository-wide pytest: not run
