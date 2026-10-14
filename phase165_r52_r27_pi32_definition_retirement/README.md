# Phase 165 R52-R27: Retire two pi3^2-specific inference rules

This package removes the legacy eta2 definition and Hopf-relation inference factories, their active bootstrap/probe calls, and their static applicability metadata. It retains typed statements and generic backward-search inference rules.

The Proposition 5.1 bootstrap already uses the new typed shared search for pi3^2. This package changes its remaining Hopf-relation lookup to the existing Phase 50 premise steps rather than recreating or asserting a new mathematical fact. This is a compatibility change, **not** a certification of the Phase 50 source provenance. Full retirement of the legacy bootstrap is outside this step.

Run `run.ps1` in a Windows PowerShell session from the repository folder. The installer validates all affected files before writing, saves a backup for each changed file, and writes its full replacement of `_build_prop51_step` to `audit_output/MODIFIED_FUNCTION.md`. It is safe to run again after a successful installation. A failed validation stops without modifying any file.

Only focused tests run; full pytest is postponed to the end of Phase 165.
