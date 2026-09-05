# EHP Proof Tracer Roadmap

## 1. 文書の役割

```text
README.md
=
current capabilities / status

docs/design.md
=
current architecture / semantics / boundaries

docs/development_log.md
=
chronological implementation history

docs/roadmap.md
=
future capability dependency
```

---

# 2. Phase 44 完了時点

Completed chain:

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left
Phase 33  Barratt–Hilton prerequisites
Phase 34  Toda Prop.3.1 Barratt–Hilton theorem rules
Phase 35  actual H((2ι₂)η₂) calculation
Phase 36  actual H(4η₂) calculation
Phase 37  actual H-side equality closure
Phase 38  Injective(H) reflection
Phase 39  PrimaryComponent minimum representation
Phase 40  TodaPrimaryGroup minimum representation
Phase 41  PreimageSubgroup minimum representation
Phase 42  WhiteheadProduct minimum representation
Phase 43  Toda Lemma 4.1 premise minimum representation
Phase 44  Toda Lemma 4.1 case semantics
```

Current full regression:

```text
1957 passed in 75.54s
```

Focused Phase 44:

```text
94 passed
```

Representative probe:

```powershell
python -m probes.probe_phase44_capabilities
```

---

# 3. Phase 44 completed capabilities

```text
symbolic GeneratorSymbol index
symbolic HomotopyElement dimension
FreeCyclicGroup
DirectSumGroup
PrimaryComponentMembershipStatement
Toda Lemma 4.1 odd case rule
Toda Lemma 4.1 even/nonzero case rule
Toda Lemma 4.1 even/zero group rule
Toda Lemma 4.1 zero-case Hopf condition rule
Toda Lemma 4.1 zero-case suspension-primary rule
case applicability / exclusivity
provenance
fixed-point integration
representative probe
```

---

# 4. Toda Lemma 4.1 completed theorem branch

```text
n odd
↓
π_{2n-1}^n = π_{2n-1}(S^n;2)
```

```text
n even
+
[ι_{n-1},ι_{n-1}] != 0
↓
π_{2n-1}^n = Z{P(ι_{2n+1})} ⊕ π_{2n-1}(S^n;2)
```

```text
n even
+
[ι_{n-1},ι_{n-1}] = 0
↓
π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)
```

with:

```text
H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```

---

# 5. Current deferred boundaries

未実装:

```text
automatic compound parity inference
general symbolic scalar simplification
general SmashProduct typing / algebra / normalization
symbolic suspension source / target arithmetic
Toda (2.1) general rule set
universal arbitrary-map equality congruence
automatic identity semantics from ι notation
Toda (4.2) Serre finiteness fact
Toda (4.3) evaluated definition
automatic Whitehead-product zero inference
automatic Whitehead-product nonzero inference
ZERO / INEQUALITY contradiction detection
Whitehead-product bilinearity
Whitehead-product antisymmetry
general existential quantification / witness objects
automatic α existence / uniqueness
PrimaryComponent membership → ordinary membership bridge
Toda Prop.4.2 2-primary EHP exact sequence
Toda (4.5) stable-range suspension isomorphism
Toda Prop.4.4 decomposition isomorphism
Toda Prop.4.4 consequence: E injective on π_i^n
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 6. Capability matrix

| capability | status | phase |
|---|---|---|
| map injectivity / equality reflection | IMPLEMENTED | 28 |
| actual H facts / typing | IMPLEMENTED | 29 |
| Toda Prop.2.2 right | IMPLEMENTED | 30 |
| SmashProduct | IMPLEMENTED | 31 |
| Toda Prop.2.2 left | IMPLEMENTED | 32 |
| ScalarExpression tree | IMPLEMENTED | 33 |
| parity → symbolic sign evaluation | IMPLEMENTED | 33 |
| symbolic IteratedSuspension exponent | IMPLEMENTED | 33 |
| Toda Prop.3.1 Barratt–Hilton | IMPLEMENTED | 34 |
| actual `H((2ι₂)η₂)=4ι₃` | IMPLEMENTED | 35 |
| `H(4η₂)=4ι₃` | IMPLEMENTED | 36 |
| `H((2ι₂)η₂)=H(4η₂)` | IMPLEMENTED | 37 |
| `(2ι₂)η₂=4η₂` | IMPLEMENTED | 38 |
| p-primary component `π_i(S^n;p)` | IMPLEMENTED | 39 |
| Toda subgroup `π_i^n` | IMPLEMENTED | 40 |
| `E^{-1}(π_{2n}(S^{n+1};2))` preimage group | IMPLEMENTED | 41 |
| Whitehead product `[a,b]` | IMPLEMENTED | 42 |
| Toda Lemma 4.1 premise zero / nonzero representation | IMPLEMENTED | 43 |
| symbolic `ι_{n-1}` / `ι_{2n±1}` | IMPLEMENTED | 44 |
| symbolic free cyclic group `Z{α}` | IMPLEMENTED | 44 |
| symbolic direct-sum group | IMPLEMENTED | 44 |
| primary-component membership statement | IMPLEMENTED | 44 |
| Toda Lemma 4.1 odd case | IMPLEMENTED | 44 |
| Toda Lemma 4.1 even / Whitehead nonzero case | IMPLEMENTED | 44 |
| Toda Lemma 4.1 even / Whitehead zero case | IMPLEMENTED | 44 |
| zero-case `H(α)=ι_{2n-1}` | IMPLEMENTED | 44 |
| zero-case `Eα∈π_{2n}(S^{n+1};2)` | IMPLEMENTED | 44 |
| Toda Prop.4.2 2-primary EHP exact sequence | NEXT | 45 |
| Toda (4.5) `E^(m-n)` isomorphism | PLANNED | later |
| Toda Prop.4.4 decomposition isomorphism | PLANNED | later |
| Toda Prop.4.4 `E` injectivity consequence | PLANNED | later |
| stable homotopy | PLANNED | later |
| higher Toda bracket | DEFERRED | concrete need |

---

# 7. Long-term dependency

```text
Phase 29
actual H equality-reflection foundation
↓
Phase 30
Toda Prop.2.2 right COMPLETE
↓
Phase 31
SmashProduct COMPLETE
↓
Phase 32
Toda Prop.2.2 left COMPLETE
↓
Phase 33
Barratt–Hilton prerequisites COMPLETE
↓
Phase 34
Toda Prop.3.1 Barratt–Hilton COMPLETE
↓
Phase 35
actual H((2ι₂)η₂)=4ι₃ COMPLETE
↓
Phase 36
H(4η₂)=4ι₃ COMPLETE
↓
Phase 37
H((2ι₂)η₂)=H(4η₂) COMPLETE
↓
Phase 38
Injective(H) reflection COMPLETE
↓
(2ι₂)η₂=4η₂ COMPLETE

actual equality branch COMPLETE
```

parallel Chapter 4 branch:

```text
Toda (4.2)
Serre finiteness
↓
Phase 39
PrimaryComponent π_i(S^n;p) COMPLETE
↓
Phase 40
TodaPrimaryGroup π_i^n COMPLETE
↓
Phase 41
PreimageSubgroup COMPLETE
↓
Phase 42
WhiteheadProduct COMPLETE
↓
Phase 43
Toda Lemma 4.1 premise representation COMPLETE
↓
Phase 44
Toda Lemma 4.1 case semantics COMPLETE
↓
Phase 45
Toda Prop.4.2 2-primary EHP exact sequence
↓
Toda (4.5)
stable-range E^(m-n) isomorphism
↓
Toda Prop.4.4
π_i^n decomposition isomorphism
↓
E is injective
↓
existing equality / ZERO reflection machinery
↓
2-primary calculations
```

---

# 8. Phase 45 candidate：Toda Prop.4.2

NEXT。

Phase 44 で critical Toda group structure を theorem-level に表現可能になった。

次の対象:

```text
Toda Proposition 4.2
2-primary EHP exact sequence
```

実装前 compatibility check:

```text
current EHP exactness representation
current E / H / P map terms
PrimaryComponent
TodaPrimaryGroup
PreimageSubgroup
Toda Prop.4.2 exact statement
```

Phase 45 で確認すべき点:

```text
ordinary EHP exactness object を再利用できるか
2-primary component を sequence object の term として保持できるか
TodaPrimaryGroup と PrimaryComponent の役割をどう分離するか
map source / target を symbolic degree で lossless に置けるか
theorem provenance を既存 ProofStep で保持できるか
```

---

# 9. Phase 45 non-goals

Phase 45 では先取りしない:

```text
Toda (4.5)
Toda Prop.4.4
general stable homotopy
general Whitehead-product algebra
automatic Whitehead zero / nonzero solver
general existential witness engine
general symbolic dimension solver
```

実装順序:

```text
compatibility check
↓
minimum representation
↓
theorem rule
↓
applicability / provenance
↓
representative probe
↓
full regression
```

---

# 10. Testing principle

各 layer で:

1. representation
2. structural distinction
3. applicability
4. invalid-case behavior
5. typing compatibility
6. integration
7. provenance
8. representative scenario
9. scope
10. full regression
11. executable probe

を確認する。

---

# 11. Phase 44 verified status

focused:

```text
tests/test_phase44_toda_lemma41_case_semantics.py
94 passed
```

related:

```text
tests/test_toda_rules.py
66 passed

tests/test_phase43_toda_lemma41_premise.py
32 passed

tests/test_phase39_primary_component.py
24 passed

tests/test_hopf_rules.py
31 passed

tests/test_expression.py
145 passed
```

full:

```text
1957 passed in 75.54s
```

probe:

```powershell
python -m probes.probe_phase44_capabilities
```

result:

```text
odd case
→ π_{2n-1}^n = π_{2n-1}(S^n;2)

even / nonzero case
→ π_{2n-1}^n = Z{P(ι_{2n+1})} ⊕ π_{2n-1}(S^n;2)

even / zero case
→ π_{2n-1}^n = Z{α} ⊕ π_{2n-1}(S^n;2)

H(α)=ι_{2n-1}
Eα ∈ π_{2n}(S^{n+1};2)
```
