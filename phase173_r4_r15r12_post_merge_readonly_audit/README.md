# Phase 173 R4-R15R12 Post-Merge Read-Only Audit

This ZIP is an observation-only check. It does not edit production files, run pytest, merge, commit, stash, reset, or clean the working tree.

Extract the package into the root of the `ehp-proof-tracer` local checkout, then run `phase173_r4_r15r12_post_merge_readonly_audit/run.ps1` with Windows PowerShell. The script fetches `origin/develop` and compares Git-cleaned blob hashes for the five production/test files changed by R15R12 and all files added under `phase173_r4_r15r12_reference_correction/`.

Git's fetch operation only refreshes remote-tracking metadata. Preserve the local working tree until output is reviewed. `AUDIT_R15R12_REMOTE_CONTENT=PASS` means the checked local files match the remote commit, not that the Web UI has been visually inspected.
