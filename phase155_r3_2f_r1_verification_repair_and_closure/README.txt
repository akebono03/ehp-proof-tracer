Phase 155-R3-2F-r1 — verification repair and closure

Why r1 is needed
----------------
The first R3-2F removed only the stale whole-module `"pi6"` ban.
Focused regression then proved that `"nu_prime"` was also a legitimate
statement field in the current generic renderer:

`statement.nu_prime`

Therefore the old Phase 143 test contract itself was too broad.

Repair
------
The two Phase 143 hardcoding tests now parse the generic renderer with AST
and inspect control-flow conditions only:

- `if`
- `while`
- conditional expressions
- comprehension filters

The following fragments remain forbidden inside those control-flow
conditions:

- `(6, 3)`
- `nu_prime`
- `ν′`
- `Proposition 5.6`

Legitimate statement-data access and rendering are allowed, while
group/generator/reference-specific branching remains prohibited.

The two test files add `import ast`.

Closure verification
--------------------
After repairing the tests, R3-2F-r1:

1. runs the two repaired tests,
2. re-runs every R3-1 candidate base test,
3. aggregates parameterized pytest node IDs,
4. recomputes source and dependency fingerprints from the CURRENT repaired
   test sources,
5. reclassifies all 332 R3-1 candidate pairs.

Boundary
--------
- production changes: none
- existing test files changed: 2
- existing test functions changed: 2
- deleted tests: 0
- repository-wide pytest: not run
