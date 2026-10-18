# Phase 165 R3 Architecture Guard

Read-only Architecture Guard for the existing typed group search and public narrative pipeline.

Run `run.ps1` from the project root after extracting this ZIP into the root. This package does not change production code, install new renderers, or add group-specific adapters.

The targeted pytest module checks the present routing contracts, including the already-known historical conditional path. The snapshot audit regenerates pi3_2 and pi4_3 twice and compares their outputs, checking kernel and first-isomorphism presentation. This **does not** establish a permanent golden baseline between code revisions; Phase 165 R4 will add that regression coverage. It also does not verify browser rendering.

Results are written to `phase165_r3_architecture_guard_results`. No full pytest is run.

## R3 test correction

Fixes only the source-coordinate mismatch in `test_no_group_specific_branch_added_to_public_adapter`: AST compare nodes now use the entire original module source, not a sliced function body. All other tests and source files are unchanged. Extract with `-Force` into the project root and invoke the included `run.ps1`. Full pytest is not run.
