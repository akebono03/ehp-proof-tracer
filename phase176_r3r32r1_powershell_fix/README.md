# Phase 176 R3R32R1 — PowerShell Join-Path Fix

This patch replaces only `phase176_r3r32_hopf_goal_frontier/run.ps1`.

## Problem

Windows PowerShell 5.1 does not accept three positional path arguments in `Join-Path`. The original runner fails after the read-only audit and before isolated pytest starts.

## Correction

Build the test path with nested `Join-Path` calls, then pass it as one argument to pytest. All other execution and error checks remain unchanged.

## Running

From the repository root, extract this ZIP with `Expand-Archive -Force`, run `run.ps1 -DryRun`, then run `run.ps1` without `-DryRun`. No full-suite pytest is performed. The patch makes no production-code, inference-rule, source-registry, or proof changes.
