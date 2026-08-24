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
* high-level inference derivation through `derive_inference_steps()`
* direct derivation of candidate `ProofStep` objects from inference rules and available proof steps
* preservation of inference-rule order through the high-level derivation path
* duplicate-aware proof-step merging through `merge_proof_steps()`
* duplicate detection based on `ProofStep.conclusion` equality
* suppression of derived conclusions that are already available
* suppression of duplicate conclusions produced by multiple rules
* preservation of the first derived proof step when multiple derived steps have the same conclusion
* extraction of genuinely new derived proof steps through `derive_new_inference_steps()`
* explicit distinction between candidate derived steps and genuinely new derived steps
* preservation of genuinely new step order
* empty new-step result when all candidate conclusions are already known
* one-round inference through `run_inference_round()`
* expansion of the available knowledge state using only genuinely new proof steps
* idempotent repeated execution when a round derives no new conclusions
* explicit preparation for fixed-point iterative inference
* human-readable proof formatting

The current inference pipeline distinguishes four separate stages:

```text
matching
↓
application
↓
candidate derivation
↓
new-fact detection
```

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

Structured match search:

```text
InferenceRule collection
+
available ProofSteps
↓
find_inference_matches()
↓
InferenceMatch tuple
```

Application:

```text
InferenceMatch collection
↓
apply_inference_matches()
↓
derived ProofStep tuple
```

Candidate derivation:

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
candidate derived ProofSteps
↓
merge_proof_steps()
↓
merged ProofStep tuple
```

Genuinely new derivation:

```text
InferenceRule collection
+
available ProofSteps
↓
derive_new_inference_steps()
↓
genuinely new ProofStep tuple
```

One inference round:

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
available ProofSteps
+
genuinely new ProofSteps
```

---

## Candidate derived steps and genuinely new steps

Phase 5-27 introduces an explicit distinction between:

```text
candidate derived ProofSteps
```

and:

```text
genuinely new ProofSteps
```

`derive_inference_steps()` returns all conclusions produced by the
currently matched inference rules.

For example:

```text
available:
A
B

rules:
A → B
A → C
```

may produce:

```text
derive_inference_steps():
B
C
```

Here `B` is a valid rule result, but it is not a new fact because `B`
is already available.

`derive_new_inference_steps()` filters the candidate results through
the existing duplicate-aware merge semantics and returns only:

```text
C
```

Thus:

```text
derive_inference_steps()
=
what the currently applicable rules derive

derive_new_inference_steps()
=
what the current round actually adds to the knowledge state
```

This distinction is important for iterative inference.

---

## derive_new_inference_steps()

The Phase 5-27 high-level API is:

```python
new_steps = derive_new_inference_steps(
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
normalize available ProofSteps
↓
derive_inference_steps()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
merged ProofSteps
↓
remove original available prefix
↓
genuinely new ProofSteps
```

Its structure is equivalent to:

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

merged_steps = merge_proof_steps(
  normalized_steps,
  derived_steps,
)

return merged_steps[
  len(normalized_steps):
]
```

No new duplicate-detection rule is introduced.

Instead, Phase 5-27 deliberately reuses the Phase 5-26 semantics
implemented by:

```text
merge_proof_steps()
```

Therefore duplicate handling remains centralized.

---

## Why slicing the merged result works

`merge_proof_steps()` preserves every existing available step as the
prefix of its result.

For example:

```text
available:
A
B

candidate derived:
B
C
D
```

produces:

```text
merged:
A
B
C
D
```

The first:

```text
len(available_steps)
```

elements are exactly the original available steps.

Therefore:

```python
merged_steps[
  len(normalized_steps):
]
```

returns:

```text
C
D
```

which are exactly the steps newly added by the merge.

This reuses the ordering guarantee introduced in Phase 5-26 rather
than duplicating novelty-detection logic.

---

## Existing-conclusion suppression

If all candidate conclusions are already known:

```text
available:
A
B

candidate derived:
B
```

then:

```text
merged:
A
B
```

and:

```text
new:
()
```

Therefore:

```python
derive_new_inference_steps(
  inference_rules,
  available_steps,
)
```

returns the empty tuple when no genuinely new conclusion is produced.

---

## Duplicate candidate suppression

If multiple rules derive the same previously unknown conclusion:

```text
available:
A

rule 1:
A → B

rule 2:
A → B
```

then candidate derivation may produce:

```text
B from rule 1
B from rule 2
```

but `merge_proof_steps()` keeps only the first new conclusion.

Therefore:

```text
derive_new_inference_steps():
B from rule 1
```

The existing rule-order semantics are preserved.

---

## New-step order

`derive_new_inference_steps()` preserves the order in which genuinely
new conclusions first occur.

For example:

```text
rules:
rule 2 → B
rule 1 → C
```

produces:

```text
new:
B
C
```

in that order.

The ordering chain remains:

```text
InferenceRule input order
↓
InferenceMatch order
↓
candidate derived-step order
↓
first genuinely new occurrence
↓
new-step order
```

---

## Premise-free rules

Premise-free inference rules remain supported.

For example:

```text
available:
()

premise-free rule:
→ A
```

produces:

```text
derive_new_inference_steps():
A
```

If `A` is already available in a later round, the same rule may still
be applicable, but:

```text
derive_new_inference_steps():
()
```

because the conclusion is no longer new.

---

## Repeated derivation and fixed-point preparation

A major consequence of Phase 5-27 is that repeated inference can now
directly report whether progress was made.

For example:

```text
available:
A

rule:
A → B
```

First call:

```text
new:
B
```

After adding `B`, a later call returns:

```text
new:
()
```

Therefore the natural fixed-point condition is now:

```python
new_steps = derive_new_inference_steps(
  inference_rules,
  available_steps,
)

if not new_steps:
  # fixed point
```

Phase 5-27 does not yet execute this loop automatically.

It only makes the termination condition directly observable.

---

## run_inference_round()

Phase 5-27 also simplifies the semantic role of
`run_inference_round()`.

It can now be understood as:

```text
available ProofSteps
+
derive_new_inference_steps()
```

Conceptually:

```python
normalized_steps = (
  _normalize_proof_steps(
    available_steps,
    "available_steps",
  )
)

new_steps = derive_new_inference_steps(
  inference_rules,
  normalized_steps,
)

return (
  normalized_steps
  + new_steps
)
```

Thus:

```text
derive_new_inference_steps()
=
return only the facts newly discovered in this round

run_inference_round()
=
return the complete knowledge state after this round
```

This makes the distinction between round delta and round result
explicit.

---

## Current limitations

The current premise search remains greedy.

For each premise pattern it selects the first matching unused proof
step and does not backtrack.

Therefore the engine still does not enumerate all possible premise
assignments.

Duplicate and novelty semantics continue to use ordinary Python
equality on conclusions:

```python
step.conclusion == known_conclusion
```

This is not yet a general mathematical-equivalence test.

The proof / inference layer does not yet automatically:

* enumerate all alternative premise assignments
* backtrack during premise search
* preserve multiple proofs of the same conclusion in the knowledge state
* maintain a separate alternative-proof repository
* canonicalize mathematically equivalent conclusions
* determine semantic mathematical equivalence
* automatically repeat inference rounds
* iterate until no new steps remain
* return a fixed-point result object
* record the number of rounds
* record the steps added in each round as history
* maintain rule-application history
* prevent all possible inference cycles
* support expression-level pattern variables
* bind expression variables
* substitute bindings into conclusion templates
* automatically select relations from a `RelationRepository`
* recursively construct proof dependency graphs
* derive E/H/P formulas from higher homotopy-theoretic relations

Phase 5-27 specifically provides the missing delta:

```text
new ProofSteps produced by one round
```

but does not yet perform repeated rounds.

---

## Tests

Run the inference tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-27:

```text
180 passed in 3.40s
```

Run the complete suite with:

```powershell
python -m pytest -v
```

At the completion of Phase 5-27:

```text
404 passed in 43.45s
```

Phase 5-26 completed with:

```text
390 passed
```

so Phase 5-27 adds 14 tests.

Phase 5-27 adds coverage for:

```text
basic genuinely-new-step derivation
existing-conclusion exclusion
duplicate-derived-conclusion exclusion
mixed existing and new conclusions
new-step order preservation
no matching rule
empty rule collection
premise-free rule with empty available steps
no new result after repeating the same derivation
single rule / single step input
list input
invalid rule input
invalid available-step input
missing conclusion builder on a matched rule
```

The complete suite passes without regression.

---

## Next direction

The inference engine can now directly answer:

```text
Did this round produce any new facts?
```

through:

```python
new_steps = derive_new_inference_steps(
  inference_rules,
  available_steps,
)
```

This provides the termination condition needed for fixed-point
inference.

The next natural operation is:

```text
available ProofSteps
↓
derive genuinely new ProofSteps
↓
new steps exist?
├── yes
│   ↓
│   add them
│   ↓
│   run another round
│
└── no
    ↓
    terminate
```

Conceptually:

```python
steps = initial_steps

while True:
  new_steps = derive_new_inference_steps(
    inference_rules,
    steps,
  )

  if not new_steps:
    break

  steps = (
    steps
    + new_steps
  )
```

The natural next phase is therefore:

```text
Phase 5-28:
fixed-point iterative inference
```

with an API such as:

```python
run_inference_until_stable(
  inference_rules,
  available_steps,
)
```

or equivalent.

Important design questions for that phase include:

* whether only the final knowledge state should be returned
* whether round count should also be returned
* whether per-round newly added steps should be retained
* whether a maximum-round safeguard should be introduced
* how to distinguish true fixed point from externally imposed termination
* whether inference history should be represented by a dedicated object

The algebra layer remains independent of these higher-level inference
mechanisms.


## Fixed-point iterative inference

Phase 5-28 introduces automatic fixed-point iteration over the
inference engine.

Phase 5-27 made the one-round delta directly observable through:

```python
derive_new_inference_steps(
  inference_rules,
  available_steps,
)
```

Phase 5-28 uses that delta as the termination condition for repeated
inference.

The new high-level API is:

```python
run_inference_until_stable(
  inference_rules,
  available_steps,
)
```

Conceptually:

```text
initial ProofSteps
↓
derive genuinely new ProofSteps
↓
new steps exist?
├── yes
│   ↓
│   append them to the knowledge state
│   ↓
│   repeat inference
│
└── no
    ↓
    return the stable knowledge state
```

The implementation is equivalent to:

```python
current_steps = initial_steps

while True:
  new_steps = derive_new_inference_steps(
    inference_rules,
    current_steps,
  )

  if not new_steps:
    return current_steps

  current_steps = (
    current_steps
    + new_steps
  )
```

Thus the inference engine can now continue applying rules until no
genuinely new conclusion is produced.

---

## run_inference_until_stable()

`run_inference_until_stable()` accepts:

```text
InferenceRule
or
tuple/list of InferenceRule
```

together with:

```text
ProofStep
or
tuple/list of ProofStep
```

and returns:

```text
tuple of ProofStep
```

representing the final knowledge state reached by the current
inference rules and matching semantics.

For example:

```text
initial:
A

round 1:
A → B

state:
A
B

round 2:
B → C

state:
A
B
C

round 3:
no genuinely new conclusion

fixed point:
A
B
C
```

The caller no longer needs to manually invoke repeated inference
rounds.

---

## Fixed-point condition

The termination condition remains exactly the one introduced in
Phase 5-27:

```python
new_steps = derive_new_inference_steps(
  inference_rules,
  current_steps,
)

if not new_steps:
  # fixed point
```

No separate termination semantics are introduced in Phase 5-28.

A stable state therefore means:

```text
under the currently registered inference rules
and the current matching semantics,
another inference round adds no new conclusion
```

This is an inference-engine fixed point.

It does not mean that all mathematically valid consequences have
necessarily been derived.

For example, inference may stop because:

```text
a required inference rule is not registered
```

or because:

```text
the current greedy premise search does not find
an alternative valid premise assignment
```

Therefore:

```text
inference-engine fixed point
```

and:

```text
mathematical completeness
```

remain distinct concepts.

---

## Multi-round derivation

Phase 5-28 confirms that a conclusion produced in one round can become
a premise in a later round.

For example:

```text
round 0:
given fact

round 1:
given fact
↓
derived Relation

round 2:
derived Relation
↓
final conclusion

round 3:
no new conclusion
```

The engine therefore supports genuine chained inference across
multiple rounds rather than only repeated execution of independent
one-round rules.

---

## Dependency preservation across rounds

Derived `ProofStep` objects retain their matched premises.

Therefore dependencies created in earlier rounds remain available to
later derived steps.

Conceptually:

```text
A
↓ rule 1
B
↓ rule 2
C
```

is represented by:

```text
B.premises = (A,)
C.premises = (B,)
```

even though `B` and `C` were produced in different inference rounds.

This preserves the proof-dependency structure while the knowledge
state grows.

---

## Duplicate suppression during iteration

Fixed-point iteration reuses the duplicate semantics introduced in
Phases 5-26 and 5-27.

Duplicate detection remains based on:

```python
step.conclusion == known_conclusion
```

Therefore a rule may remain applicable in later rounds, but if it
derives a conclusion already present in the knowledge state, that
result does not count as a new step.

For example:

```text
available:
A

rule:
A → B
```

First round:

```text
new:
B
```

Later round:

```text
candidate:
B

new:
()
```

The empty delta terminates fixed-point iteration.

Thus repeated applicability by itself does not cause an infinite loop
when the rule continues to derive the same conclusion.

---

## Ordering

`run_inference_until_stable()` preserves the existing ordering
semantics.

The ordering chain is:

```text
initial ProofStep order
↓
InferenceRule input order
↓
InferenceMatch order
↓
candidate derived-step order
↓
first genuinely new occurrence
↓
round delta order
↓
final knowledge-state order
```

Initial proof steps remain at the beginning of the final state.

New proof steps are appended in the order in which they first become
genuinely new.

---

## Inference API hierarchy

After Phase 5-28, the high-level inference APIs have the following
roles:

```text
find_inference_matches()
=
find structured rule applications

apply_inference_matches()
=
convert matches into derived ProofSteps

derive_inference_steps()
=
derive candidate ProofSteps for one state

merge_proof_steps()
=
merge candidate steps with duplicate suppression

derive_new_inference_steps()
=
return only the genuinely new one-round delta

run_inference_round()
=
return the complete state after one round

run_inference_until_stable()
=
repeat rounds until the delta becomes empty
```

The full high-level pipeline is now:

```text
InferenceRule collection
+
initial ProofSteps
↓
find_inference_matches()
↓
InferenceMatch collection
↓
apply_inference_matches()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
derive_new_inference_steps()
↓
round delta
↓
append delta to knowledge state
↓
repeat
↓
delta == ()
↓
stable knowledge state
```

---

## Current limitations

The current fixed-point engine intentionally remains minimal.

`run_inference_until_stable()` currently returns only:

```text
the final stable ProofStep tuple
```

It does not yet return:

```text
round count
per-round delta history
per-round knowledge states
rule-application history
termination metadata
```

There is also currently no:

```text
maximum-round safeguard
explicit cycle-detection mechanism
dedicated fixed-point result object
```

Termination currently relies on the knowledge state eventually
reaching a round in which:

```text
derive_new_inference_steps() == ()
```

Duplicate detection continues to use ordinary conclusion equality:

```python
step.conclusion == known_conclusion
```

and is not yet based on mathematical equivalence or canonicalization.

Premise search also remains greedy and does not backtrack or enumerate
all alternative premise assignments.

The fixed-point engine therefore inherits the current matching and
duplicate semantics unchanged.

---

## Tests

Run the inference tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-28:

```text
194 passed in 3.69s
```

Phase 5-27 completed with:

```text
180 passed
```

so Phase 5-28 adds 14 inference tests.

Phase 5-28 adds coverage for:

```text
basic fixed-point inference
multi-round inference
termination when no rule matches
empty rule collection
premise-free inference from an empty initial state
initial-step order preservation
derived-step order preservation
duplicate-conclusion suppression across repeated rounds
dependency preservation across rounds
single rule / single step input
list input
invalid rule input
invalid available-step input
missing conclusion builder on a matched rule
```

All 194 inference-rule pattern tests pass.

---

## Next direction

Phase 5-28 establishes the minimal fixed-point inference loop.

The engine can now perform:

```text
initial knowledge
↓
rule application
↓
new knowledge
↓
rule application using newly derived facts
↓
...
↓
fixed point
```

The next natural question is no longer how to repeat inference, but
how to describe and inspect the repeated inference process.

Possible next steps include:

```text
round count
per-round delta history
fixed-point result object
maximum-round safeguard
rule-application history
```

A natural next phase is to introduce structured information about a
fixed-point run while keeping the current simple final-state API
semantics clearly separated from execution-history metadata.

The algebra and EHP layers remain independent of fixed-point iteration.












