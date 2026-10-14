# Phase 165 R27-R34

Adds a generic typed statement search using the canonical backward prover. Connects the Web Operation Query view to this search. Generator search is available through `search_typed_generator_statements`; the Web Generator UI remains a separate integration task.

The tool never borrows a result from the old ProofRepository and marks a candidate proven only when the canonical reconstruction succeeds. The old explicit-repository APIs remain untouched. The existing Web Operation Query view cannot express PARTIAL, so unproved candidate goals are not displayed as results.

Run `run.ps1` from the extracted folder in the repository root. Runs targeted pytest only.
