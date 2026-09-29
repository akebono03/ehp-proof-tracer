Phase 148 RC2-4 Repair R4 — Web Narrative depth parity repair

Scope
-----
Minimal production repair for the mismatch found by R3.

Changed production file
-----------------------
web_group_proof.py

Changed import section
----------------------
Remove:
build_complete_toda_group_result_proof_replay

Keep:
build_toda_group_result_proof_replay

Changed function
----------------
build_standard_web_group_proof_view

Behavioral change
-----------------
Before:
- Web metadata / visible steps used the selected bounded replay.
- Web Narrative presentation silently switched to complete replay.

After:
- Web metadata, visible steps, and Narrative presentation all start from the
  same replay selected by max_depth.
- The existing Narrative renderer may still add narrowly defined semantic
  dependency closure. This preserves the Phase 144 semantic-closure mechanism
  without expanding the presentation to the entire recursive proof graph.
- Trace and Outline behavior are unchanged.

Historical contract intentionally superseded
--------------------------------------------
Phase 144-6 R25-22 intentionally made Web positive-depth Narrative use complete
replay to match the CLI route at that time. R3 showed that this now causes a
depth=2 Web request for pi_6^3 to feed 177 nodes / max depth 10 into Narrative,
producing 15 visible raw exactness statements.

R4 supersedes that Web-specific complete-replay contract. Archived Phase 144
files are not edited.

Focused R4 completion criteria
------------------------------
For pi_6^3, Web depth=2 Narrative:
- uses the bounded replay selected by max_depth;
- matches the public depth=2 Narrative renderer;
- shows zero raw exactness statements;
- preserves ord(nu') = 4;
- preserves pi_6^3 = Z/4{nu'};
- preserves the derived short exact sequence;
- preserves numbered equations (1), (2), (3);
- keeps Web response depth metadata at 2.

Phase boundary
--------------
No Narrative ordering repair is included.
No contribution-layer cleanup is included.
No repository-wide pytest is run.
RC3 / Phase 149 remains responsible for ordering.
