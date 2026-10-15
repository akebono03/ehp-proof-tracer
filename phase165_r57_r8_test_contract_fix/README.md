# Phase 165 R57-R8 test contract correction

Only the Phase R57-R8 targeted test file is replaced; production code is untouched. The first correction expands the registered, cited GIVEN composite into its typed components before checking the shared provider. The second correction derives a ProofStep from an InferenceMatch before inspecting its conclusion. The package installer refuses unexpected earlier test content, keeps a backup, and is idempotent.

Run `run.ps1` from the extracted folder. This runs only the R57-R8 and R57-R7 targeted pytest suites in separate processes. No full suite is executed.
