# Phase 175 R4R12R5R2 — ZIP root correction

This package fixes the packaging error in R4R12R5R1. The previous ZIP contained an unintended `r4r12r5r1_build/` prefix, so extraction into the repository root failed to replace the existing installer. This package places all files directly under `phase175_r4r12r5_iterated_suspension_endpoints/`.

The reviewed HEAD is `9203e1a8c077320a58214bda40d9bfeb17704f58`. The R4R3 source blob pin, fail-closed tests, rule changes, and six open proof obligations are unchanged.

Extract into the repository root, run `run.ps1 -DryRun`, then run `run.ps1` without the flag. This phase only runs focused pytest.
