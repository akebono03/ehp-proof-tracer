Phase 165 R12-R14 focused kernel proof closure.
Requires previously installed R12-R11, R12-R12, R12-R13.
No changes to production source, reference registry or prior test files.
Run run.ps1 from the EHP Proof Tracer project directory.
Audit runs BEFORE targeted pytest, so unresolved proof reports remain available.
A failed closing test is a genuine blocker, not a regression to hide.
No full pytest is run.
