# Phase 166 R3-G: Toda (4.5) typed registry and bidirectional specialization

This package adds the **general** Toda (4.5) iterated-suspension isomorphism to the existing Unified Statement Registry. It uses the existing `Toda45IsomorphismStatement`, `TodaIteratedSuspensionMap`, `AssertionEntry`, `ProofStepLink`, and common generic specialization rule. It does not add a target-specific proof adapter or a mathematical transport rule.

Run from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3g_toda45_registry_connection.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3g_toda45_registry_connection\run.ps1"
```

## Modified files / functions

- `phase165_r52_r27_r5_literature.py`: adds `_toda45_universal_statement` and `_register_toda45`; modifies the full `build_typed_literature_bridge` function's final registration. The resulting file retains all existing classes, references, and functions.
- `phase165_r57_r20_general_specialization.py`: adds `_linear_scalar_expression` and `_bind_symbolic_constraints`; replaces the complete `specialize_typed_statement` function. Existing inference-rule construction and backward provider remain intact.
- `phase165_r52_r27_r5_typed_references/test_r5_typed_references.py`: updates existing assertions from two references to three; retains all test functions.
- `phase166_r3g_toda45_registry_connection/test_r3g.py`: four focused tests for reference provenance, forward/backward use, invalid ranges, and prevention of concrete GIVEN promotion.

`phase165_r52_r9_shared_math.py`, inference-rule registries, web renderer, and unrelated files are **not modified**. Backups are taken before installation. This does not run the entire test suite.

The installer requires the expected current production function signatures and checks Python syntax before modification. If the local tree differs from the fetched GitHub code, do not bypass a failed installation without reviewing the differences.
