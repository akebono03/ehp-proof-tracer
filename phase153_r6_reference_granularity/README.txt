Phase 153-R6
=============

Theme
-----
Reference granularity
(参照粒度)

Goal
----
When several ProofStep objects from the same literature Reference appear in
the proof graph, do not automatically list every internally used statement in
the Reference section.

Prefer the statements that actually cross the boundary from that literature
Reference into a different proof context.

General rule
------------
For one Reference entry:

1. Keep the Phase 153-R5 root exclusion.
2. Find candidate statements used as proof-edge premises.
3. Prefer candidates whose parent step belongs to a different literature
   Reference (or has no matching Reference).
4. These are the Reference boundary frontier.
5. If there is no boundary crossing, preserve the R5 fallback behavior.

This is structural. It does not branch on:
- n = 2
- pi_6^2
- Proposition 5.6
- nu-prime
- fixed theorem names

Production change
-----------------
File:
toda_group_proof_narrative_references.py

Function:
select_toda_group_proof_narrative_reference_statement_steps()

No other production file is changed.

Expected pi_6^2 effect
----------------------
Before R6, [R2] Proposition 5.6 could expand several statements.

After R6, the Reference section should prefer the statement that crosses from
Proposition 5.6 into the proof of pi_6^2:

pi_6^3 = Z/4{nu-prime}

without expanding unrelated Proposition 5.6 statements there.

Not included in R6
------------------
- No n=2-specific rule.
- No Reference title renumbering.
- No prose rewrite of the proof body.
- No repair of repeated phrases such as "[R2]を得る".
- No redesign of Lemma 5.7 statement rendering.
- No unrelated refactoring.
- No full pytest run.

How to run
----------
Extract this directory directly under the repository root.

PowerShell:

cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r6_reference_granularity" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r6_reference_granularity.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r6_reference_granularity\run_phase153_r6.ps1"

Completion conditions
---------------------
- All focused tests pass.
- R5 root exclusion remains green.
- pi_6^2 / Proposition 5.6 has exactly one selected Reference statement.
- That statement is the pi_6^3 result.
- Representative audit passes.
- Full pytest remains deferred until the end of the Phase.

Boundary to the next R
----------------------
R6 changes only which statements are displayed under one Reference.

It does not yet rewrite the proof-body sentences that consume [R1], [R2], etc.
