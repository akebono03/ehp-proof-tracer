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
9. reconnection of theorem conclusions to generic equality / ZERO reasoning,
10. provenance and explicit inference-scope / termination boundaries.

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

Phase 9 adds Freudenthal / stable-range theorem reasoning. The implemented
boundary is:

```text
stem <= sphere_dimension - 2
→ suspension isomorphism
→ suspension injectivity
→ equality / ZERO reflection

stem == sphere_dimension - 1
→ suspension epimorphism only

stem >= sphere_dimension
→ no Freudenthal-derived conclusion
```

The representative Phase 9 chain is:

```text
Freudenthal stable range
↓
Suspension isomorphism
↓
Suspension injectivity
↓
E(x)=E(y)  and  E(x)=0
↓
x=y        and  x=0
↓
generic equality reasoning
↓
generic ZERO propagation
↓
y=0
↓
FIXED_POINT
```

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
- Phase 9-1: `SuspensionMapStatement` — completed
- Phase 9-2: stable / boundary range judgement — completed
- Phase 9-3: stable range → suspension isomorphism — completed
- Phase 9-4: boundary range → suspension epimorphism — completed
- Phase 9-5: isomorphism → injectivity / equality reflection — completed
- Phase 9-6: injectivity → ZERO reflection — completed
- Phase 9-7: stable range → ZERO reflection fixed-point integration — completed
- Phase 9-8: representative scenario + generic reasoning + provenance — completed
- Phase 9-9: theorem boundary / inference scope / termination regression — completed
- Phase 9: Freudenthal / stable-range reasoning — completed

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

`round_count` counts productive rounds. `max_rounds` is a safety bound, not a
semantic termination proof.

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

EHP-derived ZERO, ORDER-derived ZERO, Suspension-derived ZERO, and
Freudenthal-reflected ZERO all use the same generic relation machinery.

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

## Outside range

```text
stem >= sphere_dimension
```

produces no Freudenthal-derived isomorphism / epimorphism conclusion in the
current Phase 9 rule family.

## Isomorphism → injectivity

```text
SuspensionIsomorphismStatement(E)
↓
SuspensionInjectiveStatement(E)
```

Injectivity is explicit and reusable.

## Equality reflection

```text
Injective(E)
+
E(x)=E(y)
↓
x=y
```

`E(x)=E(y)` is represented by `SuspensionMapEqualityStatement` tied to the
same suspension map. Different maps do not match.

The conclusion is ordinary generic EQUALITY.

## ZERO reflection

```text
Injective(E)
+
E(x)=0
↓
x=0
```

`E(x)=0` is represented by `SuspensionMapZeroStatement` tied to the same map.
The conclusion is ordinary generic ZERO.

## Representative fixed-point scenario

```text
stable map E
+
E(x)=E(y)
+
E(x)=0
↓
isomorphism
↓
injectivity
├───────────────┐
↓               ↓
x=y             x=0
↓
y=x
└───────┬───────┘
        ↓
       y=0
```

The final conclusion is a generic `RelationType.ZERO`, and provenance is
retained from the initial map statement to the final generic relation.

## Theorem boundary

Current formal inference scope:

```text
stable
→ isomorphism
→ injectivity
→ equality / ZERO reflection

boundary
→ epimorphism only

outside
→ no Freudenthal-derived theorem conclusion
```

Boundary epimorphism does not imply injectivity in Phase 9, so boundary
`E(x)=E(y)` / `E(x)=0` facts are not reflected.

## Termination

The current Phase 9 theorem family is a finite closure family:

```text
map
→ isomorphism / epimorphism
→ injectivity
→ reflection
```

The scope regression reaches a genuine `FIXED_POINT` after three productive
rounds.

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

Phase 9 completion result:

```text
750 passed in 22.66s
```

Phase 9 suite:

```powershell
python -m pytest tests/test_stable_rules.py -v
```

Result:

```text
29 passed in 0.11s
```

Representative Phase 9 scenario:

```powershell
python -m pytest tests/test_stable_rules.py::test_phase9_representative_stable_reflection_generic_reasoning_scenario_reaches_fixed_point -v
```

Inference-scope / termination / theorem-boundary regression:

```powershell
python -m pytest tests/test_stable_rules.py::test_phase9_inference_scope_termination_and_theorem_boundary -v
```

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 10 should again begin from an actual mathematical theorem family rather
than speculative generic-engine refactoring.

Candidate directions:

- Hopf-invariant relations
- Toda composition relations
- literature-backed theorem rules
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

and the generic engine should change only when an actual mathematical rule
cannot be represented correctly with the current rule language.
