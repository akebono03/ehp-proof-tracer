# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R2 Worktree Creation Failure Diagnostic Audit

## Purpose

Diagnose why historical localization could not create a temporary Git worktree
for commit:

`a2d9a4922bb728494d01ece912595aca93b835a6`

This package does not repair worktree state.

## Changed files

Production changes: none.

Historical locator changes: none.

Population cache changes: none.

Existing project test changes: none.

The package contains only a standalone diagnostic PowerShell script, its
focused audit-only tests, and this README.

## Diagnostic checks

The audit reports:

- repository top-level and Git directory;
- whether the target commit object exists;
- the target commit subject;
- `git worktree list --porcelain`;
- whether the dedicated diagnostic path already exists;
- `.git/worktrees` metadata entries, including `gitdir` and `locked` files;
- one controlled `git worktree add --detach` attempt;
- exact native exit code, stdout, and stderr;
- registered worktrees after the attempt.

## Mutation boundary

The audit does not run `git worktree prune`.

It does not manually delete worktree metadata.

It does not alter the historical locator or population cache.

It uses a new dedicated path under the system temporary directory.

If the controlled worktree add succeeds, the audit removes only that
successfully-created diagnostic worktree with:

`git worktree remove --force`

If creation fails, no cleanup mutation is attempted.

## Focused pytest

Only the audit-harness test file is executed. The full project suite is not
run.

## Completion condition

The output should identify whether the failure is caused by a pre-existing
path, stale worktree registration/metadata, locking, or another Git-native
error. Repair should be deferred until this diagnostic result is reviewed.
