# Phase 162 R4-B3: Remove dedicated text-generation shortcut

This package removes only the Phase 162 R4-B3 dedicated-transport entry branch from `toda_group_proof_narrative_renderer.py`. It does not invent citations, alter proof steps, or change the public renderer. The dedicated transport module is left on disk but is no longer used by the common entry point.

The old R4-B3 test file expects the removed branch and will need a later update after reference selection and statement rendering are repaired. The existing generic renderer may still generate incomplete or overly symbolic prose; inspect the resulting Markdown rather than treating this rollback as final narrative acceptance.

Run `run_phase162_r4_b3_reference_correction.ps1` from the repository root. It applies the guarded correction, runs three focused regression tests, and prints the derived common-renderer output for inspection.
