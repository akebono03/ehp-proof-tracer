# Phase 160-R11

Apply the same public generator canonicalization used by Narrative output to Group query Result and Group proof Conclusion.

## Scope

Only public rendering is changed.

Internal semantic expressions remain unchanged:

- `Composition(eta_n, eta_(n+1))`
- `Composition(nu_n, nu_(n+3))`

Public group displays use canonical notation:

- consecutive eta compositions become `eta_n^r`
- `nu_n nu_(n+3)` becomes `nu_n^2`

This affects:

- Group query Result
- Group proof Conclusion
- other uses of the public `render_toda_group_structure_latex()` renderer

The raw `render_toda_expression_latex()` renderer is intentionally unchanged so derivation formulas can still expose expanded compositions when mathematically useful.

No tests are added or run in this package, following the current Phase 160 closure instruction.
