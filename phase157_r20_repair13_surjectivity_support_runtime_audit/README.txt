Phase157-R20 repair13 runtime audit

Purpose
-------
Determine whether repair12 inserts the Proposition 5.3 target-group support
paragraph before the second body-usage filter.

This audit wraps only:
- order_toda_group_proof_narrative_surjectivity_support()
- filter_toda_group_proof_narrative_reference_entries_by_body_usage()

It prints:
- relevant paragraphs before and after surjectivity support;
- selected R3/R4/R5 statements at the order call;
- R3/R4/R5 marker presence at each body-filter input;
- final public Reference headers.

Production code changes: none.
pytest: not run.
