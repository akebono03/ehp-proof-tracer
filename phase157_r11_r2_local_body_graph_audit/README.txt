Phase157 R11-R2 — A00 local-body proof-graph audit

R11-R1 established:
- the unwanted E: pi_4^2 -> pi_5^3 line is in A00 local body;
- pi_6^5 = Z/2{eta_5} is also in A00 local body;
- neither is an ordered contribution.

R11-R2 inspects only the A00 local proof graph:
- block role;
- step type and rendered statement;
- whether the step can reach the argument conclusion through local graph edges;
- immediate consumers.

No production or test code is changed.
No pytest is run.

The result determines the generic R11 implementation rule.
