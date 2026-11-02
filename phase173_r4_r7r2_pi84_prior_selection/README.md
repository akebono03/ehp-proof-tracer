# Phase 173 R4-R7R2 — Exact pi_8^4 Prior Selection

This package makes one narrowly scoped source-context change for the isolated Toda Proposition 4.4 proof of `pi_8^4`. It does **not** connect the new proof to the ordinary public Group query, modify the EHP solver, relax inference guards, assign publication metadata, or change the existing `pi_7^4` proof.

## Reviewed source

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`
- Reviewed commit: `f83f45f50739eebe179a16fd127b45a019a262ab`
- Modified tracked file: `phase173_r4_r7_source_first_rule/source.py`
- Modified function: the complete `screened_source_first_context` function; imports and all other module-level code are preserved.
- New package: `phase173_r4_r7r2_pi84_prior_selection`, containing a guarded installer, a full replacement file, the complete function, focused tests, a verification script and this documentation.

## Diagnosed failure

The `pi_8^4` root has four premises. All four are found by the existing solver. But the first group input (`pi_7^3`) is resolved as a directly screened `GIVEN` from Proposition 5.8, not as the explicitly authorized DB-prior `GIVEN` required by the guarded Toda Proposition 4.4 inference rule. The original Toda Proposition 5.8 includes both `pi_7^3` and the `pi_8^4` goal. Accepting any direct fixed step at this boundary would weaken the proof-source contract.

## Exact behavior

Only for the checked `pi_8^4` target, after the existing source-first screen:

1. Recheck that the concrete `pi_7^3` database relation is eligible as an earlier prior for this exact target.
2. Require exactly one direct fixed-source link for the same relation, with the registered source locator `Proposition 5.8`, a valid publication position, an exact relation and an empty-premise `GIVEN` step.
3. Exclude only that link from this isolated proof context, without deleting or modifying its reference or assertion in the registry.
4. Allow the *existing* recursive search to adopt the independently rechecked, explicitly labeled DB prior for `pi_7^3`. The inference rule's DB verification is unchanged.

If any reviewed condition differs, decline the context rather than guessing. The `pi_9^4`, `pi_10^4`, and `pi_7^4` routes remain unchanged.

## Run

Extract the archive into the repository root. From PowerShell in that directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r7r2_pi84_prior_selection\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r7r2_pi84_prior_selection\run.ps1"
```

The DryRun validates the exact HEAD, reviewed tracked blobs, unchanged worktree, and fixed replacement payload; it does not modify tracked source. The normal run installs the single function change, runs focused pytest only, reruns all three isolated searches and the existing `pi_7^4` public regression verifier.

The normal run intentionally leaves a **single tracked modification** (`phase173_r4_r7_source_first_rule/source.py`) for user review and commit. No automatic Git commit or push is performed. After installation, the guarded installer may be run again without repeating the change. If the original Git HEAD changes, execution refuses until reviewed again.

## Completion contract

Expect `PHASE173_R4_R7R2_FOCUSED_PYTEST=PASS`, complete/certified isolated searches with zero open goals for `pi_8^4`, `pi_9^4` and `pi_10^4`, and `PHASE173_R4_R7R2_PI74_REGRESSION=PASS`. These are **isolated** proofs, not automatically published Web proofs. Full-suite pytest is deferred until Phase 173 closeout.
