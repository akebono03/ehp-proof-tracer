# Phase 166 R3-Q: Existing Proposition 4.2 Source Order

This package maps four previously unresolved adopted Proposition 4.2 reference IDs to the existing manifest identity `toda:Proposition 4.2`. No new publication number is introduced. Only the `REVIEWED_REFERENCE_ALIASES` dictionary in `phase166_r3l_reference_order.py` is changed.

From the repository root, extract the ZIP and execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase166_r3q_unset_reference_positions\run.ps1
```

The runner saves a timestamped backup and runs four targeted tests and the six existing pi3^2 web regression tests. On failure it restores the patched file if its checksum is unchanged. It does not run the full test suite or alter the Web search entry point.

This stage addresses known source order only. It does not assert that unified publication-order Web search is complete for pi4^3 or pi5^4. The foundational suspension and eta-family positions already registered by R3-P are preserved.
