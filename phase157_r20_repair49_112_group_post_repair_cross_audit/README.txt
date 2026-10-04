Phase157-R20 repair49 — 112-group post-repair cross-audit

Purpose
-------
Audit all 112 depth-2 public Narrative outputs after repairs 42-48.

Production code changes
-----------------------
None.

pytest
------
Not run.

Scope
-----
- n = 2..15
- k = 0..7
- 112 groups
- replay depth = 2
- public Narrative renderer

Checks
------
1. Render exceptions.
2. Missing proof section / empty proof body.
3. Missing final QED marker.
4. Dangling connector lines or paragraphs.
5. Redundant generic connector immediately before [R#].
6. Exact duplicate paragraphs.
7. A normalized statement owned by exactly one presentation step but rendered
   more than once.
8. Visible direct Relation premise appearing after its visible Relation
   consumer.
9. INJECTIVE_IMAGE_ORDER reason placement:
   - all visible premises before reason;
   - reason before conclusion;
   - reason immediately adjacent to conclusion.

Important interpretation
------------------------
This is an audit, not a test suite.

A finding does not automatically mean the production rule is wrong.
Some findings may expose:
- a real general-rule regression;
- a visibility ambiguity;
- a legitimate repeated statement in different discourse roles.

Therefore repair49 reports findings by group and category rather than
modifying production code.

Output
------
- audit_output/summary.txt
- audit_output/group_summary.csv
- audit_output/findings.csv
- audit_output/exceptions.csv

Next step
---------
Classify any findings. Only confirmed general-rule defects should become the
next focused repair. If there are no material findings, proceed toward
Phase157 closure audits and the Phase-end repository-wide pytest.
