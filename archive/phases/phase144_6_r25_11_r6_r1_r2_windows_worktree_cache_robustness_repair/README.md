# Phase 144-6 R25-11-R6-R1-R2 Windows Worktree/Cache Robustness Repair

## Scope

This is an audit-runner-only robustness repair for Windows and Dropbox file
locking.

Production changes: none.

Existing project test changes: none.

The retained historical target remains selected total 190.

## Changed audit files

### `locate_historical_190.ps1`

The whole audit script is replaced.

Changes:

- adds bounded retry/backoff for transient file-system operations;
- disables interactive Git terminal prompting while creating or removing the
  temporary worktree;
- retries temporary worktree removal and pruning;
- retries population-cache reads and writes;
- updates the cache through a temporary file followed by replacement;
- checks whether the retained R5-18 foundation exists at a commit with
  `git cat-file -e` before creating a worktree;
- preserves existing cached measurements;
- preserves the six-group collector and expected total 190.

### `test_phase144_6_r25_11_r6_r1_r2.py`

New audit-only focused tests for:

- expected total 190;
- foundation prefiltering;
- worktree retry/noninteractive behavior;
- cache retry/replacement behavior;
- unchanged six-group collector boundary.

## Performance

Old commits without the R5-18 foundation are now classified without creating a
temporary worktree. This reduces worktree churn substantially.

Previously completed population-cache rows are reused.

## Completion conditions

R25-11-R6-R1-R2 is complete when:

1. the repaired PowerShell script passes parser preflight;
2. focused audit-runner tests pass;
3. historical localization resumes without interactive worktree deletion
   prompts or immediate cache-lock failure;
4. an exact selected-total-190 commit is reported, or the candidate set is
   exhausted cleanly.

No production repair is made here.

No full pytest is run.
