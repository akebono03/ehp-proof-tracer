# Phase 166 R3-C — Connect publication order to shared search

Run at the EHP Proof Tracer repository root, after installing the Phase 166 R3-B package. The installer patches only the import section and existing `reconstruct_registered_goal` function of `phase165_r3_recursive_search.py`. A complete installed-source snapshot is written as `INSTALLED_SOURCE.py.txt`; original code is saved under `backups`.

It reuses the 108 existing publication positions from the Phase 163 manifest and connects the 23 typed references via the R3-B binding. No TeX parsing, new ordering, independent-review approval, SQL, or renderer changes are made. The order is used only for fixed-reference leaf lookup. Existing internal-proof sequencing is not modified.

Run `powershell -ExecutionPolicy Bypass -File .\phase166_r3c_ordered_search\run.ps1`.

Only the nine focused R3-C cases are executed. Do not run the full suite until the phase closes. R3-D handles the complete $\pi_3^2$ proof regression.
