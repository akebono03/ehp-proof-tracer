Phase 159 — pi_4^3 repair 2 pre-implementation audit
Argument body exposure
====================================================

Purpose
-------
The previous audit showed that several pi_4^3 support steps reach the
depth=2 semantic closure but do not appear as direct Argument support and
are absent from the public Narrative.

The current architecture intentionally distinguishes:
- direct Argument support,
- recursive Argument body,
- renderer local body,
- exactness method evidence,
- frontier-hidden steps,
- final rendered multi-Argument markdown.

This audit identifies the exact stage where the support chain disappears.

No production files or existing tests are changed.

Outputs
-------
audit_output/summary.txt
audit_output/all_blocks.csv
audit_output/argument_body_blocks.csv
audit_output/local_body_blocks.csv
audit_output/method_evidence_blocks.csv
audit_output/frontier_hidden_steps.csv
audit_output/multi_argument_markdown.txt

Completion
----------
The audit is complete when the output identifies whether the current loss
occurs in:
1. dependency/body traversal,
2. local-body selection,
3. frontier hiding,
4. body renderer suppression,
or a combination.

Repository-wide pytest is not run.
