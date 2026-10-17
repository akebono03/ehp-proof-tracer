# Phase 165: Reference eligibility and backward-search stop boundary (R1)

This package audits the existing code path before changing any search behavior.
It checks the registered candidate statements for pi_3^2 and pi_4^3, whether exact fixed GIVEN links exist, and whether a reviewed order catalog can be resolved.
It does **not** change the registry, admissibility policy, search, proof graphs, or renderer. It does not certify the source ordering nor prove that the search stops at pi_3^2.

Run from the project root using `powershell -ExecutionPolicy Bypass -File .\phase165_reference_stop_r1\run.ps1`.
Results are written to `audit_result.json`. Only the three targeted tests run.

Next: inspect the runtime search frontier and the proof-order gate to implement a narrowly scoped, verified stopping boundary. Do not auto-admit unordered statements and do not consider a goal's own fixed assertion evidence for itself.
