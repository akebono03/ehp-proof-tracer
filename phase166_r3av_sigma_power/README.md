# Phase 166 R3-AV: Sigma power display

Only the `Composition` branch of `render_toda_expression_latex()` in `toda_human_readable_renderer.py` is replaced. The installer checks for the exact previous body, saves a backup and fails without modification if the source differs.

The original typed `Composition` expression is preserved. Only consecutive, degree-compatible sigma generators are displayed with exponent notation.

Run `run.ps1` from the extracted package to install and run three targeted tests. Full pytest is not run.
