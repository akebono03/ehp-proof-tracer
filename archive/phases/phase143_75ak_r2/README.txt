Phase 143-75AK-R2

R1 stopped before changing production source.
R2 fixes only the patcher by locating the toda_rules import structurally
with Python ast rather than matching an escaped newline string.

Production semantic scope remains:
- iterated_suspension_relation
- double_relation
- hopf_relation

Focused tests only. No full pytest.
