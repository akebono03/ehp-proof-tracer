Phase 154-R5 Fix1 Diagnostic

Purpose
-------
Diagnose why graph-backed Reference linkage does not fire for pi11_4.

Production changes
------------------
none

What is printed
---------------
- body immediately before linkage
- Reference entries after root-reference exclusion
- Reference numbers and markers
- statement lines
- whether the neutral marker exists
- source steps used for linkage
- all descendants from those source steps
- descendant distance
- whether the descendant remains inside the Reference source frontier
- whether the descendant is the root
- generic semantic rendering
- whether that exact rendering exists in the body

This isolates whether the failure is caused by:
1. marker numbering
2. missing source steps
3. graph traversal
4. root exclusion
5. renderer-string mismatch
6. consumer already being transformed in the body

No pytest is run here because the previous run already established:
- 31 existing/focused tests pass
- only the two new R5 linkage expectations fail

Full suite remains reserved for the end of Phase 154.
