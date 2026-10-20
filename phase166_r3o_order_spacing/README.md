# Phase 166 R3-O: Spaced statement ordering

This package migrates the 108 source reference positions in the Phase 163 manifest from 1–108 to 100–10800, converts any existing manifest component order to 100-spaced integers, and updates the common bridge to normalize pre-existing typed component positions. It preserves source identifiers, mathematical content, inference rules and the normal Web proof selection route. It does not yet insert a new foundational identity or relocate the eta-family definition.

Run `run.ps1` from the repository root. The runner prints the full modified Python functions and executes five targeted tests only. Backups are placed under `phase166_r3o_order_spacing_backups`. Run once only; a second run intentionally refuses to rescale the manifest.
