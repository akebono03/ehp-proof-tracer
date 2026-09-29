Phase 144-6-R5-8
==================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-7 showed that R4 frontier contact is too broad: most compressed dependency
edges touch something visible. R5-8 therefore audits a stronger semantic signal.

For each compressed parent -> child Argument edge, the audit asks:

1. What is the child's existing purpose subject?
2. Does that subject occur in the parent's conclusion?
3. Does it occur in a statement retained by the parent's current R4 visible
   frontier?
4. Do parent and child have the same purpose subject?

The first two occurrence checks are reported as semantic_consumption.
Same-purpose-subject is reported separately.

Why separate these?
-------------------
Group Structure Arguments use a homotopy group as their purpose subject, while
Order and Definition Arguments normally use a homotopy element. Therefore a
useful chain may involve semantic consumption even when parent and child purpose
subjects are not equal.

Representative groups
---------------------
pi_6^3
pi_8^5
pi_10^4
pi_12^5
pi_15^8
pi_16^9

No selection rule is implemented in this package.
