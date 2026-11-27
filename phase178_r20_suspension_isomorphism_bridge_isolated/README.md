# Phase 178 R20 — Isolated Suspension Isomorphism Bridge

This package adds one typed representation bridge, not a new isomorphism theorem. It reuses the existing generic `MapIsomorphism` inference from `MapInjective` and `MapSurjective` and converts a proved generic isomorphism of the same valid one-fold sphere suspension to `TodaSuspensionIsomorphismStatement`. It never creates a GIVEN or changes the shared provider.

The preflight checks the reviewed base `7390660dc6eda0364d93a29cc255d670c51c4871`, the exact R19R1 package and its two installed file changes, and the pinned dependencies. R19R1 may be committed and pushed or remain unstaged at the reviewed base. Unrelated tracked changes or staged changes are refused. The existing R19R1 code must already be installed. The only new files are this package's files.

From the repository root, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r20_suspension_isomorphism_bridge_isolated\run.ps1 -DryRun`, then repeat without `-DryRun`.

The isolated tests check valid and invalid dimensions, conditional replay of the existing generic theorem followed by the bridge, rejection of incorrect maps and unproved premises, and the real n=6 candidate frontier. Synthetic hypotheses are used only in conditional matcher tests. The historical R4C typed isomorphism tests and R19/R19R1 tests also run. No full pytest is run. A passing gate does not certify the n=6 proof or change the public search. The next phase connects the bridge to the shared provider; the zero Delta inference remains a later task.

Expected gate: `PASS_R20_ISOLATED_SUSPENSION_ISOMORPHISM_BRIDGE`.
