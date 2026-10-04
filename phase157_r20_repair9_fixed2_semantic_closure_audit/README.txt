Phase157-R20 repair9 fixed2

Purpose
-------
Audit the actual Reference pipeline used by the public Narrative.

Important correction
--------------------
repair9 fixed1 inspected the presentation before semantic closure.

The production Narrative first calls:

  build_toda_group_proof_narrative_semantic_closure_presentation()

and only then builds Reference entries.

Therefore fixed1's `Proposition 2.2 raw=NO` was not sufficient to locate the
production defect.

This audit compares:
- base presentation;
- semantic-closure presentation;
- raw References after closure;
- fixed-statement boundary output;
- statement-line selection;
- root-reference exclusion;
- dependency trees for Proposition 5.3 and Proposition 2.2.

Production code changes: none.
Test changes: none.
pytest: not run.
