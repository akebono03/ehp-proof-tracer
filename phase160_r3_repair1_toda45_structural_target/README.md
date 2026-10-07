# Phase 160-R3 Repair 1

Repair the canonical Toda (4.5) specialization so its transport map uses the structural group-degree form required by the existing Toda (4.5) inference rule.

The existing rule does not numerically simplify a concrete target degree such as `5` into `4 + 1`. It requires the target group dimension to be represented structurally as `ScalarSum(left=m, right=k)`.

This repair therefore changes only the Phase 160-R3 bridge and its focused tests.

It does not change:

- `stable_rules.py`
- `toda_rules.py`
- the Toda (4.5) theorem rule
- group-structure transport
- generator normalization
- public Narrative

No full test suite is run.
