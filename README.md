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
- stable-range / Freudenthal theorems
- Toda relations and Toda brackets
- Steenrod operations
- Hopf invariants
- literature-backed relations

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

Completed foundations:

1. finitely generated abelian-group calculation,
2. EHP exact-sequence calculation,
3. proof / relation representation,
4. generic fixed-point inference,
5. EHP-domain inference,
6. exact finite ORDER reasoning,
7. Suspension preservation,
8. Freudenthal stable-range reasoning,
9. composition reasoning,
10. Suspension–composition functoriality,
11. reconnection to generic equality / ZERO reasoning,
12. provenance and explicit inference-scope / termination boundaries.

Current architecture:

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

Phase 6 established:

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

Phase 7 added:

```text
ord(α)=n
↓
nα=0
↓
generic relation reasoning
```

Phase 8 added explicit `Suspension` expressions and preservation rules:

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Phase 8 also established that repeated Suspension can produce an unbounded
family of distinct conclusions, so bounded / staged execution may be required.

Phase 9 added Freudenthal / stable-range theorem reasoning:

```text
stable
→ suspension isomorphism
→ injectivity
→ equality / ZERO reflection

boundary
→ epimorphism only

outside
→ no Freudenthal-derived theorem conclusion
```

Phase 10 adds structured composition reasoning and Suspension–composition
functoriality.

The representative Phase 10 branch is:

```text
α∘β = γ
├──────────────────────────────┐
↓                              ↓
E(α∘β) = Eγ              E(α∘β) = Eα∘Eβ
└──────────────┬───────────────┘
               ↓
      equality symmetry /
         transitivity
               ↓
          Eα∘Eβ = Eγ
```

Phase 10 also verifies coexistence with:

```text
EHP zero composition
Toda zero composition
Toda nonzero composition equality
generic ZERO
generic equality reasoning
```

and preserves branch-specific provenance.

---

# Development status

- Phase 1: finite abelian-group calculations — completed
- Phase 2: structured subgroup calculations — completed
- Phase 3: quotient groups, exact sequences, extensions, and EHP inference — completed
- Phase 4: presentation-based calculations with free components — completed
- Phase 5: generic proof / inference engine foundation — completed
- Phase 6: EHP domain-inference foundation — completed
- Phase 7: element-order reasoning — completed
- Phase 8: Suspension reasoning foundation — completed
- Phase 9: Freudenthal / stable-range reasoning — completed
- Phase 10-1〜10-5: composition relation / zero-composition integration — completed
- Phase 10-6: `E(α∘β)` and composition internal structure — completed
- Phase 10-7: Suspension–composition functoriality — completed
- Phase 10-8: equality closure between `E(α∘β)` and `Eα∘Eβ` — completed
- Phase 10-9: EHP + Toda zero/nonzero + Suspension + generic reasoning representative scenario — completed
- Phase 10-10: representative provenance + termination / inference-scope regression — completed
- Phase 10: composition reasoning and Suspension–composition functoriality — completed

---

# Algebra layer

The algebra layer handles finitely generated abelian groups of the form:

```text
Z^r ⊕ finite torsion
```

The presentation-based path uses relation matrices, integer lattices, HNF / SNF,
and computes kernel / image / cokernel. Finite-group enumeration remains as a
reference implementation for small finite examples.

For:

```text
A --f--> B --g--> C
```

exactness is represented by:

```text
Im(f)=Ker(g)
```

and kept distinct from the abstract isomorphism:

```text
B / Im(f) ≅ Im(g)
```

---

# Proof / relation model

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

A ZERO fact is represented by:

```python
Relation(
  lhs=x,
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

Composition equalities are ordinary structured equality facts:

```python
Relation(
  lhs=Composition(
    left=alpha,
    right=beta,
  ),
  rhs=gamma,
  relation_type=RelationType.EQUALITY,
)
```

A `ProofStep` preserves:

```text
conclusion
premises
rule
note
inference_rule
```

This is the basis for end-to-end provenance.

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

`Composition(left, right)` represents composition structure.

`Suspension(expression)` represents expression structure only. It does not
itself decide stable range, theorem applicability, dimension validity,
normalization, or equality.

---

# Generic inference engine

The generic pipeline is:

```text
known ProofSteps
+
InferenceRules
↓
premise assignment search
↓
structured matching
↓
bindings / shared-binding consistency
↓
match guard
↓
conclusion construction
↓
candidate ProofSteps
↓
duplicate classification
↓
new ProofSteps
↓
next round
```

Termination reasons:

```text
FIXED_POINT
MAX_ROUNDS
```

`round_count` counts productive rounds.

`max_rounds` is a safety bound, not a semantic termination proof.

---

# Generic relation rules

Equality symmetry:

```text
x=y
↓
y=x
```

Equality transitivity:

```text
x=y
y=z
↓
x=z
```

Generic ZERO propagation:

```text
x=0
y=x
↓
y=0
```

EHP-derived ZERO, ORDER-derived ZERO, Suspension-derived ZERO,
Freudenthal-reflected ZERO, and Toda zero-composition ZERO all use the same
generic relation machinery.

---

# Phase 8: Suspension reasoning

Phase 8 introduced:

```text
Suspension(expression)
```

and the rules:

```text
x=y  → E(x)=E(y)
x=0  → E(x)=0
nα=0 → nE(α)=0
```

Suspension-derived facts remain ordinary generic `Relation` objects.

Repeated Suspension may produce:

```text
E(x)
E²(x)
E³(x)
...
```

so unrestricted fixed-point termination is not assumed for this rule family.

---

# Phase 9: Freudenthal / stable-range reasoning

## SuspensionMapStatement

Phase 9 introduces map-level theorem metadata:

```text
SuspensionMapStatement(
  sphere_dimension,
  stem,
)
```

This is deliberately separate from `Suspension(expression)`.

## Stable range

```text
stem <= sphere_dimension - 2
```

derives:

```text
SuspensionIsomorphismStatement
```

## Boundary range

```text
stem == sphere_dimension - 1
```

derives:

```text
SuspensionEpimorphismStatement
```

Stable and boundary rules do not overlap.

## Isomorphism → injectivity

```text
SuspensionIsomorphismStatement(E)
↓
SuspensionInjectiveStatement(E)
```

## Equality / ZERO reflection

```text
Injective(E)
+
E(x)=E(y)
↓
x=y
```

```text
Injective(E)
+
E(x)=0
↓
x=0
```

The conclusions reconnect to generic `Relation`.

---

# Phase 10: Composition reasoning

## Structured composition equality

Known composition facts are represented as ordinary equality relations over
`Composition`.

```text
α∘β = γ
```

is represented by:

```python
Relation(
  lhs=Composition(
    left=alpha,
    right=beta,
  ),
  rhs=gamma,
  relation_type=RelationType.EQUALITY,
)
```

There is no separate Phase 10 `NONZERO` relation type.

A Toda nonzero-composition fact is currently represented by an equality whose
right-hand side is a non-zero structured expression.

## Zero composition → generic ZERO

For a known composition equality:

```text
α∘β = 0
```

the rule:

```text
composition equality to zero
```

derives:

```text
Relation(
  lhs=α∘β,
  rhs=0,
  relation_type=ZERO,
)
```

This reconnects Toda zero-composition facts to the same generic ZERO layer
already used by EHP and ORDER reasoning.

## Suspension preserves composition equality

From:

```text
α∘β = γ
```

ordinary Suspension equality preservation gives:

```text
E(α∘β) = Eγ
```

No composition-specific Suspension representation is introduced.

## Suspension–composition functoriality

From a composition equality whose left side is a `Composition`:

```text
α∘β = γ
```

the Phase 10 functoriality rule derives:

```text
E(α∘β) = Eα∘Eβ
```

The right-hand side is represented structurally as:

```python
Composition(
  left=Suspension(alpha),
  right=Suspension(beta),
)
```

## Equality closure

Given:

```text
E(α∘β) = Eγ
E(α∘β) = Eα∘Eβ
```

generic equality symmetry / transitivity derive:

```text
Eα∘Eβ = Eγ
```

No Phase 10-specific transitivity rule is added.

## Representative Phase 10 integration

Phase 10-9 verifies coexistence of:

```text
EHP
+
Toda zero composition
+
Toda nonzero composition equality
+
Suspension
+
composition functoriality
+
generic ZERO / equality reasoning
```

The representative scenario confirms:

```text
EHP branch
Image + Kernel
→ Exactness
→ EHP zero composition
→ generic ZERO
```

```text
Toda zero branch
α∘β = 0
→ generic ZERO
→ generic ZERO propagation
```

```text
Toda nonzero / Suspension branch
α∘β = γ
→ E(α∘β)=Eγ
→ E(α∘β)=Eα∘Eβ
→ Eα∘Eβ=Eγ
```

All branches share the same generic proof infrastructure.

---

# Phase 10 provenance requirements

Derived steps must preserve:

```text
ProofRule.INFERENCE
premises
inference_rule
```

Representative branch separation:

```text
EHP branch:
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
generic ZERO
```

```text
Toda zero branch:
Toda α∘β = 0
↓
generic ZERO
```

```text
Toda nonzero / Suspension branch:
Toda α∘β = γ
├─→ E(α∘β)=Eγ
└─→ E(α∘β)=Eα∘Eβ
          ↓
    equality closure
          ↓
      Eα∘Eβ=Eγ
```

Unrelated branch premises must not appear in a derived step's direct premises.

---

# Phase 10 inference-scope / termination boundary

Phase 10 makes the execution-scope distinction explicit.

## Unrestricted structural closure is not assumed to terminate

Combining:

```text
suspension composition functoriality
+
equality symmetry
```

can generate increasing expression depth:

```text
E(α∘β)=Eα∘Eβ
↓ symmetry
Eα∘Eβ=E(α∘β)
↓ functoriality
E(Eα∘Eβ)=E²α∘E²β
↓
...
```

Therefore structural Suspension / functoriality rules are not assumed to form a
finite closure family.

The regression test deliberately runs this family with:

```text
max_rounds=3
```

and requires:

```text
MAX_ROUNDS
```

while also verifying the second-level functoriality conclusion and its
provenance.

## Staged execution

Phase 10 representative reasoning uses:

```text
structural stage
  Suspension preservation: explicit one round
  functoriality: explicit one round
        ↓
finite generic stage
  equality symmetry
  equality transitivity
  ZERO propagation
        ↓
FIXED_POINT
```

The finite generic closure is verified by an explicit terminal round with:

```text
new_steps == ()
```

This is an inference-scope policy, not a special-case modification of the
generic engine.

---

# Current limitations

- Duplicate identity uses ordinary Python equality; there is no theorem-aware
  canonical normalization.
- The accumulated knowledge state keeps the first accepted `ProofStep` for an
  equal conclusion; alternative applications remain in execution traces.
- Pattern matching is structured but not a fully general unification system.
- Exhaustive premise assignment can grow combinatorially; indexing / pruning /
  semi-naive evaluation are not implemented.
- Arbitrary symbolic rule families are not guaranteed to terminate.
- `max_rounds` is a safety bound, not semantic cycle detection.
- Repeated Suspension and composition functoriality can generate unbounded
  families of structurally distinct expressions.
- Automatic suspension-depth planning and automatic rule scheduling are not
  implemented.
- Canonical `E^n` normalization is not implemented.
- Composition associativity, identity, and bilinearity are not yet encoded as
  rule families.
- There is no first-class `NONZERO` relation type.
- `SuspensionMapStatement` metadata is currently supplied explicitly; it is not
  automatically extracted from arbitrary homotopy-group objects.
- `SuspensionEpimorphismStatement` is not yet connected to preimage / lifting
  reasoning.
- General inverse-map construction and unrestricted desuspension are not
  implemented.

---

# Tests

Full suite:

```powershell
python -m pytest -v
```

Phase 10 completion result:

```text
763 passed in 22.32s
```

Combined EHP / relation-rule suite:

```powershell
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

Result:

```text
61 passed in 1.94s
```

Phase 10-10 focused regressions:

```powershell
python -m pytest tests/test_ehp_rules.py::test_phase10_representative_provenance_is_preserved tests/test_ehp_rules.py::test_phase10_functoriality_scope_and_termination_boundary -v
```

Result:

```text
2 passed in 1.55s
```

Representative Phase 10 scenario:

```powershell
python -m pytest tests/test_ehp_rules.py::test_phase10_representative_ehp_toda_composition_suspension_scenario -v
```

The representative scenario is included in the full and combined suites.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history

Historical statements in the development log describe the project state at
that time.

Current behavior is defined by the latest README and design documents.

---

# Phase 10 completion boundary

Phase 10 is complete because the project now supports the following vertical
slice:

```text
structured composition equality
↓
Suspension preservation
+
Suspension–composition functoriality
↓
generic equality closure
↓
derived suspended composition equality
```

together with:

```text
EHP zero composition
Toda zero composition
Toda nonzero composition equality
generic ZERO reasoning
provenance
explicit inference scope
termination behavior
```

without modifying the generic inference engine.

Phase 10 does not include:

```text
NONZERO relation type
automatic proof of nonzeroness
composition associativity
composition identity
composition bilinearity
canonical composition normalization
canonical E^n normalization
automatic suspension-depth planning
automatic rule scheduling
semantic termination analysis
cycle detection
Toda bracket
Steenrod operations
double EHP
odd-primary-specific rule families
```

---

# Next development boundary

Phase 11 should again begin from an actual mathematical theorem family rather
than speculative generic-engine refactoring.

Candidate directions include:

- Hopf-invariant relations
- literature-backed theorem rules
- further Toda composition relations
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families
- future epimorphism / preimage reasoning

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
