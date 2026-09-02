# EHP Proof Tracer

A computational tool for tracing calculations and mathematical inference in
EHP exact sequences for unstable homotopy groups of spheres.

## Goal

The long-term goal is to explain how homotopy groups of spheres are determined
from mathematical input such as:

- EHP exact sequences,
- element orders,
- additive relations,
- Suspension and Freudenthal theory,
- composition,
- generalized Hopf invariants,
- homomorphisms,
- subgroup / modulo information,
- symbolic scalar constraints,
- indeterminacy,
- Toda brackets,
- typed homotopy elements,
- structured generator notation,
- literature-backed theorem repositories,
- explicit generator / composition / map facts,
- map properties,
- Toda composition formulas,
- smash-product expressions,
- and later stable-homotopy information.

The project separates:

```text
mathematical rule / theorem
knowledge / fact supply
generic inference mechanism
abelian-group calculation
```

Development principle:

```text
actual mathematical need
↓
minimal representation
↓
explicit fact / domain rule when needed
↓
existing generic engine
```

---

# Current status

Completed:

- Phase 1: finite abelian-group calculations
- Phase 2: structured subgroup calculations
- Phase 3: quotient / exact sequence / extension
- Phase 4: presentation-based finitely generated abelian groups
- Phase 5: generic proof / inference engine
- Phase 6: EHP domain inference
- Phase 7: ORDER reasoning
- Phase 8: Suspension reasoning
- Phase 9: Freudenthal / stable-range reasoning
- Phase 10: composition / Suspension-composition functoriality
- Phase 11: generalized Hopf-invariant reasoning
- Phase 12: additive expressions
- Phase 13: homomorphism reasoning
- Phase 14: set / subgroup reasoning
- Phase 15: coset / modulo reasoning
- Phase 16: symbolic scalar constraints
- Phase 17: indeterminacy
- Phase 18: Toda bracket minimum representation
- Phase 19: Toda membership / first theorem bridge
- Phase 20: indexed unstable Toda notation
- Phase 21: typed homotopy elements / source-target context
- Phase 22: structured generator representation
- Phase 23: indexed Toda theorem / validity connection
- Phase 24: theorem fact / knowledge-table integration
- Phase 25: generator typing / ambient-group facts
- Phase 26: actual Toda-generator typing expansion
- Phase 27: corrected actual ε₃ Toda-definedness / end-to-end inference
- Phase 28: map-property equality-reflection foundation
- Phase 29: actual H map facts / typing / production-fact connection
- Phase 30: Toda Prop.2.2 right suspended-composition formula
- Phase 31: SmashProduct minimum structural representation
- Phase 32: Toda Prop.2.2 left suspended-composition formula

Current architecture:

```text
literature-backed theorem facts / repository
explicit generator facts / repository
explicit composition facts / repository
explicit map facts / repository
        ↓
homotopy / EHP / map-property domain rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy / Toda / map-property statements
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

---

# Expression model

Current expression classes include:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── SmashProduct
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

Separate structural objects include:

```text
MapSymbol
ScalarSymbol
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

Important boundaries remain explicit:

```text
representation
!=
typing
!=
theorem knowledge
```

and:

```text
type-compatible
!=
zero composition
!=
Toda definedness
```

---

# Actual H map foundation

Phase 29 connected the actual Hopf map to the generic map-property machinery.

Production map identity:

```text
HOPF_MAP
=
EHP_H_MAP
=
MapSymbol(name="H")
```

Production typing fact:

```text
H : π₃(S²) → π₃(S³)
```

Production property fact:

```text
H : π₃(S²) → π₃(S³)
is an isomorphism
```

Representative proof chain:

```text
production H isomorphism fact
↓
ProofStep.GIVEN Isomorphism(H)
↓
Injective(H)

+

H(a)=H(b)
↓
a=b
```

The map identity, map typing, and map property remain distinct objects.

---

# Toda Prop.2.2

Both formulas are now represented as direct theorem rules.

## Right formula

```text
H(a ∘ Eb)=H(a) ∘ Eb
```

Production rule:

```text
toda_prop22_right_inference_rule(alpha=a, gamma=b)
```

The theorem requires no concrete fact of the form:

```text
H(a)=β
```

Its proof-level conclusion directly uses the canonical production `H` map.

A concrete fact:

```text
H(a)=β
```

can still be used in the existing generalized Hopf machinery to derive the
corresponding specialized expression. That β-based branch is retained as an
integration / consistency path, not as the statement or proof of Prop.2.2
itself.

## Left formula

```text
H((Ec) ∘ a)=E(c ∧ c) ∘ H(a)
```

Production rule:

```text
toda_prop22_left_inference_rule(alpha=a, gamma=c)
```

Again, no concrete Hopf value `H(a)=β` is required to state or apply the
theorem.

The conclusion is an actual proof-level equality:

```text
Relation(
  lhs=H((Ec)∘a),
  rhs=E(c∧c)∘H(a),
  relation_type=EQUALITY,
)
```

Both occurrences of `H` preserve the canonical production map identity.

---

# Phase 30 design correction

Phase 30 originally reached:

```text
H(a∘Eb)=H(a)∘Eb
```

through a concrete value `H(a)=β`, generalized Hopf reasoning, equality
symmetry, staged right composition, and transitivity.

That path remains useful as an integration / specialization regression.

The current theorem design is now:

```text
Toda Prop.2.2
↓
H(a∘Eb)=H(a)∘Eb
```

directly.

The β-based path is checked to agree with the direct theorem result.

---

# Phase 31: SmashProduct minimum representation

Phase 31 added:

```text
SmashProduct(
  left=a,
  right=b,
)
```

for structural expressions such as:

```text
a ∧ b
c ∧ c
E(c ∧ c)
```

`SmashProduct` is structural syntax only.

It does not currently provide:

- source / target typing,
- symmetry or commutativity rules,
- associativity rules,
- normalization,
- Barratt–Hilton theorem knowledge,
- automatic conversion to composition expressions.

Current boundary:

```text
SmashProduct(c,c)
→ no source / target attributes
```

and:

```text
E(c∧c).source = None
E(c∧c).target = None
```

---

# Phase 32: Toda Prop.2.2 left formula

Phase 32 connected the Phase 31 smash-product structure to the actual `H` map
and proof-level equality representation.

Direct theorem:

```text
a, c
↓ Toda Prop.2.2
H((Ec)∘a)=E(c∧c)∘H(a)
```

Core production rule:

```text
toda_prop22_left_inference_rule()
```

The rule:

- requires no `H(a)=β` premise,
- produces a `RelationType.EQUALITY`,
- preserves the canonical `HOPF_MAP / EHP_H_MAP` identity,
- preserves `Suspension(c)`,
- preserves `Suspension(SmashProduct(c,c))`,
- does not add smash-product typing,
- does not add Barratt–Hilton knowledge,
- does not modify the generic inference engine.

The previous β-based Phase 32 branch is retained as a specialization /
consistency path:

```text
H(a)=β
↓
H((Ec)∘a)=E(c∧c)∘β
```

together with the existing equality machinery. Its final result is checked to
agree with the direct Toda Prop.2.2 theorem.

---

# Phase 32 representative capability demo

Run:

```powershell
python -m probes.probe_phase32_capabilities
```

Representative output:

```text
Toda Prop.2.2 left formula

Theorem:
  H((Ec)∘a)=E(c∧c)∘H(a)

Parameters:
  a = a
  c = c

[1] Apply Toda Prop.2.2
  inference: Toda Prop.2.2 left formula
  premises: none

[CONCLUSION]
  H(E(c)∘a)=E((c∧c))∘H(a)

Structural confirmation:
  lhs correct = True
  rhs correct = True
  actual H map preserved = True
```

The probe also displays the current Phase 32 boundary:

```text
SmashProduct has source: False
SmashProduct has target: False
E(c∧c).source = None
E(c∧c).target = None
```

---

# Tests

Phase 30 focused suite:

```powershell
python -m pytest tests/test_phase30_prop22.py -q
```

Verified:

```text
25 passed
```

Phase 32 focused suite:

```powershell
python -m pytest tests/test_phase32_prop22.py -q
```

Verified:

```text
39 passed
```

Related suites:

```powershell
python -m pytest tests/test_hopf_rules.py -q
python -m pytest tests/test_map_facts.py -q
```

Verified:

```text
31 passed
54 passed
```

Full suite:

```powershell
python -m pytest -q
```

Verified at Phase 32 completion:

```text
1512 passed in 63.58s
```

No failures.

---

# Representative capability demos

```powershell
python -m probes.probe_phase25_capabilities
python -m probes.probe_phase26_capabilities
python -m probes.probe_phase27_capabilities
python -m probes.probe_phase28_capabilities
python -m probes.probe_phase29_capabilities
python -m probes.probe_phase30_capabilities
python -m probes.probe_phase31_capabilities
python -m probes.probe_phase32_capabilities
```

The current Phase 32 probe is the canonical demonstration of the left
Toda Prop.2.2 theorem.

The historical β-based Phase 30 / Phase 32 branches remain useful for
integration testing but are not the canonical statement of Prop.2.2.

---

# Current non-goals

Not currently implemented:

- general smash-product typing,
- smash-product algebra / normalization,
- automatic Barratt–Hilton simplification,
- symbolic scalar-expression trees such as `(-1)^n`,
- parity reduction for symbolic signs,
- Toda Prop.3.1 Barratt–Hilton,
- automatic calculation of `H((2ι₂)η₂)`,
- actual equality `H((2ι₂)η₂)=H(4η₂)`,
- final equality `(2ι₂)η₂=4η₂`,
- general theorem quantification / automatic theorem instantiation,
- stable homotopy-group model,
- stable Toda brackets,
- higher / variable-arity Toda brackets.

---

# Documentation

- `README.md` — current capabilities and current status
- `docs/design.md` — current architecture, semantics, and design boundaries
- `docs/development_log.md` — chronological implementation history
- `docs/roadmap.md` — future capabilities and dependency order

Historical statements in the development log describe the state at that time.
Current behavior is defined by the latest README and design documents.

---

# Next development boundary

Phase 32 completes both sides of Toda Prop.2.2:

```text
H(a∘Eb)=H(a)∘Eb

H((Ec)∘a)=E(c∧c)∘H(a)
```

The next mathematical target is the Barratt–Hilton layer required for the
actual calculation of:

```text
H((2ι₂)η₂)
```

The immediate next phase should introduce only the minimum prerequisite that
is actually needed for Toda Prop.3.1, with the strongest current candidate
being symbolic sign / parity support for expressions such as:

```text
(-1)^n
```

Existing `IteratedSuspension` should be reused and expanded only if a concrete
Barratt–Hilton typing requirement cannot be expressed with the current model.

Longer dependency:

```text
Phase 29
actual H map facts / equality reflection
↓
Phase 30
Toda Prop.2.2 right formula COMPLETE
↓
Phase 31
SmashProduct minimum representation COMPLETE
↓
Phase 32
Toda Prop.2.2 left formula COMPLETE
↓
minimal Barratt–Hilton prerequisites
↓
Toda Prop.3.1 Barratt–Hilton
↓
actual H((2ι₂)η₂) calculation
↓
H((2ι₂)η₂)=H(4η₂)
↓
existing Injective(H) equality reflection
↓
(2ι₂)η₂=4η₂
```
