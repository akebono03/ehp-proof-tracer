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

# 2. Phase 36 完了時点

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
```

Current full regression:

```text
1687 passed in 25.70s
```

Focused Phase 36:

```text
14 passed
```

Representative probe:

```powershell
python -m probes.probe_phase36_capabilities
```

Final Phase 36 result:

```text
H(4η₂)=4ι₃
```

---

# 3. Phase 35 completed capabilities

```text
actual H(η₂)=ι₃ literature fact
actual identity suspension facts Eι₁=ι₂ / Eι₂=ι₃
concrete Barratt–Hilton membership
concrete Barratt–Hilton applicability
concrete theorem-parameter integer addition
explicit concrete parity / sign reduction
Suspension Multiple bridge
E^1-to-E proof-level bridge
equality transport through Multiple
nested integer Multiple calculation
directed Toda (2.1) right-multiple rule
explicit IdentityMapStatement
right identity composition
canonical actual H equality preservation
E(2ι₁)=2ι₂
E(2ι₂)=2ι₃
E(2ι₁∧2ι₁)=4ι₃
H((2ι₂)η₂)=4ι₃
scope / non-goal regression
Phase 35 representative probe
Phase 35 final integrated regression
```

---

# 4. Phase 35 completed inference chain

代表:

```text
Eι₁=ι₂
+
E is homomorphism
↓
E(2ι₁)=2ι₂
```

```text
Eι₂=ι₃
+
E is homomorphism
↓
E(2ι₂)=2ι₃
```

Toda Prop.3.1:

```text
2ι₁ ∈ π₁(S¹)
2ι₁ ∈ π₁(S¹)
↓
2ι₁∧2ι₁
=
(-1)^(1·0)
(E^1(2ι₁)∘E^1(2ι₁))
```

explicit parity:

```text
1·0 is even
↓
(-1)^(1·0)=1
```

therefore:

```text
2ι₁∧2ι₁
=
E^1(2ι₁)∘E^1(2ι₁)
```

Suspension / composition calculation:

```text
E(2ι₁∧2ι₁)
=
2ι₃∘2ι₃
```

Toda (2.1), identity, nested Multiple:

```text
2ι₃∘2ι₃
=
2((2ι₃)∘ι₃)
=
2(2ι₃)
=
4ι₃
```

Toda Prop.5.1:

```text
H(η₂)=ι₃
```

Toda Prop.2.2 left:

```text
H((E(2ι₁))∘η₂)
=
E(2ι₁∧2ι₁)∘H(η₂)
```

actual left transport:

```text
E(2ι₁)=2ι₂
↓
(E(2ι₁))∘η₂=(2ι₂)∘η₂
↓
H((E(2ι₁))∘η₂)=H((2ι₂)∘η₂)
```

final:

```text
H((2ι₂)η₂)=4ι₃
```

Important:

```text
actual H equality preservation
!=
universal arbitrary-map congruence
```

```text
directed Toda (2.1)
!=
general composition bilinearity
```

---

# 5. Phase 36：H(4η₂)=4ι₃

COMPLETE。

Phase 35 の parallel result:

```text
H((2ι₂)η₂)=4ι₃
```

に対して Phase 36 では:

```text
H(4η₂)=4ι₃
```

を完成した。

actual chain:

```text
actual Homomorphism(H)
↓
H(4η₂)=4H(η₂)

Toda Prop.5.1
↓
H(η₂)=ι₃
↓ equality under Multiple
4H(η₂)=4ι₃

↓ equality transitivity
H(4η₂)=4ι₃
```

Phase 36 で追加した production capability は narrow actual-H materialization:

```text
ehp_h_homomorphism_proof_step()
```

のみ。

Important:

```text
Isomorphism(H)
↛ Homomorphism(H) automatically
```

```text
arbitrary MapSymbol
↛ automatic Homomorphism
```

```text
Phase 36
!=
general arbitrary-map homomorphism expansion project
```

verified:

```text
tests/test_phase36_actual_h_multiple.py
14 passed

full suite
1687 passed in 25.70s
```

probe:

```powershell
python -m probes.probe_phase36_capabilities
```

---

# 6. Phase 36 completed split

```text
36-1 actual H homomorphism applicability check COMPLETE
36-2 actual H homomorphism fact / bridge COMPLETE
36-3 H(4η₂)=4H(η₂) COMPLETE
36-4 H(η₂)=ι₃ substitution COMPLETE
36-5 H(4η₂)=4ι₃ transitivity closure COMPLETE
36-6 H(4η₂)=4ι₃ end-to-end integration COMPLETE
36-7 scope / non-goal regression COMPLETE
36-8 representative probe / final regression COMPLETE
36-9 Phase 36 completion COMPLETE
```

Phase 37/38 は未着手。

---

# 7. Phase 37：H-side equality

Phase 35:

```text
H((2ι₂)η₂)=4ι₃
```

Phase 36:

```text
H(4η₂)=4ι₃
```

から:

```text
H((2ι₂)η₂)=H(4η₂)
```

を構成する。

第一候補は既存 equality symmetry / transitivity:

```text
H((2ι₂)η₂)=4ι₃
```

```text
H(4η₂)=4ι₃
↓ symmetry
4ι₃=H(4η₂)
```

```text
↓ transitivity
H((2ι₂)η₂)=H(4η₂)
```

新しい theorem rule は原則不要。

Phase 37 は integration / provenance / scope の確認を中心とする。

---

# 8. Phase 38：Injective(H) reflection

Phase 28 / 29 の既存 machinery を再利用する。

```text
Isomorphism(H)
↓
Injective(H)
```

```text
Injective(H)
+
H(a)=H(b)
↓
a=b
```

ここで:

```text
a=(2ι₂)η₂
b=4η₂
```

を代入し:

```text
(2ι₂)η₂=4η₂
```

を導出する。

Important:

```text
Injective(H)
```

は actual typing / map context を満たす場合だけ使用する。

global unrestricted H injectivity として扱わない。

---

# 9. Phase 39 candidate：representative full equality proof

Phase 35–38 を統合して:

```text
H((2ι₂)η₂)=4ι₃
H(4η₂)=4ι₃
↓
H((2ι₂)η₂)=H(4η₂)
↓
Injective(H)
↓
(2ι₂)η₂=4η₂
```

を representative proof / probe にする候補。

ただし Phase 38 で十分に end-to-end proof が完成する場合、
独立 Phase とせず Phase 38 の final integration に含めてもよい。

---

# 10. Toda (2.1) current status

Phase 35 で actual `4ι₃` calculation に必要な direction:

```text
a∘(kb)=k(a∘b)
```

を実装済み。

status:

```text
DIRECTED SUBSET IMPLEMENTED
```

未実装:

```text
a∘(b₁±b₂)=a∘b₁±a∘b₂
```

```text
(a₁±a₂)∘Eb=a₁∘Eb±a₂∘Eb
```

```text
k(a∘Eb)=(ka)∘Eb
```

unrestricted bidirectional rewrite は導入しない。

actual proof need が現れた式だけ staged / directed rule として追加する。

---

# 11. Toda Prop.5.1 current status

Phase 35 で actual fact:

```text
H(η₂)=ι₃
```

を production fact として実装済み。

status:

```text
PARTIALLY IMPLEMENTED FOR ACTUAL NEED
```

同じ Proposition 5.1 に含まれる:

```text
π_3^2=Z{η₂}
```

は未実装。

actual proof need が現れるまで group-structure fact は追加しない。

---

# 12. Current deferred boundaries

未実装:

```text
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
automatic compound parity inference
general symbolic scalar simplification
general SmashProduct typing / algebra / normalization
symbolic suspension typing arithmetic
Toda (2.1) general rule set
universal arbitrary-map equality congruence
automatic identity semantics from ι notation
Toda (4.2) Serre finiteness fact
Toda (4.3) 2-primary component / π_i^n definition
WhiteheadProduct representation
Toda Lemma 4.1 structure theorem
Toda Prop.4.2 2-primary EHP exact sequence
Toda (4.5) stable-range suspension isomorphism
Toda Prop.4.4 decomposition isomorphism
Toda Prop.4.4 consequence: E injective on π_i^n
stable homotopy group model
stable Toda brackets
higher Toda brackets
```

---

# 13. Capability matrix

| capability | status | phase |
|---|---|---|
| map injectivity / equality reflection | IMPLEMENTED | 28 |
| actual H facts / typing | IMPLEMENTED | 29 |
| Toda Prop.2.2 right | IMPLEMENTED | 30 |
| SmashProduct | IMPLEMENTED | 31 |
| Toda Prop.2.2 left | IMPLEMENTED | 32 |
| ScalarExpression tree | IMPLEMENTED | 33 |
| parity → symbolic sign evaluation | IMPLEMENTED | 33 |
| symbolic sign → Multiple bridge | IMPLEMENTED | 33 |
| symbolic IteratedSuspension exponent | IMPLEMENTED | 33 |
| Barratt–Hilton structural formulas | IMPLEMENTED | 33 |
| symbolic homotopy-group membership | IMPLEMENTED | 34 |
| Toda Prop.3.1 first theorem rule | IMPLEMENTED | 34 |
| Toda Prop.3.1 second theorem rule | IMPLEMENTED | 34 |
| Toda Prop.3.1 literature provenance | IMPLEMENTED | 34 |
| Barratt–Hilton sign connection | IMPLEMENTED | 34 |
| Barratt–Hilton reduced equality closure | IMPLEMENTED | 34 |
| actual `H(η₂)=ι₃` fact | IMPLEMENTED | 35 |
| concrete Barratt–Hilton instantiation | IMPLEMENTED | 35 |
| concrete parity / sign reduction | IMPLEMENTED | 35 |
| directed Toda (2.1) right-multiple rule | IMPLEMENTED | 35 |
| explicit identity composition | IMPLEMENTED | 35 |
| `E(2ι₁)=2ι₂` | IMPLEMENTED | 35 |
| `E(2ι₂)=2ι₃` | IMPLEMENTED | 35 |
| `E(2ι₁∧2ι₁)=4ι₃` | IMPLEMENTED | 35 |
| actual `H((2ι₂)η₂)=4ι₃` | IMPLEMENTED | 35 |
| Phase 35 representative probe | IMPLEMENTED | 35 |
| `H(4η₂)=4ι₃` | IMPLEMENTED | 36 |
| `H((2ι₂)η₂)=H(4η₂)` | PLANNED | 37 |
| `(2ι₂)η₂=4η₂` | PLANNED | 38 |
| full equality representative proof | PLANNED | 38/39 |
| Toda Prop.5.1 group structure `π_3^2=Z{η₂}` | DEFERRED | concrete need |
| Toda (4.2) Serre finiteness | PLANNED | foundational 2-primary branch |
| p-primary component `π_i(S^n;p)` | PLANNED | Toda (4.3) prerequisite |
| Toda subgroup `π_i^n` | PLANNED | Toda (4.3) |
| `E^{-1}(π_{2n}(S^{n+1};2))` preimage group | PLANNED | critical degree `i=2n-1` |
| Whitehead product `[a,b]` | PLANNED | Lemma 4.1 prerequisite |
| Toda Lemma 4.1 | PLANNED | structure of `π_{2n-1}^n` |
| Toda Prop.4.2 2-primary EHP exact sequence | PLANNED | main 2-primary calculation engine |
| Toda (4.5) `E^(m-n)` isomorphism | PLANNED | stable-range theorem for `π_i^n` |
| Toda Prop.4.4 decomposition isomorphism | PLANNED | `(β,γ)↦Eβ+α∘γ` |
| Toda Prop.4.4 `E` injectivity consequence | PLANNED | reuse generic equality reflection |
| stable homotopy | PLANNED | later |
| higher Toda bracket | DEFERRED | concrete need |

---

# 14. Long-term dependency

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
actual H((2ι₂)η₂) COMPLETE
↓
H((2ι₂)η₂)=4ι₃ COMPLETE
↓
Phase 36
H(4η₂)=4ι₃ COMPLETE
↓
Phase 37
H((2ι₂)η₂)=H(4η₂)
↓
Phase 38
existing Injective(H)
↓
(2ι₂)η₂=4η₂

parallel future branch:

Toda (4.2)
Serre finiteness
↓
p-primary component π_i(S^n;p)
↓
Toda (4.3)
π_i^n definition
↓
preimage under E in degree 2n-1
↓
Whitehead product
↓
Toda Lemma 4.1
structure of π_{2n-1}^n
↓
Toda Prop.4.2
2-primary EHP exact sequence
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

# 15. Testing principle

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

追加で actual calculation branch では:

```text
constructor normalization
!=
proof-level equality
```

```text
explicit fact
!=
notation-derived semantics
```

```text
directed calculation rule
!=
general algebra
```

を regression で固定する。

---

# 16. Phase 36 verified status

focused:

```text
tests/test_phase36_actual_h_multiple.py
14 passed
```

related:

```text
tests/test_homomorphism_rules.py
39 passed
```

```text
tests/test_hopf_rules.py
31 passed
```

```text
tests/test_relation_rules.py
50 passed
```

```text
tests/test_map_property_rules.py
26 passed
```

full:

```text
1687 passed in 25.70s
```

probe:

```powershell
python -m probes.probe_phase36_capabilities
```

result:

```text
H(4η₂)=4ι₃
```

---

# 17. 次 Phase

```text
Phase 37
H((2ι₂)η₂)=H(4η₂)
```

既に:

```text
Phase 35: H((2ι₂)η₂)=4ι₃
Phase 36: H(4η₂)=4ι₃
```

がある。

第一候補は既存 equality symmetry / transitivity:

```text
H(4η₂)=4ι₃
↓ symmetry
4ι₃=H(4η₂)
```

```text
H((2ι₂)η₂)=4ι₃
4ι₃=H(4η₂)
↓ transitivity
H((2ι₂)η₂)=H(4η₂)
```

新しい theorem rule は原則不要。

その後 Phase 38 で existing actual `H` injectivity reflection を再利用する。

---

# 18. Toda 4章：2-primary calculation branch

Toda 4章の結果は、
通常の homotopy group `π_i(S^n)` だけでなく、
2-primary component と Toda が定義する部分群 `π_i^n` を用いて
EHP 型計算を進めるための独立した将来 branch とする。

この branch の中心:

```text
Serre finiteness
↓
p-primary component
↓
Toda π_i^n
↓
preimage under E
↓
Whitehead product
↓
Lemma 4.1
↓
2-primary EHP exact sequence
↓
stable-range suspension isomorphism
↓
decomposition isomorphism
↓
E injectivity
↓
2-primary calculations
```

Important:

```text
π_i^n
!=
π_i(S^n)
```

一般には同一視しない。

---

# 19. Toda (4.2) — Serre finiteness

[Toda](4.2) で利用する既知結果:

```text
π_i(S^n)
```

は、

```text
i=n
```

または、

```text
i=2n-1
```

の場合を除いて有限群である。

将来的には foundational group fact として扱う。

この fact 自体から具体的な group structure を自動生成しない。

```text
finite
!=
known decomposition
```

---

# 20. Toda (4.3) — p-primary component と π_i^n

## 20.1 p-primary component

```text
π_i(S^n;p)
```

を `π_i(S^n)` の `p`-primary component として扱う。

特に:

```text
π_i(S^n;2)
```

を優先する。

将来的には ambient homotopy group と prime を structural に持つ minimum representation を検討する。

## 20.2 Toda subgroup π_i^n

[Toda](4.3):

```text
i=n
```

のとき:

```text
π_i^n=π_n(S^n)
```

```text
i=2n-1
```

のとき:

```text
π_i^n
=
E^-1(π_{2n}(S^{n+1};2))
```

```text
i != n, 2n-1
```

のとき:

```text
π_i^n
=
π_i(S^n;2)
```

Important:

```text
π_i^n
!=
plain alias of π_i(S^n)
```

critical degree では preimage definition provenance を保持する。

---

# 21. Preimage group under suspension

critical degree:

```text
π_{2n-1}^n
=
E^-1(π_{2n}(S^{n+1};2))
```

では subgroup preimage が必要。

将来候補:

```text
PreimageSubgroup(
  map=E,
  subgroup=π_{2n}(S^{n+1};2),
)
```

semantics:

```text
x ∈ E^-1(A)
↔
E(x) ∈ A
```

element preimage と subgroup preimage を区別する。

---

# 22. Whitehead product

Toda Lemma 4.1 で:

```text
[ι_{n-1},ι_{n-1}]
```

が必要。

minimum representation candidate:

```text
WhiteheadProduct(
  left=a,
  right=b,
)
```

Important:

```text
WhiteheadProduct
!=
Composition
!=
SmashProduct
```

初期は Lemma 4.1 に必要な zero / nonzero facts の表現を優先し、
general Whitehead-product algebra は先取りしない。

---

# 23. Toda Lemma 4.1

critical group:

```text
π_{2n-1}^n
```

を parity と Whitehead product で場合分けする。

## n odd

```text
π_{2n-1}^n
=
π_{2n-1}(S^n;2)
```

## n even + Whitehead product nonzero

```text
π_{2n-1}^n
=
Z{P(ι_{2n+1})}
⊕
π_{2n-1}(S^n;2)
```

## n even + Whitehead product zero

```text
π_{2n-1}^n
=
Z{α}
⊕
π_{2n-1}(S^n;2)
```

with:

```text
H(α)=ι_{2n-1}
```

```text
Eα ∈ π_{2n}^{n+1}
```

`α` は theorem witness として扱い、
notation から自動生成しない。

---

# 24. Toda Prop.4.2 — 2-primary EHP exact sequence

[Toda] Prop.4.2:

```text
… →
π_i^n
-E→
π_{i+1}^{n+1}
-H→
π_{i+1}^{2n+1}
-Δ→
π_{i-1}^n
-E→
π_i^{n+1}
-H→
…
```

existing exactness machinery を可能な限り再利用する。

```text
new group-term representation
+
existing exactness reasoning
```

を優先し、
新しい exactness engine は作らない。

---

# 25. Toda (4.5) — stable-range suspension isomorphism

```text
n >= k+2
m >= n
```

のとき:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

は同型。

Important:

```text
Toda (4.5)
!=
existing Freudenthal theorem
```

source / theorem provenance を別々に保持する。

existing Phase 28:

```text
Isomorphism
↓
Injective
```

を再利用する。

---

# 26. Toda Prop.4.4 — decomposition isomorphism

仮定:

```text
α ∈ π_{2n-1}^n
H(α)=±ι_{2n-1}
```

map:

```text
π_{i-1}^{n-1}
⊕
π_i^{2n-1}
→
π_i^n
```

```text
(β,γ)
↦
Eβ + α∘γ
```

は同型。

将来 representation は generic lambda calculus を作らず、
actual theorem application に必要な minimum map object を優先する。

---

# 27. Prop.4.4 consequence — contextual Injective(E)

Prop.4.4 から:

```text
E:
π_{i-1}^{n-1}
→
π_i^n
```

は単射。

existing equality reflection:

```text
Injective(E)
+
Eβ₁=Eβ₂
↓
β₁=β₂
```

を再利用する。

Important:

```text
contextual Injective(E)
!=
global Injective(E)
```

typing context と theorem provenance を保持する。

---

# 28. 2-primary branch implementation order candidate

Phase 36–38 の actual equality branch を直近目標として維持する。

その後の候補:

```text
4A
PrimaryComponent minimum representation
↓
4B
TodaPrimaryGroup π_i^n
↓
4C
PreimageSubgroup under E
↓
4D
WhiteheadProduct minimum representation
↓
4E
Toda Lemma 4.1 theorem rules
↓
4F
Toda Prop.4.2 exact-sequence construction
↓
4G
Toda (4.5) suspension-isomorphism theorem
↓
4H
Toda Prop.4.4 decomposition isomorphism
↓
4I
contextual Injective(E)
↓
4J
representative 2-primary calculation
```

実際の Phase 番号は current project progress と code inspection 後に決める。

---

# 29. 2-primary branch testing principle

既存 testing principle に加えて:

```text
π_i(S^n)
!=
π_i(S^n;2)
!=
π_i^n
```

を固定する。

critical degree:

```text
i=n
i=2n-1
otherwise
```

を区別する。

Preimage subgroup:

```text
x∈E^-1(A)
↔
E(x)∈A
```

Whitehead:

```text
[ι_{n-1},ι_{n-1}]=0
```

と:

```text
[ι_{n-1},ι_{n-1}]!=0
```

を区別する。

Toda (4.5):

```text
n>=k+2
m>=n
```

の side conditions を strict に扱う。

Prop.4.4:

```text
α∈π_{2n-1}^n
H(α)=±ι_{2n-1}
```

の両 premise を要求する。

contextual `Injective(E)` が unrelated map context に漏れないことを regression で確認する。

---

# 30. 将来の2-primary representative proof direction

最終的には:

```text
known group facts
+
2-primary component
+
π_i^n
+
EHP exactness
+
stable-range suspension isomorphism
+
decomposition isomorphism
+
injective E
```

から Toda の 2-primary calculations を proof graph 上で追跡する。

扱う対象:

```text
exact group value
finite-group fact
2-primary subgroup
free Z summand
preimage-defined subgroup
chosen witness α
Whitehead-product condition
exactness
isomorphism
injectivity
```

を同一 provenance-aware framework に統合する。
