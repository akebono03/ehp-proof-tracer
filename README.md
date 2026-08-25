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


## Structured per-round inference results

Phase 5-31 introduces a structured result object for each productive
inference round.

Previously, per-round history was represented directly as:

```text
tuple[ProofStep, ...]
```

inside:

```text
InferenceRunResult.round_history
```

This was sufficient to record the genuinely new proof steps produced
in each round, but it provided no natural place to attach additional
round-level execution metadata.

Phase 5-31 introduces:

```python
@dataclass(frozen=True)
class InferenceRoundResult:
  new_steps: tuple[ProofStep, ...]
```

Each productive round is now represented explicitly by an
`InferenceRoundResult`.

The detailed execution result therefore stores:

```python
InferenceRunResult(
  steps=...,
  round_results=...,
  termination_reason=...,
)
```

where:

```text
steps
=
the final or round-limited knowledge state

round_results
=
the structured results of all productive inference rounds

termination_reason
=
why inference execution stopped
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
  round_results=(
    InferenceRoundResult(
      new_steps=(
        B,
        C,
      ),
    ),
    InferenceRoundResult(
      new_steps=(
        D,
      ),
    ),
  ),
  termination_reason=(
    InferenceTerminationReason.FIXED_POINT
  ),
)
```

Only productive rounds are represented by `InferenceRoundResult`.

The final empty check used to establish:

```text
FIXED_POINT
```

is still not recorded as a round result.

---

## round_results

The structured per-round API is available through:

```python
result.round_results
```

For example:

```python
first_round = result.round_results[0]

new_steps = first_round.new_steps
```

`round_results` preserves productive-round order.

Therefore:

```python
result.round_results[0]
```

represents the first productive round,

```python
result.round_results[1]
```

represents the second productive round,

and so on.

At Phase 5-31, an `InferenceRoundResult` contains only:

```text
new_steps
```

This is intentionally minimal.

The object provides a stable location for later round-level metadata
such as:

```text
InferenceMatch history
applicable-rule history
candidate derived steps
duplicate-rejected candidates
rule-application information
```

without requiring another redesign of the top-level execution result.

---

## Backward-compatible round_history

The previous API:

```python
result.round_history
```

is preserved.

It is now exposed as a compatibility property derived from
`round_results`:

```python
@property
def round_history(self):
  return tuple(
    round_result.new_steps
    for round_result
    in self.round_results
  )
```

Therefore existing code such as:

```python
result.round_history[0]
```

continues to return:

```text
tuple[ProofStep, ...]
```

for that productive round.

Conceptually:

```text
round_results
=
structured execution representation

round_history
=
compatibility view containing only new ProofSteps
```

For example:

```python
result.round_results == (
  InferenceRoundResult(
    new_steps=(
      B,
      C,
    ),
  ),
  InferenceRoundResult(
    new_steps=(
      D,
    ),
  ),
)
```

corresponds to:

```python
result.round_history == (
  (
    B,
    C,
  ),
  (
    D,
  ),
)
```

This preserves the Phase 5-29 / Phase 5-30 history API while allowing
the internal execution trace to evolve.

---

## round_count

`round_count` now counts structured productive-round results:

```python
@property
def round_count(self):
  return len(
    self.round_results
  )
```

Its semantics have not changed.

It still means:

```text
number of productive inference rounds
```

and does not count:

```text
the initial state
the final empty fixed-point check
an unexecuted round after MAX_ROUNDS
```

For example:

```text
initial:
A

round 1:
B

round 2:
C

termination check:
no new step
```

returns:

```text
round_count = 2
```

---

## Interaction with max_rounds

The Phase 5-30 `max_rounds` semantics are unchanged.

The round-limit check now uses:

```python
len(
  round_results
)
```

rather than the old raw history list.

For example:

```python
max_rounds=2
```

still means:

```text
allow at most two productive rounds
```

and:

```text
round_results length
=
productive round count
```

The termination reasons remain:

```python
InferenceTerminationReason.FIXED_POINT
InferenceTerminationReason.MAX_ROUNDS
```

Phase 5-31 changes only the representation of productive-round
history.

It does not change:

```text
fixed-point semantics
max-round semantics
duplicate semantics
premise matching semantics
rule application order
knowledge-state expansion semantics
```

---

## Current execution-result structure

After Phase 5-31, the detailed inference result is conceptually:

```text
InferenceRunResult
├── steps
├── round_results
│   ├── InferenceRoundResult
│   │   └── new_steps
│   ├── InferenceRoundResult
│   │   └── new_steps
│   └── ...
├── round_history
│   └── compatibility view of new_steps
├── round_count
└── termination_reason
```

This separates:

```text
run-level information
```

from:

```text
round-level information
```

for the first time.

The distinction will allow later inference phases to enrich individual
round traces without continually expanding `InferenceRunResult`
itself.

---

## Current limitations of round results

`InferenceRoundResult` currently records only:

```text
new_steps
```

It does not yet record:

```text
state before the round
state after the round
applicable inference rules
InferenceMatch objects
all candidate derived steps
candidates rejected as duplicates
rule-application counts
round index
timing information
performance information
```

In particular, it is not yet possible to inspect from the round result
alone:

```text
which matches were considered
which candidate conclusions were discarded
why a particular candidate did not enter the knowledge state
```

The current object should therefore be understood as:

```text
a structured container for productive-round output
```

rather than a complete inference execution trace.

---

## Tests

Run the inference-rule tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-31:

```text
223 passed in 4.45s
```

Phase 5-30 completed with:

```text
218 passed
```

so Phase 5-31 adds 5 tests.

The Phase 5-31 tests cover:

```text
InferenceRoundResult construction
InferenceRoundResult structural equality
structured round_results generation
productive-round ordering
round_history compatibility view
```

Existing Phase 5-29 / Phase 5-30 tests using:

```text
round_history
round_count
termination_reason
max_rounds
```

continue to pass.

---

## Phase 5-24 through Phase 5-31

The inference engine has now progressed through:

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
one-round genuinely-new delta
↓
Phase 5-28
automatic fixed-point iteration
↓
Phase 5-29
per-round history and structured run result
↓
Phase 5-30
bounded iteration and explicit termination reason
↓
Phase 5-31
structured per-round result objects
```

The execution model can now answer:

```text
What was derived?
In which productive round was it derived?
How many productive rounds ran?
Why did inference stop?
What is the structured result of each productive round?
```

---

## Next direction

`InferenceRoundResult` now provides a dedicated place for richer
execution-trace information.

The next natural extension is to record:

```text
which InferenceMatch objects were applied in each round
```

so that a productive round can describe not only:

```text
what new ProofSteps were accepted
```

but also:

```text
which rule / premise matches produced them
```

A possible next structure is:

```python
InferenceRoundResult(
  new_steps=...,
  matches=...,
)
```

After match history is available, later phases can distinguish:

```text
matched rules
candidate derived steps
accepted genuinely new steps
duplicate-rejected candidates
```

before moving on to more powerful matching semantics such as:

```text
alternative premise assignments
backtracking
expression-level patterns
pattern variables
variable bindings
substitution
```


## Phase 5-32: per-round inference-match tracing

Phase 5-32 extends the structured round result introduced in Phase
5-31.

`InferenceRoundResult` now records not only the genuinely new
`ProofStep` objects produced by a round, but also the
`InferenceMatch` objects found during that round.

Conceptually:

```text
available ProofSteps
+
InferenceRules
↓
find InferenceMatches
↓
apply matches
↓
candidate derived ProofSteps
↓
duplicate filtering
↓
genuinely new ProofSteps
```

is now represented by:

```python
InferenceRoundResult(
  new_steps=...,
  matches=...,
)
```

The two fields have intentionally different meanings.

```text
matches
=
all inference matches found before duplicate filtering

new_steps
=
only genuinely new ProofSteps added to the knowledge state
```

For example, two different inference rules may produce the same
conclusion:

```text
rule A
+
rule B
↓
same conclusion
```

In that case:

```text
matches = (
  match_from_rule_A,
  match_from_rule_B,
)
```

while:

```text
new_steps = (
  first_new_step,
)
```

because duplicate conclusions are still added only once.

Likewise, a rule may successfully match even when its generated
conclusion is already known.

In that case:

```text
matches != ()
new_steps == ()
```

This distinction allows the inference engine to preserve information
about:

* which rules were applicable
* which premises were selected
* which inference opportunities existed
* which matches actually contributed new knowledge

without changing the existing duplicate semantics of the knowledge
state.

A one-round structured result can now be obtained directly with:

```python
round_result = derive_inference_round_result(
  inference_rules,
  available_steps,
)
```

and inspected through:

```python
round_result.matches
round_result.new_steps
```

`derive_new_inference_steps()` remains the simpler API and returns only:

```python
round_result.new_steps
```

so existing callers that only need newly derived facts do not need to
handle match metadata.

The fixed-point runner also preserves these structured round results.

For example:

```python
result = run_inference_until_stable_with_history(
  inference_rules,
  initial_steps,
)
```

provides:

```python
result.round_results
```

where every productive round contains both:

```text
InferenceRoundResult
├── matches
└── new_steps
```

Therefore a multi-round inference execution can now answer both:

```text
What new facts were added in this round?
```

and:

```text
Which inference rules matched in this round?
```

The existing compatibility view:

```python
result.round_history
```

continues to expose only the per-round `new_steps`.

---

## Tests

Run the inference-rule tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-32:

```text
231 passed in 5.67s
```

Phase 5-32 adds coverage for:

```text
InferenceRoundResult.matches default
structured one-round derivation result
compatibility between structured and simple one-round APIs
no-match round result
preservation of all matches before duplicate filtering
per-round match recording in fixed-point inference
match preservation across multiple rounds
match preservation when the generated conclusion is already known
```

All 231 inference-rule pattern tests pass.

No regression was detected in the previously implemented:

```text
premise-pattern matching
inference-rule matching
premise search
rule applicability
InferenceMatch construction
InferenceMatch application
candidate derivation
duplicate-aware merging
one-round inference
fixed-point inference
round history
max-round termination
termination reasons
structured round results
```

---

## Current Phase 5 inference result structure

After Phase 5-32, the fixed-point inference result has the conceptual
structure:

```text
InferenceRunResult
├── steps
├── round_results
│   ├── round 1
│   │   ├── matches
│   │   └── new_steps
│   ├── round 2
│   │   ├── matches
│   │   └── new_steps
│   └── ...
├── round_history
├── round_count
└── termination_reason
```

where:

```text
steps
=
final accumulated knowledge state

round_results
=
structured information for productive rounds

round_history
=
compatibility view containing only new_steps

round_count
=
number of productive rounds

termination_reason
=
FIXED_POINT or MAX_ROUNDS
```

This gives the inference engine a first explicit execution trace.

It can now distinguish:

```text
rule matched
```

from:

```text
rule produced genuinely new knowledge
```

which will be important when later phases introduce more sophisticated
rule selection, diagnostics, proof tracing, and search strategies.

---

## Next direction

The round-level execution trace currently records:

```text
matches
new_steps
```

The next natural extension is to make the relationship between these
two layers more explicit.

A future round result may need to distinguish:

```text
matched rule
↓
candidate derived ProofStep
↓
accepted as genuinely new
```

from:

```text
matched rule
↓
candidate derived ProofStep
↓
discarded because conclusion was already known
```

or:

```text
matched rule
↓
candidate derived ProofStep
↓
discarded because another match produced the same conclusion first
```

This will make it possible to explain not only:

```text
what was derived
```

but also:

```text
why a matching inference did or did not change the knowledge state
```

without changing the current mathematical inference semantics.


## Phase 5-33: candidate and duplicate-rejection tracing

Phase 5-33 extends the per-round execution trace introduced in
Phase 5-31 and Phase 5-32.

A round can now preserve all four major stages of one-round inference:

```text
InferenceMatch
↓
candidate ProofStep
↓
duplicate filtering
├── accepted as genuinely new
└── rejected as duplicate
```

`InferenceRoundResult` now has the structure:

```python
@dataclass(frozen=True)
class InferenceRoundResult:
  new_steps: tuple[ProofStep, ...]
  matches: tuple[InferenceMatch, ...] = ()
  candidate_steps: tuple[ProofStep, ...] = ()
  duplicate_rejected_steps: tuple[ProofStep, ...] = ()
```

The fields have intentionally different meanings.

```text
matches
=
all InferenceMatch objects found for the round

candidate_steps
=
all ProofSteps produced by applying those matches,
before duplicate filtering

new_steps
=
candidate ProofSteps accepted as genuinely new knowledge

duplicate_rejected_steps
=
candidate ProofSteps rejected because their conclusions
were already present or had already been accepted earlier
in the same round
```

This makes the one-round execution pipeline directly inspectable:

```text
available ProofSteps
+
InferenceRules
↓
find_inference_matches()
↓
matches
↓
apply_inference_matches()
↓
candidate_steps
↓
partition_new_and_duplicate_proof_steps()
├── new_steps
└── duplicate_rejected_steps
```

---

## Candidate ProofSteps

Before Phase 5-33, `InferenceRoundResult` recorded:

```text
matches
new_steps
```

but did not preserve the actual ProofSteps produced by every match.

This meant that if a match successfully produced a conclusion that was
later rejected as a duplicate, the generated ProofStep itself was not
available from the round result.

Phase 5-33 adds:

```python
round_result.candidate_steps
```

which contains every derived ProofStep before duplicate filtering.

For example:

```text
rule A
↓
candidate X

rule B
↓
candidate X
```

produces:

```python
candidate_steps == (
  candidate_from_rule_A,
  candidate_from_rule_B,
)
```

even though only one candidate can enter the knowledge state.

Candidate order preserves inference-match order.

Therefore the relationship between:

```text
matches[i]
```

and:

```text
candidate_steps[i]
```

corresponds to the application of that match.

---

## Duplicate-rejected ProofSteps

Phase 5-33 also records candidate ProofSteps that were generated
successfully but did not expand the knowledge state.

These are available through:

```python
round_result.duplicate_rejected_steps
```

Duplicate rejection still uses the existing conclusion-equality
semantics:

```python
step.conclusion == known_conclusion
```

A candidate is rejected when its conclusion is already:

```text
present in the knowledge state
```

or:

```text
accepted earlier in the same round
```

For example:

```text
available:
A
X

rule:
A → X
```

produces:

```text
matches:
1 match

candidate_steps:
X

new_steps:
()

duplicate_rejected_steps:
X
```

The successful rule application is therefore no longer lost merely
because its conclusion was already known.

---

## Same-round duplicate rejection

Duplicate detection also applies between candidates generated in the
same round.

For example:

```text
rule A:
given → X

rule B:
given → X
```

produces:

```text
candidate_steps:
X from rule A
X from rule B
```

The first candidate is accepted:

```text
new_steps:
X from rule A
```

and the second is recorded as:

```text
duplicate_rejected_steps:
X from rule B
```

This preserves both derivations at the execution-trace level while
keeping the existing knowledge-state rule:

```text
only the first ProofStep for an equal conclusion is added
```

unchanged.

Phase 5-33 therefore begins preserving information about alternative
derivations even though alternative ProofSteps are still not stored in
the accumulated knowledge state itself.

---

## partition_new_and_duplicate_proof_steps()

The duplicate-partition logic is now available explicitly through:

```python
partition_new_and_duplicate_proof_steps(
  available_steps,
  candidate_steps,
)
```

It returns:

```python
(
  new_steps,
  duplicate_rejected_steps,
)
```

The function processes candidates in order.

Conceptually:

```text
seen conclusions
=
conclusions already present in available_steps

for each candidate:
  if conclusion already seen:
    reject as duplicate
  else:
    accept as new
    add conclusion to seen conclusions
```

Adding accepted conclusions immediately to the seen set is what makes
same-round duplicate detection possible.

Both:

```text
accepted candidate order
```

and:

```text
duplicate-rejected candidate order
```

are preserved.

---

## Detailed one-round result

`derive_inference_round_result()` now represents the complete currently
supported one-round inference trace:

```python
round_result = derive_inference_round_result(
  inference_rules,
  available_steps,
)
```

The result can be inspected through:

```python
round_result.matches
round_result.candidate_steps
round_result.new_steps
round_result.duplicate_rejected_steps
```

Conceptually:

```text
InferenceRoundResult
├── matches
├── candidate_steps
├── new_steps
└── duplicate_rejected_steps
```

The simpler API:

```python
derive_new_inference_steps()
```

continues to return only:

```python
round_result.new_steps
```

so callers that do not require execution-trace information remain
unaffected.

---

## Fixed-point inference

Productive round results preserved by:

```python
run_inference_until_stable_with_history()
```

now also contain candidate and duplicate-rejection information.

For example, suppose:

```text
round 1:
rule A derives B

round 2:
rule A derives B again
rule B derives C
```

Then round 2 can record:

```text
matches:
rule A
rule B

candidate_steps:
B
C

new_steps:
C

duplicate_rejected_steps:
B
```

This makes it possible to distinguish:

```text
rule did not match
```

from:

```text
rule matched and produced a candidate,
but the candidate was already known
```

which is important for diagnostics and proof tracing.

As before, `InferenceRunResult.round_results` stores only productive
rounds.

The final empty fixed-point check is not appended to `round_results`.

Therefore candidate or duplicate information from the final
non-productive termination check is currently not retained.

---

## Backward compatibility

The new `InferenceRoundResult` fields have empty-tuple defaults:

```python
candidate_steps: tuple[ProofStep, ...] = ()
duplicate_rejected_steps: tuple[ProofStep, ...] = ()
```

Therefore constructions such as:

```python
InferenceRoundResult(
  new_steps=(),
)
```

remain valid.

Existing APIs and semantics are preserved:

```text
round_history
round_count
termination_reason
max_rounds
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
```

The knowledge state still contains only genuinely new ProofSteps.

Phase 5-33 adds execution-trace information without changing the
mathematical inference result.

---

## Tests

Run the inference-rule tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-33:

```text
242 passed
```

Phase 5-32 completed with:

```text
231 passed
```

so Phase 5-33 adds 11 tests.

The Phase 5-33 tests cover:

```text
candidate_steps default value
duplicate_rejected_steps default value
partitioning new and duplicate candidates
same-round duplicate rejection
accepted-candidate order preservation
duplicate-rejected order preservation
candidate-step recording
already-known candidate recording
same-round duplicate candidate recording
candidate order preservation
per-round duplicate-rejection tracing during fixed-point inference
```

No regression was detected in the previously implemented:

```text
premise-pattern matching
inference-rule matching
premise search
rule applicability
InferenceMatch construction
InferenceMatch application
candidate derivation
duplicate-aware merging
one-round inference
fixed-point inference
round history
max-round termination
termination reasons
structured round results
per-round InferenceMatch tracing
```

---

## Current Phase 5 inference trace

After Phase 5-33, the inference trace is conceptually:

```text
InferenceRunResult
├── steps
├── round_results
│   ├── round 1
│   │   ├── matches
│   │   ├── candidate_steps
│   │   ├── new_steps
│   │   └── duplicate_rejected_steps
│   ├── round 2
│   │   ├── matches
│   │   ├── candidate_steps
│   │   ├── new_steps
│   │   └── duplicate_rejected_steps
│   └── ...
├── round_history
├── round_count
└── termination_reason
```

The one-round derivation path can now be inspected as:

```text
match
↓
candidate
↓
accepted or duplicate-rejected
```

This provides substantially more information than storing only the
final accumulated knowledge state.

---

## Phase 5-24 through Phase 5-33

The inference engine has now progressed through:

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
one-round genuinely-new delta
↓
Phase 5-28
automatic fixed-point iteration
↓
Phase 5-29
per-round history and structured run result
↓
Phase 5-30
bounded iteration and explicit termination reason
↓
Phase 5-31
structured per-round result objects
↓
Phase 5-32
per-round InferenceMatch tracing
↓
Phase 5-33
candidate and duplicate-rejection tracing
```

The execution model can now answer:

```text
Which rules matched?
Which ProofSteps did those matches generate?
Which candidates entered the knowledge state?
Which candidates were rejected as duplicates?
In which productive round did this happen?
Why did the overall inference run stop?
```

---

## Next direction

Phase 5-33 preserves:

```text
matches
candidate_steps
new_steps
duplicate_rejected_steps
```

but the relationship is still represented by parallel ordered
collections.

For each match, it is possible to infer that:

```text
matches[i]
↓
candidate_steps[i]
```

but acceptance or rejection is not yet represented by a dedicated
derivation-level object.

A natural future extension is therefore something conceptually like:

```text
InferenceApplicationResult
├── match
├── candidate_step
├── accepted
└── rejection_reason
```

This would make:

```text
match
→
candidate
→
acceptance decision
```

a first-class object rather than reconstructing the relationship from
multiple collections.

Possible later extensions include:

```text
alternative premise assignments
backtracking
expression-level patterns
pattern variables
variable bindings
substitution
alternative proof preservation
```

The current greedy matching and conclusion-equality semantics remain
unchanged.


## Phase 5-34: structured inference application results

Phase 5-34 introduces a derivation-level object connecting each
`InferenceMatch` directly to the candidate `ProofStep` produced by
applying that match.

Phase 5-33 recorded:

```text
matches
candidate_steps
new_steps
duplicate_rejected_steps
```

as separate ordered collections.

Because match order and candidate order were preserved, the
relationship:

```text
matches[i]
↓
candidate_steps[i]
```

could be reconstructed.

However, that relationship was still implicit.

Phase 5-34 makes it explicit through:

```python
@dataclass(frozen=True)
class InferenceApplicationResult:
  match: InferenceMatch
  candidate_step: ProofStep
```

An individual rule application is therefore represented as:

```text
InferenceApplicationResult
├── match
└── candidate_step
```

This provides a first-class representation of:

```text
which inference match was applied
```

and:

```text
which candidate ProofStep that application produced
```

---

## InferenceApplicationResult

An `InferenceApplicationResult` represents one application of one
`InferenceMatch`.

For example:

```python
application_result = InferenceApplicationResult(
  match=match,
  candidate_step=candidate_step,
)
```

contains:

```text
match
=
the InferenceRule and selected premises

candidate_step
=
the ProofStep generated by applying that match
```

Conceptually:

```text
InferenceRule
+
selected premises
↓
InferenceMatch
↓
rule application
↓
candidate ProofStep
```

is represented by:

```text
InferenceApplicationResult
├── match
│   ├── inference_rule
│   └── premises
└── candidate_step
```

Because `InferenceApplicationResult` is a frozen dataclass, it also
supports structural equality.

---

## apply_inference_matches_with_results()

Phase 5-34 adds:

```python
apply_inference_matches_with_results(
  inference_matches,
)
```

This applies one or more `InferenceMatch` objects and returns:

```text
tuple[InferenceApplicationResult, ...]
```

rather than returning only candidate ProofSteps.

For example:

```python
results = apply_inference_matches_with_results(
  inference_matches,
)
```

provides:

```python
results[0].match
results[0].candidate_step
```

for the first application.

The function preserves input match order.

Therefore:

```text
inference_matches[i]
```

corresponds directly to:

```text
results[i].match
```

and the candidate produced from that match is:

```text
results[i].candidate_step
```

The existing:

```python
apply_inference_matches()
```

API remains available and continues to return only:

```text
tuple[ProofStep, ...]
```

for callers that do not require derivation-level trace information.

---

## Per-round application results

`InferenceRoundResult` now includes:

```python
application_results: tuple[
  InferenceApplicationResult,
  ...
] = ()
```

Its full Phase 5-34 structure is:

```python
@dataclass(frozen=True)
class InferenceRoundResult:
  new_steps: tuple[ProofStep, ...]
  matches: tuple[InferenceMatch, ...] = ()
  candidate_steps: tuple[ProofStep, ...] = ()
  duplicate_rejected_steps: tuple[ProofStep, ...] = ()
  application_results: tuple[
    InferenceApplicationResult,
    ...
  ] = ()
```

The fields now describe different views of the same round:

```text
matches
=
all inference matches found

application_results
=
explicit match → candidate application records

candidate_steps
=
all candidates generated by those applications

new_steps
=
candidates accepted into the knowledge state

duplicate_rejected_steps
=
candidates rejected by conclusion equality
```

---

## Relationship with existing round fields

For a round result:

```python
round_result
```

the following correspondence holds:

```python
tuple(
  result.match
  for result
  in round_result.application_results
) == round_result.matches
```

and:

```python
tuple(
  result.candidate_step
  for result
  in round_result.application_results
) == round_result.candidate_steps
```

Thus the Phase 5-33 fields are preserved.

`application_results` does not replace:

```text
matches
candidate_steps
new_steps
duplicate_rejected_steps
```

at this stage.

Instead, it introduces an explicit derivation-level relationship
between:

```text
match
```

and:

```text
candidate
```

while retaining the existing round-level views.

---

## Duplicate candidates and application results

`InferenceApplicationResult` is created before duplicate filtering.

Therefore application results preserve successful rule applications
even when their candidates do not enter the knowledge state.

For example:

```text
rule A
↓
candidate X

rule B
↓
candidate X
```

produces conceptually:

```text
application_results:
  application A:
    match = match A
    candidate = X from rule A

  application B:
    match = match B
    candidate = X from rule B
```

while duplicate filtering produces:

```text
new_steps:
X from rule A

duplicate_rejected_steps:
X from rule B
```

Both applications remain visible.

This preserves the distinction between:

```text
rule application happened
```

and:

```text
candidate changed the knowledge state
```

---

## Acceptance status is not yet part of InferenceApplicationResult

Phase 5-34 does not yet add:

```text
accepted
rejected
rejection_reason
```

to `InferenceApplicationResult`.

The object currently represents only:

```text
match
↓
candidate
```

Acceptance is still determined by the existing round-level partition:

```text
candidate_steps
↓
partition_new_and_duplicate_proof_steps()
├── new_steps
└── duplicate_rejected_steps
```

Therefore a caller that needs to know whether a candidate was accepted
must still compare the candidate with:

```text
new_steps
```

and:

```text
duplicate_rejected_steps
```

Phase 5-34 intentionally separates:

```text
application representation
```

from:

```text
acceptance-decision representation
```

so that these concerns can be extended independently.

---

## Fixed-point inference

Application results are also preserved in productive rounds returned
by:

```python
run_inference_until_stable_with_history()
```

For example:

```text
round 1:
rule A derives B

round 2:
rule A derives B again
rule B derives C
```

can now be represented as:

```text
round 1
├── application_results
│   └── rule A match → B
├── candidate_steps
│   └── B
├── new_steps
│   └── B
└── duplicate_rejected_steps
    └── ()

round 2
├── application_results
│   ├── rule A match → B
│   └── rule B match → C
├── candidate_steps
│   ├── B
│   └── C
├── new_steps
│   └── C
└── duplicate_rejected_steps
    └── B
```

Thus multi-round execution can now directly answer:

```text
Which match produced this candidate?
```

without reconstructing the relationship from parallel collections.

As before, only productive rounds are stored in:

```python
result.round_results
```

The final non-productive fixed-point check is not stored.

---

## Backward compatibility

The new field has an empty-tuple default:

```python
application_results: tuple[
  InferenceApplicationResult,
  ...
] = ()
```

Therefore existing constructions such as:

```python
InferenceRoundResult(
  new_steps=(),
)
```

remain valid.

Existing APIs remain available:

```text
apply_inference_match()
apply_inference_matches()
derive_inference_steps()
derive_new_inference_steps()
run_inference_round()
run_inference_until_stable()
run_inference_until_stable_with_history()
round_history
round_count
termination_reason
max_rounds
```

Phase 5-34 changes the execution trace representation without changing
the mathematical inference result.

---

## Tests

Run the inference-rule tests with:

```powershell
python -m pytest tests/test_inference_rule_pattern.py -v
```

At the completion of Phase 5-34:

```text
255 passed in 1.06s
```

Phase 5-33 completed with:

```text
242 passed
```

so Phase 5-34 adds 13 tests.

The Phase 5-34 tests cover:

```text
InferenceApplicationResult construction
InferenceApplicationResult structural equality
application_results default value
single application result generation
multiple application result generation
application-result order preservation
empty application collection
list input normalization
invalid application-result input rejection
round-level application-result recording
consistency with matches
consistency with candidate_steps
duplicate-candidate preservation
fixed-point per-round application-result preservation
```

The new application-result trace was also verified together with the
existing:

```text
new_steps
duplicate_rejected_steps
```

partition.

All 255 inference-rule pattern tests pass.

---

## Current Phase 5 inference trace

After Phase 5-34, the inference trace is conceptually:

```text
InferenceRunResult
├── steps
├── round_results
│   ├── round 1
│   │   ├── matches
│   │   ├── application_results
│   │   │   ├── match → candidate
│   │   │   └── ...
│   │   ├── candidate_steps
│   │   ├── new_steps
│   │   └── duplicate_rejected_steps
│   ├── round 2
│   │   └── ...
│   └── ...
├── round_history
├── round_count
└── termination_reason
```

The derivation path is now:

```text
InferenceMatch
↓
InferenceApplicationResult
↓
candidate ProofStep
↓
duplicate partition
├── accepted as new
└── duplicate rejected
```

Phase 5-33 could observe all of these stages through separate round
collections.

Phase 5-34 additionally makes:

```text
match → candidate
```

an explicit object-level relationship.

---

## Phase 5-24 through Phase 5-34

The inference engine has now progressed through:

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
one-round genuinely-new delta
↓
Phase 5-28
automatic fixed-point iteration
↓
Phase 5-29
per-round history and structured run result
↓
Phase 5-30
bounded iteration and explicit termination reason
↓
Phase 5-31
structured per-round result objects
↓
Phase 5-32
per-round InferenceMatch tracing
↓
Phase 5-33
candidate and duplicate-rejection tracing
↓
Phase 5-34
structured match-to-candidate application results
```

The execution model can now answer:

```text
Which rules matched?
Which premises were selected?
Which candidate did each match generate?
Which candidates entered the knowledge state?
Which candidates were rejected as duplicates?
In which productive round did this happen?
Why did the overall inference run stop?
```

---

## Next direction

`InferenceApplicationResult` currently records:

```text
match
candidate_step
```

The next natural extension is to record the result of duplicate
filtering on the same object.

Conceptually:

```text
InferenceApplicationResult
├── match
├── candidate_step
├── accepted
└── rejection_reason
```

or an equivalent status representation could allow each application
to answer directly:

```text
Was this candidate accepted?
```

and:

```text
If not, why was it rejected?
```

Possible rejection reasons could eventually distinguish:

```text
conclusion already known before the round
same conclusion accepted earlier in the round
other future rejection policies
```

This would extend the current:

```text
match
→
candidate
```

object into:

```text
match
→
candidate
→
decision
```

without changing the existing knowledge-state semantics.

Later phases can then proceed toward:

```text
alternative premise assignments
backtracking
expression-level patterns
pattern variables
variable bindings
substitution
alternative proof preservation
```

while keeping the execution trace explicit.










