# Phase 162 R3-2 repair1

Fix the prior installer error `Expected exactly one lower-panel label; refusing replacement`.

The previous installer searched for an embedded newline rather than the source code's escaped `\\n` string representation. The repair matches the uniquely occurring Japanese heading itself within the existing n=3, k=2 Web hook.

The upper Group proof path is unchanged. The original R3-2 integration and focused tests are retained. No full test suite is run.

Run `run_phase162_r3_2.ps1` from inside the extracted folder placed in the repository root. The installer backs up the existing integration and `web_group_proof.py` before replacement.
