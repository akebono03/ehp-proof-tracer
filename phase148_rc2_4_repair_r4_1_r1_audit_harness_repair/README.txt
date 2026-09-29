Phase 148 RC2-4 Repair R4.1-R1
Audit harness current-Argument-API repair

Reason
------
The original R4.1 audit used argument.body_blocks. The current
TodaGroupProofNarrativeArgument API has no body_blocks attribute.

Current API confirmed on GitHub develop:
- supporting_blocks
- conclusion_block
- child_argument_indices

The renderer's actual local body is produced separately by:
extract_toda_group_proof_narrative_argument_local_body_blocks(...)

Repair
------
Audit harness only.

The repaired ownership report distinguishes:
1. supporting:
   membership in argument.supporting_blocks
2. conclusion:
   membership in argument.conclusion_block
3. local_body:
   membership in the renderer's extracted local body

Production changes
------------------
None.

Existing production tests changed
---------------------------------
None.

Phase boundary
--------------
No production repair.
No exactness policy change.
No Narrative ordering change.
No repository-wide pytest.
