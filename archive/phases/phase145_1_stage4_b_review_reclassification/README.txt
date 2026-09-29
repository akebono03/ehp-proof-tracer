Phase 145-1 Stage 4 - B_REVIEW Reason Reclassification

Purpose
-------
Reclassify the remaining Phase artifacts by concrete reason combinations.
This stage is audit-only. It performs no deletion and no production/test/doc
modification.

Checks
------
- Requires the audited HEAD:
  3bcb84fe687ace64f15859df1f9dcb5da7113266
- Respects Stage 1 and Stage 3 local deletions by analyzing only tracked files
  still present in the worktree.
- Separates canonical references, artifact-only references, apply scripts,
  payload, test material, unique content, and byte-identical canonical copies.
- Produces explicit A-candidates for a later human review.
- Does not automatically delete any candidate.

Outputs
-------
output/phase145_1_stage4_reclassification.csv
output/phase145_1_stage4_summary.txt

Testing
-------
No pytest is run. Repository-wide pytest remains reserved for the end of
Phase 145.
