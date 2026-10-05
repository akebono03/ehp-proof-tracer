Phase 158-R5-5d
================

Purpose
-------

Run a generic public-sequence cross-audit without changing production code.

This phase does NOT encode any fixed number of groups as an architecture
contract.  The current historical audit corpus is only:

  n = 2..15
  k = 0..7
  Web Narrative depth = 2

Generic diagnostics
-------------------

1. Visible Argument intervals owned by unrelated Arguments should not cross.
   Nested parent/child Argument intervals are allowed.

2. Standalone transition prose such as "以上より," or "したがって,"
   must not dangle at the end of the proof or immediately before another
   standalone transition.

3. Repeated visible Argument conclusions are recorded for classification.
   They are findings, not automatically production defects.

4. The root target must remain before one terminal QED marker "□".

Important boundary
------------------

A finding is diagnostic.

Do NOT modify production code until a finding is classified against:

- nested Argument ownership,
- renderer suppression / deduplication,
- generic-rendering equivalence,
- deliberate restatement required by proof flow.

Files added by this package
---------------------------

- audit_phase158_r5_5d.py
- test_phase158_r5_5d.py
- run_phase158_r5_5d.ps1
- README.txt

Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.

Output
------

audit_output/
  summary.txt
  groups.csv
  argument_interval_findings.csv
  transition_findings.csv
  duplicate_conclusion_findings.csv
  target_qed_findings.csv
  exceptions.csv
  contexts/*.txt

Result interpretation
---------------------

PASS:
  No finding and no exception.

FINDINGS:
  One or more diagnostic findings were recorded. Classify them before
  changing production code.

EXCEPTIONS:
  Rendering/audit exception occurred. Resolve the audit execution problem
  before interpreting sequence findings.
