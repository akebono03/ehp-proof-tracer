# Phase 174 R3-R7-R52R2: Registry assertion ID lookup repair

The R52R1 audit progressed past proposal-comparison checks and then raised an `AttributeError` because it treated dictionary keys as `AssertionEntry` objects. This package changes the R52 audit to obtain the first actual `AssertionEntry` via `registry._assertions.values()` before reading `assertion_id`.

This patch changes only the R52 audit module and its static regression tests. It does not change production inference, source-first evidence, public Web routing, or rendering. The patch checks exact SHA-256 hashes and supports safe reruns. Run `run.ps1 -DryRun` before `run.ps1` from the unpacked repository root.

Results from the complete R52 canonical probe remain unverified until the user's Windows execution. Full-suite pytest is deferred until the end of Phase 174.
