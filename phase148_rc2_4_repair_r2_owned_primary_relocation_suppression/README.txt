Phase 148 RC2-4 Repair R2 — Owned-primary relocation suppression

Changed production file
-----------------------
toda_group_proof_narrative_argument_body_renderer.py

Changed function
----------------
render_toda_group_proof_narrative_argument_body_markdown

Import changes
--------------
None.

Production behavior change
--------------------------
The R1 relocation filter suppressed only UNOWNED_RECURSIVE exactness steps.

R2 applies the existing RC2 exposure policy consistently to relocation:
- OWNED_PRIMARY raw exactness steps: do not relocate
- UNOWNED_RECURSIVE raw exactness steps: do not relocate
- AMBIGUOUS_RELEVANT: preserve conservative current behavior
- unclassified steps: preserve current behavior

The existing exactness contribution renderer remains responsible for
OWNED_PRIMARY display. Therefore its derived short exact sequence is retained
while its raw exactness windows remain suppressed.

Non-goals
---------
- no proof graph changes
- no provenance deletion
- no Argument ordering changes
- no Narrative ordering changes
- no new mathematical heuristic
- no RC3 work

Tests
-----
The focused R2 test verifies:
- all three pi_6^3 raw exactness statements are absent
- the owned pi_6^3 derived short exact sequence remains
- the higher-level pi_6^3 method sequence remains
- pi_10^4 recursive exactness remains hidden
- pi_16^9 recursive exactness remains hidden

The runner also re-runs the relevant RC2/RC1/Phase143 focused tests.

No repository-wide pytest is run in this repair.
