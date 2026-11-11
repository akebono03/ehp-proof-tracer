# EHP Proof Tracer — Phase 174 R62

This is a read-only audit of three existing source-attribution policies in the common proof narrative renderer. It verifies their distinct conditions, gives fixture-only counterexamples to an unconditional "cite every ancestor" rewrite, and reruns the two certified public proof regressions. The audit does not modify production modules, mathematics, existing tests or the global documentation.

## Run on Windows

Unzip `R62.zip` in the existing EHP Proof Tracer repository root, then execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r62_attribution_policy_boundary_audit\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r62_attribution_policy_boundary_audit\run.ps1
```

`run.ps1` runs focused tests only; it does not run the full suite. Its strict source guard checks the exact reviewed Git blob hashes and tolerates whole-file CRLF/LF differences. The local Git HEAD is reported but not used as a brittle equality gate. The full audit writes a JSON report outside the repository, under the user's local application data directory.

The result is a policy-boundary decision, **not** proof that every individual rendered sentence is cited optimally. Later work must supply precise sentence-to-ProofStep binding before merging citation-selection algorithms.
