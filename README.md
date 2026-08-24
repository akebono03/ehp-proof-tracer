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
  and explicitly supplied `ProofStep` objects
* premise candidate search over available proof steps
* distinct-step assignment for multiple premise patterns
* inference-rule applicability checks
* applicable-rule search
* structured `InferenceMatch` objects
* application of single and multiple inference matches
* construction of derived `ProofStep` objects
* preservation of rule and premise metadata in derived proof steps
* one-round candidate derivation through `derive_inference_steps()`
* duplicate-aware merging through `merge_proof_steps()`
* extraction of genuinely new proof steps through `derive_new_inference_steps()`
* one-round state expansion through `run_inference_round()`
* automatic fixed-point iteration through `run_inference_until_stable()`
* use of newly derived steps as premises in later rounds
* fixed-point termination when no genuinely new conclusion is produced
* preservation of dependencies across inference rounds
* structured fixed-point execution results through `InferenceRunResult`
* per-round histories of genuinely new proof steps
* productive-round counting through `round_count`
* detailed fixed-point execution through `run_inference_until_stable_with_history()`
* explicit inference termination reasons
* configurable maximum productive-round limits
* distinction between fixed-point termination and round-limit termination
* validation of `max_rounds`
* backward-compatible final-state-only inference
* input normalization for single and multiple inference rules
* human-readable proof formatting

For example, an EHP exactness calculation can be represented as:

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

An inference rule can describe its required premises structurally:

```python
rule = InferenceRule(
  name="example inference",
  premise_patterns=(
    PremisePattern(
      proof_rule=ProofRule.RELATION,
      statement_type=Relation,
      relation_type=RelationType.ZERO,
    ),
  ),
  conclusion_builder=builder,
)
```

A successful match is represented explicitly:

```python
InferenceMatch(
  inference_rule=rule,
  premises=(
    matched_step,
  ),
)
```

The high-level one-round pipeline is:

```text
available ProofSteps
+
InferenceRules
↓
find_inference_matches()
↓
apply_inference_matches()
↓
candidate derived ProofSteps
↓
merge_proof_steps()
↓
genuinely new ProofSteps
```

The genuinely new part of a round can be obtained directly:

```python
new_steps = derive_new_inference_steps(
  inference_rules,
  available_steps,
)
```

Conceptually:

```text
state_n
+
delta_n
=
state_{n+1}
```

where:

```text
state_n
=
currently known ProofSteps

delta_n
=
genuinely new ProofSteps derived in the current round
```

Fixed-point inference is available through:

```python
stable_steps = run_inference_until_stable(
  inference_rules,
  initial_steps,
)
```

Conceptually:

```text
initial state
↓
derive new steps
↓
append genuinely new steps
↓
repeat
↓
no genuinely new steps
↓
fixed point
```

A conclusion produced in one round can therefore become a premise in a
later round:

```text
A
↓ rule 1
B
↓ rule 2
C
```

Detailed fixed-point execution is available through:

```python
result = run_inference_until_stable_with_history(
  inference_rules,
  initial_steps,
)
```

The result is represented by:

```python
InferenceRunResult(
  steps=...,
  round_history=...,
  termination_reason=...,
)
```

where:

```text
steps
=
the knowledge state at termination

round_history
=
the genuinely new ProofSteps produced in each productive round

round_count
=
the number of productive rounds

termination_reason
=
why iterative inference stopped
```

For example:

```text
initial:
A

round 1:
B
C

round 2:
D

termination check:
no new ProofSteps
```

is represented conceptually as:

```python
InferenceRunResult(
  steps=(
    A,
    B,
    C,
    D,
  ),
  round_history=(
    (
      B,
      C,
    ),
    (
      D,
    ),
  ),
  termination_reason=(
    InferenceTerminationReason.FIXED_POINT
  ),
)
```

The final empty termination check is not stored in `round_history`.

Only productive rounds are counted:

```text
round_count == 2
```

---

## Maximum-round safeguard

Phase 5-30 adds an optional inference-round limit:

```python
result = run_inference_until_stable_with_history(
  inference_rules,
  initial_steps,
  max_rounds=10,
)
```

`max_rounds` means:

```text
maximum number of productive rounds allowed
```

The accepted values are:

```text
None
or
a non-negative integer
```

`None` preserves the previous behavior:

```text
continue until a fixed point is detected
```

A non-negative integer limits knowledge-state expansion.

For example:

```python
max_rounds=2
```

allows at most:

```text
round 1
round 2
```

to add new proof steps.

After two productive rounds, execution stops before attempting another
derivation round.

---

## Termination reason

Termination is represented explicitly by:

```python
class InferenceTerminationReason(Enum):
  FIXED_POINT = "fixed_point"
  MAX_ROUNDS = "max_rounds"
```

A normal fixed-point termination returns:

```python
result.termination_reason
== InferenceTerminationReason.FIXED_POINT
```

A round-limit termination returns:

```python
result.termination_reason
== InferenceTerminationReason.MAX_ROUNDS
```

This distinction is important because:

```text
MAX_ROUNDS
```

does not imply that the returned state is a fixed point.

It only means that the configured number of productive rounds has been
used.

For example:

```text
max_rounds = 1

initial:
A

round 1:
B

stop
```

returns:

```text
steps:
A
B

round_count:
1

termination_reason:
MAX_ROUNDS
```

without checking whether another round could derive additional facts.

---

## Exact-limit semantics

Suppose a rule system requires exactly two productive rounds to produce
all currently derivable facts:

```text
initial:
A

round 1:
B

round 2:
C
```

and:

```python
max_rounds=2
```

is specified.

The result is:

```text
round_count = 2
termination_reason = MAX_ROUNDS
```

even if a subsequent inference check would find no new step.

This is intentional.

The engine has not performed the additional check required to prove
that the current state is a fixed point.

Therefore:

```text
FIXED_POINT
```

is returned only when:

```python
derive_new_inference_steps(...)
```

has actually returned:

```python
()
```

before the round limit is reached.

---

## max_rounds = 0

A zero limit is valid:

```python
max_rounds=0
```

and means:

```text
perform zero productive rounds
```

The initial state is returned immediately with:

```text
round_count = 0
termination_reason = MAX_ROUNDS
```

No inference rule is applied.

---

## Simple and detailed APIs

Both fixed-point APIs accept `max_rounds`.

Detailed API:

```python
result = run_inference_until_stable_with_history(
  inference_rules,
  available_steps,
  max_rounds=10,
)
```

This exposes:

```text
steps
round_history
round_count
termination_reason
```

Simple API:

```python
steps = run_inference_until_stable(
  inference_rules,
  available_steps,
  max_rounds=10,
)
```

This returns only:

```text
tuple[ProofStep, ...]
```

The simple API delegates to the detailed API.

Therefore both APIs use exactly the same:

```text
round-limit semantics
duplicate semantics
fixed-point semantics
```

Callers that need to distinguish:

```text
fixed point reached
```

from:

```text
round limit reached
```

should use:

```python
run_inference_until_stable_with_history()
```

---

## max_rounds validation

`max_rounds` accepts:

```text
None
0
1
2
...
```

Invalid types raise `TypeError`.

For example:

```text
1.5
"10"
True
False
```

are rejected.

Although Python `bool` is a subclass of `int`, boolean values are
explicitly rejected because they do not represent meaningful
round-count configuration.

Negative integers raise `ValueError`.

For example:

```text
-1
```

is invalid.

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

The inference layer now supports safe bounded fixed-point execution, but
its matching semantics remain intentionally simple.

Premise search is currently greedy:

```text
for each premise pattern
↓
select the first unused matching ProofStep
```

It does not yet:

```text
enumerate every valid premise assignment
perform backtracking
rank alternative premise assignments
compare alternative proofs
```

Duplicate detection currently uses ordinary Python conclusion equality:

```python
step.conclusion == known_conclusion
```

It does not yet use:

```text
mathematical equivalence
canonical forms
normalization of homotopy expressions
```

If two derivations produce the same conclusion, only the first
`ProofStep` added to the knowledge state is retained.

Alternative proofs of the same conclusion are not yet preserved.

`max_rounds` protects against unrestricted repeated inference, but it is
not cycle detection or a proof of termination.

The inference engine does not yet detect:

```text
semantic cycles
repeated state patterns beyond conclusion deduplication
unbounded conclusion generation
```

`InferenceRunResult` currently stores:

```text
final or limited state
per-round new-step history
productive-round count
termination reason
```

but does not yet store:

```text
configured max_rounds
terminal empty-round record
per-round complete state snapshots
InferenceMatch history
applicable-rule history
candidate steps rejected as duplicates
rule-application counts
timing or performance metadata
```

The fixed point should therefore be understood as:

```text
a fixed point under the currently registered rules,
current greedy matching semantics,
and current conclusion-equality semantics
```

rather than a claim of mathematical completeness.

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

Run the inference-rule tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-30:

```text
218 passed in 3.90s
```

for:

```text
tests/test_inference_rule_pattern.py
```

Phase 5-29 completed with:

```text
208 inference-rule pattern tests passed
```

so Phase 5-30 adds 10 inference termination / round-limit tests.

The Phase 5-30 tests cover:

```text
InferenceTerminationReason values
FIXED_POINT termination
MAX_ROUNDS termination
max_rounds = 0
fixed point reached before the limit
exact-limit semantics
negative max_round rejection
non-integer max_round rejection
bool max_round rejection
simple API max_round propagation
```

---

## Next direction

The Phase 5 inference engine has now progressed through:

```text
Phase 5-24
candidate derivation
↓
Phase 5-25
one-round state expansion
↓
Phase 5-26
duplicate-aware merge
↓
Phase 5-27
one-round delta
↓
Phase 5-28
automatic fixed-point iteration
↓
Phase 5-29
per-round history and structured result
↓
Phase 5-30
bounded iteration and explicit termination reason
```

The engine can now safely answer:

```text
What was derived?
In which productive round was it derived?
How many productive rounds ran?
Why did inference stop?
```

The next natural problem is to improve the structure of the execution
trace itself.

Possible next directions include:

```text
structured per-round result objects
rule / match application history
duplicate-rejected candidate history
```

before moving on to more powerful premise matching such as:

```text
alternative premise assignments
backtracking
expression-level patterns
variable bindings
substitution
```










