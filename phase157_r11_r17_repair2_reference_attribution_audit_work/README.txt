Phase157 R11-R17 repair2 pre-audit

repair1 result:
- 71 passed
- 4 failed
- all remaining failures are Reference attribution / pruning

This audit does not change production or tests.

Targets:
- pi_6^3
- pi_10^4
- pi_12^5
- pi_16^9

For each public Reference it prints:
- public [R#] title
- raw source step
- direct consumers
- whether each consumer is visible in body
- whether consumer is root
- literature ownership of consumer
- final body marker count

Purpose:
separate
- direct public consumer
- root direct consumer
- Reference-owned ancestry
before repair2 implementation.

No pytest.
Full pytest remains deferred until Phase157 closure.
