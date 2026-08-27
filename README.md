# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to build a proof tracer that can explain how homotopy
groups of spheres are determined from mathematical input such as:

- EHP exact sequences
- composition relations
- element orders
- suspension relations
- Toda relations
- Toda brackets
- Steenrod operations
- Hopf invariants
- stable-range results
- known literature-backed relations

The project deliberately separates:

```text
mathematical rule / theorem
```

from:

```text
generic inference mechanism
```

and from:

```text
abelian-group calculation
```

so that each layer can evolve independently.

---

# Current status

The project has completed the foundations of:

1. finitely generated abelian-group calculation,
2. EHP exact-sequence calculation,
3. proof / relation representation,
4. a generic inference engine,
5. the first EHP domain-inference vertical slice,
6. exact finite element-order reasoning,
7. the first Suspension domain-rule family,
8. cross-domain EHP + ORDER + Suspension provenance tracing.

The current architecture is:

```text
homotopy / EHP domain rules
        ↓
generic proof / inference engine
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

Phase 5-65 is the completion point of the generic inference-engine foundation.

Phase 6 established the first EHP-domain reasoning chain:

```text
Image / Kernel facts
↓
EHP exactness
↓
EHP zero composition
↓
generic ZERO relation
↓
equality reasoning
↓
ZERO propagation
```

Phase 7 added exact finite ORDER semantics:

```text
ord(α) = n
↓
nα = 0
↓
generic equality reasoning
↓
equivalent expressions are zero
```

Phase 8 added explicit Suspension expressions and Suspension-preservation rules:

```text
x = y
↓
E(x) = E(y)
```

```text
x = 0
↓
E(x) = 0
```

and, for multiples,

```text
nα = 0
↓
nE(α) = 0
```

The Phase 8 representative scenario executes EHP-derived and ORDER-derived
reasoning in the same knowledge state, applies Suspension to both branches,
and verifies that their provenance chains remain independent.

Phase 8 also formalizes an important execution boundary:

```text
Suspension preservation
+
unrestricted fixed-point iteration
```

can generate:

```text
E(x)
E²(x)
E³(x)
...
```

as distinct conclusions.

Therefore Suspension preservation is mathematically repeatable, but is not
assumed to be fixed-point terminating under unrestricted execution.

The current policy is:

- use staged `run_inference_round()` execution when a specific Suspension
  depth is intended,
- use `max_rounds` when bounded repeated execution is intended,
- treat `MAX_ROUNDS` as a valid safety termination result,
- do not add artificial "only suspend once" guards to mathematical rules,
- do not add Suspension-specific branches to the generic engine.

---

# Development status

- Phase 1: finite abelian-group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, and EHP inference — completed
- Phase 4: presentation-based calculations with free components — completed
- Phase 5: generic proof / inference engine foundation — completed
- Phase 6: EHP domain-inference foundation — completed
- Phase 7: element-order reasoning integrated with generic relation inference — completed
- Phase 8-1: `Suspension` expression representation — completed
- Phase 8-2: Suspension preserves equality — completed
- Phase 8-3: Suspension preserves ZERO — completed
- Phase 8-4: Suspension preserves zero multiples — completed
- Phase 8-5: ORDER-derived ZERO multiple → Suspension integration — completed
- Phase 8-6: Suspension-derived equality → generic ZERO propagation — completed
- Phase 8-7: EHP-derived ZERO → Suspension integration — completed
- Phase 8-8: representative EHP + ORDER + Suspension scenario — completed
- Phase 8-9: representative provenance chain regression — completed
- Phase 8-10: Suspension termination / inference-scope boundary — completed
- Phase 8: Suspension reasoning foundation — completed

---

# Algebra layer

## Finitely generated abelian groups

The algebra layer is designed for groups of the form:

```text
Z^r ⊕ finite torsion
```

including:

```text
0
Z
Z^2
Z/2
Z/4
Z/2 ⊕ Z/4
Z ⊕ Z/2
Z ⊕ Z/4
```

The general calculation path is presentation based:

```text
group presentation
↓
relation matrix
↓
integer lattice
↓
Hermite normal form
↓
Smith normal form
↓
kernel / image / cokernel
```

Finite-group enumeration is retained as an independent reference
implementation for small finite examples.

## Exact sequences

For:

```text
A --f--> B --g--> C
```

exactness is determined through:

```text
Im(f) = Ker(g)
```

as equality of subgroups / lattices.

The abstract relationship:

```text
B / Im(f) ≅ Im(g)
```

is treated separately from exactness.

## Extensions

For finite short exact sequences:

```text
0 → A → B → C → 0
```

the project can enumerate finite abelian candidate structures for the middle
group and test whether they can occur.

---

# EHP layer

For an EHP segment:

```text
π_{n+k-1}(S^{n-1})
        --E-->
π_{n+k}(S^n)
        --H-->
π_{n+k}(S^{2n-1})
        --P-->
π_{n+k-2}(S^{n-1})
```

the project can:

- construct E, H, and P homomorphisms from data,
- calculate images and kernels,
- test exactness,
- calculate general finitely generated abelian-group structures,
- construct exact-sequence objects,
- compare quotient and image structures,
- infer finite middle-group candidates from extension data.

The algebra layer does not know the homotopy-theoretic meaning of E, H, or P.

---

# Proof / relation model

## Relation

`Relation` stores:

```text
lhs
rhs
relation_type
source
note
```

Current `RelationType` values:

```text
EQUALITY
ZERO
ORDER
```

## ORDER semantics

A concrete ORDER relation:

```text
Relation(
  lhs=α,
  rhs=n,
  relation_type=RelationType.ORDER,
)
```

means:

```text
ord(α) = n
```

where `n` is the exact positive finite additive order.

The helper:

```text
order_relation(element, order, source=None, note=None)
```

requires a positive `int`.

The current ORDER model does not represent:

- `ord(α) | n`,
- infinite order,
- automatic order calculation from group structure.

## ProofStep

A `ProofStep` records:

```text
premises
↓
rule
↓
conclusion
```

and preserves:

- its conclusion,
- explicit premise `ProofStep` objects,
- a `ProofRule`,
- an optional note,
- the concrete `InferenceRule` that generated it.

Different domain branches may share one knowledge state without sharing
premises.

---

# Expression model

Current structured expressions include:

```text
Zero
HomotopyElement
Multiple
Composition
Suspension
```

Generator helpers include:

```text
eta(n)
nu(n)
sigma(n)
```

`Suspension` is a structural expression:

```text
Suspension(expression=x)
```

and nested Suspension is allowed:

```text
Suspension(
  Suspension(x)
)
```

The expression layer does not itself decide:

- whether an expression is zero,
- whether two expressions are equal,
- whether a Suspension theorem applies,
- dimension validity,
- stable range,
- normalization or simplification.

Those remain domain-rule responsibilities.

---

# Generic inference engine

The generic inference pipeline is:

```text
known ProofSteps
+
InferenceRules
↓
premise-pattern search
↓
all valid premise assignments
↓
structured matching
↓
PatternVariable bindings
↓
shared-binding consistency
↓
InferenceMatch
↓
conclusion construction / substitution
↓
candidate ProofSteps
↓
application classification
↓
new ProofSteps
↓
next round
```

## Rule representation

`InferenceRule` can contain:

```text
name
description
premise_patterns
conclusion_builder
conclusion_pattern
match_guard
```

## Fixed-point and bounded execution

`run_inference_until_stable_with_history()` runs until either:

```text
no genuinely new conclusion is produced
```

or:

```text
max_rounds is reached
```

Termination reasons:

```text
FIXED_POINT
MAX_ROUNDS
```

`max_rounds` is a safety bound, not a proof that a symbolic rule family
terminates.

---

# Generic relation rules

## Equality symmetry

```text
x = y
↓
y = x
```

## Equality transitivity

```text
x = y
y = z
↓
x = z
```

## Generic ZERO propagation

```text
x = 0
y = x
↓
y = 0
```

This rule is expression-type independent.

EHP-derived ZERO, ORDER-derived ZERO, and Suspension-derived ZERO can all
participate in the same generic relation machinery.

---

# Phase 6: EHP domain inference foundation

Representative chain:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
Composition(H,E) = 0
↓
generic equality reasoning
↓
target = 0
```

The generic engine contains no EHP-specific theorem branch.

---

# Phase 7: element-order reasoning

Representative chain:

```text
ord(α) = n
↓
nα = 0
↓
equality closure
↓
target = nα
↓
target = 0
```

EHP-derived and ORDER-derived ZERO facts can coexist in one knowledge state
while retaining independent premise chains.

---

# Phase 8: Suspension reasoning

## Suspension expression

Phase 8 introduces:

```text
Suspension(expression)
```

as an explicit expression node.

Nested Suspension is intentionally representable.

## Suspension preserves equality

```text
x = y
↓
E(x) = E(y)
```

implemented by:

```text
suspension_preserves_equality_inference_rule()
```

## Suspension preserves ZERO

```text
x = 0
↓
E(x) = 0
```

implemented by:

```text
suspension_preserves_zero_inference_rule()
```

## Suspension preserves zero multiple

```text
nα = 0
↓
nE(α) = 0
```

implemented by:

```text
suspension_preserves_zero_multiple_inference_rule()
```

The scalar coefficient is preserved while the underlying expression is
suspended.

## Reconnection to generic reasoning

Suspension-derived EQUALITY and ZERO facts remain ordinary generic
`Relation` objects.

For example:

```text
x = y
y = 0
↓ Suspension rules
E(x) = E(y)
E(y) = 0
↓ generic ZERO propagation
E(x) = 0
```

No Suspension-specific ZERO propagation rule is required.

## EHP integration

An EHP-derived ZERO can be suspended:

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
Composition(H,E) = 0
↓
E(Composition(H,E)) = 0
```

## ORDER integration

An ORDER-derived zero multiple can be suspended:

```text
ord(α)=n
↓
nα=0
↓
nE(α)=0
```

## Representative Phase 8 scenario

The representative Phase 8 scenario runs both branches:

```text
EHP branch                         ORDER branch

Image + Kernel                    ord(α)=n
      ↓                               ↓
  Exactness                         nα=0
      ↓                               ↓
EHP zero composition             nE(α)=0
      ↓
Composition(H,E)=0
      ↓
E(Composition(H,E))=0
```

The final knowledge state contains both suspended results.

## Provenance

The representative provenance regression fixes the chains:

```text
image_step + kernel_step
↓
exactness_step
↓
zero_composition_step
↓
ehp_zero_step
↓
suspended_ehp_zero_step
```

and:

```text
order_step
↓
order_zero_step
↓
suspended_order_zero_step
```

The two chains share the inference infrastructure but do not contaminate each
other's premise lists.

---

# Suspension termination / inference-scope boundary

Suspension preservation rules are mathematically repeatable.

Therefore:

```text
x = 0
↓
E(x) = 0
↓
E²(x) = 0
↓
E³(x) = 0
↓
...
```

and analogous chains for EQUALITY and zero multiples are valid rule
applications.

Because every nested Suspension is a distinct Python conclusion, ordinary
duplicate rejection does not force this process to stop.

Consequently:

```text
Suspension preservation rules
```

are not classified as unrestricted fixed-point-safe rule families.

Current execution policy:

### Explicit one-round scope

Use:

```text
run_inference_round()
```

when only the next Suspension level is intended.

One round derives:

```text
x = 0
→
E(x) = 0
```

but not:

```text
E²(x) = 0
```

unless another Suspension round is explicitly run.

### Bounded repeated scope

Use:

```text
run_inference_until_stable_with_history(
  ...,
  max_rounds=n,
)
```

when repeated Suspension is intentionally bounded.

If new nested Suspension conclusions continue to appear, the expected
termination reason is:

```text
InferenceTerminationReason.MAX_ROUNDS
```

This is a valid safety termination result, not an error.

### No artificial domain restriction

The mathematical rule is not changed to reject an already-suspended
expression.

In particular, the project does not impose:

```text
E(x) may be suspended only once
```

because that would incorrectly weaken the theorem.

The separation is:

```text
mathematical applicability
≠
execution scope
```

---

# Phase 8 completion boundary

Phase 8 is complete because the project can now represent and execute the
first Suspension theorem family while preserving the existing architecture.

Completion means:

1. `Suspension` is a first-class structured expression.
2. nested Suspension is representable.
3. equality can be suspended.
4. ZERO can be suspended.
5. zero multiples can be suspended with coefficient preservation.
6. ORDER-derived ZERO multiples can enter Suspension reasoning.
7. Suspension-derived equalities reconnect to generic ZERO propagation.
8. EHP-derived ZERO can enter Suspension reasoning.
9. EHP + ORDER + Suspension can coexist in one representative scenario.
10. both domain branches preserve independent provenance.
11. unrestricted Suspension closure is recognized as potentially unbounded.
12. `MAX_ROUNDS` behavior is fixed by regression tests.
13. staged rule scope is fixed by regression tests.
14. no Suspension-specific branch was added to the generic engine.
15. the full regression suite passes.

Phase 8 does not implement:

- dimension validation for Suspension,
- automatic source / target homotopy-group tracking for an expression,
- Freudenthal suspension theorem,
- stable-range isomorphism / epimorphism inference,
- automatic suspension depth planning,
- canonical `E^n` notation,
- expression normalization,
- theorem-aware equality,
- inverse desuspension reasoning,
- automatic order preservation theorems beyond the explicit zero-multiple rule,
- Hopf-invariant theorem families,
- Toda composition relations,
- Toda brackets,
- Steenrod operations,
- double EHP,
- odd-primary-specific theorem families.

These remain future phases.

---

# Current limitations

## Conclusion equality

Duplicate identity still uses ordinary Python equality.

There is no canonical mathematical normalization.

## Alternative proofs

The execution trace can record multiple applications, but the knowledge state
keeps the first accepted `ProofStep` for an equal conclusion.

## Pattern-language depth

Structured relation and dataclass-statement matching is supported, but the
engine is not a fully recursive unification system over arbitrary mathematical
syntax trees.

## Unbound conclusion variables

An unbound `PatternVariable` substitutes to `None`.

Domain rules must bind all conclusion variables needed for a valid result.

## Search complexity

Exhaustive premise assignment may grow combinatorially.

The engine does not yet implement:

- indexing,
- pruning,
- memoization,
- semi-naive evaluation,
- agenda / worklist optimization,
- rule prioritization.

## Termination

Finite closure families such as equality symmetry / transitivity may terminate
through conclusion duplicate rejection.

Arbitrary rule families are not guaranteed to terminate.

Phase 8 provides a concrete example: repeated Suspension can generate an
unbounded family of distinct conclusions.

`max_rounds` remains the safety mechanism for bounded execution.

---

# Tests

Run the full project suite with:

```powershell
python -m pytest -v
```

At Phase 8 completion:

```text
721 passed in 22.16s
```

Run the relation-rule suite with:

```powershell
python -m pytest tests/test_relation_rules.py -v
```

Current verified result:

```text
28 passed
```

Run the combined EHP / relation-rule suite with:

```powershell
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

Current verified result:

```text
50 passed
```

Phase 8 termination / inference-scope regression tests:

```powershell
python -m pytest tests/test_relation_rules.py::test_suspension_preservation_rules_require_bounded_fixed_point_scope tests/test_relation_rules.py::test_suspension_reasoning_scope_is_controlled_by_active_rule_set -v
```

Current verified result:

```text
2 passed
```

---

# Documentation

- `README.md` — current project capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history

Historical statements in `development_log.md` describe the project state at
that time.

Current behavior and design boundaries are defined by the latest README and
design documents.

---

# Next development boundary

Phase 9 should again begin from an actual mathematical theorem family rather
than speculative generic-engine refactoring.

Natural candidates after Suspension foundation include:

- stable-range / Freudenthal reasoning,
- Hopf-invariant relations,
- Toda composition relations,
- literature-backed theorem rules,
- Toda brackets,
- Steenrod operations,
- double EHP,
- odd-primary-specific rule families.

The governing rule remains:

```text
new mathematical knowledge
=
new domain InferenceRule
```

and:

```text
change the generic engine
only when an actual mathematical rule
cannot be represented correctly
with the current rule language
```
