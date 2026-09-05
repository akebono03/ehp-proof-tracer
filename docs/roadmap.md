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

# 2. Phase 47 完了時点

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
Phase 45  Toda Proposition 4.2 2-primary EHP exact sequence
Phase 46  Toda (4.5) stable-range E^(m-n) isomorphism
Phase 47  Toda Proposition 4.4 decomposition isomorphism
```

Current full regression:

```text
2277 passed in 55.61s
```

Representative probe:

```powershell
python -m probes.probe_phase47_capabilities
```

---

# 3. Phase 47 completed capabilities

```text
TodaPrimaryGroupMembershipStatement
DirectSumGroup TodaPrimaryGroup summands
symbolic Proposition 4.4 source / target
TodaProp44DecompositionMap
structural Eβ+α∘γ formula
TodaProp44IsomorphismStatement
Toda Proposition 4.4 theorem rule
positive / negative Hopf applicability
guard-aware applicability
invalid-case rejection
cross-instance rejection
theorem provenance
one-round fixed-point integration
representative probe
```

---

# 4. Toda (4.5) completed theorem branch

premises:

```text
n ≥ k+2
m ≥ n
```

map:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

theorem result:

```text
Toda45IsomorphismStatement(
  map=<specific TodaIteratedSuspensionMap>
)
```

meaning:

```text
the supplied E^(m-n) map instance
is an isomorphism by Toda (4.5)
```

---

# 5. Phase 46 architecture result

```text
ScalarGreaterEqualStatement
=
structural inequality premise
```

```text
TodaIteratedSuspensionMap
=
instance-aware map-level source / target / exponent structure
```

```text
Toda45IsomorphismStatement
=
instance-aware Toda theorem isomorphism
```

Current generic boundary:

```text
IsomorphismStatement.map
=
MapSymbol

InjectiveMapStatement.map
=
MapSymbol
```

therefore:

```text
TodaIteratedSuspensionMap
!= MapSymbol
```

and Phase 46 intentionally does not add:

```text
Toda45IsomorphismStatement
→ IsomorphismStatement
→ InjectiveMapStatement
```

generic inference engine and generic map-property API remain unchanged.

---

# 6. Current deferred boundaries

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
symbolic map typing solver
general symbolic dimension solver
automatic symbolic image/kernel group construction
instance-aware generic ExactnessStatement
general symbolic inequality solver
automatic numeric inequality validation
generic map-property type generalization
Toda45IsomorphismStatement → IsomorphismStatement bridge
generic injectivity consequence for TodaIteratedSuspensionMap
Toda Prop.4.4 consequence: E injective on π_i^n
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 7. Capability matrix

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
| symbolic E / H / Δ map terms | IMPLEMENTED | 45 |
| symbolic Toda EHP long sequence | IMPLEMENTED | 45 |
| instance-aware exactness window | IMPLEMENTED | 45 |
| Toda Prop.4.2 E-H exactness | IMPLEMENTED | 45 |
| Toda Prop.4.2 H-Δ exactness | IMPLEMENTED | 45 |
| Toda Prop.4.2 Δ-E exactness | IMPLEMENTED | 45 |
| Toda exactness → generic exactness bridge | IMPLEMENTED | 45 |
| Toda Prop.4.2 → zero-composition reuse | IMPLEMENTED | 45 |
| Toda (4.5) `E^(m-n)` isomorphism | IMPLEMENTED | 46 |
| Toda Prop.4.4 decomposition isomorphism | IMPLEMENTED | 47 |
| Toda Prop.4.4 `E` injectivity consequence | NEXT | 48 candidate |
| stable homotopy | PLANNED | later |
| higher Toda bracket | DEFERRED | concrete need |

---

# 8. Long-term dependency

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
Toda Prop.4.2 2-primary EHP exact sequence COMPLETE
↓
Phase 46
Toda (4.5)
stable-range E^(m-n) isomorphism COMPLETE
↓
Phase 47
Toda Prop.4.4
π_i^n decomposition isomorphism COMPLETE
↓
Phase 48 candidate
Toda Prop.4.4 consequence
E is injective
↓
existing equality / ZERO reflection machinery
↓
2-primary calculations
```

---

# 9. Phase 46：Toda (4.5) COMPLETE

Toda (4.5):

```text
n ≥ k+2
m ≥ n
```

のとき:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

は isomorphism。

implemented layers:

```text
ScalarGreaterEqualStatement
↓
TodaIteratedSuspensionMap
↓
Toda45IsomorphismStatement
```

applicability:

```text
n ≥ k+2
m ≥ n
source = π_{n+k}^n
target = π_{m+k}^m
exponent = m-n
```

を同一 symbolic instance として guard-aware に確認。

representative:

```text
3 GIVEN premises
↓
1 Toda45IsomorphismStatement
↓
fixed point
```

generic map-property bridge は type boundary のため deferred。

---

# 10. Phase 46 verified status

focused:

```text
tests/test_phase46_toda_45_compatibility.py
17 passed

tests/test_phase46_toda_45_stable_range_premise.py
11 passed

tests/test_phase46_toda_45_suspension_map.py
15 passed

tests/test_phase46_toda_45_theorem_semantics.py
14 passed

tests/test_phase46_toda_45_applicability_compatibility.py
16 passed

tests/test_phase46_toda_45_probe.py
10 passed
```

related:

```text
tests/test_toda_rules.py
66 passed

tests/test_map_property_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed
```

full:

```text
2143 passed in 64.31s
```

probe:

```powershell
python -m probes.probe_phase46_capabilities
```

result:

```text
n ≥ k+2
m ≥ n

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m}

E^(m-n): π_{n+k}^{n} → π_{m+k}^{m} is isomorphism

theorem isomorphism count = 1
premise count = 3
derived round count = 1
fixed point = True
```

---

# 11. Phase 47：Toda Proposition 4.4 COMPLETE

Toda Proposition 4.4:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

のとき:

```text
Φ:
π_{i-1}^{n-1} ⊕ π_i^{2n-1}
→
π_i^n

Φ(β,γ)=Eβ+α∘γ
```

は isomorphism。

implemented layers:

```text
TodaPrimaryGroupMembershipStatement
↓
DirectSumGroup with TodaPrimaryGroup summands
↓
TodaProp44DecompositionMap
↓
TodaProp44IsomorphismStatement
```

applicability:

```text
membership degree = 2n-1
same α
H(α)=±ι_{2n-1}
source first = π_{i-1}^{n-1}
source second = π_i^{2n-1}
target = π_i^n
formula = Eβ+α∘γ
```

を同一 symbolic instance として guard-aware に確認。

representative:

```text
3 GIVEN premises
↓
1 TodaProp44IsomorphismStatement
↓
fixed point
```

generic map-property bridge と E injectivity consequence は deferred。

---

# 12. Phase 47 verified status

focused:

```text
tests/test_phase47_toda_prop44_compatibility.py
20 passed

tests/test_phase47_toda_prop44_decomposition_groups.py
17 passed

tests/test_phase47_toda_prop44_decomposition_map.py
27 passed

tests/test_phase47_toda_prop44_toda_membership.py
15 passed

tests/test_phase47_toda_prop44_theorem_semantics.py
22 passed

tests/test_phase47_toda_prop44_applicability_compatibility.py
21 passed

tests/test_phase47_toda_prop44_probe.py
12 passed
```

related:

```text
tests/test_toda_rules.py
66 passed

tests/test_map_property_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed
```

full:

```text
2277 passed in 55.61s
```

probe:

```powershell
python -m probes.probe_phase47_capabilities
```

result:

```text
α ∈ π_{2n-1}^{n}
H(α) = ι_(2n-1)

Φ: π_{i-1}^{n-1} ⊕ π_{i}^{2n-1} → π_{i}^{n}
Φ(β,γ) = Eβ + α∘γ

Φ: π_{i-1}^{n-1} ⊕ π_{i}^{2n-1} → π_{i}^{n} is isomorphism

theorem isomorphism count = 1
premise count = 3
derived round count = 1
fixed point = True
```

---

# 13. Phase 48 candidate：Toda Proposition 4.4 consequence E injective

NEXT。

最初は compatibility check。

確認対象:

```text
TodaProp44IsomorphismStatement
TodaProp44DecompositionMap
EHP_E_MAP
existing InjectiveMapStatement
existing generic isomorphism → injective rule
instance-aware source / target of E
first-summand inclusion semantics
後続 equality / ZERO reflection への接続
```

Phase 48 の目的は:

```text
Proposition 4.4 decomposition isomorphism
↓
E injective
```

という mathematical consequence を、decomposition map 全体と suspension `E` を混同せず表現すること。

まだ先取りしない:

```text
generic map-property type generalization
automatic generic Toda-isomorphism bridge
stable homotopy theory
general symbolic dimension solver
general Whitehead-product algebra
automatic Whitehead zero / nonzero solver
general existential witness engine
```

---

# 14. Testing principle

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
