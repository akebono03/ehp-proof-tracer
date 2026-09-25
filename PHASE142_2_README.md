# Phase 142-2 package

This package contains the minimal generic NarrativeBlock renderer for Phase 142-2.

Files:
- toda_group_proof_generic_narrative_renderer.py
- tests/test_phase142_2_generic_narrative_renderer.py

The existing dedicated pi_6^3 renderer is intentionally unchanged.

## Windows PowerShell

From the EHP Proof Tracer repository root, extract this ZIP so that the two files above are placed at the repository root and under tests/.

Then run:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
python -m pytest tests/test_phase142_2_generic_narrative_renderer.py -q
```

Do not run the full test suite yet. The full suite belongs at the end of Phase 142.
