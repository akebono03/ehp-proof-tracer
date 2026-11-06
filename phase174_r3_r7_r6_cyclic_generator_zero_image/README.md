# Phase 174 R3-R7-R6: Cyclic Generator Zero-Image Audit

This package isolates a general inference for a finite-cyclic group presentation and a proved zero image of its generator. It does not register facts, change the production proof search, or declare a new completed group proof.

## Usage

From the repository root on Windows, extract the ZIP at the repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r6_cyclic_generator_zero_image\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r6_cyclic_generator_zero_image\run.ps1"
```

The script runs focused pytest groups in separate processes because historical packages have identically named test modules. It never runs the full test suite.

The audit report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r6\cyclic_generator_zero_image.json`. Preconditions include a reviewed GitHub `develop` lineage, pinned source blobs, and the previous R5 live audit report.

The underlying Toda source is an adopted transcription; the original printed edition has not been independently authenticated. A registered database group presentation is an unproved proposal until its proper proof is reconstructed.

The package is deliberately **not** wired into the shared expansion provider or Web UI. A root candidate or a source quotation does not discharge its two independent proof obligations.
