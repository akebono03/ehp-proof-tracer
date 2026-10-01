Phase 153-R8
============

Theme
-----
Reference-use prose normalization
(参照使用文の自然化)

Observed problem
----------------
After R7, pi_6^2 contained:

このことから、[R2]を得る。

[R2] is a Reference used by the proof. It is not a mathematical conclusion
derived by the proof body.

R8 general rule
---------------
When Reference duplicate suppression replaces a displayed mathematical
statement with [Rk]:

- if the resulting sentence treats [Rk] as something "obtained", normalize it
  to:
  [Rk]を用いる。
- if the line already contains [Rk] together with the duplicate statement,
  normalize it to the same Reference-use sentence;
- do not change ordinary non-Reference mathematical derivations ending in
  "を得る。".

Production file
---------------
toda_group_proof_narrative_contribution_renderer.py

Modified function
-----------------
suppress_toda_group_proof_narrative_reference_body_duplicates()

Imports
-------
No import changes.

Out of scope
------------
- Reference selection
- Reference granularity
- aggregate suppression
- whether [R3] should replace the current derivation through [R4]
- title-only [R1] relevance
- general Japanese prose rewriting

Those remain separate issues.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r8_reference_use_prose_normalization" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r8_reference_use_prose_normalization.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r8_reference_use_prose_normalization\run_phase153_r8_reference_use_prose_normalization.ps1"

Full pytest remains deferred until the end of Phase 153.
