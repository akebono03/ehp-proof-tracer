# Phase 165 R6-1: Legacy entrypoint retirement

This package deletes the obsolete R37 audit entrypoint and historical R40/R41 pi3^2 replay entrypoints. Their historical tests are also deleted when present. It preserves the active typed source registry and shared backward-search entry.

The script checks imports among root-level production `.py` modules and stops if another module imports a deletion target. Deleted files are backed up under `phase165_r6_1_removed_legacy_backup/`. This is a limited, fail-closed migration, not a claim that every duplicate installer artifact or historical test in every subdirectory has been removed.

Run `run.ps1`; it runs focused pytest only. Complete Phase-level pytest is deferred. Removing the remaining pi3^2 source-support module (`phase165_r14_r35_leaf_binding.py`, etc.) must wait for active typed source registration to be disentangled.
