# Phase 169 Git Ref Conflict Recovery R1

This package diagnoses invalid Git reference files created by a Dropbox conflicted-copy operation. It makes no changes to the EHP Proof Tracer application, proof data, database, tests, or documentation.

Run `run.ps1` without arguments first from the repository root. It recursively scans the Git common directory's `refs` tree, inventories suspicious files, checks `packed-refs` separately, and displays Git reference enumeration warnings. It does not modify any file in the default mode.

After reviewing candidate paths and pausing Dropbox sync and other Git writers, run `run.ps1 -Repair`. It moves **only** invalid loose files named like `develop (...競合コピー...)` immediately within `refs/heads` or `refs/remotes/origin` to a new backup directory outside the repository. It validates the original `HEAD`, `develop`, and `origin/develop` commit IDs before and after; it rolls back if validation fails.

`NO_CONFLICT_CANDIDATE_FOUND`, `NO_CANDIDATE_BUT_GIT_REPORTS_BROKEN_REF`, or `PACKED_REFS_NEEDS_MANUAL_REVIEW` are **not** successful repairs. In those cases, inspect the printed diagnostic lines and do not use force or reset commands. The `-Repair` command does not run a Git fetch, pull, checkout or reset. Run `git fetch origin develop` manually only after successful repair.

The contained tests use throwaway Git repositories. Focused pytest is run with the cache provider disabled, so tracked `.pytest_cache` files are not updated. No full test suite is run.
