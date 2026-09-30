# Phase 150 / RC4-5B-3-R1

Minimal repair for the two focused-test failures found after RC4-5B-3.

Changes:

- add Unicode `β` -> LaTeX `\\beta` to the existing general Greek rendering table;
- update the Phase 150 RC4-5 visible-reason count test so it checks sentences
  produced by typed reasons rather than the obsolete fixed fallback sentence;
- add one focused beta-rendering regression test.

No changes are made to the reference/binding semantic model, other RC4 reason
kinds, RC5 EHP naming, or RC6 formatting.

Repository-wide tests are intentionally not run.
