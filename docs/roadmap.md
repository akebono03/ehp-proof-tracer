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

# 2. Phase 45 完了時点

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
```

Current full regression:

```text
2060 passed in 70.48s
```

Representative probe:

```powershell
python -m probes.probe_phase45_capabilities
```

---

# 3. Phase 45 completed capabilities

```text
canonical symbolic E
canonical symbolic H
canonical symbolic Δ
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
Toda Prop.4.2 E-H exactness rule
Toda Prop.4.2 H-Δ exactness rule
Toda Prop.4.2 Δ-E exactness rule
instance-aware exactness
guard-aware theorem applicability
theorem provenance
Toda exactness → generic ExactnessStatement bridge
existing generic EHP zero-composition reuse
three-round fixed-point integration
representative probe
```

---

# 4. Toda Proposition 4.2 completed theorem branch

```text
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
```

is exact.

```text
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
```

is exact.

```text
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
-E→
π_i^{n+1}
```

is exact.

Generic consequences now reusable:

```text
H∘E = 0
Δ∘H = 0
E∘Δ = 0
```

---

# 5. Phase 45 architecture result

```text
TodaEHPSequence
=
long structural sequence
```

```text
TodaEHPExactnessWindow
=
instance-aware three-term structural window
```

```text
TodaProp42ExactnessStatement
=
instance-aware theorem exactness
```

```text
ExactnessStatement
=
instance-lossy generic exactness projection
```

```text
EHPZeroCompositionStatement
=
existing generic exactness consequence
```

End-to-end:

```text
TodaEHPExactnessWindow
↓
TodaProp42ExactnessStatement
↓
ExactnessStatement
↓
EHPZeroCompositionStatement
```

generic inference engine は変更していない。

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
Toda (4.5) stable-range suspension isomorphism
Toda Prop.4.4 decomposition isomorphism
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
| Toda (4.5) `E^(m-n)` isomorphism | NEXT | 46 candidate |
| Toda Prop.4.4 decomposition isomorphism | PLANNED | later |
| Toda Prop.4.4 `E` injectivity consequence | PLANNED | later |
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
Phase 46 candidate
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

# 9. Phase 46 candidate：Toda (4.5)

NEXT。

Toda (4.5):

```text
n ≥ k+2
```

のとき:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m

(m ≥ n)
```

は isomorphism。

Phase 45 までで Chapter 4 の critical group structure と 2-primary EHP exactness が theorem-level に接続されたため、次は stable-range suspension isomorphism が自然。

実装前 compatibility check:

```text
IteratedSuspension
existing map isomorphism statement
TodaPrimaryGroup
symbolic scalar inequalities
symbolic E^(m-n) representation
symbolic domain / codomain compatibility
Toda (4.5) exact statement
```

Phase 46 で確認すべき点:

```text
existing IteratedSuspension を map-level E^(m-n) に再利用できるか
existing Isomorphism statement が symbolic map / group terms を保持できるか
n ≥ k+2 / m ≥ n premise を current scalar statements で表せるか
TodaPrimaryGroup source / target を lossless に保持できるか
theorem provenance を current ProofStep で保持できるか
```

---

# 10. Phase 46 non-goals

Phase 46 では先取りしない:

```text
Toda Prop.4.4
Toda Prop.4.4 decomposition theorem
Toda Prop.4.4 E injectivity consequence
general stable homotopy theory
general symbolic inequality solver
general symbolic dimension simplifier
general Whitehead-product algebra
automatic Whitehead zero / nonzero solver
general existential witness engine
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

# 11. Testing principle

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

# 12. Phase 45 verified status

focused:

```text
tests/test_phase45_toda_prop42_compatibility.py
17 passed

tests/test_phase45_toda_prop42_sequence.py
19 passed

tests/test_phase45_toda_prop42_exactness_compatibility.py
17 passed

tests/test_phase45_toda_prop42_exactness_instance.py
18 passed

tests/test_phase45_toda_prop42_theorem_semantics.py
16 passed

tests/test_phase45_toda_prop42_bridge.py
16 passed
```

related:

```text
tests/test_toda_rules.py
66 passed

tests/test_ehp_rules.py
26 passed

tests/test_inference_rule_pattern.py
438 passed
```

full:

```text
2060 passed in 70.48s
```

probe:

```powershell
python -m probes.probe_phase45_capabilities
```

result:

```text
π_i^n -E→ π_{i+1}^{n+1} -H→ π_{i+1}^{2n+1}
π_{i+1}^{n+1} -H→ π_{i+1}^{2n+1} -Δ→ π_{i-1}^n
π_{i+1}^{2n+1} -Δ→ π_{i-1}^n -E→ π_i^{n+1}

E-H exact
H-Δ exact
Δ-E exact

H∘E = 0
Δ∘H = 0
E∘Δ = 0

derived round count = 3
fixed point = True
```
