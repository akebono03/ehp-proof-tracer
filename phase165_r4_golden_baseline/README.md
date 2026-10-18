# Phase 165 R4 — Golden Narrative Regression

This package freezes the current, locally repaired public Narrative for pi3_2 and pi4_3. It changes no production files.

## Usage

Extract the ZIP into the repository root and run `powershell -ExecutionPolicy Bypass -File ".\phase165_r4_golden_baseline\run.ps1"` from that root.

The first run captures the two JSON baselines from the currently installed implementation and verifies them. Subsequent runs compare exactly, including public Markdown and Web rendered-line structures. Existing baselines are **never rewritten**. Commit or retain the JSON baselines to preserve the contract. On an intentional approved presentation change, review the diff and explicitly remove and regenerate only the affected baseline; do not make automatic update the normal test behavior.

The first run requires the already validated Phase 165 R2 changes. It checks that the pi4_3 proof tree contains the kernel and quotient and that these facts are present and ordered in public Narrative. The check does not certify browser or KaTeX rendering. The project-wide pytest suite is not run.
