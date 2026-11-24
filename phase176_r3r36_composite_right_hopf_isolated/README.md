# Phase 176 R3R36 — Isolated Composite Right-Hopf Formula

This package extends the **typed, source-dependent, backward-search candidate** for Toda Proposition 2.2 to a **composite suspended right factor**. It does not change the existing elementary-right-factor provider, any production file, any reference, or any registered group result.

## Scope

The existing source-backed identity is

$$H(\alpha\circ E\beta)=H(\alpha)\circ E\beta.$$

The original typed provider accepts a `HomotopyElement` as $\beta$. R3R36 adds an **isolated** candidate for a typed `Composition` as $\beta$. For the current mathematical frontier, it recognizes $\beta=\eta_5\eta_6$ without registering that expression as a new source assertion.

The local substitution is conditional on two independently proved relations:

1. The cited specialization $H(\alpha\circ E\beta)=H(\alpha)\circ E\beta$.
2. A separately proved $H(\alpha)=\delta$.

No candidate is a proof. A local inference replay using screened source steps does **not** verify the shared DFS source-order gate, prove $H(\nu'\eta_6^2)$, or prove $\pi_8^3$.

## Installation and execution

Extract `EHP_Phase176_R3R36_Composite_Right_Hopf_Isolated.zip` into the existing `ehp_proof` repository root, on the `develop` branch **after R3R35**. Do not reset or discard existing local modifications.

```powershell
$script = ".\phase176_r3r36_composite_right_hopf_isolated\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R3R36 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw 'R3R36 focused run failed' }
```

The second invocation runs only focused test modules, each in a separate pytest process. It does not invoke the full test suite. Audit results are saved to:

`%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r36_composite_right_hopf_isolated\report.json`

## Scope boundary

- New files: `source.py`, `audit.py`, `run.ps1`, `tests/test_source.py`, and documentation in this isolated package.
- Existing repository files changed: **none**.
- New GIVEN facts, direct group-theorem registration, rendering changes, or special-case narratives: **none**.
- Next stage: audit a public provider connection, then verify equality transport and the actual shared proof search before making a group-theorem claim.
