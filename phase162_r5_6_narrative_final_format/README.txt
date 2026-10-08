Phase 162 R5-6 narrative presentation polish

Changed production module: phase162_web_narrative_integration.py
Modified function: build_phase162_web_validated_isomorphism_markdown (full function included)
New helpers: _format_phase162_proof_sentences and _compose_phase162_group_conclusion, inserted before build_phase162_web_validated_isomorphism_markdown.
New focused tests: tests/test_phase162_r5_6_narrative_final_format.py
No import changes in this module.

Scope: WEB n=3,k=2 supplemental validated proof only. The existing primary group-proof renderer is deliberately untouched. This is a presentation-level corollary combining the validated E isomorphism with the known pi_4^2 group and suspension of eta_2^2; it is not presented as a new R7 validated ProofStep. The EHP exact sequence is shown explicitly. Paragraphs are split at Japanese full stops and punctuation in the proof body is normalized to ASCII. References and math expressions are preserved.

Run from repository root using run_phase162_r5_6_narrative_final_format.ps1.
Use focused tests only. Full suite remains for Phase 162 R6.
