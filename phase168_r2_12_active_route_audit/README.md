# Phase 168 R2-12 Active Web Route Audit

Read-only audit of the completed `pi_4^2` Web narrative path. It observes one Web call, the `PartialProofResult`, the presentation built by `phase165_r56_presentation_adapter`, and the reference entries created in the contribution renderer. It does not modify repository sources or perform a full test suite run.

Run `powershell -ExecutionPolicy Bypass -File .\phase168_r2_12_active_route_audit\run.ps1` from the repository root. Outputs are placed in `output/active_route_trace.json` and `output/active_route_trace.md`.

This audit deliberately uses the completed route, not a direct call to the old renderer. Results reflect the local working tree and are not proof certificates.
