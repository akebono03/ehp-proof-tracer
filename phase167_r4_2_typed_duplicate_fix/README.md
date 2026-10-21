# Phase 167 R4-2: Typed duplicate equation display

Only the existing `render_toda_group_proof_narrative_markdown()` in `toda_group_proof_narrative_renderer.py` is changed. The full resulting function is written as `modified_function_full.py.txt` at installation time. Imports are added only inside the existing function. No new renderer or public route is introduced.

The read-only audit showed two statements: `TodaEtaFamilyDefinitionStatement(index=3, iterated_suspension exponent=1)` and `GeneratorSuspension(E, eta2, eta3)`. The typed predicate matches both source and target generators. After building the original narrative, the earlier equation display is suppressed, retaining the existing `E(eta2) = eta3` line and all proof steps. Nothing is deduplicated merely because text looks similar.

Before/after full Web narratives are compared for pi3^2, pi4^3 and stable 1-stem pi5^4, pi6^5, pi7^6. The only allowed difference is removal of `\eta_{3}=E\eta_{2}.` in pi4^3; all other lines must match. The R4-1 typed internal rule suppression must already be present. Two targeted pytest tests run. On error the code is restored to its previous R4-1 state. No 2-stem and no full pytest.

Run in the repository root with `powershell -ExecutionPolicy Bypass -File ".\phase167_r4_2_typed_duplicate_fix\run.ps1"`.
