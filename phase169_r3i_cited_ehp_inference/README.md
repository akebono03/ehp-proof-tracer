# Phase 169 R3I — Citation-Screened EHP Terminal Inference

This package connects the **existing** n=3 EHP terminal inference rules to the original, explicitly sourced statements adopted in R3H. It retains the original inference-only rules and permits distinct, narrowly scoped inference candidates whose premises are exactly matched, earlier cited `GIVEN` proof steps. The newly derived conclusions are `INFERENCE` proof steps. No source leaf or mathematical claim is synthesized.

## Scope

- Replace the complete `shared_expansion_provider()` function in `phase165_r52_r9_shared_math.py`.
- Insert the complete new `expand_cited_ehp_terminal_goal()` function in `phase165_r14_r5_ehp_connection.py`, immediately before `audit_ehp_connection()`.
- Keep `build_shared_typed_bridge()` and `phase169_r3h_source_registry.py` unchanged.
- Keep the existing `expand_registered_ehp_terminal_goal()` and all `toda_rules.py` factories unchanged.
- No imports at module scope are changed; local imports appear in each complete function.
- No project documentation, Web renderer or legacy tests are modified.

The guarded installer accepts either an applied but uncommitted R3H state over reviewed Git blob `628395c31025828c645f5641536913c56afafcb3`, or a directly committed R3H state whose parent contains that blob. It refuses any unexpected edit or historical rule revision.

## Execution on Windows PowerShell

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r3i_cited_ehp_inference.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3i_cited_ehp_inference\run.ps1"
```

The runner performs guarded installation, focused pytest, and a live proof-frontier audit. On failure, it restores both patched production modules to their precise R3H state. It does not run the full pytest suite.

## Required result

`R3I_FOCUSED_PYTEST_EXIT_CODE=0`, `R3I_AUDIT_EXIT_CODE=0`, and `R3I_COMPLETE`.

The audit reports the observed `pi_5^3` search status without assuming it is complete. The terminal claims have to be **derived** from authentic earlier source leaves, not merely enumerated as proposals. Full-suite regression tests remain deferred until the end of Phase 169.
