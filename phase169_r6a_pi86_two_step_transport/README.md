# Phase 169 R6A — Verified two-step suspension transport for pi_8^6

This package adds a single backward-expansion candidate for the typed pi_8^6 group goal. It connects a prior, uniquely positioned pi_6^4 group result to the certified Toda (4.5) isomorphism and two separately proved, consecutive eta-square suspension images.

It **does not** use the pi_7^5 group presentation as a prior citation, create a GIVEN step, alter Toda's stable-range condition, or change the Renderer, registered sources, or existing public APIs.

## Files

- `rule.py`: complete new functions `_two_step_eta_square_images`, `two_step_eta_square_transport_rule`, and `expand_prior_two_step_eta_square_transport`.
- `patch.py`: complete Git-blob-pinned patch, verification, and full-function export.
- `audit.py`: canonical proof, trust-boundary, Web narrative, and Reference audit.
- `tests/test_r6a_two_step_transport.py`: six focused integration/negative tests.
- `tests/test_r6a_patch_guard.py`: three patch integrity tests.
- `run.ps1`: patch, focused pytest, audit, and rollback on failure.
- `IMPLEMENTATION_JA.md`: scope, expected results, and phase boundary.

## Run

From the repository root on Windows:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r6a_pi86_two_step_transport.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r6a_pi86_two_step_transport\run.ps1"
```

The runner expects branch `develop` and the reviewed Git blob for `phase165_r52_r9_shared_math.py`. It rejects a modified provider before applying any patch.

The runner calls only focused tests. A successful audit writes `output/audit.md`, `output/audit.json`, and `output/web_narrative.md`. The complete changed production function and file are exported to `output/shared_expansion_provider_FULL.py` and `output/phase165_r52_r9_shared_math.py.FULL`. Failure after patch application restores the backed-up provider bytes.
