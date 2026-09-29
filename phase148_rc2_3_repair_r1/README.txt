Phase 148 RC2-3 Repair R1

Cause
-----
The RC2-3 contribution filter suppresses UNOWNED_RECURSIVE exactness
contributions, but an exactness ProofStep can also enter Narrative through
direct-derivation-premise relocation.

The pi_10^4 failure exposed this second rendering path.

Production change
-----------------
File:
  toda_group_proof_narrative_argument_body_renderer.py

Function:
  render_toda_group_proof_narrative_argument_body_markdown

Minimal repair:
- Build the ProofStep-id set belonging to exactness blocks classified
  UNOWNED_RECURSIVE.
- Exclude only those steps from relocated_direct_premises.
- OWNED_PRIMARY and AMBIGUOUS_RELEVANT behavior is unchanged.
- Proof graph and provenance are unchanged.
- Argument/Narrative ordering is unchanged.

Test added
----------
tests/test_phase148_rc2_3_repair_r1.py

No repository-wide pytest is run here.
