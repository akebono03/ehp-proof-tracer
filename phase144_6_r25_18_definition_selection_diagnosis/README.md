# Phase 144-6 R25-18

Production code is not changed.

This single diagnosis compares only:

- depth=2 presentation + semantic closure
- full presentation + semantic closure

for pi_6^3, and prints semantic roles, dependency semantics, and argument roles.
Its sole purpose is to identify why the full presentation loses
`ESTABLISH_DEFINITION` while the depth=2 closure keeps it.
