Phase 143-75AE implementation R3

R2 successfully applied the import and semantic renderer, but wrote two
backslashes before LaTeX text instead of one.

R3 changes exactly that Phase 143-75AE renderer string:
  double-backslash text -> single-backslash text

No import, inference rule, API, or document changes are made.
The same Phase 73 tests and four focused renderer tests are run.
Full regression remains deferred until the end of Phase 143.
