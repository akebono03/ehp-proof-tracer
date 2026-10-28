# Phase 169 R10EC-R1: Align a cyclic non-compression test

This package corrects **only a test precondition** in the original R10EC bundle. The existing test incorrectly assumes that the current search for `pi_5^4` is complete. The previously verified R10A cyclic `pi_10^8` case is complete and serves the same negative test purpose: a direct-sum-only projection must return `None` for a cyclic group.

No proof search, mathematics, inference logic, production code, or renderer is changed by this adapter. On success it invokes the original R10EC runner, which performs the production renderer patch and its focused tests and audits.

The package checks the Git branch, a reviewed commit ancestor, the renderer Git blob, and exact SHA-256 hashes of the original test and original R10EC runner. It produces the fully replaceable updated test file, full updated imports, and full updated test function under `output/`. Failure rolls back this package's test change; the original R10EC runner independently rolls back any production renderer change.

Extract both R10EC and this R1 package at the root of the checkout, then execute `phase169_r10ecr1_cyclic_test_alignment/run.ps1` with Windows PowerShell. No full pytest suite is run.
