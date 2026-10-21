# Phase 166 R3-AR: Exceptional Generator Notation

This ZIP updates only `toda_human_readable_renderer.py` and runs four focused tests.

The existing `_render_unicode_math_name_latex` function is replaced in full by the installer; the entire resulting function is saved as `_render_unicode_math_name_latex_full.py.txt`. It normalizes combining overbars and numeric indices following Greek letters. Other mathematics and proof searching are untouched.

Run the included `run.ps1` in PowerShell. The original renderer is backed up under `phase166_r3ar_exceptional_notation_backup`.

The test suite does not prove any group relation or inspect browser rendering. Full pytest is deferred to the phase boundary.
