# Phase 165 R27-R45: Typed inference execution

Install the independent typed inference execution layer and connect Web Generator Execution to it. The implementation uses only established `ProofStep` premises and exact `InferenceMatch` instances. It never auto-selects multiple candidates. Legacy calculation and repository modules are untouched. Run `run.ps1` from the extracted folder in the repository. Only targeted tests are run, not the full suite.
