# Phase 165 R6-2 R4-R8 — Canonical Scalar Specialization Deduplication

Install using `run.ps1` from the EHP Proof Tracer repository root. This patch narrowly deduplicates two independently implemented scalar-specialization routes only when they have the same exact cited `GIVEN` ProofStep and the generic typed scalar substitution checker confirms the goal. Other valid derivations remain distinct.

`installed_function_full.py.txt` is generated after installation for a complete view of the changed canonical function. A `.r4_r8_before.bak` backup is written prior to modification. The full suite is not run.
