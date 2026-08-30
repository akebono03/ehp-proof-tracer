# EHP Proof Tracer Roadmap

## 1. この文書の目的

この文書は、EHP Proof Tracer の将来拡張に関する長期的な設計方針を記録する。

`README.md` は current capabilities / current status、
`docs/design.md` は current architecture / semantics / boundaries、
`docs/development_log.md` は chronological implementation history を扱う。

この `docs/roadmap.md` は、まだ未実装の機能を含む将来構想と、
それらの依存関係・実装優先順位を整理するための文書とする。

Phase 18 完了時点では、以下の基盤が実装済みである.

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
Indeterminacy
Toda bracket minimum representation
Toda bracket membership representation
Toda bracket definedness from zero compositions
```

したがって、次の直接的な開発対象候補は:

```text
Phase 19
Toda bracket membership / first theorem bridge
```

である。

その後、

```text
Toda bracket membership / value
indexed unstable Toda notation
typed homotopy elements
stable homotopy groups
structured generators
iterated suspension
theorem representation
knowledge-table integration
stable Toda brackets
higher Toda brackets
```

へ必要に応じて進む。

この文書に記載された項目は、記載されているだけでは実装済みを意味しない。
各機能は必要な Phase において個別に仕様化し、
既存 API と generic inference engine を不必要に壊さない最小変更で導入する。

---

# 2. 現在の実装基盤

Phase 17 完了時点で、proof / inference layer には次の主要構造がある。

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

加えて:

```text
MapSymbol
ScalarSymbol
```

Proof-level statement / relation:

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
CosetMembershipStatement
SignIndeterminacyStatement
CoefficientIndeterminacyStatement
```

Current examples:

```text
α+β
-α
nα
kβ
α=kβ+γ

f(α+β)=f(α)+f(β)

α∈A
A⊆B
A=B

α≡β mod A
α+A
α∈β+A

k odd
k even
k≡1 mod 2

x=±α
x∈{kβ+γ | k odd}
```

Phase 17 representative integration:

```text
x=kβ+γ
k odd
x≡δ mod A
↓
k≡1 mod 2
CoefficientIndeterminacyStatement
SignIndeterminacyStatement
CosetMembershipStatement
ModuloStatement
↓
FIXED_POINT
```

without:

```text
x=δ
```

and without concrete candidate enumeration.

---

# 3. 基本設計原則

## 3.1 actual mathematical need first

```text
actual mathematical need
↓
minimal representation
↓
domain InferenceRule
↓
existing generic engine
```

完全な symbolic algebra system、完全な theorem prover、完全な higher Toda
system を先に実装しない。

## 3.2 不定性を消さずに保持する

Implemented Phase 17 forms:

```text
x=±α
x≡β mod A
x∈β+A
x∈{kβ+γ | k odd}
```

値が未確定でも、判明している制約を first-class knowledge として保持する。

## 3.3 candidate enumeration を避ける

```text
k odd
```

から:

```text
1,3,5,...
```

を無限列挙しない。

```text
x∈β+A
```

から coset element を列挙しない。

Toda bracket でも同じ原則を維持する。

## 3.4 数学的対象と表示 notation を分離する

```text
Eν'
```

は generator name に operation を埋め込まず:

```text
Suspension(ν')
```

として扱う。

```text
8ι_7
```

は:

```text
Multiple(8,ι_7)
```

として扱う。

## 3.5 mathematical applicability と active inference scope を分離する

数学的に正しい theorem でも、常に無制限に生成しない。

```text
mathematical applicability
≠
active inference scope
```

## 3.6 fixed-point termination を壊さない

必要に応じて:

```text
goal-directed reasoning
bounded execution
staged execution
explicit active scope
```

を利用する。

---

# 4. Phase 18: Toda bracket minimum representation

## 4.1 目的

Phase 18 は Toda bracket を初めて first-class に表現する。

最初の原則:

```text
bracket input structure
≠
bracket value
```

Toda bracket を:

```text
TodaBracket(...) -> Expression
```

という一意値を返す関数として設計しない。

## 4.2 最初の actual notation

最初の対象候補:

```text
{a,b,c}
```

Three-fold unstable bracket を最小 actual example とする。

必要であれば次に:

```text
{a,E^t b,E^t c}_t
```

へ拡張する。

## 4.3 set-valued semantics

Toda bracket は一般に集合値・不定性を持つ。

したがって将来的な statement は:

```text
x ∈ {a,b,c}
```

や:

```text
{a,b,c} ⊆ x+A
```

のような形を候補とする。

Phase 17 の indeterminacy infrastructure を最大限再利用する。

## 4.4 no universal set hierarchy first

Phase 18-1 でいきなり:

```text
GeneralSetExpression
GeneralCandidateFamily
UniversalIndeterminacy
```

を作らない。

Actual bracket example から必要な minimal representation を決める。

## 4.5 stable / unstable notation

次を同一視しない:

```text
{a,b,c}
<a,b,c>
```

Stable bracket は独立した stable context を必要とする可能性が高い。

---

# 5. Indexed Unstable Toda Bracket

## 5.1 notation

Toda の記法:

```text
{a,E^t b,E^t c}_t
```

の下付き `t` を表示 decoration として捨てない。

候補:

```text
TodaBracket(
  entries=(...),
  index=t,
)
```

## 5.2 suspension exponent と bracket index

```text
E^t b
```

の `t` と:

```text
{...}_t
```

の `t` は、notation 上同じ記号でも内部では別フィールドとして保持する。

Theorem が一致を要求するときに explicit side condition で接続する。

## 5.3 IteratedSuspension

Current `Suspension` の nested application で concrete iteration は表せるが、
symbolic exponent:

```text
E^t α
```

はまだ first-class ではない。

Actual indexed bracket が要求する Phase で:

```text
IteratedSuspension
```

または同等の minimal structure を検討する。

Phase 18 の最初の subphase で先取りしない。

---

# 6. Toda Bracket Membership

目標例:

```text
μ_3 ∈ {η_3, Eν', 8ι_7, ν_7}
```

この notation の bracket order / index / stem semantics は actual literature
example と照合して確定する。

Important:

```text
entry count
≠
automatically bracket order
```

とし、記法だけから意味を決め打ちしない。

Possible representation:

```text
TodaBracketValueStatement
```

または:

```text
MembershipStatement-like dedicated statement
```

のどちらが適切かは Phase 18 actual example で決定する。

Current `MembershipStatement` は subgroup membership 専用なので、
単純に set expression へ型を広げることは避ける。

---

# 7. Toda Defining Conditions

Three-fold Toda bracket の theorem application には一般に composition
conditions が必要になる。

候補:

```text
a∘b=0
b∘c=0
```

Current project already has:

```text
Composition
ZERO relation
known zero-composition reasoning
```

Phase 18 以降では、この既存 infrastructure を bracket defining conditions
へ接続する。

ただし representation Phase で theorem rule を先取りしない。

---

# 8. Toda Indeterminacy

Toda bracket value / containment は Phase 17 の原則を維持する。

```text
bracket membership
≠
exact value
```

```text
bracket containment in coset
≠
representative equality
```

Potential future forms:

```text
x ∈ TodaBracket(...)
```

```text
TodaBracket(...) ⊆ x+A
```

```text
x = ±α
```

```text
x ∈ {kβ+γ | k odd}
```

必要に応じて Phase 17 statements と接続する。

No candidate enumeration.

---

# 9. Typed Homotopy Elements

Toda bracket の well-definedness を本格的に検査する段階では、
各 element の type が必要になる。

Unstable:

```text
α : S^m → S^n
α ∈ π_m(S^n)
```

必要情報候補:

```text
source sphere
target sphere
ambient homotopy group
stem
```

Addition:

```text
ambient_group(a)=ambient_group(b)
```

Composition:

```text
target(b)=source(a)
```

Phase 18 minimal bracket representation が typing を必要としない範囲では
先取りしない。

Actual defining-condition theorem が要求した時点で導入する。

---

# 10. Stable Homotopy Groups

Stable context:

```text
α ∈ π_k^S
```

を unstable group と区別する。

Stable degree / stem convention を明文化する。

Unstable class と stable class を notation conversion だけで同一視せず:

```text
stabilization
Freudenthal
stable-range theorem
```

等の explicit bridge を利用する。

---

# 11. Structured Generator Representation

Toda の具体例では:

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

などが必要になる。

将来的に:

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

等を検討。

Important:

```text
ν
ν'
\barν
```

を表示違いとして collapse しない。

Operation は generator name に埋め込まない。

---

# 12. Iterated Suspension

Future actual notation:

```text
E^t α
```

Potential:

```text
IteratedSuspension(
  expression=α,
  exponent=t,
)
```

`t` は symbolic scalar との関係を検討する。

Typing:

```text
α : S^m → S^n
↓
E^t α : S^(m+t) → S^(n+t)
```

一般的 symbolic exponent simplifier は先に実装しない。

---

# 13. ORDER / Divisibility / Annihilator

Current:

```text
ord(a)=n
→
na=0
```

Mathematically:

```text
ord(a)=n
n divides m
→
ma=0
```

だが:

```text
2a=0
4a=0
6a=0
...
```

を無限生成しない。

Future candidate:

```text
Divides(n,m)
Annihilator(a,n)
```

または goal-directed check。

---

# 14. Theorem Representation

Long-term theorem data:

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

Current multi-premise `InferenceRule` と接続する。

Universal quantification はまず:

```text
typed pattern variables
+
side conditions
```

を候補とする。

全面的 first-order logic system を先に実装しない。

Existential statements:

```text
∃β, α=2β
```

は actual theorem need が出た段階で symbolic witness を検討する。

---

# 15. Knowledge Tables / Existing Data

Existing group / generator / EHP data は再利用する。

Goal:

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

Possible known facts:

```text
π_n(S^k)=G
π_k^S=G
ord(α)=n
α∘β=γ
H(α)=β
μ_3 ∈ TodaBracket(...)
```

Literature provenance を維持する。

---

# 16. Stable Toda Bracket

Stable notation:

```text
<a,b,c>
```

Unstable notation:

```text
{a,b,c}
```

と同一視しない。

Stable entries:

```text
a ∈ π_p^S
b ∈ π_q^S
c ∈ π_r^S
```

Defining conditions:

```text
ab=0
bc=0
```

Result degree / stem は採用 convention を明文化して検査する。

Set-valued semantics:

```text
x ∈ <a,b,c>
```

```text
<a,b,c> ⊆ x+A
```

---

# 17. Higher Toda Brackets

Higher / variable-arity bracket は future-capable design にするが、
full implementation は actual concrete example まで延期する。

Important distinctions:

```text
number of entries
higher-bracket order
Toda notation degree
bracket index
stem
```

を混同しない。

Initial priority:

```text
three-fold unstable bracket
three-fold stable bracket
```

Higher brackets は concrete literature need が出た時点で実装する。

---

# 18. Provenance for Toda Reasoning

Toda reasoning でも:

```text
known composition fact
+
zero-composition fact
+
Toda theorem
↓
bracket membership / containment
```

の dependency chain を追跡可能にする。

Alternative derivation policy:

```text
first accepted ProofStep
+
duplicate-rejected alternative trace
```

を維持する。

---

# 19. Long-Term Input Model

## Known data

```text
unstable homotopy group tables
stable homotopy group tables
generator tables
E/H/P map tables
order facts
composition facts
known Toda-bracket facts
```

## Theorems

```text
variables
types
quantification
assumptions
side conditions
conclusion
source
```

## User assumptions / query facts

```text
specific elements
specific dimensions
specific stem
temporary assumptions
target statement
```

これらを共通 proof graph に接続する。

---

# 20. 推奨 Phase 順

Phase 17 まで:

```text
Phase 12  Additive expressions
Phase 13  Homomorphism reasoning
Phase 14  Set / subgroup reasoning
Phase 15  Coset / modulo reasoning
Phase 16  Symbolic scalar constraints
Phase 17  Indeterminacy
Phase 18  Toda bracket minimum representation
```

完了。

次:

```text
Phase 19 candidate
Toda bracket membership / first bracket theorem bridge
        ↓
Phase 20 candidate
Indexed unstable Toda notation
  {a,E^t b,E^t c}_t
        ↓
Typed homotopy-element extension
  when defining-condition validation requires it
        ↓
Structured generators / iterated suspension
  as actual notation requires
        ↓
Theorem representation / knowledge-table integration
        ↓
Stable homotopy representation
        ↓
Stable Toda bracket
  <a,b,c>
        ↓
Higher Toda bracket
  only when actual examples require it
```

Phase 19 以降の番号は provisional。

Actual mathematical need に応じて再配置可能。

---

# 21. Phase 18 完了

Phase 18 では three-fold unstable Toda bracket の最小表現を導入した。

Implemented object:

```text
TodaBracket(a,b,c)
```

Notation:

```text
{a,b,c}
```

Important:

```text
TodaBracket
≠
Expression
```

Bracket entries are ordered structural inputs.

Implemented statements:

```text
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

Semantics:

```text
x∈{a,b,c}
```

```text
{a,b,c} defined
```

Existing composition / ZERO reasoning と接続:

```text
a∘b=0
b∘c=0
↓
ZERO(a∘b)
ZERO(b∘c)
↓
{a,b,c} defined
```

The two zero compositions must share the middle entry.

Current boundaries:

```text
definedness
≠
membership
```

```text
membership
≠
exact value
```

```text
x∈{a,b,c}
+
x=±α
↛
x=α
```

Phase 17 indeterminacy と同一 knowledge state に coexist 可能。

Provenance:

```text
original composition equalities
↓
generic ZERO facts
↓
Toda definedness
```

を追跡可能。

Representative scenario は:

```text
FIXED_POINT
```

に到達し、explicit terminal check:

```text
new_steps == ()
```

を確認済み。

Verified:

```text
tests/test_toda_rules.py
20 passed in 3.36s
```

```text
full suite
1048 passed in 61.09s
```

Generic inference engine:

```text
unchanged
```

---

# 22. Phase 19 candidate：Toda bracket membership / first theorem bridge

## 22.1 目的

Phase 18 では:

```text
x∈{a,b,c}
```

を first-class known statement として保持可能になった。

Phase 19 では actual mathematical theorem / known Toda fact を使って、
membership conclusion を導出する最初の bridge を検討する。

Intended shape:

```text
explicit theorem premises
↓
TodaBracketMembershipStatement
```

Important:

```text
{a,b,c} defined
↛
x∈{a,b,c}
```

なので、definedness だけから arbitrary element membership を生成する rule
は導入しない。

## 22.2 actual example first

最初の theorem bridge は literature / concrete known bracket example に
基づいて仕様化する。

Possible target form:

```text
known Toda fact
μ_3 ∈ {...}
```

ただし具体的な notation / entry count / bracket order / stem semantics は
actual source と照合してから固定する。

## 22.3 provenance

Membership conclusion には:

```text
theorem / known fact
composition assumptions if required
source / literature provenance
```

を保持する。

## 22.4 no universal theorem language yet

Phase 19 で直ちに:

```text
universal quantified theorem framework
general set containment algebra
general candidate-set solver
```

を導入しない。

---

# 23. Phase 20 candidate：indexed unstable Toda notation

Target notation:

```text
{a,E^t b,E^t c}_t
```

Phase 20 では下付き bracket index と suspension exponent を separate
structural fields として保持する。

```text
bracket index t
≠
suspension exponent t
```

同じ notation symbol を使っていても内部で collapse しない。

必要に応じて:

```text
IteratedSuspension
```

または同等の minimal structure を検討する。

Stable notation:

```text
<a,b,c>
```

は引き続き別 context として deferred。

---

# 24. 実装状況


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
| coset membership indeterminacy `x∈β+A` | IMPLEMENTED | Phase 17 |
| sign indeterminacy `x=±α` | IMPLEMENTED | Phase 17 |
| coefficient-family indeterminacy | IMPLEMENTED | Phase 17 |
| modulo ↔ coset-membership bridge | IMPLEMENTED | Phase 17 |
| equality → sign indeterminacy | IMPLEMENTED | Phase 17 |
| symbolic odd equality → coefficient indeterminacy | IMPLEMENTED | Phase 17 |
| Toda bracket `{a,b,c}` | IMPLEMENTED | Phase 18 |
| Toda bracket membership | IMPLEMENTED | Phase 18 |
| Toda bracket definedness from zero compositions | IMPLEMENTED | Phase 18 |
| indexed unstable bracket `{a,E^t b,E^t c}_t` | PLANNED | after minimal bracket |
| typed source / target | PLANNED | when bracket validity needs it |
| ambient homotopy group validation | PLANNED | addition / equality / bracket typing |
| stable homotopy group `π_k^S` | PLANNED | stable context |
| structured generator notation | PLANNED | prime / bar / index |
| iterated suspension `E^t α` | PLANNED | indexed Toda notation |
| divisibility / annihilator reasoning | PLANNED | no infinite enumeration |
| theorem representation | PLANNED | assumptions / conclusion / source |
| universal quantification | PLANNED | typed pattern variables first |
| existential statements | PLANNED | witness later |
| knowledge-table integration | PLANNED | tables as known fact sources |
| stable Toda bracket `<a,b,c>` | PLANNED | stable layer required |
| stable degree / stem checking | PLANNED | convention to be fixed |
| higher Toda bracket | DEFERRED | concrete need required |

---

# 25. Phase 18 completion boundary

Implemented:

```text
TodaBracket(a,b,c)
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

Bridges:

```text
a∘b=0
b∘c=0
↓
generic ZERO
↓
{a,b,c} defined
```

Coexistence:

```text
x∈{a,b,c}
x=±α
```

```text
x∈{a,b,c}
x∈β+A
```

Safety:

```text
{a,b,c} defined
↛
x∈{a,b,c}
```

```text
x∈{a,b,c}
↛
exact value
```

```text
x∈{a,b,c}
+
x=±α
↛
x=α
```

No candidate enumeration.

No general set-valued expression hierarchy.

No indexed unstable notation yet.

No stable / higher Toda bracket yet.

Current representative Toda rule family reaches finite:

```text
FIXED_POINT
```

and terminal:

```text
new_steps == ()
```

Verified:

```text
tests/test_toda_rules.py
20 passed in 3.36s
```

```text
full suite
1048 passed in 61.09s
```

---

# 26. Testing Principle



新しい mathematical layer を追加するときは:

1. representation test
2. structural distinction / typing test
3. single-rule semantic test
4. invalid-premise rejection
5. multi-round integration
6. generic-rule reconnection
7. provenance
8. representative mathematical scenario
9. termination / inference-scope boundary
10. full regression

Toda bracket では追加で:

```text
defining composition validity
zero-composition assumptions
membership / containment
indeterminacy preservation
index / suspension-parameter distinction
stable / unstable distinction
```

を actual implemented scope に応じてテストする。

---

# 27. Documentation Policy

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

# 28. 長期目標

最終的には:

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

を同一 proof graph 上で扱う。

その際:

```text
exact value
partial information
sign uncertainty
coefficient uncertainty
coset uncertainty
Toda-bracket membership
stable Toda-bracket membership
```

を provenance 付き knowledge として保持する。

EHP Proof Tracer の長期的な方向性は:

```text
数学的に判明している情報を、
型・確定値・部分情報・不定性・定理・既知データとして構造化し、
provenance を保った推論で接続する
```

proof tracer / reasoning system へ発展させることである。
