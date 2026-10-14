# Phase 165 R52-R17-R1 installer fix

Fix the R17 installer to detect the existing R16 `search_shared_group_goal()` signature structurally rather than by a fixed line. This package is safe to re-run after partial installation. It retains R16 mathematics, search semantics, and prior API parameters. Run `run.ps1` at repository root. Only targeted tests are executed.
