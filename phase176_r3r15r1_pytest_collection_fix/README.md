# Phase 176 R3R15R1: Pytest Collection Fix

This patch changes only the Phase 176 R3R15 PowerShell runner. The original runner collected two separate `test_provider.py` files within a single pytest invocation and failed with an import-file-mismatch collection error.

The patched runner runs the same four focused test files in separate pytest processes, preserving pytest's existing import behavior. It checks each exit code and stops on failure. The audit and mathematical inference code are unchanged, and no production provider is registered.

Extract this archive at the repository root with `Expand-Archive -Force`. The patch replaces `phase176_r3r15_shared_extra_provider_probe/run.ps1` from the earlier R3R15 package. Then run the same runner first with `-DryRun` and then normally. Tests use `-p no:cacheprovider`; the full suite is not run.

The isolated probe's PASS does not certify the completion of the group proof.
