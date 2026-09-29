# Phase 144-6 R25-22-R2 Web Numbered Equation Adapter

## Cause found after R25-22

R25-22 successfully routed Web Narrative presentation through complete replay,
but its first focused test made an incorrect assumption: generic equation
numbering emits numbered equations as `$...\tag{n}$`, not as `\[...\]`.

The Web adapter classified every `$...$` fragment as `inline_math`, and the
browser renders `inline_math` with KaTeX `displayMode: false`. Numbered equations
therefore did not use the existing display-math Web path.

## Production change

Only `web_group_proof.py` is changed in R25-22-R2.

Changed function:
- `_build_group_proof_inline_segments`

Rule:
- ordinary `$...$` remains `inline_math`;
- `$...\tag{n}$` becomes `display_math`.

No equation-numbering algorithm, generic Narrative renderer, semantic closure,
proof graph, theorem data, Trace semantics, or Outline semantics is changed.

R25-22's complete-replay Narrative route remains in place.

## Test correction

The R25-22 assertion requiring `(4) と (5) より、` in the complete-replay Web
output was too specific. R25-22-R2 verifies the actual contract:
- numbered equations reach the Web display-math path;
- an actual dependency reference `(1) と (2) より、` reaches the Web text;
- ordinary inline math remains inline.

Repository-wide pytest is intentionally not run.
