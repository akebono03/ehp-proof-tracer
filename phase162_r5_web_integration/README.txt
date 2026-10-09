Phase 162 R5 Web Narrative Integration

Changes only web_group_proof.py narrative branch for n=3,k=2, adds
phase162_web_narrative_integration.py, and adds focused tests.
Existing group result remains the root result. The validated E isomorphism
narrative is appended as a distinct section and parsed by the existing web
Markdown line parser. All other modes/groups follow their preexisting route.

Production input evidence is obtained from the Phase 55/58 representative
probes and four Phase 59 EHP exactness witnesses; never from tests.
Provenance is verified through Phase 161 R7 before display.

The installer makes a backup of web_group_proof.py, writes the full updated
build_standard_web_group_proof_view function in CHANGED_FUNCTION_FULL.txt,
then runs focused pytest only. Full suite is reserved for R6.
