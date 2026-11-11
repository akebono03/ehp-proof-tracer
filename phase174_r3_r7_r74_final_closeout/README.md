# Phase 174 R74 — Final Closeout Gate

This package runs the end-of-phase active pytest suite once, only after source, Git, prior evidence, documentation, and focused-test guards pass. A failure or interruption is recorded and never retried automatically.

The reviewed base is either the R73 pre-merge HEAD with exactly five unstaged R73 document edits, or the merged R73 HEAD with no tracked edits. This package does not fetch or alter Git history, the index, production proof code, or mathematical rules. It does not install any document before the full pytest suite passes.

On success it writes five complete Markdown files to `output/full_files/`, retains full originals in `output/original_files/`, creates a five-document ZIP, updates the canonical five documents, and records the suite result outside the repository under `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r74_final_closeout/`. It does not assume that a focused pytest result implies full-suite success.

Run `run.ps1 -DryRun` and then `run.ps1` using Windows PowerShell from the repository root. A prior attempt/report blocks reruns unless a verified successful report already describes the current final documents; then the script reports that it is already closed without launching tests again.
