# Phase 166 R3-C Stage 2

Extract this archive into the EHP Proof Tracer repository root and run `powershell -ExecutionPolicy Bypass -File .\phase166_r3c_stage2\run.ps1`.

This installation adds publication-order filtering to shared proof search only when the caller supplies an explicit typed citing-assertion ID. The existing implicit public goal path is unchanged. It uses existing typed statements and GIVEN links; it does not create proof facts or parse TeX. Only focused pytest runs. Confirm `n=2, k=1` in the Web UI after installation.
