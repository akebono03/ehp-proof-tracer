# Phase 169 R3N1: test import correction

Repair the single missing `eta` import in the focused R3N test fixture. No production behavior is changed. The bundled runner delegates to the existing guarded R3N pipeline; full-suite pytest is not run.
