# Phase 168 R2-6b — Auto-generated ProofStepLink audit

This diagnostic does not modify production code. It audits the existing `screen_shared_proof_context` route with `explicit_publication_target=True` for Proposition 5.3 and Proposition 5.6.

It distinguishes source archives (`SOURCE_ONLY`), statement-component metadata (`METADATA_ONLY`), and mathematical dataclass assertions (`TYPED_REGISTERED`). Raw `build_shared_typed_bridge()` link counts are not interpreted as missing citations.

The report records automatically generated GIVEN links and their source locations, and is saved to `output/autolink_audit.json`.

Run `run.ps1` in PowerShell from the repository root after extracting the ZIP. Only the four dedicated audit tests run; this is not a full test suite.
