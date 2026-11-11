# Phase 174 R64R2 — CRLF fixture correction

This package corrects one Windows-sensitive test fixture in the R64R1 test suite.
It does not modify any production module, mathematical rule, proof, reference, or existing API.

Extract `R64R2.zip` into the repository root, then run
`phase174_r3_r7_r64r2_crlf_fixture_test_fix/run.ps1 -DryRun`, followed by
`phase174_r3_r7_r64r2_crlf_fixture_test_fix/run.ps1`.

The installer pins three unchanged dependencies and the entire target test module.
It accepts only the reviewed old or corrected test blob. It preserves LF/CRLF and
rejects stray CR bytes, including doubled CRLF. The test suite disables pytest cache.

Full-suite pytest is intentionally excluded until the Phase closes.
