# Phase 165 Renderer R4 Fast Migration

This package migrates the 40 R1-inventoried legacy imports without recursively parsing the repository, renames the shadowed canonical function into a preserved private callable, and removes the old compatibility package. It takes a new backup at `.phase165_renderer_r4_fast_backup` and does not touch the existing recovery backup `.phase165_renderer_r4_backup`.

Run `run.ps1` from an extracted package in the repository root. It snapshots before and after, runs focused pytest, and attempts rollback on test failure. Do not run the earlier R4 installer. Full pytest is not run.

All transformations must be reviewed against the recovered R3 state. Historical imports and regression tests are migrated because deleting the alias otherwise breaks them. The 40 R1 import records cover 40 sites across fewer files; this package does not claim to find arbitrary dynamic imports.

R4 BOM fix R1: Preflight accepts UTF-8 BOM Python files and preserves original BOM when writing migrated files. This fixes the pre-mutation SyntaxError observed in Windows. Run only after the prior R4 fast installer failed before backup creation.
