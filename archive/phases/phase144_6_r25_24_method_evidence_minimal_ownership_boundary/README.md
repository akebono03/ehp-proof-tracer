# Phase 144-6 R25-24 Method Evidence Minimal Ownership Boundary

## Goal

Prevent complete-replay Narrative rendering from treating the full recursive
exactness ancestry of an argument as method evidence.

## Production files

- `toda_group_proof_narrative_method_evidence.py`
  - `extract_toda_group_proof_narrative_argument_method_evidence`
- `toda_group_proof_narrative_argument_multi_renderer.py`
  - `render_toda_group_proof_narrative_multi_argument_markdown`

## Rule

The existing method-evidence API remains recursive by default.

A new keyword-only option, `minimal_ownership=True`, treats an `EXACTNESS`
block as a terminal evidence boundary:

- the reached exactness block is retained;
- traversal does not continue through that exactness block into older
  exactness ancestry.

The generic multi-argument production renderer opts into this boundary.

For the rendered local body, non-exact blocks still come from the existing
argument-local body. Exactness blocks are retained only when they belong to the
selected minimal method evidence.

## Preserved behavior

This phase does not change:

- semantic closure;
- argument construction;
- argument ordering;
- direct-premise protection;
- the R25-11 frontier rule;
- equation numbering;
- exactness component construction;
- the legacy/default method-evidence API behavior.

## Tests

The package runs:

- focused R25-24 tests;
- existing Phase143 method-evidence/exactness regressions;
- the existing generic pi6 production-route regression;
- a six-group ownership-count audit.

Repository-wide pytest is intentionally deferred until the end of Phase
144-6.
