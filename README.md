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
* input normalization for single and multiple inference rules
* human-readable proof formatting

The current rule-matching pipeline has five levels.

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

For example, a rule requiring a relation and a given fact can be
defined as:

```python
InferenceRule(
  name="combined rule",
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.RELATION,
    ),
    PremisePattern(
      proof_rule=ProofRule.GIVEN,
    ),
  ),
)
```

The available proof steps do not need to be stored in the same order
as the premise patterns when premise search is used.

For example:

```text
available:
  GIVEN
  RELATION
```

can satisfy:

```text
patterns:
  RELATION
  GIVEN
```

because `find_matching_premises()` searches the available collection
for each premise pattern.

The selected premises are returned in rule-pattern order:

```text
(
  relation_step,
  given_step,
)
```

The current premise search selects the first matching unused step for
each pattern.

A single proof step is not reused for multiple premise patterns within
the same rule.

Therefore a rule requiring:

```text
GIVEN
GIVEN
```

is not applicable when only one matching `GIVEN` step exists.

If two distinct matching steps exist, the rule can be applicable.

A rule with:

```text
premise_patterns = ()
```

requires no premises.

In that case:

```python
find_matching_premises(
  rule,
  available_steps,
)
```

returns:

```text
()
```

and:

```python
is_inference_rule_applicable(
  rule,
  available_steps,
)
```

returns:

```text
True
```

Thus:

```text
()
```

means that premise search succeeded for a rule requiring no premises,
while:

```text
None
```

means that one or more required premises could not be found.

`is_inference_rule_applicable()` is intentionally a thin query over
`find_matching_premises()`.

It does not duplicate:

```text
premise matching
available-step search
step-reuse checks
input normalization
```

and instead returns whether matching premises can be found.

Multiple rules can now be searched at once.

For example:

```python
find_applicable_inference_rules(
  (
    combined_rule,
    given_rule,
    relation_rule,
  ),
  available_steps,
)
```

checks each rule against the same collection of available proof steps
and returns only those that are currently applicable.

Conceptually:

```text
rules:
  rule A
  rule B
  rule C

available ProofSteps
↓
applicability check for each rule
↓
applicable rules only
```

If rule A and rule C are applicable, the result is:

```text
(
  rule_a,
  rule_c,
)
```

The input rule order is preserved.

The search does not rank, prioritize, or choose among applicable rules.

If multiple rules are applicable, all of them are returned.

If no rules are applicable, the result is:

```text
()
```

An empty rule collection also returns:

```text
()
```

A premise-free rule remains applicable even when no proof steps are
available.

The rule collection can be supplied as:

```text
a single InferenceRule
a tuple of InferenceRule
a list of InferenceRule
```

and available steps can likewise be supplied as:

```text
a single ProofStep
a tuple of ProofStep
a list of ProofStep
```

The applicable-rule search intentionally reuses the existing
applicability query:

```text
find_applicable_inference_rules()
↓
is_inference_rule_applicable()
↓
find_matching_premises()
↓
matches_premise_pattern()
```

so premise-matching behavior remains centralized.

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

Therefore the current applicability and applicable-rule search mean:

```text
applicable under the current greedy premise-search algorithm
```

rather than a complete search over every possible premise assignment.

The proof / inference layer does not yet automatically:

* enumerate all possible premise assignments
* backtrack over alternative premise assignments
* select among multiple applicable premise assignments
* pair an applicable rule with its matched premises as a structured result
* rank or prioritize multiple applicable inference rules
* choose which applicable inference rule to apply
* match internal expression structures
* bind pattern variables
* substitute bound variables
* construct conclusions from inference rules
* search a `RelationRepository` automatically for required relations
* apply inference rules automatically
* add derived conclusions back into the available proof-step collection
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

These belong to later inference phases.

---

## Tests

Run the complete test suite with:

```powershell
python -m pytest -v
```

At the completion of Phase 5-20:

```text
303 passed in 23.01s
```

Phase 5-20 includes applicable-rule-search tests covering:

```text
single applicable rule
multiple applicable rules
input-order preservation
no applicable rules
empty rule collections
premise-free rules
multiple premise patterns
relation-type requirements
single InferenceRule input
list input
invalid rule input
invalid rule entries
invalid available-step input
invalid ProofStep entries
```

The complete test suite also includes the existing algebra, EHP,
expression, formatter, proof, repository, premise-pattern,
inference-rule matching, premise-search, and applicability tests.

---

## Next direction

The current inference-rule pipeline is:

```text
InferenceRule collection
+
available ProofSteps
↓
find_applicable_inference_rules()
↓
applicable InferenceRules
```

At this point the engine can determine:

```text
which rules can currently be used
```

but the returned result contains only the `InferenceRule`.

The next useful step is to retain the matched premises together with
the applicable rule.

Conceptually:

```text
InferenceRule
+
available ProofSteps
↓
find_matching_premises()
↓
rule + matched premises
```

A possible structured result is:

```python
@dataclass(frozen=True)
class InferenceMatch:
  inference_rule: InferenceRule
  premises: tuple[ProofStep, ...]
```

Then a collection search could conceptually produce:

```text
InferenceRule collection
+
available ProofSteps
↓
find inference matches
↓
(
  InferenceMatch(...),
  InferenceMatch(...),
  ...
)
```

This would preserve not only:

```text
which rule is applicable
```

but also:

```text
which ProofSteps make that rule applicable
```

without requiring the caller to repeat premise search after finding
applicable rules.

This should still remain separate from actual conclusion construction.

Possible later directions include:

* structured rule-and-premise matches
* `InferenceMatch`
* alternative premise assignments
* backtracking premise search
* enumeration of all premise assignments
* rule priority and rule selection
* expression-level relation patterns
* pattern variables and variable binding
* substitution
* conclusion construction
* automatic relation selection
* automatic inference-rule application
* iterative inference over newly derived ProofSteps
* composition relations
* Toda brackets
* integration of derived homotopy relations with EHP map data
* recursive proof dependency collection
* proof dependency graph construction
* literature-backed automatic proof tracing

The algebra layer remains independent of these higher-level inference
mechanisms.












