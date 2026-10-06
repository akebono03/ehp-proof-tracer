Phase 159 R1-7c R4 map-property "である" repair1 closure audit

Purpose
-------
Verify that repair1 removed the confirmed public proof-body forms:

- は単射である.
- は全射である.

while concise forms remain visible:

- は単射.
- は全射.

Scope
-----
Audit only.

Range:
  n=2..15
  k=0..7
  max_depth=2

This is a reproducible audit sample only. It is not a permanent group-count
contract.

The audit reports:
- render failures;
- outputs/occurrences still containing forbidden old prose;
- outputs/occurrences containing concise map-property prose.

Production code changes: none.
Test code changes: none.
No full pytest.
