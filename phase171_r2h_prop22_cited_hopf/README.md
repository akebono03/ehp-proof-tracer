# Phase 171 R2H — Cited Toda Proposition 2.2 Right-Hopf Derivation

This package registers the **source-verified general right-Hopf formula** from the adopted Toda Chapter II transcription and connects a narrowly typed two-step inference to the shared backward-search provider. It **does not** prove the group structure of `pi_6^3` or identify `eta_6` with `E(eta_5)`.

The source is archived as `toda:tex:ch2:0009` with reviewed SHA-256 `5560fe950f06dea97bd152bc97dd29661576697a7d7e58b41c938f0b3e373146`, publication position 3700, and locator `Proposition 2.2`. The original printed edition has not been independently verified.

## Changed production scope

- `phase165_r52_r9_shared_math.py`: complete functions `build_shared_typed_bridge` and `shared_expansion_provider` are affected; two guarded insertions attach the new cited source and proposal provider. There is no import-section change.
- New `phase171_r2h_prop22_cited_hopf/source.py`: complete source verification and typed inference functions. No existing rule or test is removed.
- `phase168_r2_8_3_generator_identity/identity.py` and all R2G work are left unchanged.

## Usage

Unzip the package at the repository root. Run `run.ps1 -DryRun`, followed by `run.ps1` from PowerShell. The runner checks the reviewed shared-source blob, backs it up under `%LOCALAPPDATA%\EHPProofTracerRecovery`, applies the narrow edit, runs focused pytest, and audits the resulting proof tree. It never runs the repository-wide test suite.

`output/build_shared_typed_bridge_FULL.py` and `output/shared_expansion_provider_FULL.py` are emitted by the installer after application, containing the complete actual replacement functions. The source module, installer, audit, test functions and PowerShell source are also included in `CHANGED_CODE_FULL_JA.md`.

## Intended proof scope

The screened general formula is `GIVEN`. Its concrete specialization `H(alpha o E beta) = H(alpha) o E beta` is `INFERENCE`. Substituting an independently screened `H(alpha)=beta` yields `H(alpha o E beta)=beta o E beta` as a second `INFERENCE`. No target group presentation is promoted to a source assertion.

The later identity `eta_6=E eta_5`, EHP exactness, order-four extension, and generator conclusion remain separate obligations for future R2H follow-up or R2I.
