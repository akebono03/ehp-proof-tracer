Phase 145-2 Archive Implementation Resume R2

R2 fixes only the Resume R1 working-tree preflight.

Problem in R1
-------------
A normal staged rename is reported by git status as:

R  old/path -> archive/phases/new/path

R1 split that line into old/new paths but incorrectly required the old source
path itself to be under archive/phases/. That rejected the valid partial
Phase 145-2 moves created by the first implementation.

R2 repair
---------
For rename rows:
- the old path must belong to the exact Stage 1 audited artifact population;
- the new path must be inside the allowed Phase 145-2 archive/package boundary.

For non-rename rows, the existing Phase 145-2 boundary remains enforced.

No production code, canonical test, historical artifact content, or archive
policy is changed.

After the resume completes, the runner performs canonical Python syntax
preflight and the repository-wide pytest final gate.
