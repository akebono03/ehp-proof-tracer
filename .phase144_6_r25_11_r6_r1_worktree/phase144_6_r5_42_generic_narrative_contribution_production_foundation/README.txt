Phase 144-6-R5-42
generic Narrative contribution placement/order production foundation

Production change:
- add toda_group_proof_narrative_contribution_ordering.py
- no renderer output change
- no public CLI/Web route change
- no existing API removal/change

The production builder promotes the audited Phase 38-41 structure:
dedup -> necessity -> placement -> proof-graph topological ordering.

For the two non-unique definition Arguments, ties are resolved only by already
stored semantic order: argument.supporting_blocks, then local-body block/step order.
The Phase 41 diagnostic stable key is not used as a production rule.

Targeted tests only. Do not run the full suite in this subphase.
