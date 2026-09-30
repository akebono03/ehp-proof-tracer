# Phase 150 RC4-5 Visible Reason Multiplicity Audit

Audit only. No production code, existing tests, or documentation are changed.

For each of the six RC4-5 representative groups, this audit records:

- typed reason count
- rendered reason sentence
- typed reasons that map to the same sentence
- number and character positions of sentence occurrences in Narrative
- approximate line positions and nearby Narrative context
- typed-side duplication versus rendered-side duplication

The purpose is to distinguish:
1. intentional many-to-one reason rendering;
2. duplicate emission through multiple Narrative paths;
3. an invalid one-reason/one-visible-sentence test contract.

No full regression is run.
