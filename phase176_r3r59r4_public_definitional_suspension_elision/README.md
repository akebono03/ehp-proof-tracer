# Phase 176 R3R59R4 — Public Definitional Suspension Elision

Connect the verified R3R59R3 display-only projection after the finite cyclic lift projection. The mathematical proof, search, registry, and partial renderer are unchanged. Expected complete narrative: 21 to 19 body rows, 62 proof steps, 51 inference steps, 11 GIVEN steps, 10 citations, no open goals.

## Exact replacements

The `*_FULL.py.txt` files contain complete replacement functions; the `*_BEFORE.py.txt` files preserve their exact previous versions. `apply.py` accepts only the pinned prior source or the exact applied source, preserves line endings, refuses unknown bytes and partial patches, and checks the historical preflight against inverse-verified bytes. The five existing test files are changed only to use a scoped previous-stage context. Historical stand-alone audit runners retain their original stage-specific pins and expectations; they are not current public acceptance gates.

## Run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r59r4_public_definitional_suspension_elision\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r59r4_public_definitional_suspension_elision\run.ps1
```

Only focused pytest groups run (38 expected tests). No full suite, no commit or push. The final audit observes the actual trusted Web render, compares it with the isolated projection and the disabled-hook baseline, checks exactly two removed rows and two citation-prefix changes, and preserves the proof model and partial view. Reports are written outside the repository under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r59r4_public_definitional_suspension_elision/`.

Expected gate: `PASS_R3R59R4_PUBLIC_DEFINITIONAL_SUSPENSION_ELISION_CONNECTED`.
