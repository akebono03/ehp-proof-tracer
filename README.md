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
  and an explicitly supplied sequence of `ProofStep` objects
* exact premise-count matching for explicitly supplied inference-rule premises
* premise candidate search over an existing collection of proof steps
* first-match premise selection
* distinct-step assignment for multiple premise patterns
* detection of missing premise candidates
* support for premise-free inference rules
* inference-rule applicability checks over available proof steps
* applicable-rule search over a collection of inference rules
* preservation of inference-rule input order during applicable-rule search
* support for multiple simultaneously applicable inference rules
* structured `InferenceMatch` objects containing an applicable rule and
  its selected premises
* single-rule structured match search
* collection-level structured match search
* preservation of premise-pattern order in structured matches
* explicit distinction between no match and a successful premise-free match
* input normalization for single and multiple inference rules
* optional conclusion builders attached to `InferenceRule`
* separation of inference matching from inference application
* conversion of a single `InferenceMatch` into a derived `ProofStep`
* preservation of matched premises as dependencies of the derived step
* preservation of the applied `InferenceRule` on the derived step
* support for premise-free inference-rule application
* collection-level application of multiple `InferenceMatch` objects
* conversion of an `InferenceMatch` collection into multiple derived `ProofStep` objects
* preservation of `InferenceMatch` input order during collection-level application
* normalization of single, tuple, and list `InferenceMatch` input
* explicit separation between collection-level match search and collection-level application
* human-readable proof formatting

The current inference pipeline has now reached collection-level rule
application.

Individual premise matching:

```text
PremisePattern
+
ProofStep
↓
matches_premise_pattern()
↓
True / False
```

Explicit rule-premise matching:

```text
InferenceRule
+
explicit ProofStep sequence
↓
matches_inference_rule()
↓
True / False
```

Premise search:

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
matched ProofStep tuple
or
None
```

Applicability query:

```text
InferenceRule
+
available ProofSteps
↓
is_inference_rule_applicable()
↓
True / False
```

Applicable-rule search:

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
↓
applicable InferenceRule tuple
```

Single structured match:

```text
InferenceRule
+
available ProofSteps
↓
find_inference_match()
↓
InferenceMatch
or
None
```

Collection structured match:

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch tuple
```

Single rule application:

```text
InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

Collection rule application:

```text
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep tuple
```

For example, a rule requiring a given fact can be defined as:

```python
InferenceRule(
  name="given inference",
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.GIVEN,
    ),
  ),
  conclusion_builder=lambda premises: (
    "derived from "
    + premises[0].conclusion
  ),
)
```

A single match can be found and applied as:

```python
match = find_inference_match(
  rule,
  available_steps,
)

derived_step = apply_inference_match(
  match,
)
```

The resulting `ProofStep` records:

```text
conclusion
matched premises
ProofRule.INFERENCE
applied InferenceRule
```

Phase 5-23 extends the same model to multiple matches.

For example:

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

Conceptually:

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
(
  InferenceMatch(rule_a, premises_a),
  InferenceMatch(rule_b, premises_b),
)
↓
apply_inference_matches()
↓
(
  derived_step_a,
  derived_step_b,
)
```

`apply_inference_matches()` is intentionally a thin collection-level
wrapper over `apply_inference_match()`.

Conceptually:

```text
apply_inference_matches()
↓
for each InferenceMatch
↓
apply_inference_match()
↓
derived ProofStep
```

It does not duplicate:

```text
conclusion-builder validation
conclusion construction
ProofRule.INFERENCE assignment
premise preservation
InferenceRule preservation
```

Those responsibilities remain centralized in
`apply_inference_match()`.

The input order of the `InferenceMatch` collection is preserved.

For example:

```text
(
  match_b,
  match_a,
)
```

produces:

```text
(
  derived_step_b,
  derived_step_a,
)
```

This is important because `find_inference_matches()` already preserves
the input order of inference rules.

Therefore the combined path:

```text
InferenceRule order
↓
find_inference_matches()
↓
InferenceMatch order
↓
apply_inference_matches()
↓
derived ProofStep order
```

remains deterministic.

`apply_inference_matches()` accepts:

```text
single InferenceMatch
tuple of InferenceMatch
list of InferenceMatch
```

and normalizes them to a tuple.

An empty collection is valid and returns:

```text
()
```

Invalid input is rejected explicitly.

For example:

```text
non-InferenceMatch input
```

or:

```text
a tuple/list containing a non-InferenceMatch object
```

raises `TypeError`.

Collection-level matching and collection-level application remain
separate.

The current intended use is:

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

rather than combining both operations inside either function.

This preserves the distinction between:

```text
which rules match and with which premises
```

and:

```text
which already-selected matches are actually applied
```

It also allows callers to inspect, filter, prioritize, or otherwise
process the `InferenceMatch` collection before application.

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

The proof / inference layer can currently:

```text
describe premise requirements
↓
match individual ProofSteps
↓
validate explicitly supplied premise sequences
↓
search available ProofSteps for matching premises
↓
determine whether an InferenceRule is currently applicable
↓
search a collection for currently applicable InferenceRules
↓
retain each applicable rule together with its matched premises
↓
apply a single structured InferenceMatch
↓
construct a derived ProofStep
↓
apply multiple structured InferenceMatch objects
↓
construct multiple derived ProofSteps
```

The current premise search is greedy.

For each premise pattern it:

```text
scans available steps from the beginning
↓
selects the first matching unused step
↓
continues to the next pattern
```

It does not backtrack when an earlier selection prevents a later
pattern from matching.

Therefore an `InferenceMatch` currently represents:

```text
the premise assignment selected by the current greedy search
```

rather than a complete enumeration of all possible premise assignments.

The proof / inference layer does not yet automatically:

* enumerate all possible premise assignments
* backtrack over alternative premise assignments
* return multiple alternative `InferenceMatch` objects for the same rule
* rank or prioritize multiple applicable inference rules
* choose which applicable inference rules should actually be applied
* combine match search and application into a high-level inference operation
* match internal expression structures
* bind pattern variables
* substitute bound variables
* represent expression-level conclusion templates
* derive mathematical variable bindings from matched premises
* search a `RelationRepository` automatically for required relations
* add derived conclusions back into the available proof-step collection
* detect duplicate derived conclusions
* iterate inference until no new conclusions are found
* recursively construct proofs
* recursively collect proof dependencies
* construct a proof DAG
* derive E/H/P formulas from homotopy-theoretic relations

Expression-level matching remains intentionally separate.

For example, the current matcher can recognize a proof step containing:

```text
RelationType.ZERO
```

but cannot yet recognize the internal expression pattern:

```text
mα = 0
```

or bind:

```text
m = 2
α = η_3
```

A conclusion builder can inspect concrete matched `ProofStep` objects,
but the inference engine does not yet derive structured variable
bindings automatically.

Therefore the current application mechanism should be understood as:

```text
structured premise selection
+
explicit Python conclusion builder
+
single or collection-level application
```

rather than a complete symbolic inference system.

---

## Tests

Run the complete test suite with:

```powershell
python -m pytest -v
```

At the completion of Phase 5-23:

```text
354 passed in 21.65s
```

Phase 5-23 adds collection-level inference-application tests covering:

```text
multiple InferenceMatch application
derived-step order preservation
premise preservation
InferenceRule preservation
empty InferenceMatch collection
single InferenceMatch input
list input
invalid collection input
invalid InferenceMatch entries
find_inference_matches() to apply_inference_matches() integration
```

The complete test suite also includes the existing algebra, EHP,
expression, formatter, proof, repository, premise-pattern,
inference-rule matching, premise-search, applicability,
applicable-rule-search, structured-match, and single-match
application tests.

---

## Next direction

The current inference pipeline now reaches:

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep collection
```

This establishes a complete collection-level path from:

```text
available facts
+
multiple inference rules
```

to:

```text
multiple newly derived proof steps
```

while preserving the separation between matching and application.

A natural next step is a high-level operation that composes the two
existing stages:

```text
InferenceRule collection
+
available ProofSteps
↓
match
↓
apply
↓
derived ProofSteps
```

Such an API should remain a thin composition of:

```text
find_inference_matches()
```

and:

```text
apply_inference_matches()
```

rather than duplicating either responsibility.

After that, the next major transition is:

```text
available ProofSteps
+
derived ProofSteps
↓
expanded available ProofSteps
↓
search again
```

which leads toward iterative automatic inference.

Before iterative inference becomes practical, the system will also
need to address questions such as:

* how duplicate conclusions should be detected
* whether an already-known conclusion should be added again
* how rule application history should be retained
* how repeated premise-free rules should be prevented from producing
  unbounded duplicate results
* how multiple applicable rules should be prioritized
* whether derived steps should immediately become premises for other
  rules in the same inference round

Separately, general mathematical rule representation still requires:

```text
expression-level pattern
↓
variable binding
↓
substitution
↓
conclusion construction
```

Possible next steps include:

* a high-level match-and-apply API
* derived-step insertion into available facts
* duplicate conclusion detection
* inference rounds
* fixed-point iterative inference
* expression-level premise patterns
* pattern variables
* variable bindings
* substitution
* structured conclusion templates
* extending `InferenceMatch` with bindings
* alternative premise assignments
* backtracking premise search
* rule priority and rule selection
* automatic relation selection
* composition relations
* Toda brackets
* integration of derived homotopy relations with EHP map data
* recursive proof dependency collection
* proof dependency graph construction
* literature-backed automatic proof tracing

The algebra layer remains independent of these higher-level inference
mechanisms.














