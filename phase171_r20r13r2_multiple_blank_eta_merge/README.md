# Phase 171 R20R13R2 — Verified η equation formatting correction

This package corrects only Markdown presentation of an already verified EHP proof.

The R20R12 narrative duplicate suppressor can remove a duplicate equation and
leave its empty paragraph separator. The R20R13 eta-combiner expected at most
one blank separator between adjacent certified equations. This package permits
multiple empty lines while refusing to jump across any nonempty proof sentence.

The expected output is one citation-tagged equation line combining
`E(η₂)=η₃`, `E(η₃²)=η₄²`, and `E(η₂³)=η₃³`.

## Installation

Extract the ZIP at the root of the existing Git worktree. Execute `run.ps1 -DryRun`
first, then `run.ps1`. The installer edits only the existing R20R13
`projection.py` file and writes full source text to its visible `output` folder.
It does not edit the renderer, mathematical inference rules, proofs, databases,
or reference records. Focused pytest and a public-proof audit run after installation.

Requires the develop branch with the reviewed R20R13 projection content and renderer hook. The installer's content checks accept later commits only when the tracked projection is identical to the reviewed version.
