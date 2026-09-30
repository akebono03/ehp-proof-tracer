# Phase 150 RC4-7B-7 Detached Argument Rendering Audit

Audit-only package. No production files or existing tests are changed.

## Purpose

Determine whether Arguments skipped by the generic multi-Argument renderer as `DETACHED` are:

1. actually disconnected from the root proof, or
2. reachable from the root through block-level proof dependencies but missing from `child_argument_indices`.

The audit compares:

- Argument role,
- discourse role,
- root Argument,
- `child_argument_indices`,
- root child reachability,
- block-level root dependency reachability,
- transition role and source roles,
- local-body membership.

## Representative groups

- `pi_10^4` control
- `pi_12^5` primary target
- `pi_15^8` positive control
- `pi_16^9` primary target

## Classifications

- `MAIN_ARGUMENT`
- `DETACHED_BUT_ROOT_DEPENDENCY_REACHABLE`
- `DETACHED_AND_ROOT_DEPENDENCY_UNREACHABLE`

## Phase boundary

This package does not modify:

- Argument ownership,
- `child_argument_indices`,
- discourse classification,
- local-body extraction,
- transition extraction,
- renderer behavior,
- reason prose,
- group-specific renderers.

The repository-wide test suite is intentionally not run.

If detached Arguments are root-dependency reachable, the next step is a minimal production repair of either the discourse policy or the Argument handoff representation. If they are truly disconnected, ownership must be reviewed instead.
