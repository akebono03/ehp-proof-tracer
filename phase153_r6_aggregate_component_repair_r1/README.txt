Phase 153-R6 Aggregate Component Repair R1
==========================================

Reason for repair
-----------------
The first R6 implementation successfully selected one Reference boundary
ProofStep for pi_6^2 / Proposition 5.6, but that ProofStep itself was an
aggregate statement containing several group relations.

Observed focused-test result:

1 failed, 13 passed

The remaining failure showed that one selected statement still rendered:

pi_5^2
pi_6^3
pi_7^4
pi_8^5
pi_(n+3)^n

together.

Repair rule
-----------
Do not add a Proposition 5.6-specific branch.

For a selected aggregate Reference statement:

1. inspect relation-valued components;
2. extract each component's top-level group generator(s);
3. inspect external consumer conclusions of the aggregate ProofStep;
4. if exactly one component has a top-level generator actually contained in
   an external consumer conclusion, render only that component;
5. if the component is not uniquely determined, keep the existing aggregate
   rendering.

For pi_6^2, the external conclusion contains nu-prime as the right factor of
eta_2 composed with nu-prime, so the unique consumed component is:

pi_6^3 = Z/4{nu-prime}

Production change
-----------------
toda_group_proof_narrative_contribution_renderer.py

Added helpers:
- _phase153_r6_nested_value_contains()
- _phase153_r6_group_relation_generators()
- _phase153_r6_reference_aggregate_component()
- _phase153_r6_render_reference_statement()

Modified function:
- _toda_group_proof_narrative_reference_statement_lines_by_number()

No change is made to:
- theorem definitions,
- proof graph construction,
- Phase 153-R5 root exclusion,
- n=2-specific logic,
- proof-body prose.

How to run
----------
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase153_r6_aggregate_component_repair_r1" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase153_r6_aggregate_component_repair_r1.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase153_r6_aggregate_component_repair_r1\run_phase153_r6_aggregate_component_repair_r1.ps1"

Completion conditions
---------------------
- R5 tests remain green.
- Original R6 tests become green.
- New aggregate-component test becomes green.
- pi_6^2 / Proposition 5.6 renders exactly one statement.
- That statement contains pi_6^3.
- It does not contain pi_5^2, pi_7^4, pi_8^5, or the stable family relation.
- Representative audit passes.
- Full pytest is not run until the end of the Phase.
