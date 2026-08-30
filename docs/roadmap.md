# EHP Proof Tracer Roadmap

## 1. この文書の目的

この文書は、EHP Proof Tracer の将来拡張に関する長期的な設計方針を記録する。

`README.md` は current capabilities / current status、
`docs/design.md` は current architecture / semantics / boundaries、
`docs/development_log.md` は chronological implementation history を扱う。

この `docs/roadmap.md` は、まだ未実装の機能を含む将来構想と、
それらの依存関係・実装優先順位を整理するための文書とする。

Phase 16 完了時点では、以下の基盤が実装済みである。

```text
Abelian group calculation
EHP reasoning
ORDER
Suspension
Freudenthal
Composition
Generalized Hopf invariant
Additive expressions
Homomorphism reasoning
Set / subgroup reasoning
Coset / modulo reasoning
Symbolic scalar constraints
```

したがって、今後はこれらを前提として、

```text
indeterminacy
typed homotopy elements
stable homotopy groups
structured generators
iterated suspension
theorem representation
knowledge-table integration
unstable Toda brackets
stable Toda brackets
```

へ進む。

この文書に記載された項目は、記載されているだけでは実装済みを意味しない。
各機能は必要な Phase において個別に仕様化し、
既存 API と generic inference engine を不必要に壊さない最小変更で導入する。

---

# 2. 現在の実装基盤

Phase 16 完了時点で、proof / inference layer には次の主要構造がある。

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── Composition
├── MapApplication
└── Suspension
```

加えて、

```text
MapSymbol
ScalarSymbol
```

がある。

Proof-level statement / relation として、

```text
Relation
ProofStep
InferenceRule
MembershipStatement
SubsetStatement
SubgroupEqualityStatement
ModuloStatement
CosetEqualityStatement
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

などが利用可能である。

Current implemented examples:

```text
α+β
-α
nα
kβ
α = kβ + γ

f(α+β)=f(α)+f(β)

α∈A
A⊆B
A=B

α≡β mod A
α+A

k odd
k even
k≡1 mod 2
```

Phase 16 の代表的接続:

```text
k odd
↓
k≡1 mod 2

ord(β)=2
+
k≡1 mod 2
↓
kβ=β

kβ=β
↓
kβ≡β mod Ker(H)

Exactness(E,H)
↓
Im(E)=Ker(H)

kβ≡β mod Ker(H)
↓
kβ≡β mod Im(E)
```

この既存基盤を再利用して将来機能を構築する。

---

# 3. 基本設計原則

## 3.1 actual mathematical need first

新機能は、

```text
actual mathematical need
↓
minimal representation
↓
domain InferenceRule
↓
existing generic engine
```

の順に導入する。

将来必要になりそうという理由だけで、
完全な symbolic algebra system、
完全な theorem prover、
完全な higher Toda bracket system を先に実装しない。

## 3.2 不定性を消さずに保持する

Toda 型の計算では、

```text
α = ±β
α ≡ β mod A
α = kβ + γ
k odd
α ∈ β + A
```

のような部分情報が現れる。

これらを単なる「未確定」として捨てず、

```text
値は未確定でも、
判明している制約は proof-level knowledge として保持する
```

ことを基本方針とする。

## 3.3 数学的対象と表示 notation を分離する

例えば、

```text
Eν'
```

は generator name `"Eν'"` ではなく、

```text
Suspension(ν')
```

として表現する。

```text
8ι_7
```

は、

```text
Multiple(8,ι_7)
```

として表現する。

## 3.4 数学的 well-definedness を検査する

将来の expression / theorem layer では、
式が書けるだけでなく、数学的に定義されるかを検査できるようにする。

例えば、

```text
a+b
```

には、

```text
ambient_group(a)=ambient_group(b)
```

が必要である。

また、

```text
α∘β
```

には、

```text
target(β)=source(α)
```

が必要である。

## 3.5 mathematical applicability と active inference scope を分離する

数学的に成立する推論を、常にすべて自動生成する必要はない。

例えば、

```text
ord(a)=2
```

から、

```text
2a=0
4a=0
6a=0
8a=0
...
```

を無限列挙しない。

基本原則:

```text
mathematical applicability
≠
active inference scope
```

## 3.6 fixed-point termination を壊さない

構造的深さや係数を無限に増やす推論は、
unrestricted fixed-point-safe とみなさない。

必要に応じて、

```text
goal-directed reasoning
bounded execution
staged execution
explicit active scope
```

を利用する。

---

# 4. Typed Homotopy Elements

## 4.1 unstable type

将来的に各 unstable homotopy element について、

```text
α : S^m → S^n
```

を保持し、

```text
α ∈ π_m(S^n)
```

を導出可能にする。

必要な情報:

```text
source sphere
target sphere
ambient homotopy group
stem
```

## 4.2 addition typing

```text
α+β
```

は、

```text
ambient_group(α)=ambient_group(β)
```

の場合にのみ定義する。

異なる群の元同士の加法は ill-typed とする。

## 4.3 equality typing

```text
α=β
```

についても、
原則として同じ ambient group の元同士であることを要求する。

## 4.4 composition typing

```text
α∘β
```

について、

```text
target(β)=source(α)
```

を必要条件とする。

Toda bracket の defining composition の検査にも利用する。

## 4.5 Suspension typing

```text
α : S^m → S^n
```

なら、

```text
Eα : S^(m+1) → S^(n+1)
```

を導出できるようにする。

---

# 5. Stable Homotopy Groups

## 5.1 stable homotopy element

stable homotopy class を first-class に扱えるようにする。

概念的には、

```text
α ∈ π_k^S
```

を表現する。

必要な情報:

```text
stable degree
stem
stable group
```

## 5.2 unstable / stable の区別

以下を同一の型として暗黙に扱わない。

```text
α ∈ π_m(S^n)
```

と、

```text
α ∈ π_k^S
```

stable range で対応がある場合も、
Freudenthal / stabilization theorem 等の明示的 reasoning を通して接続する。

## 5.3 stable composition degree

stable composition / product では、
degree / stem の加法を型検査に利用できるようにする。

概念的には、

```text
deg(αβ)=deg(α)+deg(β)
```

のような情報を扱う。

実装時には採用する stable degree convention を明文化する。

## 5.4 stabilization bridge

unstable class から stable class への移行を単なる notation conversion としない。

必要に応じて、

```text
stabilization
stable-range theorem
Freudenthal
```

を通じた明示的 bridge とする。

---

# 6. Structured Generator Representation

## 6.1 generator を単なる文字列にしない

Toda の計算では、

```text
η_3
ν'
μ_3
ι_7
\barν
ε
ζ
σ
```

などの記号が頻繁に現れる。

これらを generator identity として構造化する。

概念的には、

```text
GeneratorSymbol
  family
  index
  decoration
  source
  target
  ambient_group
  stable_or_unstable
```

を想定する。

## 6.2 decoration

必要に応じて、

```text
prime
bar
tilde
hat
subscript
superscript
```

などを identity の一部として保持する。

例えば、

```text
ν
ν'
\barν
```

を同じ generator の表示違いとみなさない。

## 6.3 generator と expression の分離

```text
Eν'
```

は、

```text
Suspension(ν')
```

とする。

```text
8ι_7
```

は、

```text
Multiple(8,ι_7)
```

とする。

generator の名前に operation を埋め込まない。

---

# 7. Iterated Suspension

## 7.1 `E^t α`

Toda の記法で現れる、

```text
E^t α
```

を表現できるようにする。

候補:

```text
IteratedSuspension(
  expression=α,
  exponent=t,
)
```

## 7.2 symbolic exponent

`t` は concrete integer に限定せず、
必要に応じて symbolic integer とする。

例えば、

```text
E^t α
E^(t+1) α
E^(n-r) α
```

を将来的に扱える余地を残す。

## 7.3 typing

```text
α : S^m → S^n
```

なら、

```text
E^t α : S^(m+t) → S^(n+t)
```

を導出できるようにする。

## 7.4 iterated suspension composition

必要になった場合に、

```text
E^s(E^t α)=E^(s+t) α
```

のような theorem rule を追加する。

一般的な symbolic exponent simplifier は先に実装しない。

---

# 8. ORDER / Divisibility / Annihilator

## 8.1 current order fact

Current implementation:

```text
ord(a)=n
↓
na=0
```

## 8.2 multiples of the order

数学的には、

```text
ord(a)=n
n divides m
↓
ma=0
```

である。

例えば、

```text
ord(a)=2
```

なら、

```text
4a=0
6a=0
8a=0
...
```

である。

## 8.3 no infinite enumeration

これらを fixed-point inference で無限列挙しない。

将来的には、

```text
Divides(n,m)
```

または、

```text
Annihilator(a,n)
```

のような constraint を検討する。

## 8.4 goal-directed check

例えば target が、

```text
6a=0
```

なら、

```text
ord(a)=2
2 divides 6
↓
6a=0
```

と必要時に確認する方式を優先する。

---

# 9. Indeterminacy

## 9.1 Phase 17 の中心候補

Phase 16 完了後の自然な次層は、

```text
Indeterminacy
```

である。

## 9.2 sign indeterminacy

```text
±α
```

を単なる文字列でなく、

```text
α または -α
```

という first-class uncertainty として扱えるようにする。

## 9.3 coefficient indeterminacy

例えば、

```text
α = kβ + γ
k odd
```

を、
具体的な `k` を選ばずに保持する。

Phase 16 の scalar constraint を possible representative family として利用できるようにする。

## 9.4 coset indeterminacy

既存 Phase 15 の coset / modulo layer を使って、

```text
α ∈ β+A
```

のような情報を扱えるようにする。

値を一意に確定しなくても、
coset membership 自体を proof result として保持する。

## 9.5 narrowing

将来的には複数の constraint を合わせて不定性を狭めることも検討する。

ただし set intersection 等は actual theorem need が出た時点で追加する。

---

# 10. Theorem Representation

## 10.1 theorem を data として保持する

将来的には数学的定理を、
Python 内の個別 rule implementation だけでなく、

```text
theorem name
source / provenance
variables
types
quantification
assumptions
side conditions
conclusion
```

を持つ theorem data として表現できるようにする。

## 10.2 assumptions / conclusion

定理は明示的に、

```text
assumptions
↓
conclusion
```

を持つ。

複数仮定は current multi-premise inference と接続する。

## 10.3 universal quantification

「任意の α」については、
current pattern variable の仕組みを拡張し、

```text
typed pattern variables
+
side conditions
```

で表現することを第一候補とする。

全面的な first-order logic system を先に導入しない。

## 10.4 existential statements

将来的に、

```text
∃β, α=2β
```

のような存在命題を表現できるようにする。

必要になった場合には symbolic witness を検討する。

---

# 11. Knowledge Tables / Existing Data

## 11.1 existing tables are reusable

過去に作成したホモトピー群テーブル、
generator data、
E/H/P data 等は原則として再利用する。

ただし、

```text
table lookup
↓
answer
```

だけで終えるのではなく、

```text
table / repository
↓
known fact
↓
Statement / Relation
↓
InferenceRule
↓
derived conclusion
```

という使い方を目標とする。

## 11.2 known group facts

例えば、

```text
π_n(S^k)=G
```

や、

```text
π_k^S=G
```

を known group fact として利用する。

## 11.3 known generator facts

generator table を structured generator representation と接続する。

## 11.4 known map facts

例えば、

```text
E(α)=β
H(γ)=δ
P(η)=θ
```

を provenance 付き known relation として取り込む。

## 11.5 known composition / order / bracket facts

文献から得られる、

```text
ord(α)=n
α∘β=γ
H(α)=β
μ_3 ∈ {...}
```

なども known fact source として取り込めるようにする。

---

# 12. Unstable Toda Bracket

## 12.1 three-fold bracket

まず優先するのは、
実際に Toda の計算で必要になる three-fold bracket である。

例えば、

```text
{α,β,γ}
```

や、

```text
{a,E^t b,E^t c}_t
```

を扱う。

## 12.2 set-valued semantics

Toda bracket を単一 element を返す関数としない。

例えば、

```text
δ ∈ {α,β,γ}
```

や、

```text
{α,β,γ} ⊆ δ+A
```

を表現できるようにする。

## 12.3 indexed bracket

Toda の記法に現れる、

```text
{a,E^t b,E^t c}_t
```

の下付き `t` を、
表示 decoration として捨てない。

内部的には、

```text
TodaBracket(
  entries=(...),
  index=t,
)
```

のように保持する。

## 12.4 suspension exponent と bracket index

```text
E^t b
```

の suspension exponent と、

```text
{a,E^t b,E^t c}_t
```

の bracket index は、
記法上同じ `t` でも内部では別フィールドとして保持する。

必要な theorem が両者の一致を要求する場合に side condition で接続する。

## 12.5 defining conditions

Toda bracket の definition / theorem application に必要な、

```text
composition is defined
composition is zero
dimension condition
suspension condition
```

などを明示的 assumptions として扱う。

## 12.6 stem / dimension

例えば、

```text
9-stem
```

のような情報を保持または導出できる余地を残す。

---

# 13. Higher Toda Brackets

## 13.1 design policy

higher Toda bracket を理論上表現可能な設計にはしておく。

ただし、
4次以降の具体例・具体的 theorem が今後の実装で本当に必要になるかは、
現時点では確定しない。

したがって、

```text
higher Toda bracket support
=
future-capable design
```

とし、

```text
full implementation
=
deferred until actual mathematical example
```

とする。

## 13.2 variable arity

Toda bracket representation を、
固定3項の constructor に強く依存させない。

概念的には、

```text
TodaBracket(
  entries=(...)
)
```

のような variable-arity を許せる構造を候補とする。

ただし初期実装では three-fold bracket だけを validation してもよい。

## 13.3 order / degree / arity を混同しない

以下を別概念として扱う。

```text
number of entries
higher-bracket order
Toda notation degree
bracket index
stem
```

---

# 14. Stable Toda Bracket

## 14.1 notation

stable homotopy category における Toda bracket は、
unstable bracket notation と区別して、

```text
<a,b,c>
```

のような notation を扱えるようにする。

## 14.2 stable context

stable Toda bracket の entries は、

```text
a ∈ π_p^S
b ∈ π_q^S
c ∈ π_r^S
```

のような stable classes として型付けする。

## 14.3 set-valued semantics

stable Toda bracket も単一 element として扱わず、

```text
x ∈ <a,b,c>
```

や、

```text
<a,b,c> ⊆ x+A
```

のような set / coset-valued information を表現できるようにする。

## 14.4 defining conditions

stable bracket についても、

```text
ab=0
bc=0
```

等の defining conditions を theorem assumptions として明示する。

## 14.5 stable degree / stem checking

stable bracket の result degree / stem を、
採用する convention に従って計算・検査できるようにする。

degree convention は実装 Phase で文献と照合し、明文化する。

## 14.6 stable and unstable brackets are distinct

次を単なる notation difference として同一視しない。

```text
{a,b,c}_t
```

と、

```text
<a,b,c>
```

stable / unstable context、
typing、
definition、
indeterminacy が異なる可能性を保持する。

## 14.7 shared infrastructure

一方で以下は共有できる可能性が高い。

```text
entries
membership
subset
coset indeterminacy
provenance
theorem assumptions
typed variables
```

共通 base representation と stable / unstable specialization のどちらが適切かは、
actual theorem implementation 時に決める。

---

# 15. Toda Bracket Membership Example

将来的に次のような式を表現できるようにする。

```text
μ_3 ∈ {η_3, Eν', 8ι_7, ν_7}
```

内部的には概念上、

```text
MembershipStatement(
  element=μ_3,
  set_expression=TodaBracket(...)
)
```

に相当する構造を想定する。

この例の具体的 bracket order / degree / stem semantics は、
文献に基づいて実装 Phase で確定する。

現時点では、
記法だけを見て

```text
entry count
=
Toda bracket order
```

と決め打ちしない。

---

# 16. Provenance for Toda Reasoning

Toda bracket reasoning でも current provenance 方針を維持する。

例えば、

```text
known composition fact
+
zero composition theorem
+
Toda bracket theorem
↓
x ∈ <a,b,c>
```

の dependency chain を追跡可能にする。

同じ conclusion に alternative derivation がある場合は、

```text
first accepted ProofStep
+
duplicate-rejected alternative trace
```

を基本とする。

---

# 17. Long-Term Input Model

長期的には、
推論エンジンへの入力を大きく3種類に分ける。

## 17.1 Known data

```text
unstable homotopy group tables
stable homotopy group tables
generator tables
E/H/P map tables
order facts
composition facts
known Toda-bracket facts
```

## 17.2 Theorems

```text
variables
types
quantification
assumptions
side conditions
conclusion
source
```

## 17.3 User assumptions / query facts

```text
specific elements
specific dimensions
specific stem
temporary assumptions
target statement
```

これらを共通の proof / theorem application layer に接続する。

---

# 18. 推奨する依存順

Phase 16 までで、

```text
Abelian group expression
Homomorphism reasoning
Set / subgroup reasoning
Coset / modulo
Symbolic scalar constraints
```

は実装済みである。

今後の推奨依存順は、

```text
Phase 17
Indeterminacy
  ±α
  coefficient uncertainty
  coset-valued uncertainty
        ↓
Typed homotopy elements
  source / target
  ambient unstable group
        ↓
Stable homotopy group representation
  π_k^S
  stable degree / stem
        ↓
Structured generators
  η_n
  ν'
  μ_n
  ι_n
  stable generator identity
        ↓
Iterated suspension
  E^t α
        ↓
ORDER divisibility / annihilator extension
        ↓
Theorem representation
  assumptions
  conclusion
  typed variables
  quantification
        ↓
Knowledge-table integration
        ↓
Three-fold unstable Toda bracket
  {a,b,c}
  {a,E^t b,E^t c}_t
        ↓
Stable Toda bracket
  <a,b,c>
        ↓
Higher Toda bracket
  only when actual examples require it
```

とする。

これは厳密な Phase 番号ではなく、
設計上の依存関係である。

---

# 19. 実装状況

| 項目 | 状態 | 備考 |
|---|---|---|
| Additive expression `α+β` | IMPLEMENTED | Phase 12 |
| additive inverse `-α` | IMPLEMENTED | Phase 12 |
| symbolic coefficient `kβ` | IMPLEMENTED | Phase 16 |
| homomorphism reasoning | IMPLEMENTED | Phase 13 |
| membership `α∈A` | IMPLEMENTED | Phase 14 |
| subset `A⊆B` | IMPLEMENTED | Phase 14 |
| coset `α+A` | IMPLEMENTED | Phase 15 |
| modulo `α≡β mod A` | IMPLEMENTED | Phase 15 |
| `Odd(k)` / `Even(k)` | IMPLEMENTED | Phase 16 |
| scalar congruence | IMPLEMENTED | Phase 16 |
| `α=kβ+γ` structural form | IMPLEMENTED | Phase 16 |
| sign indeterminacy `±α` | PLANNED | Phase 17 candidate |
| coefficient-family indeterminacy | PLANNED | Phase 17 candidate |
| typed source / target | PLANNED | composition / Toda typing |
| ambient homotopy group validation | PLANNED | addition / equality typing |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| structured generator notation | PLANNED | prime / bar / index |
| iterated suspension `E^t α` | PLANNED | indexed Toda notation |
| divisibility / annihilator reasoning | PLANNED | no infinite multiple-zero enumeration |
| theorem representation | PLANNED | assumptions / conclusion / source |
| universal quantification | PLANNED | typed pattern variables first |
| existential statements | PLANNED | witness later |
| knowledge-table integration | PLANNED | tables as known fact sources |
| unstable three-fold Toda bracket | PLANNED | first bracket target |
| indexed unstable bracket | PLANNED | `{a,E^t b,E^t c}_t` |
| Toda bracket membership | PLANNED | e.g. `μ_3 ∈ {...}` |
| stable Toda bracket `<a,b,c>` | PLANNED | stable homotopy layer required |
| stable degree / stem checking | PLANNED | convention to be fixed |
| higher Toda bracket | DEFERRED | implement only when concrete need appears |

---

# 20. Phase 17 Boundary

Phase 16 で symbolic scalar constraint layer が完成した。

次の自然な Phase は、

```text
Phase 17: Indeterminacy
```

である。

候補となる actual mathematical forms:

```text
±α
```

```text
α = kβ + γ
k odd
```

```text
α ∈ β+A
```

Phase 17 では、
不定性を premature に representative へ collapse しない。

Toda bracket 全体を先取りせず、
後の Toda reasoning に必要な uncertainty semantics を最小単位で導入する。

---

# 21. Stable Homotopy / Toda Boundary

stable homotopy group と stable Toda bracket は、
将来の独立した重要層とする。

ただし Phase 17 で先取りしない。

stable layer を実装する際には最低限、

```text
stable element
stable group π_k^S
stable degree / stem
stable composition typing
stable Toda bracket <a,b,c>
```

を一貫した convention で設計する。

unstable data との接続は、
stabilization theorem / stable-range reasoning を通じて明示する。

---

# 22. Higher Toda Bracket Boundary

higher Toda bracket は、
設計上は将来対応可能にしておく。

しかし、

```text
4次以降の具体的 bracket を
この project で実際に必要とするか
```

は現時点では確定していない。

そのため、

```text
three-fold unstable bracket
+
three-fold stable bracket
```

を優先し、

```text
higher bracket implementation
```

は具体的文献例・定理・計算が必要になった時点まで延期する。

---

# 23. Testing Principle

新しい mathematical layer を追加するときは、

1. representation test
2. typing / validity test
3. single-rule semantic test
4. invalid-premise rejection
5. multi-round integration
6. generic-rule reconnection
7. provenance
8. representative mathematical scenario
9. termination / inference-scope boundary
10. full regression

を基本とする。

Toda bracket ではさらに、

```text
defining composition validity
zero-composition assumptions
degree / stem consistency
indeterminacy
membership / containment
```

をテストする。

---

# 24. Documentation Policy

```text
README.md
=
current capabilities / current status

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

roadmap の項目が実装された場合は、
その Phase 完了時に状態を更新する。

---

# 25. 長期目標

最終的には、

```text
known unstable homotopy groups
+
known stable homotopy groups
+
generator / map tables
+
quantified theorems
+
EHP exactness
+
ORDER
+
Suspension / stabilization
+
composition
+
Hopf invariant
+
additive reasoning
+
subgroup / modulo reasoning
+
symbolic scalar constraints
+
indeterminacy
+
unstable Toda brackets
+
stable Toda brackets
↓
new homotopy-theoretic conclusions
```

を同一の proof graph 上で扱えることを目標とする。

その際、

```text
exact value
partial information
sign uncertainty
coefficient uncertainty
coset uncertainty
Toda-bracket membership
stable Toda-bracket membership
```

をすべて provenance 付き knowledge として保持する。

EHP Proof Tracer の長期的な方向性は、

```text
数学的に判明している情報を、
型・確定値・部分情報・不定性・定理・既知データとして構造化し、
provenance を保った推論で接続する
```

proof tracer / reasoning system へ発展させることである。
