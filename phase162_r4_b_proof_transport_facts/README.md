# Phase 162 R4-B — Connected proof witness extraction

This limited first increment adds a reusable extraction function for connected suspension-transport proof steps. It does not change the public or baseline renderer, create proof steps, or guess references.

Run from the repository root after extracting the package:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase162_r4_b_proof_transport_facts\run_phase162_r4_b.ps1
```

Focused tests check that a connected witness exists for pi_5^4 and that removing the isomorphism from a copied transport step prevents extraction. They do not certify the mathematical correctness of the full proof tree or complete Phase 162 R4-B narrative formatting.
