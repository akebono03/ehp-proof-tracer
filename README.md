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
* high-level inference derivation through `derive_inference_steps()`
* direct derivation of multiple `ProofStep` objects from inference rules and available proof steps
* preservation of inference-rule order through the high-level derivation path
* one-round inference through `run_inference_round()`
* expansion of the available proof-step collection with newly derived proof steps
* preservation of existing available-step order during an inference round
* preservation of derived-step order during an inference round
* duplicate-aware proof-step merging through `merge_proof_steps()`
* duplicate detection based on `ProofStep.conclusion` equality
* suppression of derived conclusions that are already available
* suppression of duplicate conclusions produced by multiple rules in the same round
* preservation of the first derived proof step when multiple derived steps have the same conclusion
* idempotent repeated execution when the same derivation produces no new conclusions
* explicit separation between one-round inference and iterative fixed-point inference
* human-readable proof formatting

The current inference pipeline has low-level matching and application
APIs together with high-level derivation, merge, and one-round
execution APIs.

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

High-level derivation:

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
candidate derived ProofStep tuple
```

Duplicate-aware merge:

```text
available ProofSteps
+
derived ProofSteps
↓
merge_proof_steps()
↓
merged ProofStep tuple
```

One inference round:

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
derive candidate ProofSteps
↓
merge by conclusion equality
↓
expanded available ProofSteps
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

The lower-level search and application path remains available:

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

derived_steps = apply_inference_matches(
  matches,
)
```

The equivalent high-level derivation is:

```python
derived_steps = derive_inference_steps(
  inference_rules,
  available_steps,
)
```

Conceptually:

```text
InferenceRule collection
+
available ProofSteps
↓
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
↓
candidate derived ProofStep collection
```

`derive_inference_steps()` intentionally returns candidate derived
proof steps without removing duplicate conclusions.

This allows callers that need to inspect every applicable rule result
to continue using the derivation API independently of knowledge-state
merging.

Phase 5-26 introduces:

```python
merge_proof_steps(
  available_steps,
  derived_steps,
)
```

Conceptually:

```text
available ProofSteps
+
candidate derived ProofSteps
↓
normalize both collections
↓
collect existing conclusions
↓
scan derived ProofSteps in order
↓
already-known conclusion?
├── yes → skip
└── no  → append
↓
merged ProofStep tuple
```

The duplicate criterion is:

```python
derived_step.conclusion == known_conclusion
```

rather than full `ProofStep` equality.

Therefore differences in:

```text
premises
ProofRule
InferenceRule
note
```

do not make two entries distinct for the purpose of the merged
available knowledge state if their conclusions compare equal.

For example:

```text
available:
A
B

derived:
B
C
```

becomes:

```text
A
B
C
```

The existing `B` is preserved and the derived duplicate is skipped.

Duplicate conclusions within the derived collection are also removed.

For example:

```text
available:
A

derived:
B from rule 1
B from rule 2
```

becomes:

```text
A
B from rule 1
```

because derived proof steps are scanned in order and the first proof
step introducing a new conclusion is retained.

Thus merge ordering is:

```text
all existing available steps
↓
first occurrence of each genuinely new derived conclusion
```

Existing available-step order is preserved.

Derived-step order is preserved among conclusions that are actually
added.

Input normalization remains consistent with the existing proof APIs.

`merge_proof_steps()` accepts:

```text
single ProofStep
tuple of ProofStep
list of ProofStep
```

for both:

```text
available_steps
derived_steps
```

and returns a tuple.

Invalid inputs continue to raise `TypeError` through
`_normalize_proof_steps()`.

Phase 5-26 also changes `run_inference_round()`.

The Phase 5-25 implementation was conceptually:

```text
normalized available steps
+
derived steps
```

The Phase 5-26 implementation is:

```python
normalized_steps = (
  _normalize_proof_steps(
    available_steps,
    "available_steps",
  )
)

derived_steps = derive_inference_steps(
  inference_rules,
  normalized_steps,
)

return merge_proof_steps(
  normalized_steps,
  derived_steps,
)
```

Therefore:

```text
run_inference_round()
↓
derive_inference_steps()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
duplicate-safe expanded knowledge state
```

The matching semantics of a round have not changed.

All matches for one round are still computed from the proof steps
available at the beginning of that round.

Newly derived proof steps are not used as premises during the same
round.

For example:

```text
rule A:
given fact
→ intermediate fact

rule B:
intermediate fact
→ final fact
```

with only the given fact initially available produces:

```text
round 1:
given fact
intermediate fact
```

The final fact still requires a later round.

Phase 5-26 changes only how candidate derived proof steps are merged
into the available knowledge state.

An important new property is that repeated execution of the same
derivation can now be idempotent.

For example:

```text
available:
A

rule:
A → B
```

after the first round:

```text
A
B
```

Running the same round again derives `B` as a candidate again, but
`merge_proof_steps()` recognizes that conclusion as already known.

The result remains:

```text
A
B
```

rather than:

```text
A
B
B
```

This removes the simplest duplicate-growth problem that existed in
Phase 5-25.

Premise-free rules also benefit from this behavior.

A premise-free rule may remain applicable in every round, but if it
produces the same conclusion each time, the repeated conclusion is not
added again to the available knowledge state.

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
↓
derive candidate ProofSteps in one high-level call
↓
merge candidate ProofSteps into available ProofSteps
↓
remove already-known conclusions
↓
remove duplicate derived conclusions
↓
perform one duplicate-safe inference round
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

The duplicate semantics introduced in Phase 5-26 are intentionally
simple.

The current knowledge-state merge criterion is:

```text
same conclusion
=
duplicate for merge purposes
```

This means that:

```text
same conclusion
+
different premises
```

or:

```text
same conclusion
+
different inference rules
```

are not both retained in the merged available-step collection.

For example:

```text
A, B → C
```

and:

```text
D, E → C
```

may produce two distinct candidate `ProofStep` objects through
`derive_inference_steps()`.

However, when they are merged into the available knowledge state,
only the first occurrence of conclusion `C` is retained.

This is a knowledge-state policy, not yet a complete alternative-proof
management system.

The current inference engine therefore does not yet automatically:

* enumerate all possible premise assignments
* backtrack over alternative premise assignments
* return multiple alternative `InferenceMatch` objects for one rule
* rank or prioritize multiple applicable inference rules
* preserve multiple proofs of the same conclusion in the merged knowledge state
* maintain a dedicated alternative-proof repository
* identify the genuinely new steps as a separate return value
* report how many new conclusions were added in a round
* automatically repeat inference rounds
* iterate until no new conclusions are found
* explicitly detect a fixed point
* record inference-round numbers
* retain inference-round history
* maintain rule-application history
* distinguish repeated applications from new applications
* detect inference cycles
* match internal expression structures
* bind pattern variables
* substitute bound variables
* represent expression-level conclusion templates
* derive mathematical variable bindings from matched premises
* search a `RelationRepository` automatically for required relations
* recursively construct proofs
* recursively collect proof dependencies
* construct a proof DAG
* derive E/H/P formulas from homotopy-theoretic relations

The merge implementation currently checks conclusion equality by
ordinary Python equality:

```python
step.conclusion == known_conclusion
```

It does not yet provide a separate notion of:

```text
mathematical equivalence
```

or:

```text
canonicalized conclusion
```

Therefore two mathematically equivalent conclusions are treated as
duplicates only if their Python equality comparison reports equality.

Expression-level matching and mathematical normalization remain
separate future concerns.

The current inference mechanism should therefore be understood as:

```text
structured ProofStep-level premise matching
+
explicit Python conclusion builder
+
candidate derivation
+
conclusion-equality duplicate filtering
+
single-round knowledge-state expansion
```

rather than a complete symbolic or fixed-point inference system.

---

## Tests

Run the complete test suite with:

```powershell
python -m pytest -v
```

The inference-rule pattern test file can be run separately with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-26:

```text
tests/test_inference_rule_pattern.py:
166 passed in 3.27s

complete test suite:
390 passed
```

Phase 5-25 completed with:

```text
376 passed
```

so Phase 5-26 adds 14 tests.

Phase 5-26 adds tests covering:

```text
basic ProofStep merge
new derived-step insertion
existing-conclusion suppression
duplicate-derived-conclusion suppression
available-step order preservation
new-step order preservation
empty available collection
empty derived collection
single ProofStep input
list input
invalid available-step input
invalid derived-step input
existing conclusion suppression through run_inference_round()
same derived conclusion from multiple rules
idempotent repeated round for the same derivation
```

The complete test suite also includes the existing algebra, EHP,
expression, formatter, proof, repository, premise-pattern,
inference-rule matching, premise-search, applicability,
applicable-rule-search, structured-match, inference-application,
high-level derivation, and one-round inference tests.

No regression was observed from introducing duplicate-aware merging.

---

## Next direction

The current inference pipeline is now:

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
derive_inference_steps()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
duplicate-safe expanded ProofSteps
```

This means the proof engine can now safely represent:

```text
knowledge state before a round
↓
inference
↓
candidate facts
↓
duplicate filtering
↓
knowledge state after the round
```

without repeatedly appending an already-known conclusion.

The next useful distinction is between:

```text
all candidate derived ProofSteps
```

and:

```text
ProofSteps that are genuinely new in this round
```

Currently:

```python
merge_proof_steps(
  available_steps,
  derived_steps,
)
```

returns only the full merged knowledge state.

It does not separately expose:

```text
newly added ProofSteps
```

For iterative inference, this information is useful because:

```text
no newly added ProofSteps
```

provides a natural fixed-point termination condition.

A natural next step is therefore to introduce an operation such as:

```text
available ProofSteps
+
candidate derived ProofSteps
↓
new-step detection
↓
genuinely new ProofSteps
```

Conceptually:

```text
derive candidate steps
↓
remove conclusions already known
↓
remove duplicate candidate conclusions
↓
return only genuinely new steps
```

This can then support:

```text
round
↓
new steps?
├── yes → perform another round
└── no  → fixed point
```

A possible next API direction is:

```python
find_new_proof_steps(
  available_steps,
  derived_steps,
)
```

or an equivalent helper separating:

```text
novelty detection
```

from:

```text
collection merge
```

Once genuinely new steps can be obtained directly, the next stage can
introduce fixed-point iterative inference.

Conceptually:

```text
available ProofSteps
↓
derive candidate ProofSteps
↓
find genuinely new ProofSteps
↓
merge
↓
new steps exist?
├── yes → next round
└── no  → terminate
```

This would move the system from:

```text
duplicate-safe one-round inference
```

to:

```text
fixed-point iterative inference
```

while keeping termination semantics explicit.

Separately, richer proof semantics will eventually require deciding how
to preserve:

```text
same conclusion
+
different proof
```

because Phase 5-26 intentionally keeps only the first such proof in the
merged available knowledge state.

Possible future directions therefore include:

* explicit new-step detection
* merge result objects containing both merged and newly added steps
* fixed-point iterative inference
* round count and termination information
* inference-round history
* rule-application history
* alternative-proof storage
* distinction between fact identity and proof identity
* mathematical conclusion canonicalization
* mathematical equivalence beyond Python equality
* alternative premise assignments
* backtracking premise search
* rule priority and rule selection
* expression-level premise patterns
* pattern variables
* variable bindings
* substitution
* structured conclusion templates
* automatic relation selection
* composition relations
* Toda brackets
* integration of derived homotopy relations with EHP map data
* recursive proof dependency collection
* proof dependency graph construction
* literature-backed automatic proof tracing

The algebra layer remains independent of these higher-level inference
mechanisms.


















