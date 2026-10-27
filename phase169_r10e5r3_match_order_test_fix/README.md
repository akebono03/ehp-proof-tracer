# EHP Proof Tracer — Phase 169 R10E5-R3

This package repairs one outdated test assertion. The project's inference-matching engine matches premises by typed patterns, independent of the input order. The R10E5 composite suspension rule is correct; the previous test wrongly expected reversed input to be rejected.

Install this ZIP at the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase169_r10e5r3_match_order_test_fix\run.ps1`. The script first patches only the one test, runs the package's two focused checks, then invokes the existing R10E5 runner and its limited regression tests and audit. It does not run the full pytest suite. On failure it restores the test; the R10E5 runner restores its own production source.

This update adds no production logic and does not alter the trust boundary.
