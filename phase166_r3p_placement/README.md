# Phase 166 R3-P: Proof-use ordering placement

This patch places the foundational suspension identity at publication position 7701 and the eta-family definition at publication position 7800, component position 300. It moves the three following Proposition 5.1 components to 400, 500, and 600, retaining existing identifiers, source descriptions, claims, links, and inference rules.

Run `run.ps1` in PowerShell from the extracted package. It is designed for a repository where Phase 166 R3-O (100-step positions) and R3-N are already applied. The patch backs up the two modified production files before writing changes. It does not run the full test suite.

The source of the eta-family definition remains its existing Chapter V transcription. This phase assigns proof-use placement, not a new literary attribution.
