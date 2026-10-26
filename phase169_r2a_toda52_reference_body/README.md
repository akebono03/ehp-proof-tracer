# Phase 169 R2A — Toda (5.2) reference-body projection

## Scope

This guarded package changes **only** the registered-source sentence projection for the already-adopted `Toda52UniversalStatement`. The canonical backward search, trust screening, group structure data, source records, proof tree, Narrative Model, and Web renderer are untouched.

The real `pi_4^2` search is checked before and after installation. It must have three ProofSteps, including a typed, explicitly linked `(5.2)` GIVEN. A citation inferred only from a rule name is insufficient.

## Files

- `phase168_r3_37c_reference_projection.py`: the only production file to be replaced; full, final version in `full_files/`.
- `project_reference_bodies()`: the only changed production function; complete replacement in `full_functions/`.
- The module's top-level imports do not change. An import of `Toda52UniversalStatement` is added inside the changed function.
- `tests/test_phase169_r2a_toda52_reference_body.py`: new complete focused test module, run from the extracted package. Existing tests are not edited.
- `audit.py`, `apply.py`, and `run.ps1`: read/verify, guarded copy with backup, and focused checks.

No other project documentation is modified in this subphase.

## Windows PowerShell

Extract this archive into the repository root, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase169_r2a_toda52_reference_body\run.ps1"
```

## Guardrails

The installer refuses unexpected source content, preserving unrecognized local changes. It keeps the original bytes in `output/phase168_r3_37c_reference_projection.py.before` and can restore them:

```powershell
python -B ".\phase169_r2a_toda52_reference_body\apply.py" restore
```

Focused tests and a live citation audit run after installation. The full pytest suite is **not** run before phase closeout. This change does not assert that the `pi_5^3` proof is complete; that is a separate Phase 169 step.
