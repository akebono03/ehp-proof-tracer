Phase 162 R3-2 - Reference display integration

Extract at repository root, then run:
powershell -ExecutionPolicy Bypass -File .\phase162_r3_2_reference_display\run_phase162_r3_2.ps1

Updated: phase162_validated_proof_presentation.py
Updated: tests/test_phase162_r2_validated_proof_presentation.py
New: tests/test_phase162_r3_2_reference_display.py

The implementation only collects FIXED_STATEMENT nodes for literature references.
It uses the existing reference entry markdown renderer, including its catalog
ranges, and the existing statement renderers; PROOF_INTERNAL stays in proof body.
No synthetic generalization is made from a specialized statement.
The currently available generality of fixed statements is limited by their
existing registered structured conclusions and reference catalog.

No web change or whole-suite test is performed.
