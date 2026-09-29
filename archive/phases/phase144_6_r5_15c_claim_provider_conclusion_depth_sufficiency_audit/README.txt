Phase 144-6-R5-15C
====================

Audit only. No production code, tests, or project documents are modified.

Hypothesis:
  required claim/provider conclusion depth
  -> rebuild replay at that depth
  -> rebuild the complete generic Narrative pipeline
  -> verify sufficiency

Candidate depth is the maximum shortest depth of:
- required Group Structure Argument conclusion
- required final-generator Definition Argument conclusions
- required final-generator Order Argument conclusions
- required typed Transport/Integration provider steps

At candidate depth the audit rebuilds replay, presentation, semantic sidecar,
blocks, arguments, and generic multi-argument Narrative markdown.

It then compares:
- required claim signatures
- typed provider signatures
- Reference count
- equation-tag count

Primary benchmark:
  pi_6^3 full_depth=10
  desired candidate_depth=3

No n/k-specific depth rule is used.
No inference-rule-name parsing is used.
