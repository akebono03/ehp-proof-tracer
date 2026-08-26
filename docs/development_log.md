# ehp_proof 開発記録

この文書は Phase 7-8、すなわち Phase 7 完了時点までの開発履歴を、
現在の実装と矛盾しない形に整理した改訂版である。

重要な読み方:

```text
各 Phase の「制限」「次の課題」
=
その Phase 時点の歴史的記録
```

であり、現在の制限とは限らない。

現在仕様は README.md と design.md を優先する。

---

# Phase 1：有限群計算の安定化

## 完了内容

- `GroupElement`
- `GroupMap.apply()`
- `GroupMap.kernel()`
- `GroupMap.image()`
- EHP 完全列の exactness 判定
- finite EHP examples の確認

### 状態

完了

---

# Phase 2：部分群を構造として扱う

## 主な実装

- `Subgroup`
- `GroupMap.kernel_subgroup()`
- `GroupMap.image_subgroup()`
- subgroup generator calculation
- subgroup equality
- abstract finite subgroup structure

完全性:

```text
Im(f) = Ker(g)
```

を単なる位数比較ではなく、
中間群の部分群として比較できるようにした。

### 状態

完了

---

# Phase 3：完全列から群構造を推論する

## 主な成果

### QuotientGroup

有限群について quotient coset と quotient structure を導入。

### InducedMap

第一同型定理:

```text
G / Ker(f) ≅ Im(f)
```

を explicit finite-group object として検証可能にした。

### ExactSequenceStep

```text
A --f--> B --g--> C
```

について、

```text
Im(f)
Ker(g)
B / Im(f)
Im(g)
```

をまとめて扱う。

### EHP integration

EHP segment から general exact-sequence calculation へ接続。

### Extension candidates

有限 short exact sequence:

```text
0 → A → B → C → 0
```

から finite abelian middle-group candidates を列挙・検証。

EHP exactness から candidate middle-group structures を取得できるようにした。

### 到達点

```text
EHP data
↓
kernel / image
↓
exact sequence
↓
quotient
↓
extension
↓
possible middle-group structures
```

### 状態

完了

---

# Phase 4：presentation-based finitely generated abelian groups

Phase 4 では finite-only calculation から、

```text
Z^r ⊕ finite torsion
```

へ一般化した。

## 主な成果

- presentation representation
- integer lattice
- HNF / SNF
- general kernel structure
- general image structure
- general cokernel structure
- free / torsion / mixed maps
- non-diagonal maps
- zero group / zero map handling
- presentation-based exactness
- quotient / image structure comparison
- EHP layer integration
- finite-enumeration cross-check

## 設計境界

Phase 4 の終了時点で、

```text
proof / inference
↓
homotopy / EHP data
↓
abelian-group algebra
↓
integer linear algebra
```

という層構造を明確化した。

### 状態

完了

---

# Phase 5：Proof / Generic Inference Engine

Phase 5 は、

```text
なぜその conclusion が得られたか
```

を追跡・自動推論する generic engine を構築する Phase とした。

Phase 5-65 を generic inference engine foundation の完成点とする。

## Phase 5 前半：Proof / Relation / Expression foundation

導入・整理した主な model:

```text
Relation
ProofStep
Proof
LiteratureReference
Expression
Zero
HomotopyElement
Multiple
Composition
RelationRepository
formatter
```

relation と proof provenance、
expression structure と表示、
group calculation と theorem reasoning を分離した。

## InferenceRule / PremisePattern 基盤

段階的に、

- structured `InferenceRule`
- `PremisePattern`
- premise matching
- multiple premise patterns
- rule applicability
- applicable-rule search
- `InferenceMatch`
- match application
- derived `ProofStep`
- multiple matches application

を導入した。

基本 pipeline:

```text
available ProofSteps
+
InferenceRules
↓
premise matching
↓
InferenceMatch
↓
application
↓
candidate ProofStep
```

## one-round / fixed-point execution

以下を段階的に導入した。

- one-round state expansion
- duplicate-aware merge
- genuinely new delta
- automatic fixed-point iteration
- per-round history
- structured `InferenceRunResult`
- `max_rounds`
- `FIXED_POINT` / `MAX_ROUNDS`
- `InferenceRoundResult`
- per-round matches
- candidate / duplicate tracing
- application result
- acceptance status
- rejection reason

## exhaustive assignment

greedy first assignment から、
deterministic backtracking による exhaustive assignment search へ変更。

```text
find_all_matching_premises()
find_inference_matches_for_rule()
```

を canonical all-match APIs とした。

## PatternVariable / VariableBinding

導入:

```text
PatternVariable
VariableBinding
match_pattern_value()
match_relation_pattern()
merge_variable_bindings()
```

repeated variable consistency と
shared binding consistency を実装。

## multi-premise shared bindings

複数 premise をまたぐ shared variable の値を統合し、
conflict branch を reject しながら backtrack 可能にした。

## InferenceMatch.bindings

matching phase の bindings を application phase へ明示的に引き渡すようにした。

## conclusion substitution

導入:

```text
lookup_variable_binding()
substitute_pattern_value()
substitute_relation_pattern()
substitute_statement_pattern()
substitute_inference_conclusion()
```

`conclusion_pattern` から structured conclusion を生成可能にした。

dataclass fields への substitution を可能にした。

## multiple binding assignments / branch and merge

一つの rule が複数 binding assignment を持ち、
複数 conclusion を生成できることを end-to-end で確認。

さらに、

```text
branch
↓
several intermediate conclusions
↓
later rule
↓
merge
```

まで fixed-point inference で処理可能にした。

## Phase 5 completion boundary

Phase 5-65 では、

```text
multiple premises
all assignments
pattern variables
bindings
shared-binding consistency
structured conclusion substitution
multiple conclusions
multiple rules
multi-round propagation
branching
merging
fixed-point execution
execution tracing
```

を generic engine として統合した。

generic engine はここで基盤完成とし、
以後の engine 拡張は actual domain rule の必要性からのみ行う方針とした。

### 状態

完了

---

# Phase 6：EHP domain inference rules

Phase 6 では、

```text
generic engine を作る
```

から、

```text
実際の EHP mathematics を rule として投入する
```

へ移行した。

## Phase 6-1：Image + Kernel → Exactness

最初の EHP-specific rule:

```text
Image(first_map)
+
Kernel(second_map)
↓
Exactness(first_map, second_map)
```

を実装。

## Phase 6-2 / 6-3：structured statement support

dataclass-based statement pattern matching、
statement conclusion substitution、
`match_guard` を整備。

EHP-specific validity check を generic engine の branch として書かず、
rule の guard として表現できるようにした。

## Phase 6-4 / 6-5：Exactness と Image / Kernel propagation

```text
Exactness
+
Image
↓
Kernel
```

および、

```text
Exactness
+
Kernel
↓
Image
```

を実装。

## Phase 6-6：fixed-point integration

Phase 6-1 / 6-4 / 6-5 を同時に実行し、
相互伝播が fixed point に到達することを確認。

## Phase 6-7：Exactness → EHP zero composition

```text
Exactness(first_map, second_map)
↓
EHPZeroCompositionStatement(first_map, second_map)
```

を実装。

## Phase 6-8：multi-round integration

Image + Kernel から Exactness、
さらに zero composition まで multi-round に進むことを確認。

## Phase 6-9：EHP zero composition → generic ZERO

EHP-specific statement を、

```text
Relation(
  lhs=Composition(second_map, first_map),
  rhs=Zero(),
  relation_type=ZERO,
)
```

へ bridge。

## Phase 6-11 / 6-13：composition ZERO propagation

composition-specific ZERO fact を equality の両 orientation で伝播する
relation rules を導入。

known-zero expression は `Composition` に限定した。

## Phase 6-14：equality symmetry

```text
x = y
↓
y = x
```

を generic rule として導入。

## Phase 6-16：equality transitivity

```text
x = y
y = z
↓
x = z
```

を generic rule として導入。

## Phase 6-18：equality closure

symmetry + transitivity を fixed point まで実行し、
connected equality component の closure を構築可能にした。

## Phase 6-19：equality closure → ZERO propagation

direct equality ではなく、
複数 round で生成された equality を ZERO propagation が利用できることを
確認。

## Phase 6-20：EHP → equality closure → ZERO

```text
EHP facts
↓
generic ZERO
+
external equality chain
↓
target = 0
```

まで end-to-end に接続。

## Phase 6-21：Phase 6 representative completion

代表 rule set:

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
ZERO propagation
equality symmetry
equality transitivity
```

を同時に実行。

final target ZERO を導出し、
追加 round の:

```text
new_steps == ()
```

まで確認して genuine fixed point を成立させた。

## Phase 6 到達点

```text
EHP data / structural facts
↓
EHP-specific inference
↓
generic Relation
↓
equality closure
↓
ZERO propagation
↓
traceable derived relation
↓
fixed point
```

generic engine に EHP-specific branch は追加しなかった。

### 状態

完了

---

# Phase 7：Element-order relations

Phase 7 では Phase 6 の次の actual mathematical rule family として
element order を選択した。

基本目標:

```text
ord(α)=n
↓
nα=0
↓
generic equality reasoning
```

を Phase 5 / Phase 6 の既存 inference infrastructure へ載せる。

---

# Phase 7-1：ORDER semantics

`RelationType.ORDER` を concrete exact-order fact として明確化した。

representation:

```text
Relation(
  lhs=α,
  rhs=n,
  relation_type=RelationType.ORDER,
)
```

semantics:

```text
ord(α) = n
```

`n` は exact positive finite additive order とする。

## order_relation()

concrete fact constructor:

```text
order_relation(element, order, source=None, note=None)
```

を導入。

validation:

- positive integer のみ許可
- `bool` は reject
- zero / negative は reject
- float / string は reject

`Relation.__post_init__` へ ORDER-specific validation は入れなかった。

理由:

```text
inference pattern の Relation
```

では rhs に `PatternVariable` を置く必要があるため。

## テスト

- exact order representation
- source / note preservation
- nonpositive rejection
- noninteger rejection

を確認。

当時 full suite:

```text
698 passed
```

### 状態

完了

---

# Phase 7-2：ord(α)=n → nα=0

新 rule:

```text
order_implies_zero_multiple_inference_rule()
```

を relation rule layer に追加。

premise:

```text
ord(α)=n
```

conclusion:

```text
Multiple(n, α)=0
```

具体的には:

```text
Relation(
  lhs=Multiple(
    coefficient=n,
    expression=α,
  ),
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

## 実装上の確認

既存 `substitute_pattern_value()` が dataclass fields を recursive に
substitution できるため、
nested `Multiple` conclusion 専用 engine feature は不要だった。

ORDER-specific theorem を generic engine に追加せず、
`InferenceRule` と `conclusion_pattern` だけで表現できた。

invalid bound order は rule guard で reject。

## テスト

- ORDER → ZERO
- non-ORDER relation rejection
- invalid order rejection

を確認。

full suite:

```text
701 passed
```

### 状態

完了

---

# Phase 7-3：order-derived ZERO → equality propagation

Phase 6 の ZERO propagation rules は
known-zero expression を `Composition` に限定していた。

そのため、

```text
Multiple(n, α)=0
```

を generic relation reasoning へ流すために、
expression type に依存しない rule を追加した。

新 rule:

```text
zero_equality_implies_zero_inference_rule()
```

semantics:

```text
x = 0
y = x
↓
y = 0
```

## integration test

```text
ord(η3)=2
↓
2η3=0

ν4=2η3
↓
ν4=0
```

を same fixed-point run で確認。

Phase 6 composition-specific rules は削除せず維持。

full suite:

```text
702 passed
```

### 状態

完了

---

# Phase 7-4：order-derived ZERO → equality closure → ZERO

direct equality ではなく、
symmetry / transitivity で生成された equality を経由して
ORDER-derived ZERO が伝播することを確認。

代表 input:

```text
ord(α)=2
2α=middle
target=middle
```

derivation:

```text
ord(α)=2
↓
2α=0

2α=middle
target=middle
↓ equality closure
target=2α

2α=0
target=2α
↓
target=0
```

round count 自体は completion criterion としなかった。

理由は equality closure の productive rounds が rule ordering や
生成される closure facts に依存し得るため。

重要 criterion は final relation と fixed point の成立。

full suite:

```text
703 passed
```

### 状態

完了

---

# Phase 7-5：EHP-derived ZERO と ORDER-derived ZERO の共存

Phase 6 EHP branch と Phase 7 ORDER branch を
同じ fixed-point run に投入。

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

両 ZERO relation が同じ final knowledge state に存在することを確認。

さらにそれぞれが別 source `InferenceRule` を provenance として保持。

## import regression

Phase 7-5 実装時、
`tests/test_ehp_rules.py` の `relation_rules` import を置換した際に、
Phase 6 既存テストで必要な:

```text
equality_symmetry_inference_rule
```

などが一時的に import から落ちた。

このため既存 Phase 6 テスト2件が `NameError` となった。

production logic の failure ではなかった。

既存 imports を復元し、
Phase 7-5 用 import だけを追加する形へ修正。

修正後:

```text
2 passed
35 passed
704 passed
```

を確認。

### 状態

完了

---

# Phase 7-6：EHP / ORDER provenance chain

Phase 7-5 では2 branch の conclusion 共存を確認した。

Phase 7-6 では dependency chain 自体を end-to-end に検証。

EHP branch:

```text
image_step
      \
       exactness_step
      /
kernel_step
       ↓
zero_composition_step
       ↓
ehp_zero_step
```

確認内容:

- Exactness step の premises = Image / Kernel
- Exactness source rule が正しい
- zero-composition step の premise = Exactness
- EHP ZERO step の premise = zero-composition
- 各 step が `ProofRule.INFERENCE`
- 各 step が正しい `inference_rule` を保持

ORDER branch:

```text
order_step
↓
order_zero_step
```

確認内容:

- ORDER ZERO premise = original ORDER step
- source rule = ORDER → ZERO rule

さらに branch cross-contamination がないことを確認。

same knowledge state を共有しても proof provenance は独立して保持される。

full suite:

```text
705 passed
```

### 状態

完了

---

# Phase 7-7：representative Phase 7 fixed-point scenario

Phase 7 の最終 integration test として、
主要 rule family を同じ run に投入。

代表 rule set:

```text
EHP exactness inference
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
ORDER → ZERO
equality symmetry
equality transitivity
generic ZERO propagation
```

## EHP branch

```text
Image + Kernel
↓
Exactness
↓
EHP zero composition
↓
Composition(H,E)=0
```

さらに EHP equality chain から closure を作り、

```text
EHP target = Composition(H,E)
```

を導出。

generic ZERO propagation により:

```text
EHP target = 0
```

へ到達。

## ORDER branch

```text
ord(η3)=2
↓
2η3=0
```

ORDER equality chain から closure を作り、

```text
ORDER target = 2η3
```

を導出。

generic ZERO propagation により:

```text
ORDER target = 0
```

へ到達。

## genuine fixed point

completion criterion は final ZERO conclusion だけではなく、
final state に追加 round を適用して:

```text
new_steps == ()
```

となること。

これにより representative Phase 7 rule set 全体が
genuine fixed point に到達することを確認。

## テスト結果

Phase 7 representative focused test:

```text
1 passed
```

Phase 7 後半 integration tests:

```text
3 passed
```

EHP / relation rule combined suite:

```text
37 passed
```

full project suite:

```text
706 passed in 60.22s
```

failure なし。

### 状態

完了

---

# Phase 7-8：成果・設計境界・現状整理

Phase 7-8 では新しい production feature を追加しない。

README / design / development_log を Phase 7 完了状態へ更新し、
Phase 7 を正式終了する。

## Phase 7 の成果

1. `ORDER` relation の exact finite additive order semantics を確立した。
2. validated concrete constructor `order_relation()` を導入した。
3. `ord(α)=n → nα=0` を domain `InferenceRule` として実装した。
4. nested `Multiple` conclusion が既存 recursive dataclass substitution で
   生成できることを確認した。
5. expression type 非依存の generic ZERO propagation を追加した。
6. ORDER-derived ZERO を direct equality で伝播できた。
7. ORDER-derived ZERO を equality closure 経由で伝播できた。
8. EHP-derived ZERO と ORDER-derived ZERO を同一 run に共存させた。
9. 両 branch の ProofStep provenance / dependency chain を保持した。
10. representative EHP + ORDER + equality rule set を genuine fixed point
    まで実行した。
11. Phase 7 のための generic engine 改造は不要だった。
12. full regression suite 706 tests が pass した。

## Phase 7 の設計境界

Phase 7 は次を実装していない。

```text
automatic order computation
order divisibility relation
infinite order
expression arithmetic normalization
theorem-aware equality
proof DAG traversal API
branch identifiers
all alternative proof collection
suspension theorem family
Hopf invariant theorem family
stable-range theorem family
Toda relations
Toda brackets
Steenrod operations
double EHP
odd-primary-specific theorem families
```

これらを Phase 7 の scope に先取りしない。

## Phase 7 completion summary

```text
Phase 5
generic inference engine foundation
        ↓
Phase 6
EHP-derived generic ZERO
        ↓
Phase 7
ORDER-derived generic ZERO
        ↓
shared equality closure / ZERO propagation
        ↓
multiple domain branches
        ↓
traceable provenance
        ↓
genuine fixed point
```

Phase 7 によって、

```text
異なる数学的 theorem family が
同じ generic Relation を生成し、
同じ fixed-point reasoning infrastructure を共有する
```

という architecture が実証された。

### 状態

完了

---

# Phase 7 完了後の境界

次 Phase も speculative generic-engine refactoring から開始しない。

actual mathematical rule family を選び、

```text
known facts
+
new theorem rule
↓
existing generic engine
```

でまず表現を試す。

current candidate directions:

- suspension relations
- Hopf invariant relations
- stable-range theorems
- Toda composition relations
- literature-backed theorem rules
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem families

generic engine を変更するのは、

```text
actual rule が current rule language では
正しく表現できない
```

と実証された場合のみ。

---

# Current verified status

Phase 7-7 / Phase 7-8 boundary:

```text
python -m pytest -v
```

結果:

```text
706 passed in 60.22s
```

EHP / relation rules:

```text
python -m pytest tests/test_ehp_rules.py tests/test_relation_rules.py -v
```

結果:

```text
37 passed
```

---

# 文書運用方針

```text
README.md
=
current capabilities / current status

docs/design.md
=
current design decisions / semantics / boundaries

docs/development_log.md
=
chronological implementation history
```

development_log の historical limitation を
current limitation として再掲しない。

今後の各 Phase では、

1. mathematical rule の意味
2. rule representation
3. tests
4. generic engine 変更の有無
5. current limitation への影響
6. next Phase との境界

を記録する。
