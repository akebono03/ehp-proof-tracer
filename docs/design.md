# ehp_proof 設計メモ

この文書は Phase 7-8、すなわち Phase 7 完了時点の
「現在の設計」を正本としてまとめる。

過去の各 Phase で書かれた設計メモには、その当時は正しかった
「未実装」「今後の課題」という記述がある。

現在の仕様判断では、本ファイルの最新記述を優先する。

---

# 1. 全体アーキテクチャ

基本の依存方向は次とする。

```text
homotopy / EHP domain inference rules
        ↓
generic proof / inference engine
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

逆向き依存は作らない。

特に algebra 層は、

```text
E
H
P
Toda bracket
Hopf invariant
element order theorem
```

などのホモトピー論的意味を知らない。

generic inference engine も、
個別の EHP theorem や element-order theorem の内容を知らない。

---

# 2. integer linear algebra / algebra 層

## 2.1 責務

integer linear algebra / algebra 層は、

- relation matrix
- integer lattice
- Hermite normal form
- Smith normal form
- finitely generated abelian group
- group homomorphism
- kernel
- image
- cokernel
- subgroup
- quotient
- exact sequence
- finite extension candidate

を担当する。

## 2.2 有限生成アーベル群

一般形を、

```text
Z^r ⊕ finite torsion
```

として統一的に扱う。

自由部分を別理論にしない。

## 2.3 finite enumeration

有限群については全元列挙方式を削除しない。

その役割は presentation-based calculation に対する
reference implementation / cross-check である。

## 2.4 exactness

完全性:

```text
Im(f) = Ker(g)
```

は中間群内の部分群 / lattice の一致として判定する。

一方、

```text
B / Im(f) ≅ Im(g)
```

は抽象群構造の同型である。

この2つを混同しない。

## 2.5 primary decomposition

algebra 層では、

```text
Z/2
Z/3
Z/4
Z/9
```

を同じ有限生成アーベル群として扱う。

```text
2-primary
odd-primary
double EHP
```

などの理論上の区別は上位 domain 層の責務とする。

---

# 3. homotopy / EHP data 層

EHP 層は、

- 対象ホモトピー群の選択
- generator 名
- E/H/P の構築
- source / target generator の対応
- repository data から homomorphism matrix への変換

を担当する。

一般群論計算は algebra 層へ委譲する。

群の抽象構造と、

```text
η
ν
σ
ξ
λ
```

などの数学的 generator 名は分離する。

---

# 4. Expression 層

Expression は数学的式の構造を保持する。

現在の基礎型:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
└── Composition
```

補助 generator factory:

```text
eta(n)
nu(n)
sigma(n)
```

Expression 層は、

- 式の簡約
- dimension validity
- theorem application
- algebra calculation
- order calculation

を担当しない。

例えば、

```text
Multiple(2, η)
```

を見ても Expression 層自身はそれが zero かどうかを判断しない。

その判断は domain rule / relation reasoning の責務である。

`HomotopyElement` と algebra 層の `GroupElement` は別概念とする。

---

# 5. Relation / Proof 層

## 5.1 Relation

`Relation` は既知の数学的 relation / fact を表す。

現在の fields:

```text
lhs
rhs
relation_type
source
note
```

`RelationType`:

```text
EQUALITY
ZERO
ORDER
```

`lhs` / `rhs` は `Expression` に限定しない。

理由は、

```text
ord(α)
Ker(H)
Im(E)
π_n(S^m)
```

など、単純な expression equality 以外の fact を
同じ relation model に載せるためである。

## 5.2 EQUALITY

```text
Relation(
  lhs=x,
  rhs=y,
  relation_type=RelationType.EQUALITY,
)
```

は現在の relation layer では directed data representation として保持する。

数学的な対称性・推移性は object の自動 canonicalization ではなく、
明示的な inference rules によって導出する。

## 5.3 ZERO

```text
Relation(
  lhs=x,
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

は `x = 0` という fact を表す。

ZERO は EHP 固有の概念ではない。

Phase 6 では EHP zero-composition が generic ZERO へ bridge し、
Phase 7 では element-order fact からも generic ZERO が生成される。

この shared representation により異なる theorem family の結果を
同じ generic relation rule が利用できる。

## 5.4 ORDER

具体的な exact finite order fact は、

```text
Relation(
  lhs=α,
  rhs=n,
  relation_type=RelationType.ORDER,
)
```

で表し、

```text
ord(α) = n
```

を意味する。

`n` は正の整数とする。

この semantics は exact order であり、

```text
ord(α) divides n
```

という weaker statement ではない。

現時点では infinite order を `RelationType.ORDER` で表現しない。

## 5.5 order_relation()

concrete ORDER fact の生成には、

```text
order_relation(
  element,
  order,
  source=None,
  note=None,
)
```

を利用する。

`order` は positive `int` を要求する。

以下は invalid:

```text
True
0
-1
2.0
"2"
```

ORDER validation を `Relation.__post_init__` に入れない。

理由は inference pattern として、

```text
rhs=PatternVariable("order")
```

を保持する必要があるためである。

すなわち、

```text
Relation
=
permissive structural fact / pattern container
```

と、

```text
order_relation()
=
validated concrete exact-order constructor
```

を分離する。

## 5.6 LiteratureReference

文献 metadata:

```text
label
author
title
year
locator
```

を構造化する。

relation の source と ProofStep の note / inference provenance を混同しない。

## 5.7 ProofStep

`ProofStep` は1回の計算・推論を表す。

```text
premises
↓
rule
↓
conclusion
```

現在の fields:

```text
conclusion
premises
rule
note
inference_rule
```

## 5.8 ProofRule と InferenceRule

両者は別概念である。

```text
ProofRule
=
ProofStep の大分類
```

```text
InferenceRule
=
具体的な数学的推論規則
```

generic inference によって生成された step は、

```text
ProofRule.INFERENCE
```

を持ち、さらに具体的な source `InferenceRule` を保持する。

## 5.9 provenance / dependency

derived step の依存関係は、

```text
ProofStep.premises
```

で直接保持する。

Phase 7-6 では、

```text
Image + Kernel
↓
Exactness
↓
EHPZeroCompositionStatement
↓
EHP-derived ZERO
```

と、

```text
ORDER fact
↓
ORDER-derived ZERO
```

の dependency chain を同一 fixed-point run 内で明示的に検証した。

knowledge state を共有しても、
各 ProofStep の premise chain は混線させない。

独立 DAG class や branch identifier は現時点では導入しない。

---

# 6. RelationRepository / formatter

RelationRepository は、

```text
known Relation の保存・検索
```

を担当する。

theorem application や inference execution は担当しない。

formatter は、

```text
Expression
Statement
ProofStep
Proof
```

などの表示を担当する。

model 自体に表示専用 state を持ち込まない。

---

# 7. Generic inference engine

Phase 5-65 を generic inference engine の基盤完成点とする。

## 7.1 責務

generic engine の責務は、

```text
どの数学 theorem が正しいか
```

ではなく、

```text
与えられた rule を
どのように match / bind / apply / iterate するか
```

である。

したがって engine に、

```python
if rule_is_ehp:
  ...
```

や、

```python
if relation_type_is_order:
  ...
```

のような domain-specific theorem branch を入れない。

Phase 7 でも generic engine 自体の変更なしに
ORDER rule family を実装できたことを重要な設計確認とする。

---

# 8. InferenceRule

現在の主な構造:

```text
name
description
premise_patterns
conclusion_builder
conclusion_pattern
match_guard
```

## 8.1 conclusion_builder

任意 callable によって conclusion を構築できる。

互換性や、pattern substitution だけでは書きづらい特殊な construction
のために残す。

## 8.2 conclusion_pattern

structured Relation または dataclass statement pattern に bindings を
代入して conclusion を生成できる。

Phase 7 の ORDER rule では nested expression:

```text
Multiple(
  coefficient=?order,
  expression=?element,
)
```

を conclusion pattern の内部に置く。

## 8.3 builder と pattern

両方が指定された場合は現実装では builder を優先する。

この precedence は current API semantics とする。

## 8.4 match_guard

`match_guard` は、

```text
matched premises
bindings
```

を受け取る optional callable である。

premise matching / binding consistency が成立した後に
domain-specific validation を追加するために使う。

例えば ORDER rule では pattern relation 自体は permissive なので、
bound order が positive integer かどうかを guard で確認できる。

---

# 9. PremisePattern

現在の fields:

```text
proof_rule
statement_type
statement_pattern
relation_type
relation_pattern
```

outer category matching と、
Relation / dataclass statement の structured matching を併用できる。

empty pattern は任意の step に match する。

---

# 10. PatternVariable / VariableBinding

## 10.1 PatternVariable

pattern 内の変数を表す。

構造的 equality は name による。

## 10.2 VariableBinding

```text
PatternVariable
→
value
```

を explicit object として保持する。

value は任意型を許す。

---

# 11. Matching semantics

## 11.1 match_pattern_value()

pattern が `PatternVariable` なら binding を生成する。

literal なら ordinary Python equality を要求する。

## 11.2 match_relation_pattern()

`Relation` の、

```text
lhs
rhs
relation_type
```

を structured に match する。

同じ variable が繰り返し現れる場合は binding consistency を要求する。

現時点の matching は、
任意の nested expression tree を完全再帰 unification する言語ではない。

Phase 7 の ORDER premise は、

```text
lhs=?element
rhs=?order
```

として element / order 全体を bind するため、
この制限に抵触しない。

## 11.3 match_statement_pattern()

dataclass statement の直接 fields を match する。

EHP の structured statement matching に利用する。

---

# 12. Substitution semantics

## 12.1 substitute_pattern_value()

`PatternVariable` は bound value へ置換する。

さらに dataclass instance であれば、
各 field に対して再帰的に substitution を行う。

これにより Phase 7 では、

```text
Relation(
  lhs=Multiple(
    coefficient=?order,
    expression=?element,
  ),
  rhs=Zero(),
  relation_type=ZERO,
)
```

を、

```text
?order = 2
?element = η3
```

から、

```text
2η3 = 0
```

へ具体化できる。

このため nested `Multiple` substitution 専用の engine feature は追加しない。

## 12.2 unbound variable

unbound `PatternVariable` は現在 `None` へ substitution される。

domain rule は conclusion に必要な variable を premise で bind する責任を持つ。

---

# 13. 複数 premise と shared bindings

複数 premise の matching では、
同じ `PatternVariable` は同じ value へ bind されなければならない。

binding conflict branch は reject し、
backtracking は別 candidate を探索する。

これにより relation theorem は、
単なる statement type の組合せではなく、
共有される数学的対象の整合性を要求できる。

---

# 14. Exhaustive premise assignment

canonical search API:

```text
find_all_matching_premises()
```

search semantics:

- ordered assignment
- premise pattern order を維持
- available step order を維持
- deterministic depth-first backtracking
- 1 assignment 内では同じ available-step index を再利用しない
- binding conflict branch は除外
- valid assignment はすべて列挙

first-result compatibility APIs は維持する。

---

# 15. InferenceMatch / application

`InferenceMatch` は、

```text
inference_rule
premises
bindings
```

を持つ。

`apply_inference_match()` は、

```text
ProofRule.INFERENCE
```

の derived `ProofStep` を生成し、
matched premises と source `InferenceRule` を保存する。

この保存が Phase 7-6 の provenance test の基礎である。

---

# 16. Duplicate semantics

knowledge state の重複判定は、

```python
step.conclusion == known_conclusion
```

という ordinary Python equality に基づく。

同じ conclusion が複数 derivation から得られた場合、
final knowledge state には最初に accepted された ProofStep を保持する。

別 derivation candidate は application / rejection trace には残り得る。

現時点では theorem-aware equivalence や all-proof collection は行わない。

---

# 17. Fixed-point semantics

fixed-point execution は、
各 productive round で genuinely new conclusions を追加する。

新しい conclusion がなくなれば:

```text
InferenceTerminationReason.FIXED_POINT
```

で終了する。

`max_rounds` は safety bound であり、
semantic cycle detector ではない。

Phase completion の representative test では、
termination reason の確認に加えて final state にもう一度 round を適用し、

```text
new_steps == ()
```

を確認する。

これを genuine fixed-point confirmation とする。

---

# 18. Equality rules

## 18.1 symmetry

```text
x = y
↓
y = x
```

## 18.2 transitivity

```text
x = y
y = z
↓
x = z
```

## 18.3 equality closure

symmetry + transitivity を fixed point まで反復することで、
connected component 内の directed equality closure が得られる。

special graph algorithm は導入しない。

closure は generic rule execution の結果として生成する。

reflexive equality も symmetry / transitivity の組合せから
derived conclusion として現れ得る。

---

# 19. ZERO propagation rules

## 19.1 Phase 6 composition-specific rules

Phase 6 では EHP composition ZERO を対象として、
known-zero lhs が `Composition` であることを guard する
ZERO propagation rules を導入した。

これらは既存 Phase 6 API / regression として維持する。

## 19.2 Phase 7 generic ZERO propagation

Phase 7 では、

```text
x = 0
y = x
↓
y = 0
```

という expression-type-independent rule を追加する。

この rule は known-zero lhs が `Composition` であることを要求しない。

そのため、

```text
Composition(H,E) = 0
```

だけでなく、

```text
Multiple(n, α) = 0
```

にも利用できる。

この generic ZERO propagation が、
異なる domain theorem family を共通 relation layer へ接続する重要な bridge
となる。

---

# 20. Phase 6 EHP rule family

Phase 6 の代表 rule family:

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
equality symmetry
equality transitivity
ZERO propagation
```

EHP-specific intermediate statement と generic Relation を分離する。

EHP zero composition から generic ZERO へ移る点を
domain / generic integration boundary とする。

---

# 21. Phase 7 ORDER rule family

## 21.1 mathematical semantics

Phase 7 の中心 theorem:

```text
ord(α) = n
↓
nα = 0
```

ここで `ord(α)=n` は exact finite additive order を意味する。

## 21.2 representation

premise:

```text
Relation(
  lhs=?element,
  rhs=?order,
  relation_type=ORDER,
)
```

conclusion:

```text
Relation(
  lhs=Multiple(
    coefficient=?order,
    expression=?element,
  ),
  rhs=Zero(),
  relation_type=ZERO,
)
```

## 21.3 rule boundary

ORDER rule は relation/domain rule layer に置く。

generic engine に ORDER-specific branch を追加しない。

## 21.4 validation

concrete ORDER facts は `order_relation()` で validation する。

pattern-side / match-side では positive integer constraint を
`match_guard` で確認できる。

---

# 22. EHP-derived ZERO と ORDER-derived ZERO の統合

Phase 7-5 以降では同一 run 内に、

```text
EHP branch
```

と、

```text
ORDER branch
```

を置く。

例:

```text
EHP branch                         ORDER branch

Image + Kernel                    ord(α)=n
      ↓                               ↓
  Exactness                         nα=0
      ↓
EHP zero composition
      ↓
Composition(H,E)=0
```

両方とも generic `RelationType.ZERO` に到達するため、
その後の equality reasoning は共通化できる。

domain theorem の由来は ProofStep provenance で区別する。

---

# 23. provenance 設計

同じ knowledge state に複数 domain branch が存在しても、
ProofStep の dependency は明示的に保持する。

EHP branch:

```text
Image / Kernel
↓
Exactness
↓
EHPZeroCompositionStatement
↓
ZERO
```

ORDER branch:

```text
ORDER
↓
ZERO
```

derived ZERO が同じ `RelationType.ZERO` であっても、
source `InferenceRule` と premises によって理由を識別する。

現時点では追加の branch ID は導入しない。

---

# 24. Phase 7 representative fixed point

Phase 7 completion scenario の representative rule set:

```text
EHP exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
ORDER → ZERO
equality symmetry
equality transitivity
generic ZERO propagation
```

代表 initial facts は、

```text
EHP Image / Kernel facts
EHP equality chain
ORDER fact
ORDER equality chain
```

を含む。

最終的に、

```text
EHP target = 0
ORDER target = 0
```

の双方を同じ fixed-point run で導出する。

final state に追加 round を適用して、

```text
new_steps == ()
```

を確認する。

---

# 25. Phase 7 completion criteria

Phase 7 は次を満たしたため完了とする。

1. exact finite ORDER fact を structured Relation で表現できる。
2. concrete order constructor が positive integer validation を行う。
3. `ord(α)=n → nα=0` を `InferenceRule` として実装できる。
4. nested `Multiple` conclusion を既存 substitution で生成できる。
5. ORDER-derived ZERO が generic equality reasoning に接続できる。
6. equality closure を経て別 expression へ ZERO を伝播できる。
7. EHP-derived ZERO と ORDER-derived ZERO を同じ run で扱える。
8. 両 branch が同じ `RelationType.ZERO` representation を共有できる。
9. branch ごとの ProofStep provenance を保持できる。
10. EHP branch と ORDER branch の dependency が混線しない。
11. representative Phase 7 rule set が genuine fixed point に到達する。
12. generic engine に ORDER-specific branch を追加していない。
13. generic engine に speculative refactoring を加えていない。
14. full regression suite が通る。

---

# 26. Phase 7 で実装しないもの

Phase 7 の責務を越えるため、以下は実装しない。

- element order の自動計算
- group structure から generator order を自動推論
- `ord(α) | n` のような divisibility relation
- infinite-order representation
- `Multiple` の算術簡約
- nested multiple normalization
- scalar arithmetic theorem rules
- expression canonicalization
- theorem-aware equality
- proof DAG traversal API
- branch identifier
- all alternative proof collection
- suspension theorem family
- Hopf-invariant theorem family
- stable-range theorem family
- Toda relation family
- Toda bracket
- Steenrod operations
- double EHP
- odd-primary-specific theorem family

これらは将来 Phase で actual mathematical requirement が生じたときに扱う。

---

# 27. Current limitations

## 27.1 conclusion equality

duplicate detection は ordinary Python equality。

数学的 canonical form / theorem-aware equivalence は未導入。

## 27.2 alternative proofs

same conclusion に対する複数 derivation candidate は execution trace に
残り得るが、knowledge state は first accepted ProofStep を保持する。

## 27.3 pattern language

Relation と dataclass statement の structured matching は可能。

ただし arbitrary expression AST 全体を対象にした fully recursive
unification language ではない。

## 27.4 substitution

dataclass field substitution は recursive だが、
unbound variable は `None` になる。

## 27.5 performance

exhaustive assignment は組合せ的に増加し得る。

未導入:

- indexing
- pruning
- memoization
- semi-naive evaluation
- agenda / worklist optimization
- rule priority

## 27.6 termination

`max_rounds` は safety bound。

arbitrary symbolic rule family の semantic termination proof は行わない。

---

# 28. Testing principle

domain rule を追加するときは、

1. single-rule semantic test
2. invalid / mismatched premise test
3. fixed-point integration
4. provenance / premises confirmation
5. representative scenario
6. full regression

の順で確認する。

Phase 7-7 完了時 full suite:

```text
706 passed
```

EHP / relation-rule combined suite:

```text
37 passed
```

---

# 29. Future domain-rule candidates

Phase 7 後の候補:

- broader suspension relations
- Hopf invariant relations
- stable-range theorems
- Toda composition relations
- literature-backed theorem rules
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families

今後も、

```text
new mathematical knowledge
=
new domain InferenceRule
```

を基本とする。

generic engine を変更するのは、

```text
actual mathematical rule が
current generic rule language では
正しく表現できない
```

と確認できた場合のみ。

---

# 30. Documentation policy

文書の役割:

```text
README.md
=
現在できること / current status

docs/design.md
=
現在採用している architecture / semantics / boundaries

docs/development_log.md
=
chronological implementation history
```

過去の development log にある
「未実装」「次の課題」は historical statement として読む。

current status は README / design の最新版を正とする。
