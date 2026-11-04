# Phase 173 R4–R15R16R2: Common Verified Tree Narrative

This Phase step eliminates the R15R16 special-case sentences for abstract group progress. It traverses the already-certified abstract `ProofStep` ancestry, builds the existing `ProofNarrativeModel`, and calls the very same `render_model_backed_narrative_markdown()` used for completed and incomplete proofs. No theorem-specific milestone prose is added.

The original named-generator `PartialProofResult`, its `SEARCH_FAILED` status, all open goals, and its `CertifiedAbstractStructure` remain unchanged. Only evidence already present in the certificate is supplied to the shared rendering pipeline. Mathematically unrenderable source types are not converted to guessed formulas. Verified Reference locators are taken from actual cited inference rules and database-source steps.

This package replaces only the R15R16 local intermediate-progress function, adds one generic proof-tree adapter, and updates the R15R16 test that previously required hand-written sentences. The existing common punctuation layout is preserved, including ASCII commas/periods and sentence-final line breaks.

## Windows execution

Expand the ZIP into the repository root, then run `phase173_r4_r15r16r2_shared_tree_narrative/run.ps1 -DryRun` and subsequently `run.ps1`. Both source guard and targeted pytest are included. A failure restores exactly the pre-R15R16R2 state, without reverting R15R16 or overwriting other user edits.

This patch requires the **uncommitted R15R16 installation** on top of reviewed GitHub `develop` commit `92f967c079f4a66e19a598e0acc54b742f11df9c`, or a descendant with unchanged reviewed source blobs. If R15R16 has since been committed, the guard intentionally stops for a fresh audit.

Full-suite pytest is reserved for Phase 173 closeout.
