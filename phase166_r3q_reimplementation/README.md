# Phase 166 R3-Q reimplementation

Extract this ZIP into the existing EHP Proof Tracer project root. Run the included `run.ps1` from PowerShell while the working directory is the project root.

This release separates goal selection from published-reference eligibility. It uses the existing publication-order comparator only when a unique, directly recorded, positioned assertion identifies the requested goal. Unlocated or ambiguous goals retain the existing search behavior. No artificial positions, precomputed proofs, new mathematical rules, or renderer modifications are introduced.

The script backs up the original module before making the change and runs focused tests, including the established six-test public pi3^2 regression. It does not run the full suite. Production files are not modified if the function shape fails preliminary checks.
