Phase157 R11-R5 — generic stage transition audit

R11-R4 established on current local HEAD:
- semantic closure is idempotent;
- the unwanted suspension-isomorphism line is already present in generic output;
- therefore double closure is not the cause.

R11-R5 monkeypatches the current local contribution renderer only for this
one audit run and records target-statement presence before and after each
pipeline stage.

Targets:
- unwanted: E: pi_4^2 -> pi_5^3 is an isomorphism
- needed: pi_6^5 = Z/2{eta_5}

This identifies the exact function where a False -> True transition occurs.

Production code changes: none
Test code changes: none
pytest: not run
