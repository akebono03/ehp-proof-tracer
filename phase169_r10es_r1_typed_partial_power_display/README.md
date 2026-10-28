# Phase 169 R10ES-R1 — Typed Partial Composition Power Rendering

This package makes the existing public Toda expression renderer print a typed consecutive power inside a longer, mixed composition. For instance, it renders `ν₃₀∘ν₃₃∘κ̄₃₆` as `\nu_{30}^{2}\bar{\kappa}_{36}` without changing the underlying Composition tree.

The implementation changes only `render_toda_expression_latex()` in `toda_human_readable_renderer.py`. Existing imports, other functions, proofs, references, source registries and inference rules are unchanged. The complete replacement function is included in `full_functions/render_toda_expression_latex.py`.

The patch refuses to run unless the branch is `develop`, the HEAD is the inspected `f94d8bff28692e5a2b293e7cbbb654e89284e1ba`, and the source Git blob matches the recorded identity. A local tracked change also blocks the operation. If a limited test or the live audit fails, the original source file is restored from the per-run backup.

## Windows PowerShell

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10es_r1_typed_partial_power_display.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10es_r1_typed_partial_power_display\run.ps1"
git status -sb
```

The focused tests cover typed partial powers, rejections of malformed type information, earlier whole-family power rendering, and previous direct-sum proof rendering. The live audit verifies completed proofs for stems 26, 14, 16 and 9 and replays the trust boundary. The full pytest suite is deliberately not run.

No mathematical conclusion is inferred by this presentation change; no `GIVEN` or proof rule is added.
