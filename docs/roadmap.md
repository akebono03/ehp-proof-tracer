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

# 2. Phase 34 完了時点

Completed chain:

```text
Phase 28  map injectivity / isomorphism / equality reflection
Phase 29  actual H facts / typing / isomorphism
Phase 30  Toda Prop.2.2 right
Phase 31  SmashProduct minimum representation
Phase 32  Toda Prop.2.2 left
Phase 33  Barratt–Hilton prerequisites
Phase 34  Toda Prop.3.1 Barratt–Hilton theorem rules
```

Current full regression:

```text
1620 passed in 23.32s
```

Focused Phase 34:

```text
35 passed
```

---

# 3. Phase 34 completed capabilities

```text
HomotopyGroupMembershipStatement
Toda Prop.3.1 first theorem rule
Toda Prop.3.1 second theorem rule
strict symbolic applicability
invalid-case rejection
unrelated-premise tolerance
structured literature provenance
Phase 33 sign-evaluation connection
generic equality-transitivity closure
scope / non-goal regression
Phase 34 representative probe
Phase 34 final integrated regression
```

theorem premises:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)
```

first conclusion:

```text
a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
```

second conclusion:

```text
a∧b
=
(-1)^(ph)
(E^p b∘E^(q+h)a)
```

provenance:

```text
Toda Prop.3.1
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 3.1
```

---

# 4. Phase 34 completed inference chain

代表:

```text
a ∈ π_{p+k}(S^p)
b ∈ π_{q+h}(S^q)

↓ Toda Prop.3.1

a∧b
=
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)

+

((p+k)h) is even

↓
(-1)^((p+k)h)=1

↓
(-1)^((p+k)h)
(E^q a∘E^(p+k)b)
=
E^q a∘E^(p+k)b

↓ equality transitivity

a∧b
=
E^q a∘E^(p+k)b
```

重要:

```text
Barratt–Hilton
!=
general SmashProduct normalization
```

```text
symbolic homotopy-group membership
!=
symbolic source / target solver
```

---

# 5. Phase 35+：actual H((2ι₂)η₂) calculation

NEXT。

Phase 34 までで:

```text
Toda Prop.2.2 left
+
SmashProduct
+
Barratt–Hilton theorem rules
+
sign machinery
+
H injectivity
```

が準備済み。

次は abstract symbolic formula ではなく、具体的に:

```text
H((2ι₂)η₂)
```

を計算する。

想定 target chain:

```text
H((2ι₂)η₂)
↓ Toda Prop.2.2 left
E(2ι₁∧2ι₁)H(η₂)
↓ Toda Prop.3.1 / concrete Barratt–Hilton
4ι₃
```

このために必要になる可能性がある concrete pieces:

```text
typing of ι₁, ι₂, ι₃, η₂
H(η₂)=ι₃
2ι₁ ∈ appropriate homotopy group
concrete Barratt–Hilton parameter instantiation
concrete parity/sign evaluation
composition of multiples / identity maps
```

ただし Phase 35+ では actual calculation に必要な順に1つずつ導入する。

一般的な symbolic arithmetic や Toda (2.1) 全体を先取りしない。

---

# 6. parallel calculation of H(4η₂)

もう一方:

```text
H(4η₂)
```

について:

```text
H(4η₂)
↓ H homomorphism
4H(η₂)
↓ H(η₂)=ι₃
4ι₃
```

が必要。

既存 homomorphism machinery を再利用できるかをまず確認する。

不足がある場合のみ、actual H map に必要な最小 fact / bridge を追加する。

---

# 7. equality target

両側を計算後:

```text
H((2ι₂)η₂)=4ι₃
```

```text
H(4η₂)=4ι₃
```

から:

```text
H((2ι₂)η₂)=H(4η₂)
```

を構成する。

その後 Phase 28 / 29 を再利用:

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

最終 target:

```text
(2ι₂)η₂=4η₂
```

---

# 8. Phase 35+ の候補分割

実装時は actual code を確認して最小単位に切る。

候補:

```text
Phase 35-1
actual generator / identity typing check
```

```text
Phase 35-2
H(η₂)=ι₃ fact representation
```

```text
Phase 35-3
concrete Prop.2.2-left application setup
```

```text
Phase 35-4
2ι₁∧2ι₁ Barratt–Hilton concrete instantiation
```

```text
Phase 35-5
concrete sign / parity reduction
```

```text
Phase 35-6
composition / multiple calculation to 4ι₃
```

```text
Phase 35-7
H((2ι₂)η₂)=4ι₃ representative chain
```

その後必要に応じて:

```text
H(4η₂)=4ι₃
H-side equality
Injective(H) reflection
```

へ進む。

この番号は actual code inspection 後に確定する。

---

# 9. Toda (2.1) future candidate

既知として利用候補:

```text
a∘(b₁±b₂)=a∘b₁±a∘b₂
```

```text
(a₁±a₂)∘Eb=a₁∘Eb±a₂∘Eb
```

```text
k(a∘b)=a∘(kb)
```

```text
k(a∘Eb)=(ka)∘Eb
```

ただし unrestricted bidirectional rewrite は導入しない。

Phase 35+ の actual `4ι₃` calculation で必要になった式だけ staged / directed rule として追加する。

---

# 10. Toda (5.1) future candidate

既知として利用候補:

```text
π_i(S¹)=0  (i>1)
π_i(S^n)=0  (i<n)
π_n(S^n)=Z{ι_n}
```

actual proof need が現れた時点で foundational fact layer として導入する。

---

# 11. Current deferred boundaries

未実装:

```text
automatic compound parity inference
general symbolic scalar simplification
general SmashProduct typing / algebra / normalization
symbolic suspension typing arithmetic
Toda (2.1) general rule set
actual H((2ι₂)η₂) evaluation
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
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

# 12. Capability matrix

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
| actual `H((2ι₂)η₂)` calculation | NEXT | 35+ |
| `H((2ι₂)η₂)=H(4η₂)` | PLANNED | after actual H calculations |
| `(2ι₂)η₂=4η₂` | PLANNED | reuse equality reflection |
| Toda (2.1) | PLANNED | concrete need |
| Toda (5.1) | PLANNED | concrete need |
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

# 13. Long-term dependency

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
Phase 35+
actual H((2ι₂)η₂)
↓
H((2ι₂)η₂)=4ι₃
↓
H(4η₂)=4ι₃
↓
H((2ι₂)η₂)=H(4η₂)
↓
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

---

# 15. Phase 34 verified status

focused:

```text
tests/test_phase34_barratt_hilton.py
35 passed
```

related:

```text
tests/test_phase33_barratt_hilton.py
73 passed
```

```text
tests/test_scalar_rules.py
18 passed
```

```text
tests/test_relation_rules.py
50 passed
```

full:

```text
1620 passed in 23.32s
```

probe:

```powershell
python -m probes.probe_phase34_capabilities
```

---

# 16. 次 Phase

```text
Phase 35+
actual H((2ι₂)η₂) calculation
```

最初に current generator typing / identity-map representation / `H(η₂)=ι₃` / multiple representation を確認し、actual calculation に不足する最小 capability だけを特定する。

不足がある場合のみ production code を追加する。

---

# 17. Toda 4章：2-primary calculation branch

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

# 18. Toda (4.2) — Serre finiteness

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

概念的には:

```text
HomotopyGroupFinitenessFact(
  group=π_i(S^n),
  finite=True,
  conditions=(i != n, i != 2n-1),
)
```

のような表現候補がある。

ただし actual implementation では、
一般 quantified condition を先に作らず、
既存 theorem-fact machinery で必要最小限に表現できるかを確認する。

この fact 自体から具体的な group structure を自動生成しない。

```text
finite
!=
known decomposition
```

---

# 19. Toda (4.3) — p-primary component と π_i^n

## 19.1 p-primary component

```text
π_i(S^n;p)
```

を、

```text
π_i(S^n)
```

の `p`-primary component として扱う。

特にこの project では、
Toda 4章の 2-primary calculation に必要な:

```text
π_i(S^n;2)
```

を優先する。

将来的な group expression / reference 候補:

```text
PrimaryComponent(
  group=π_i(S^n),
  prime=2,
)
```

Important:

```text
π_i(S^n;2)
```

を文字列だけで保持せず、
ambient homotopy group と prime を structural に持てる形を優先する。

## 19.2 Toda subgroup π_i^n

[Toda](4.3) の定義:

```text
i=n
```

のとき:

```text
π_i^n
=
π_n(S^n)
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

将来的には `π_i^n` を独立した group-family reference として扱う。

候補:

```text
TodaPrimaryGroup(
  degree=i,
  sphere_dimension=n,
)
```

または equivalent minimal representation。

Important:

```text
TodaPrimaryGroup(i,n)
```

を単なる alias にしない。

特に critical degree:

```text
i=2n-1
```

では preimage により定義されるため、
definition provenance を保持する。

---

# 20. Preimage group under suspension

critical degree:

```text
π_{2n-1}^n
=
E^-1(π_{2n}(S^{n+1};2))
```

は、
以前 roadmap に挙げた element preimage:

```text
f^-1(a)
```

より一段一般的な、

```text
map inverse image of a subgroup
```

を実際に必要とする具体例である。

将来的な候補:

```text
PreimageSubgroup(
  map=E,
  subgroup=π_{2n}(S^{n+1};2),
)
```

Semantics:

```text
x ∈ E^-1(A)
↔
E(x) ∈ A
```

この bridge を proof-level に保持できるようにする。

Important:

```text
preimage of element
```

と:

```text
preimage of subgroup
```

を区別する。

Toda (4.3) では後者が中心となる。

---

# 21. Whitehead product

Toda Lemma 4.1 では:

```text
[ι_{n-1},ι_{n-1}]
```

が現れる。

したがって将来的に Whitehead product の最小 structural representation が必要になる。

候補:

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
```

```text
WhiteheadProduct
!=
SmashProduct
```

として distinct expression とする。

初期実装では Lemma 4.1 に必要な:

```text
[ι_{n-1},ι_{n-1}] = 0
```

または:

```text
[ι_{n-1},ι_{n-1}] != 0
```

という known fact / theorem premise を表現できればよい。

general Whitehead-product algebra は先取りしない。

---

# 22. Toda Lemma 4.1

[Toda] Lemma 4.1 は、
critical group:

```text
π_{2n-1}^n
```

の構造を parity と Whitehead product により場合分けする。

## 22.1 n odd

```text
n odd
↓
π_{2n-1}^n
=
π_{2n-1}(S^n;2)
```

## 22.2 n even and Whitehead product nonzero

```text
n even
+
[ι_{n-1},ι_{n-1}] != 0
↓
π_{2n-1}^n
=
Z{P(ι_{2n+1})}
⊕
π_{2n-1}(S^n;2)
```

## 22.3 n even and Whitehead product zero

```text
n even
+
[ι_{n-1},ι_{n-1}] = 0
↓
π_{2n-1}^n
=
Z{α}
⊕
π_{2n-1}(S^n;2)
```

ここで `α` は:

```text
H(α)=ι_{2n-1}
```

かつ:

```text
Eα ∈ π_{2n}^{n+1}
=
π_{2n}(S^{n+1};2)
```

を満たす元。

この case は将来的に:

```text
existential / chosen witness
+
map equation
+
membership
```

を接続する actual theorem scenario となる。

Important:

```text
α
```

は notation から自動生成する named generator ではなく、
Lemma 4.1 の条件を満たす witness element として扱う。

---

# 23. Toda Prop.4.2 — 2-primary EHP exact sequence

[Toda] Proposition 4.2:

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

は exact sequence である。

この sequence は、
通常の homotopy group を直接並べる既存 EHP layer とは別に、
Toda subgroup:

```text
π_i^n
```

を domain object とする 2-primary EHP branch として扱う。

Important:

```text
existing EHP exactness machinery
```

を可能な限り再利用する。

新しい exactness engine を作らず、

```text
new group-term representation
+
existing exactness reasoning
```

で成立するかを先に確認する。

また map 名:

```text
E
H
Δ
```

の typing context は、
通常の EHP sequence と Toda `π_i^n` sequence で区別できるようにする。

この exact sequence を、
2-primary component の計算の主要 engine とする。

---

# 24. Toda (4.5) — stable-range suspension isomorphism

[Toda](4.5):

```text
n >= k+2
```

のとき、
任意の:

```text
m >= n
```

について:

```text
E^(m-n):
π_{n+k}^n
→
π_{m+k}^m
```

は同型。

この theorem は、
Toda `π_i^n` family に対する stable-range theorem として扱う。

将来的な conclusion:

```text
Isomorphism(
  E^(m-n):
  π_{n+k}^n
  →
  π_{m+k}^m
)
```

Important:

既存 Freudenthal theorem と数学的に関連していても、
同じ theorem fact として暗黙統合しない。

```text
Toda (4.5)
!=
existing Freudenthal rule
```

とし、
source / theorem provenance を保持する。

既存 Phase 28 の:

```text
Isomorphism
↓
Injective
```

をそのまま再利用できる。

したがって:

```text
E^(m-n)(a)=E^(m-n)(b)
+
Toda (4.5)
↓
a=b
```

という equality reflection が可能になる。

---

# 25. Toda Prop.4.4 — decomposition isomorphism

仮定:

```text
α ∈ π_{2n-1}^n
```

```text
H(α)=±ι_{2n-1}
```

このとき:

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

は任意の `i` で同型。

この theorem は、
以下を一度に接続する代表的 theorem scenario となる。

```text
direct sum
Suspension
Composition
Sum
Map / function representation
Isomorphism
```

将来的な map representation 候補:

```text
TodaDecompositionMap(
  alpha=α,
  n=n,
  i=i,
)
```

または actual theorem application 時に構築する lambda-like map expression。

ただし generic lambda calculus は導入しない。

重要なのは:

```text
(β,γ)
↦
Eβ + α∘γ
```

という map の数学的 identity と typing を保持し、
その map に対する `IsomorphismStatement` を導けることである。

---

# 26. Prop.4.4 consequence — suspension E is injective

Proposition 4.4 から特に:

```text
E:
π_{i-1}^{n-1}
→
π_i^n
```

は任意の `i` で単射。

これは current generic map-property machinery に直接接続できる。

```text
Injective(E)
+
Eβ₁=Eβ₂
↓
β₁=β₂
```

また:

```text
Injective(E)
+
Eβ=0
↓
β=0
```

の ZERO reflection も将来候補。

Important:

proof trace 上では:

```text
Toda Prop.4.4
↓
decomposition map isomorphism
↓
E injective
```

という theorem provenance を保持する。

`E` の injectivity を notation から global fact として登録しない。

typing context:

```text
E:
π_{i-1}^{n-1}
→
π_i^n
```

を含む contextual property とする。

---

# 27. 2-primary branch implementation order candidate

Phase 35+ の actual H calculation を直近目標として維持する。

Toda 4章 branch はその後の有力候補として、
actual proof need に応じて次の順を検討する。

```text
4A
PrimaryComponent / π_i(S^n;2) minimum representation
↓
4B
TodaPrimaryGroup π_i^n minimum representation
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

# 28. 2-primary branch testing principle

各 layer で既存 testing principle に加えて、
次を確認する。

```text
π_i(S^n)
!=
π_i(S^n;2)
!=
π_i^n
```

critical degree branch:

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

Whitehead condition:

```text
[ι_{n-1},ι_{n-1}]=0
```

と:

```text
[ι_{n-1},ι_{n-1}]!=0
```

を strict に区別する。

Toda (4.5):

```text
n>=k+2
m>=n
```

の side conditions を満たさない場合に theorem を適用しない。

Prop.4.4:

```text
α∈π_{2n-1}^n
H(α)=±ι_{2n-1}
```

の両 premise を必要とし、
不足時には isomorphism を生成しない。

また contextual `Injective(E)` が
unrelated E map / typing context に漏れないことを regression で確認する。

---

# 29. 将来の2-primary representative proof direction

最終的には Toda 4章 branch を用いて:

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

から、
Toda の 2-primary homotopy-group calculations を
proof graph 上で追跡できることを目標とする。

この branch では特に:

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

を同一の provenance-aware framework で扱う。

