Phase 156-R5 repair7 boundary identity diagnostic

Production changes: none.

Purpose
=======
Determine why the public pi_6^3 Narrative still expands the internal proof of
Toda (5.3) after repair6/repair7.

The diagnostic prints, for depth 2 and 3:

- every (5.3) Reference entry step
- Python object identity
- selected/unselected status
- inference rule and LiteratureReference
- DEFINITION_APPLICABILITY / Lemma 5.2 reason conclusion identity
- whether that conclusion belongs to any Reference entry
- ESTABLISH_DEFINITION argument conclusion identity
- public Narrative body

This decides whether the correct generic boundary should be based on:
- exact ProofStep identity,
- LiteratureReference identity,
- ancestry ownership,
- or argument ownership.

No pytest and no repository changes are made.
