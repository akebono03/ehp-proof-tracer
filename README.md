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
* high-level inference derivation through `derive_inference_steps()`
* composition of structured match search and application without duplicating either implementation
* direct derivation of multiple `ProofStep` objects from inference rules and available proof steps
* preservation of inference-rule order through the high-level derivation path
* normalization of single, tuple, and list rule / proof-step input through existing lower-level APIs
* one-round inference through `run_inference_round()`
* expansion of the available proof-step collection with newly derived proof steps
* preservation of existing available-step order during an inference round
* preservation of derived-step order during an inference round
* explicit separation between one-round inference and iterative inference
* human-readable proof formatting

The current inference pipeline has low-level matching and application
APIs together with high-level derivation and one-round execution APIs.

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
derived ProofStep tuple
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
derived ProofSteps
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
derived ProofStep collection
```

`derive_inference_steps()` is intentionally a thin composition of the
existing collection-level matching and application functions.

Its implementation is equivalent to:

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

return apply_inference_matches(
  matches
)
```

It does not reimplement:

```text
rule normalization
ProofStep normalization
premise search
InferenceMatch construction
conclusion-builder validation
conclusion construction
ProofRule.INFERENCE assignment
premise preservation
InferenceRule preservation
```

These responsibilities remain in the lower-level APIs.

This keeps:

```text
find_inference_matches()
```

and:

```text
apply_inference_matches()
```

available as independently usable operations while also providing a
convenient entry point for the common:

```text
find
↓
apply
```

workflow.

For example, callers that need to inspect or select matches can still
use:

```python
matches = find_inference_matches(
  inference_rules,
  available_steps,
)

selected_matches = ...

derived_steps = apply_inference_matches(
  selected_matches,
)
```

while callers that want to apply every currently matched rule can use:

```python
derived_steps = derive_inference_steps(
  inference_rules,
  available_steps,
)
```

Phase 5-25 adds one more high-level operation:

```python
expanded_steps = run_inference_round(
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
run_inference_round()
↓
normalize available ProofSteps
↓
derive_inference_steps()
↓
derived ProofSteps
↓
available ProofSteps + derived ProofSteps
```

Its implementation is intentionally thin:

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

return (
  normalized_steps
  + derived_steps
)
```

The distinction between the two high-level APIs is:

```text
derive_inference_steps()
= return only newly derived ProofSteps

run_inference_round()
= return the existing available ProofSteps
  followed by newly derived ProofSteps
```

For example, if:

```text
available:
(
  given_step,
)

derived:
(
  derived_step,
)
```

then:

```python
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

returns:

```text
(
  derived_step,
)
```

while:

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

returns:

```text
(
  given_step,
  derived_step,
)
```

The existing available-step order is preserved.

For example:

```text
(
  step_a,
  step_b,
  step_c,
)
```

remains the prefix of the returned collection:

```text
(
  step_a,
  step_b,
  step_c,
  ...
)
```

The derived-step order is also preserved.

Because:

```text
find_inference_matches()
```

preserves inference-rule input order and:

```text
apply_inference_matches()
```

preserves `InferenceMatch` input order,

the composed derivation path preserves:

```text
InferenceRule order
↓
InferenceMatch order
↓
derived ProofStep order
```

and `run_inference_round()` preserves:

```text
existing available-step order
↓
derived-step order
```

For example:

```text
rules:
(
  rule_b,
  rule_a,
)

available:
(
  step_1,
  step_2,
)
```

can produce:

```text
(
  step_1,
  step_2,
  derived_from_rule_b,
  derived_from_rule_a,
)
```

If no inference rule matches the currently available proof steps,

```python
derive_inference_steps(
  inference_rules,
  available_steps,
)
```

returns:

```text
()
```

and therefore:

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

returns the normalized existing steps unchanged.

Likewise an empty rule collection leaves the available proof-step
collection unchanged.

Premise-free inference rules remain applicable even if the available
proof-step collection is empty.

For example:

```text
available:
()

premise-free rule
↓
derived ProofStep
```

produces:

```text
(
  derived_step,
)
```

when `run_inference_round()` is called.

Input normalization continues to use the existing APIs.

The high-level inference functions therefore support forms such as:

```text
single InferenceRule
tuple of InferenceRule
list of InferenceRule

single ProofStep
tuple of ProofStep
list of ProofStep
```

and return tuples of `ProofStep` objects.

Invalid rule or proof-step input is rejected by the existing
normalization logic.

A matched rule still requires a callable conclusion builder.

For example, if an applicable rule has:

```text
conclusion_builder = None
```

then application through:

```text
derive_inference_steps()
```

or:

```text
run_inference_round()
```

raises the same `ValueError` as direct
`apply_inference_match()` application.

This is intentional: the high-level functions do not weaken or
duplicate application validation.

An important semantic boundary is that `run_inference_round()`
performs exactly one inference round.

All matching for the round is performed against the proof steps that
were available at the beginning of the round.

Newly derived proof steps are appended only after derivation for that
round has completed.

Therefore the behavior is:

```text
available ProofSteps at start of round
↓
find matches
↓
derive all currently available conclusions
↓
append derived ProofSteps
↓
return expanded collection
```

and not:

```text
derive one ProofStep
↓
immediately add it
↓
search again inside the same round
↓
derive another ProofStep
```

For example, suppose:

```text
rule A:
given fact
→ intermediate fact

rule B:
intermediate fact
→ final fact
```

and only the given fact is available at the beginning of the round.

One call to:

```python
run_inference_round(
  inference_rules,
  available_steps,
)
```

derives the intermediate fact, but does not use that newly derived fact
to activate rule B during the same round.

A second round is required:

```python
steps = run_inference_round(
  inference_rules,
  steps,
)

steps = run_inference_round(
  inference_rules,
  steps,
)
```

This explicit round boundary is intentional and separates one-round
inference from future iterative inference.

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
compose collection-level match search and application
↓
derive currently available ProofSteps in one high-level call
↓
perform one inference round
↓
append the derived ProofSteps to the available ProofStep collection
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

Both:

```text
derive_inference_steps()
```

and:

```text
run_inference_round()
```

inherit this matching behavior because they delegate matching to
`find_inference_matches()`.

The current inference-round implementation also performs simple tuple
concatenation:

```text
existing ProofSteps
+
derived ProofSteps
```

It does not detect whether a newly derived conclusion is already known.

Therefore repeated calls can currently introduce duplicate conclusions.

For example:

```text
A
```

together with:

```text
A → B
```

produces after one round:

```text
A
B
```

but running the same round again may produce:

```text
A
B
B
```

because no duplicate handling is performed yet.

The proof / inference layer does not yet automatically:

* enumerate all possible premise assignments
* backtrack over alternative premise assignments
* return multiple alternative `InferenceMatch` objects for the same rule
* rank or prioritize multiple applicable inference rules
* choose a subset of matches when using the high-level derivation API
* detect duplicate derived conclusions
* detect duplicate `ProofStep` objects during round expansion
* distinguish genuinely new facts from already-known facts
* merge alternative proofs of the same conclusion
* iterate inference until no new conclusions are found
* detect a fixed point
* prevent repeated premise-free inference across multiple rounds
* prevent repeated application of the same rule to the same premises
* detect cyclic inference
* record inference-round boundaries or round numbers
* retain explicit inference-round history
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

Therefore the current inference mechanism should be understood as:

```text
structured ProofStep-level premise matching
+
explicit Python conclusion builder
+
single / collection-level application
+
high-level derivation
+
single-round available-step expansion
```

rather than a complete symbolic or iterative inference system.

---

## Tests

Run the complete test suite with:

```powershell
python -m pytest -v
```

At the completion of Phase 5-25:

```text
376 passed in 44.79s
```

Phase 5-25 adds one-round inference tests covering:

```text
basic one-round inference
multiple derived-step insertion
available-step order preservation
derived-step order preservation
no applicable rule
empty rule collection
empty available-step collection
premise-free inference with empty available steps
single InferenceRule and ProofStep input
list input
invalid rule input
invalid ProofStep input
missing conclusion builder on an applicable rule
```

The complete test suite also includes the existing algebra, EHP,
expression, formatter, proof, repository, premise-pattern,
inference-rule matching, premise-search, applicability,
applicable-rule-search, structured-match, single-match application,
collection-level application, and high-level derivation tests.

---

## Next direction

The current inference pipeline now reaches a complete explicit
one-round operation:

```text
InferenceRule collection
+
available ProofSteps
↓
run_inference_round()
↓
available ProofSteps
+
derived ProofSteps
```

Internally:

```text
run_inference_round()
↓
derive_inference_steps()
↓
find_inference_matches()
↓
apply_inference_matches()
```

so the lower-level matching, application, and derivation APIs remain
independently available.

The proof engine can therefore now represent:

```text
knowledge state before one round
↓
inference
↓
expanded knowledge state after one round
```

The next major transition is not simply to repeat
`run_inference_round()` automatically.

Before iterative inference can be introduced safely, the system needs
to define how existing and newly derived facts are merged.

The central problem is duplicate handling.

For example:

```text
available:
A

rule:
A → B
```

produces:

```text
A
B
```

after one round.

A second round can currently produce:

```text
A
B
B
```

because `B` is not recognized as already known.

Important questions include:

* how equality or equivalence of conclusions should be determined
* whether duplicate detection should compare `ProofStep` objects or only conclusions
* whether the same conclusion with different premises should be retained
* whether multiple proofs of the same mathematical fact should be preserved
* whether the same rule may derive the same conclusion from different premises
* how repeated application of the same rule to the same premises should be handled
* how premise-free rules should be prevented from generating the same result every round
* how genuinely new facts should be distinguished from repeated facts
* how inference history should be retained
* whether round numbers or round objects should be introduced
* how termination should be detected

A natural next step is therefore:

```text
available ProofSteps
+
derived ProofSteps
↓
duplicate-aware merge
↓
expanded ProofSteps
+
newly added ProofSteps
```

Conceptually:

```text
existing ProofSteps
+
derived ProofSteps
↓
compare conclusions
↓
retain genuinely new facts
↓
expanded available ProofSteps
```

Once this merge semantics is defined, iterative inference can proceed as:

```text
available ProofSteps
↓
run inference round
↓
derive candidate ProofSteps
↓
duplicate-aware merge
↓
new ProofSteps?
├── yes → next round
└── no  → fixed point
```

This would move the system from:

```text
single-round inference
```

to:

```text
fixed-point iterative inference
```

with an explicit termination condition.

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

* duplicate conclusion detection
* proof-step collection merge
* new-fact detection
* alternative-proof handling
* inference-round representation
* fixed-point iterative inference
* termination detection
* inference history
* repeated-rule-application control
* premise-free rule repetition control
* cyclic-inference detection
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


















