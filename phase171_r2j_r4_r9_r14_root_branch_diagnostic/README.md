# Phase 171 R2J–R4–R9–R14: Read-Only Root Branch Diagnostics

This package investigates why the normal, source-screened proof search for `pi_6^3` remains partial even though a cited forward equality and its reverse can be independently reconstructed.

## Scope

- No changes to existing repository source files, classes, functions, rule registries, or proof trees.
- No additional `GIVEN` proof leaves.
- No replay of an earlier completed proof into the public search.
- No change to the Trust Boundary or Web rendering.
- No full pytest run (focused test module only).

R13 confirmed that, in one public root-search branch, the reverse equality tries to reconstruct a forward equality that is already active. This explains a failed branch, but does not establish that the cycle is the **only** reason the root remains unproved. The existing recursive search already skips `RegisteredGoalUnresolved` expansions. R14 therefore records the original resolver's exception origins and propagation rather than bypassing cycle prevention.

## Requirements

Run from the `develop` branch of `akebono03/ehp-proof-tracer`, with the reviewed R11 shared provider committed. The package verifies the exact reviewed provider blob (`10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac`) and checks that the worktree version matches HEAD after line-ending normalization. Other tracked changes are not modified.

## Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\EHP_Phase171_R2J_R4_R9_R14_ROOT_BRANCH_AUDIT_ONLY.zip" `
  -DestinationPath "." `
  -Force

powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase171_r2j_r4_r9_r14_root_branch_diagnostic\run.ps1" `
  -DryRun

powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase171_r2j_r4_r9_r14_root_branch_diagnostic\run.ps1"

git status -sb
git diff --stat
```

## Report

The runtime creates `output/audit.json` with:

- Original public status, initial open-goal role, and diagnostic.
- Number of root expansion routes and all observed candidate names/subgoal shapes.
- Counts of exceptions **originating** at `resolve`, distinguished from parent-level propagation.
- `cycle`, `no_derivation`, `ambiguous_derivations`, and other unresolved reason categories.
- `active_roles`, original candidate rule/subgoals, and accepted option count at an exception site.

`candidate_rule` is the resolver's current local expansion at the instant of the exception and may refer to the most recently attempted expansion when the exception is raised after a loop. It must not be interpreted as an authoritative proof dependency by itself.

A traceback report is observational. A cycle found in an abandoned branch is not evidence that the root would become complete if this branch were removed.

The output classification is deliberately conservative. `ROOT_PARTIAL_WITH_ZERO_DERIVATION_SUBGOALS` means some subgoals had zero verified derivations, **not** that they alone caused the root failure. Inspect `exception_events` and `provider_events` to determine the causal route before any patch.

## Validation

`python -m pytest -q -p no:cacheprovider phase171_r2j_r4_r9_r14_root_branch_diagnostic/tests/test_audit.py`

The package's Python syntax and diagnostic tracer have been checked outside the repository, but repository-dependent focused tests and live proof search must run in the actual project workspace.
