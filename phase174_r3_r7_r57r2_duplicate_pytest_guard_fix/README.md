# Phase 174 R57R2 — pytest decorator repair

This package fixes a **test collection error**, not a mathematical proof rule.

The R57 installer replaced a function body without removing the original
`@pytest.mark.parametrize("n", ...)` decorator. Its replacement text accidentally
included the same decorator, causing pytest to reject the test during collection.

R57R2 removes the duplicate decorator in the installed R56 test and corrects
R57's embedded replacement template and final SHA-256 pin. It preserves the
R57 mathematical implementation, shared proof search, narrative renderer,
references and all existing proof steps.

Unzip at the EHP Proof Tracer repository root. Use `run.ps1 -DryRun`, then
`run.ps1`. The full run executes only focused tests and the original R57 public
proof audit, not the repository-wide test suite.
