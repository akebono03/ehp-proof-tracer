# Phase 168 R3-26a — Renderer Separation After R3-25a

This package requires the exact, successfully tested R3-25a renderer function. The installer verifies the complete function SHA-256 before making any changes and aborts if its version does not match. It preserves the previous renderer in a timestamped backup.

The patch extracts only the typed exactness window merging algorithm into `phase168_r3_26_exactness_projection.py`, providing `ExactnessChain` and `project_exactness_chains()`. The renderer retains type-to-prose conversion, deferred quotient wording, and Reference presentation. No original source import section, search rules, Proof Tree, or citation logic is changed.

The integration test cases verify the 4-arrow pi3^2 and 3-arrow pi4^3 chains, and the package also runs R3-23, R3-24, R3-25 and R3-25a limited regression tests. The full pytest suite must run only at the end of Phase 168.

Unzip into the repository root and execute `powershell -ExecutionPolicy Bypass -File .\phase168_r3_26a_after_r3_25a\run.ps1`.

No integration tests were run in the packaging environment. Syntax validation only.
