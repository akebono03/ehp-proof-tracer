Phase 162 R10 Repair 1: identity-based citation test correction

Only updates phase162_r10_reference_boundary/test_r10.py.
No production code, Renderer, ProofStep, or validation rules are changed.

A valid citation has two nodes with the same conclusion:
- trusted GIVEN citation leaf, and
- verified INFERENCE that applies that leaf.
The original test incorrectly counted both as distinct literature citations.
The revised test verifies identity, shape, no third matching ancestry, no
lemma52 inference, and a reduced total node count.

Run from EHP Proof Tracer root:
  powershell -ExecutionPolicy Bypass -File .\phase162_r10_repair1_citation_identity_test\run.ps1
Only 3 focused tests are executed. No full suite.
