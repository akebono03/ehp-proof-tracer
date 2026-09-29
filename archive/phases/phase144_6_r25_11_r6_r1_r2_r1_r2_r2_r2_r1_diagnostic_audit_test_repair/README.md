# Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R2-R1 Diagnostic Audit Test Repair

## Current objective

Phase 144-6 currently needs to locate the historical commit where the retained
six-group selected contribution population was exactly 190. The current
population is 192.

The historical locator reached commit
`a2d9a4922bb728494d01ece912595aca93b835a6`, where the required foundation
exists, but temporary worktree creation failed.

The R2-R2 diagnostic audit was prepared to identify that Git worktree failure.
Its own focused test stopped before the diagnostic ran because the test searched
for the substring `git worktree prune`, which also occurs in the harmless
status message:

`No git worktree prune was run.`

## Scope

This repair changes only the complete audit-only test file:

`test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r2.py`

Production changes: none.

Diagnostic PowerShell changes: none.

Historical locator changes: none.

Population cache changes: none.

Existing project test changes: none.

## Test repair

The destructive-cleanup test now inspects executable lines. It ignores comments
and `Write-Host` status messages, then rejects an actual `git worktree prune`
command or a metadata-directory `Remove-Item` command.

The safety status messages remain explicitly required.

## Runner

The runner:

1. replaces the audit-only test;
2. verifies the unchanged diagnostic PowerShell still parses;
3. runs only the five focused diagnostic tests;
4. if they pass, immediately runs the existing worktree diagnostic for
   `a2d9a4922bb728494d01ece912595aca93b835a6`.

No full project pytest is run.

## Completion condition

The five focused tests pass and Sections A-I of the existing diagnostic execute,
revealing the native Git worktree-add result without pruning or manually
deleting Git worktree metadata.
