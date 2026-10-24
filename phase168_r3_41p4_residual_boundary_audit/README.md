# Phase 168 R3-41P4 — Residual Renderer Boundary Audit

This package audits remaining proof-validation calls and rule-name coupling in the common Renderer, without changing project source files or tests.

## Prerequisites

Run this after R3-41P3 has passed. The audit checks that the previous removal of `specialize_typed_statement` from the Renderer and Typed Projection is still present.

## Windows PowerShell

From the root of the `ehp-proof-tracer` checkout:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p4_residual_boundary_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p4_residual_boundary_audit\run.ps1"
```

The script audits the public Web path for three completed groups and runs a limited set of pytest files. It does not run the full pytest suite.

## Outputs

The package writes within `phase168_r3_41p4_residual_boundary_audit/output/`:

- `audit.json`, `audit.md`: source diagnostics, runtime validator call log and typed-step attribution.
- `pi3_2_current.md`, `pi4_3_current.md`, `pi5_4_current.md`: full proof and Reference output.
- `pi*_fulltext.diff`: byte-for-byte comparison with the saved R3-41P3 output.
- `audit_stdout.log`, `audit_stderr.log`, `pytest_focused_stdout.log`, `pytest_focused_stderr.log`: full logs.
- `review_bundle.zip`: the resulting inspection bundle, including logs and comparisons even on failure.

## Interpretation

- `prop42_exactness_indices()` and `_stable_eta_renaming_shape()` are instrumented without bypassing their original implementations.
- A `0` call count does **not** demonstrate that the validator is dispensable. It only means that the sampled three Web proofs did not exercise it.
- Rule-name-dependent suppression candidates are identified by reading the Proof Tree. No suppression logic is modified.
- ProofStep counts, citations, frozen proof texts, and primary benchmark explanations must remain unchanged.

The sole purpose is evidence collection before making the next minimal responsibility-boundary change. No new adapters or future-phase features are introduced.
