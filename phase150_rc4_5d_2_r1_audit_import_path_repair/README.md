# Phase 150 / RC4-5D-2-R1

Audit-harness-only repair.

The previous package launched its audit with only the repository root on
`PYTHONPATH`. Existing Phase 65 test helpers import sibling test modules by
top-level module name, so direct script execution also requires the repository
`tests` directory on `PYTHONPATH`.

This repair changes only the audit runner:

- repository root remains on `PYTHONPATH`;
- repository `tests` directory is added to `PYTHONPATH`;
- production code is unchanged;
- existing tests are unchanged;
- the semantic audit itself is unchanged.

Repository-wide tests remain deferred until the end of Phase 150.
