# EHP Proof Tracer

A computational tool for tracing calculations in EHP exact sequences
for unstable homotopy groups of spheres.

## Goal

The long-term goal is to build a proof tracer that explains how
homotopy groups of spheres are determined from:

* EHP exact sequences
* composition relations
* Toda brackets
* Steenrod operations
* known element orders and relations
* literature references

The current algebra layer is designed to work with finitely generated
abelian groups, including both free and torsion components.

---

## Current status

The project has progressed from finite-group enumeration to
presentation-based calculations for finitely generated abelian groups.

Groups of the form

```text
Z^r ⊕ finite torsion
```

can be handled by the same algebra layer.

The current calculation pipeline is:

```text
group presentation
↓
homomorphism matrix
↓
integer lattice
↓
Hermite / Smith normal form
↓
kernel / image / cokernel
↓
exact sequence
↓
quotient / image structure
↓
EHP exactness
```

Finite-group enumeration is retained as an independent reference
implementation for testing presentation-based calculations.

---

## Current features

### Homotopy group data

* Load homotopy groups and generators from `data/sphere.csv`
* Represent group generators and their orders
* Construct E, H, and P maps from EHP data
* Keep homotopy-theoretic generator information separate from the
  abstract abelian-group calculation layer

---

### Finitely generated abelian groups

The algebra layer supports groups such as:

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

The intended general form is

```text
Z^r ⊕ Z/d1 ⊕ ... ⊕ Z/ds.
```

---

### Homomorphisms

Homomorphisms are represented by integer matrices.

The implementation supports:

* finite → finite
* finite → free
* free → finite
* free → free
* mixed → mixed
* non-diagonal maps
* zero groups and zero maps

For a homomorphism

```text
f : G → H
```

the presentation-based algebra layer can compute:

```text
Ker(f)
Im(f)
Coker(f)
```

as abstract finitely generated abelian groups.

---

### Presentation-based calculations

General group calculations use integer presentations and lattices.

The main calculation path is:

```text
relation matrix
↓
integer lattice
↓
Hermite normal form
↓
Smith normal form
↓
abelian-group structure
```

This avoids the need to enumerate all elements when free components
such as `Z` are present.

---

### Finite-group reference calculations

For small finite abelian groups, the earlier enumeration-based
algorithms are retained.

They can explicitly compute:

* group elements
* subgroups
* quotient cosets
* kernels
* images

These algorithms are used as an independent reference implementation
for cross-checking the presentation-based calculations.

---

### Subgroups

Finite subgroups can be represented as structured objects containing:

* ambient group
* elements
* generators
* order
* abstract structure

Examples:

```text
()       -> 0
(2,)     -> Z/2
(4,)     -> Z/4
(2, 2)   -> Z/2 ⊕ Z/2
(2, 4)   -> Z/2 ⊕ Z/4
```

---

### Quotient groups

For finite groups, the program can explicitly:

* construct quotient groups
* enumerate cosets
* compute quotient-group order
* compute quotient-group structure
* verify induced quotient maps

For general finitely generated abelian groups,
quotient structures can also be computed from presentations without
enumerating cosets.

---

### Exact sequences

For

```text
A --f--> B --g--> C
```

the program can compute:

```text
Im(f)
Ker(g)
B / Im(f)
Im(g)
```

and test exactness:

```text
Im(f) = Ker(g).
```

This works for sequences containing free components.

For example,

```text
Z --×2--> Z --mod 2--> Z/2
```

is correctly detected as exact because

```text
Im(×2) = 2Z
Ker(mod 2) = 2Z.
```

The program also tracks the first-isomorphism-theorem relation

```text
B / Im(f) ≅ Im(g)
```

as an abstract group-structure relation.

Exactness and abstract group isomorphism are treated as distinct
concepts.

---

### First isomorphism theorem

For a homomorphism

```text
f : G → H
```

the finite-group layer can explicitly construct and verify

```text
G / Ker(f) ≅ Im(f).
```

The general presentation layer computes the corresponding abstract
group structures without requiring full element enumeration.

---

### Extension candidates

For a finite short exact sequence

```text
0 → A → B → C → 0
```

the middle group `B` is not necessarily uniquely determined.

For example,

```text
0 → Z/2 → B → Z/2 → 0
```

allows both

```text
Z/4
Z/2 ⊕ Z/2
```

as possible middle groups.

The program can:

* enumerate finite abelian group structures of the required order
* construct abstract candidate groups
* test whether a candidate contains a subgroup isomorphic to `A`
* test whether the corresponding quotient is isomorphic to `C`
* return valid middle-group candidates

The current extension-candidate enumeration remains focused on finite
abelian groups.

---

### EHP calculations

For an EHP segment

```text
π_{n+k-1}(S^{n-1})
        --E-->
π_{n+k}(S^n)
        --H-->
π_{n+k}(S^{2n-1})
        --P-->
π_{n+k-2}(S^{n-1})
```

the program can:

* construct the E, H, and P homomorphisms
* compute images and kernels
* check exactness
* compute general abelian-group structures
* construct exact-sequence steps
* compare quotient and image structures
* infer possible finite middle-group structures from extension data

The EHP layer delegates general exact-sequence calculations to the
algebra layer.

---

## Verified examples

### Finite EHP example: n = 3, k = 5

For

```text
π_7(S^2)
  --E-->
π_8(S^3)
  --H-->
π_8(S^5)
  --P-->
π_6(S^2)
```

the program verifies

```text
Im(E) = Ker(H)
Im(H) = Ker(P).
```

It derives

```text
π_8(S^3):
  candidate = Z/2
```

and for the Hopf target:

```text
π_8(S^5):
  candidates =
    Z/8
    Z/2 ⊕ Z/4.
```

The known value

```text
π_8(S^5) = Z/8
```

is contained in the candidate set.

---

### Noncyclic finite example: n = 11, k = 18

The program verifies exactness for an example containing larger
noncyclic finite abelian groups.

For example,

```text
π_29(S^11)
≅ Z/8 ⊕ Z/4 ⊕ Z/2.
```

The general structure API verifies relationships such as

```text
Im(E)
≅ Z/2 ⊕ Z/2 ⊕ Z/4
```

and

```text
π / Im(E)
≅ Im(H)
≅ Z/2 ⊕ Z/2.
```

---

### General exact-sequence example

The presentation layer handles sequences involving free groups.

For example,

```text
Z --×2--> Z --mod 2--> Z/2
```

is exact, while

```text
Z --×2--> Z --mod 4--> Z/4
```

is not exact.

This provides the algebraic foundation required for EHP segments
containing free components.

---

## Architecture

The project separates general algebra from homotopy-theoretic data.

```text
proof / inference layer
        ↓
homotopy / EHP data layer
        ↓
abelian group algebra
        ↓
integer linear algebra
```

### Integer linear algebra

Responsible for:

* relation matrices
* integer lattices
* Hermite normal form
* Smith normal form

This layer has no knowledge of EHP sequences or homotopy groups.

### Abelian group algebra

Responsible for:

* finitely generated abelian groups
* homomorphisms
* kernels
* images
* cokernels
* subgroups
* quotients
* exact sequences
* extensions

This layer treats `E`, `H`, and `P` simply as group homomorphisms.

### Homotopy / EHP layer

Responsible for:

* homotopy-group data
* generator names
* construction of E, H, and P
* translating EHP data into group homomorphisms

### proof / inference layer

The proof / inference layer is being developed to derive and trace
mathematical relations from sources such as:

* composition relations
* Toda brackets
* Steenrod operations
* Hopf invariants
* stable-range results
* known element orders
* literature references

The distinction is intentional:

```text
derive a mathematical relation
```

and

```text
calculate its algebraic consequences
```

are separate responsibilities.

---

## Primary components

The algebra layer is not restricted to the 2-primary component.

Groups such as

```text
Z/2
Z/4
Z/3
Z/9
```

are all handled as ordinary finitely generated abelian groups.

The distinction between:

* classical EHP
* double EHP
* 2-primary data
* odd-primary data

belongs to the homotopy/inference layers rather than the core algebra
engine.

---


## Development status

* Phase 1: finite abelian group calculations — completed
* Phase 2: structured subgroup calculations — completed
* Phase 3: quotient groups, exact sequences, extensions, and EHP inference — completed
* Phase 4: presentation-based calculations with free components — completed
* Phase 5: proof / inference foundation — in progress

Phase 5 currently supports:

* structured homotopy expressions
* mathematical relations
* relation repositories and structural relation search
* proof steps and proofs
* kernel / image / cokernel proof steps
* exactness and EHP exactness proof construction
* explicit proof dependencies through premises
* conversion of known relations into proof steps
* relation-based inference steps
* relation source and note metadata in formatted proofs
* structured literature references with author, title, year, and locator
* inference from multiple mathematical relations
* inference combining relations with existing proof steps
* structured inference-rule metadata
* explicit distinction between proof-step categories and mathematical inference rules
* premise-pattern metadata for inference rules
* premise requirements based on proof-step category, statement type, and relation type
* multiple premise patterns for a single inference rule
* machine-checkable matching between a `PremisePattern` and a `ProofStep`
* matching by proof-step category
* matching by conclusion type
* matching by relation type
* ordered matching between all premise patterns of an `InferenceRule`
  and multiple `ProofStep` objects
* exact premise-count matching for inference rules
* human-readable proof formatting

For example, an EHP exactness calculation can now be represented as:

```text
1. Im(E) ≅ 0
   [image computation]

2. Ker(H) ≅ 0
   [kernel computation]

3. Im(E) = Ker(H)
   [ehp exactness]
   Premises: 1, 2
```

Known mathematical relations can participate directly in proof
dependencies:

```text
1. 2η_3 = 0
   [relation]

2. η_3 has order dividing 2
   [relation]
   Premises: 1
```

Multiple known relations can be combined in a single inference:

```text
1. 2η_3 = 0
   [relation]

2. 2η_4 = 0
   [relation]

3. combined result
   [relation]
   Premises: 1, 2
```

The mathematical inference rule used by an inference step can also be
recorded explicitly:

```text
1. 2η_3 = 0
   [relation]

2. η_3 has order dividing 2
   [relation]
   Inference rule: zero relation implies order bound
   Premises: 1
```

This distinguishes:

```text
ProofRule
```

which describes the broad category of a proof step, from:

```text
InferenceRule
```

which describes the specific mathematical rule used to derive a
conclusion from its premises.

An inference rule can describe the kinds of premises it expects.

For example:

```python
InferenceRule(
  name=(
    "zero relation implies "
    "order bound"
  ),
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.RELATION,
      statement_type=Relation,
      relation_type=RelationType.ZERO,
    ),
  ),
)
```

describes a rule that expects a proof step satisfying:

```text
ProofRule.RELATION
+
conclusion type = Relation
+
RelationType.ZERO
```

A premise pattern can be compared directly with an actual proof step:

```python
matches_premise_pattern(
  pattern,
  step,
)
```

The matcher currently uses only the fields represented by
`PremisePattern`:

```text
proof_rule
statement_type
relation_type
```

Unspecified fields act as wildcards.

For example:

```python
PremisePattern()
```

matches any `ProofStep`, while:

```python
PremisePattern(
  proof_rule=ProofRule.RELATION,
  statement_type=Relation,
  relation_type=RelationType.ZERO,
)
```

matches only a step satisfying all three conditions.

The conditions are combined conjunctively:

```text
proof rule matches
AND
conclusion type matches
AND
relation type matches
```

when all three are specified.

A `relation_type` requirement also requires the conclusion to be a
`Relation`.

This makes premise-pattern specifications machine-checkable at the
individual proof-step level.

The entire premise specification of an inference rule can also be
checked against actual proof steps.

For example:

```python
matches_inference_rule(
  rule,
  (
    relation_step,
    given_step,
  ),
)
```

compares:

```text
rule.premise_patterns[0] ↔ relation_step
rule.premise_patterns[1] ↔ given_step
```

using `matches_premise_pattern()` for each pair.

Inference-rule premise matching is currently ordered.

Therefore:

```text
patterns:
  RELATION
  GIVEN

steps:
  RELATION
  GIVEN
```

matches, while:

```text
steps:
  GIVEN
  RELATION
```

does not.

The number of proof steps must also match the number of premise
patterns exactly.

Therefore both missing and additional premise steps cause the rule
match to fail.

A rule with:

```text
premise_patterns = ()
```

matches only an empty proof-step sequence.

This provides machine-checkable matching for a complete explicitly
supplied inference-rule premise list, while keeping automatic premise
search as a separate later concern.

Relation sources can be represented as structured literature
references.

For example:

```text
Source: Toda — H. Toda, Composition Methods in Homotopy Groups of Spheres, 1962
```

The literature reference model can store:

```text
label
author
title
year
locator
```

while relation-specific mathematical notes, inference-step notes, and
inference-rule metadata remain separate.

---

## Current limitations

Some finite-group functionality still uses explicit element or subgroup
enumeration.

In particular, extension-candidate generation currently focuses on
finite abelian groups and relatively small examples.

The presentation layer can calculate algebraic consequences of known
homomorphisms, but it does not yet derive E/H/P formulas themselves
from Toda relations, composition relations, or other homotopy-theoretic
theorems.

The current proof / inference layer can compare all declared premise
patterns of an `InferenceRule` with an explicitly supplied sequence of
`ProofStep` objects.

This matching is currently:

```text
ordered
+
position-based
+
exact in premise count
```

The proof / inference layer does not yet automatically:

* search an existing collection of proof steps for matching premises
* assign proof steps to premise patterns in arbitrary order
* enumerate alternative premise assignments
* match internal expression structures
* bind pattern variables
* construct conclusions from inference rules
* select applicable relations
* select premise proof steps automatically
* apply inference rules automatically
* recursively collect proof dependencies
* construct a proof DAG
* derive E/H/P formulas from homotopy-theoretic relations

Expression-level matching is intentionally separate from the current
proof-step-level matcher.

For example, the current matcher can recognize that a step contains a

```text
RelationType.ZERO
```

relation, but it does not yet recognize the internal pattern

```text
mα = 0
```

or bind values such as

```text
m = 2
α = η_3.
```

These belong to later proof / inference phases.

---

## Project documentation

More detailed development and design notes are kept separately:

* `docs/development_log.md` — implementation history and Phase progress
* `docs/design.md` — design decisions and mathematical/computational rationale

---

## Tests

Run the complete test suite with:

```powershell
python -m pytest -v
```

At the completion of Phase 5-17:

```text
257 passed in 20.88s
```

Phase 5-17 includes tests for:

```text
single-premise rule matching
multiple-premise rule matching
ordered premise matching
premise-count mismatch
empty-premise rules
single / tuple / list ProofStep input
invalid rule input
invalid ProofStep input
```

The complete test suite includes the existing algebra, EHP,
expression, formatter, proof, repository, and inference-pattern tests.

The development log records test-suite results at each implementation
checkpoint.

---

## Next direction

The current matching pipeline is:

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

and:

```text
InferenceRule.premise_patterns
+
explicit ProofStep sequence
↓
matches_inference_rule()
↓
True / False
```

The next useful step is to move from checking an explicitly supplied
premise sequence to finding suitable premises from a collection of
existing proof steps.

Conceptually:

```text
InferenceRule
+
available ProofSteps
↓
search for matching premises
↓
candidate premise sequence
```

This should remain separate from expression-level pattern matching.

A minimal first version should continue to use only the information
already available in `PremisePattern`:

```text
proof_rule
statement_type
relation_type
```

and should not yet introduce expression unification.

Questions for the next phase include:

```text
Should premise candidates initially be searched in rule order?

Should the first matching ProofStep be returned, or all matches?

Should one ProofStep be reusable for multiple premise patterns?

How should multiple possible premise assignments be represented?
```

The simplest next step is to search existing ProofSteps in rule order
and return an explicitly matched premise sequence without yet
introducing general unordered matching.

Possible later directions include:

* premise candidate search
* unordered multiple-premise matching
* inference-rule applicability over a proof-step collection
* expression-level relation patterns
* pattern variables and variable binding
* conclusion construction
* automatic relation selection
* automatic premise selection
* automatic inference-rule application
* composition relations
* Toda brackets
* integration of derived homotopy relations with EHP map data
* recursive proof dependency collection
* proof dependency graph construction
* literature-backed automatic proof tracing

The algebra layer remains independent of these higher-level
homotopy-theoretic inference mechanisms.








