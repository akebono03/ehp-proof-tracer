# Phase 173 R4-R2 — Read-Only Generalization Audit

This package inspects existing Toda (5.2) and (5.6) public proof-search routes on the reviewed GitHub `develop` commit. It does **not** patch any production file or register an additional theorem.

## CSV coordinate correction

The original audit parser refused to read the real `data/sphere.csv` at row 2: the database contains a row with `n=0`, `k=-1` before the groups in scope. The audit concerns `n>=3`, so the corrected parser validates `n` first, skips rows with `n<3`, and only then requires a nonnegative integer `k`. This matches the existing Phase 173 R1 audit's interpretation. Invalid coordinates for `n>=3` still cause an explicit refusal. No group records or mathematical rules are changed.

## Execution

From the repository root, extract the archive and invoke:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r2_generalization_audit\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r2_generalization_audit\run.ps1
```

The default `frontier` scope checks seven groups, including the previously completed `pi_7^4` regression target. The optional `-Scope n3-all` checks `n=3, k=4..33` and the three `n=4` targets. Individual workers have a configurable timeout (`-TimeoutSeconds 240` by default).

Each worker reuses `phase173_r1_nge3_audit.audit --worker`, collecting its real typed search and web narrative results. This package never interprets database group structures as mathematical axioms. Reports and worker logs are saved outside the repository to `%LOCALAPPDATA%\EHPProofTracerRecovery`.

The preflight requires the exact reviewed `develop` HEAD `e4162e013365970877658021ff3e31503d585fa2`, clean tracked files, and seven source blob identities. The remote HEAD is also checked unless `-SkipRemoteCheck` is explicitly provided. Refusal is preferable to running on unreviewed code.

`PHASE173_R4_R2_AUDIT=PASS` means that the audit itself ran successfully, **not** that all mathematical proofs completed. Consult `audit.json` for `open_goal_text`, `diagnostics`, and `search_references`. The full test suite is deferred until the end of Phase 173.
