Phase 144-6-R5-4 Argument dependency gap audit

Purpose
-------
Audit the mismatch between proof dependency closure and
TodaGroupProofNarrativeArgument.child_argument_indices.

This package does NOT modify production code, tests, or project documents.

Targets
-------
- pi_15^8
- pi_16^9
- depths 0 through 8

The audit prints
----------------
- root Argument
- direct child_argument_indices
- Argument conclusions reachable in the root block dependency closure
- gap Arguments
- the exact block path from the root conclusion to each gap Argument conclusion
- whether each hop comes from presentation.edges or semantic dependencies
- a coarse structural classification

Important
---------
Reachability alone does not mean an Argument is required in Narrative prose.
R5-4 is intended to identify the dependency shape before any depth-policy
implementation is attempted.
