Phase 144-6-R5-15P-R1
=======================

Mapper-shape compatibility fix.

Failure cause
-------------
The first 15P apply script searched for a mapper fragment using
"block.role is ... MAP_PROPERTY".

The actual 15M mapper first assigns:

  role = block.role

and then compares:

  role is ... MAP_PROPERTY

Therefore the fixed-string anchor did not exist.

R1 change
---------
The R1 apply script no longer patches around a formatting-sensitive mapper
fragment. It locates the complete function boundary of:

  _contribution_for_premise_block

and replaces that whole function with the 15P version.

The enum extension is idempotent, so R1 is safe if the failed first apply
already inserted the three enum members before stopping.

Production mapping
------------------
EXACTNESS  -> ESTABLISH_EXACTNESS
DEFINITION -> ESTABLISH_DEFINITION
MEMBERSHIP -> ESTABLISH_MEMBERSHIP

No statement class, n/k, or inference-rule name is used.

Changed project files
---------------------
- toda_group_proof_narrative_evidence_contributions.py
  - complete TodaGroupProofNarrativeEvidenceContribution enum is extended
  - complete _contribution_for_premise_block function is replaced
- tests/test_phase144_6_r5_15p_evidence_contribution_vocabulary.py
  - new focused tests

Boundary
--------
R4 visibility, renderer, CLI, Web, ProofStep, InferenceRule, and
TodaProofEdge are unchanged.
No full pytest is run before the end of Phase 144.
