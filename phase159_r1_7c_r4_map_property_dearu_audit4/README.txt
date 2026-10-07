Phase 159 R1-7c R4 map-property "である" function-owner audit4

Purpose
-------
Audit3 classified the eight confirmed public occurrences as:
- seven later contribution/dependency insertion occurrences;
- one raw/aggregate statement occurrence.

GitHub inspection shows literal production sources in:
- toda_group_proof_narrative_contribution_renderer.py
- toda_group_proof_aggregate_statement_renderer.py

Audit4 identifies the exact owning function(s) for every current literal:
- は単射である.
- は全射である.

Method
------
The audit parses the current Python modules with ast and reports:
- source line number;
- exact source line;
- every enclosing function;
- nested helper ownership when applicable.

This determines the smallest replaceable production units before any
implementation change.

Production code changes: none.
Test code changes: none.
No full pytest.
