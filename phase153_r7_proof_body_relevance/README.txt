Phase 153-R7
=============

Theme
-----
Proof-body relevance / aggregate suppression
(証明本文の関連性・集約展開抑制)

Scope
-----
R6 made the Reference section granular, but the proof body for pi_6^2 still
expanded the unused internal premises of the Proposition 5.6 aggregate.

R7 reuses the R6 aggregate-component decision and changes display only.

General rule
------------
When an aggregate Reference step has exactly one structurally consumed
component:

1. retain the premise whose conclusion is the selected component;
2. suppress sibling aggregate premises from the displayed proof body if they
   have no independent external consumer;
3. suppress the aggregate-summary finite-dimensional derivation sentence;
4. keep the Proof graph unchanged.

This rule does not branch on n=2, pi_6^2, Proposition 5.6, or nu-prime.

Changed production files
------------------------
toda_group_proof_narrative_contribution_renderer.py
toda_group_proof_narrative_renderer.py

New test
--------
tests/test_phase153_r7_proof_body_relevance.py

Expected pi_6^2 effect
----------------------
The Reference section continues to contain the consumed:

pi_6^3 = Z/4{nu-prime}

The proof body no longer expands:
- pi_5^2
- pi_7^4
- pi_8^5
- pi_(n+3)^n
- n >= 6
- the aggregate "Toda Proposition 5.6 の有限次元結果を得る" sentence

The exact wording of the remaining [R2] use is deliberately not redesigned in
this R7 package. If it remains unnatural after aggregate suppression, that is
handled as a later focused prose-normalization step.

Run
---
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r7_proof_body_relevance" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r7_proof_body_relevance.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r7_proof_body_relevance\run_phase153_r7.ps1"

Verification
------------
Focused tests include Phase 153 R5, R6, R7 and the existing structured /
production Reference regression tests.

Representative audit:
pi_4^2
pi_5^2
pi_6^2
pi_7^2
pi_8^2
pi_9^2
pi_10^6
pi_12^7

Full pytest is intentionally deferred until the end of Phase 153.
