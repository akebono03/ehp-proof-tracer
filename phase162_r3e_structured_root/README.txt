Phase 162 R3-E: structured ROOT-ONLY proof composition (focused step)

Scope: The final group-structure-transport inference is rendered directly from
its original ProofStep premises and presentation edges. No historical Markdown,
no search for the text marker "以上より,", and no proof-type-specific literal.

Crucial: This experimental output is ROOT-ONLY. It does not narrate the proofs
of the three source premises (the 123-node ancestry). Therefore it does NOT
replace the existing public narrative yet; doing so would delete mathematical
proof content. This is deliberate and will be addressed by the next phase.

Unzip the archive in the project root and run:
  powershell -ExecutionPolicy Bypass -File .\phase162_r3e_structured_root\run_phase162_r3e.ps1

Focus tests only; full test suite is not run.
Output files:
  phase162_r3e_output/structured_root_only.md
  phase162_r3e_output/r3e_audit.json
