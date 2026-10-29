# Phase 171 R2J-R4-R2 — Triple-Eta Generator Image Replay

This is a **read-only**, source-positioned replay of the typed generator suspension

`E(eta_2 o eta_3 o eta_4) = eta_3 o eta_4 o eta_5`.

It reuses existing composition-suspension and cited eta-definition inference rules. The pi_5^2 database row specifies the *target of the search*, never a proved premise. The separately screened Toda (5.3) double relation identifies the required target expression but is not admitted into the image's proof ancestry.

A successful replay is reported as `IMAGE_REPLAY=INFERRED`; a missing inference returns `IMAGE_REPLAY=UNFINISHED` with unresolved typed goals in `output/audit.json`. Both outcomes preserve the distinction between an inference candidate and a completed proof. Neither outcome proves the order-four presentation of pi_6^3.

## Files and scope

New files: `audit.py`, `tests/test_audit.py`, `run.ps1`, this `README.md`, `監査仕様.md`, `CODE_FULL_JA.md`, and package `__init__.py` files. Existing repository production files and tests are unchanged. No `GIVEN` is introduced. No full pytest suite is run.

## Running in Windows PowerShell

Extract the archive into the existing repository root, keeping the directory `phase171_r2j_r4_r2_generator_image_replay`. The earlier `phase171_r2j_r4_r1_extension_frontier_audit` package from R4-R1 must already be present.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r2_generator_image_replay\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r2_generator_image_replay\run.ps1"
```

The preflight checks the `develop` branch without switching branches. Focused pytest runs with the cache provider disabled. The replay reports its evidence without assuming success.
