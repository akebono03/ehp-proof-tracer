# Phase 165 R52-R13 — Adopted typed literature component registration

This installation adds a generic explicit-source registration API and uses it to register the four finite-dimensional clauses of Toda Proposition 5.1. It retains the R52-R12 generic component expansion and shared backward search, and does not replay a completed proof.

## Changed files and units

- New `phase165_r52_r13_reference_registration.py`: `register_adopted_composite_reference`, `build_adopted_prop51_reference`.
- Existing `phase165_r52_r9_shared_math.py`: inside `build_shared_typed_bridge`, add the explicit source to the default tuple, without modifying the other logic.
- New `test_phase165_r52_r13_reference_registration.py`: four complete targeted tests.
- `install.py`, `run.ps1`: guarded installation and targeted tests.

The exact source claim is adopted from the user-accepted Toda Proposition 5.1 and the existing typed model. This is **not** an independent original-edition transcription audit or a proof of the claim. The generic function requires an explicit caller-supplied locator, source identity, and typed composite. It does not promote an arbitrary `INFERENCE` step to a `GIVEN` step. The symbolic `n>=3` applicability guard is still a separate future implementation; never use the symbolic higher-eta clause at an unverified `n`.

Run at repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r52_r13_reference_registration.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r13_reference_registration\run.ps1"
```

The runner executes 3 targeted test modules, not full pytest. Passing the tests confirms typed reference retrieval, not completion of the `pi_4^3` proof. The next step is general quantified specialization and common EHP goal expansion.
