Phase157-R20 repair17 runtime audit

Purpose
-------
Locate why the generic eta suspension bridge

  eta_6 = E eta_5

is not present after repair16.

The audit checks:
- Equation (5.7) proof-step premises;
- eta_5 / eta_6 definition nodes in semantic closure;
- body paragraphs immediately before bridge insertion;
- body paragraphs immediately after bridge insertion;
- final eta-related public Narrative paragraphs.

Hypothesis
----------
The proof graph contains both eta definitions, but the current bridge insertion
requires the eta_6 definition paragraph itself to be visible as an anchor.
Reference/internal suppression may have removed that paragraph before the
bridge function runs.

Production code changes: none.
Tests: none.
pytest: not run.
