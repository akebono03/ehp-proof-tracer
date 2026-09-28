# Phase 144-6 R12 compact argument diagnosis R2

No production changes.

R2 fixes the diagnostic import error by reusing the existing
`tests.test_phase143_19_method_evidence._method_evidence_data` helper.
The runner temporarily creates `tests/__init__.py` when needed and removes it
after execution.
