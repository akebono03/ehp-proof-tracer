# EHP Proof Tracer — Phase 176 R3R27R1

This package isolates the **second** equation of Toda (5.5), namely the universal relation $4\nu_n=\eta_n^3$ for $n\ge5$, as a source-verified typed theorem. The reviewed chapter-V transcript explicitly defines $\eta_n^3=\eta_n\circ\eta_{n+1}\circ\eta_{n+2}$.

The existing public source for the **first** equation $2\nu_n=E^{n-3}\nu'$ remains unchanged. The new registration is isolated: it is **not yet merged into the public shared source registry or public backward-search provider**. A guarded backward expansion requires a separately inferred $\nu$-family member and the two source facts (Toda (5.5) and the general $\eta$ notation). A candidate is not a proof certificate.

## Installation and execution

Extract the ZIP at the repository root on `develop`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r27r1_toda55_quadruple_isolated\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r27r1_toda55_quadruple_isolated\run.ps1
```

The resulting report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r27r1_toda55_quadruple_isolated\report.json`.

The package creates only a new folder, does not modify existing public code, does not add a direct group-result GIVEN, does not claim a complete proof of $\pi_8^3$, and does not run the full pytest suite.
