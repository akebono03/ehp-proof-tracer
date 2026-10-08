Phase 161 — Selective Production connection (read-only feasibility experiment)

Purpose:
- Build the REAL production repository and applicability catalog.
- Search production proof ancestry for the exact E: pi_4^2 -> pi_5^3 isomorphism.
- Extract a seven-rule proof trace and its boundary premises, if present.
- Build strictly temporary, isolated repository/catalog objects using ONLY real production ProofStep and InferenceRule instances.
- For this experiment alone mark the seven selected rules eligible and compare bounded search at depths 2,3,4.
- No production source files, tests, original repository or catalog are modified.

Important:
- Ancestry-driven extraction is NOT full goal-only discovery.
- "fixed_point_safe=True" in the temporary catalog is an experimental override, NOT safety certification.
- If the ancestry does not match exactly 7 rules / 6 premises, stop and report the difference rather than adding Phase 59 test seed facts.
- The output is phase161_selective_connection_validation.json in the repository root.

Command (PowerShell, repository root):
  powershell -ExecutionPolicy Bypass -File .\phase161_selective_connection_validation\run_phase161_selective_connection.ps1
