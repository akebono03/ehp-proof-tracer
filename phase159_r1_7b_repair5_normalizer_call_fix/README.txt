Phase 159-R1-7b repair5

Fixes the repair3 application bug where the R1-7b helper was defined
but never called from `_phase158_normalize_public_narrative_contract`.

This repair changes only the production call site.
It reuses the repair4 focused tests.

No repository-wide pytest is run.
