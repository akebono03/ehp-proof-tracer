# ehp_proof 開発記録

この文書は Phase 6-21、すなわち Phase 6 完了時点までの開発履歴を、
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

## 3-1 QuotientGroup

有限群について quotient coset と quotient structure を導入。

## 3-2 InducedMap

第一同型定理:

```text
G / Ker(f) ≅ Im(f)
```

を explicit finite-group object として検証可能にした。

## 3-3 ExactSequenceStep

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

## 3-4 EHP integration

EHP segment から general exact-sequence calculation へ接続。

## 3-5〜3-7 Extension candidates

有限 short exact sequence:

```text
0 → A → B → C → 0
```

から finite abelian middle-group candidates を列挙・検証。

EHP exactness から candidate middle-group structures を
取得できるようにした。

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

## 実 EHP data

自由部分を含む EHP example を用い、
presentation path を実 EHP calculation に接続した。

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

---

# Phase 5-1〜5-10：Proof / Relation / Expression foundation

## Phase 5-1

`Relation` / `ProofStep` / `Proof` を導入。

```text
Relation
=
known mathematical fact

ProofStep
=
one calculation / inference

Proof
=
derivation collection
```

という区別を設定。

## Phase 5-2

Expression model:

```text
Zero
HomotopyElement
Multiple
Composition
```

を導入。

## Phase 5-3 以降

Relation repository、Relation → ProofStep、
kernel/image/cokernel ProofStep、
exactness ProofStep、
EHP exactness Proof、
formatter などを段階的に接続。

## Phase 5-10 到達点

```text
Expression
↓
Relation
↓
Repository
↓
ProofStep
↓
Proof
↓
formatter
```

および、

```text
GroupMap
↓
kernel / image calculation
↓
ProofStep
↓
exactness ProofStep
↓
Proof
```

を同じ proof model で表現可能になった。

---

# Phase 5-11〜5-23：InferenceRule 基礎

この区間では、

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

などを段階的に構築した。

到達した基本 pipeline:

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

---

# Phase 5-24：candidate derivation

high-level candidate derivation API を整備。

```text
InferenceRules
+
available steps
↓
matches
↓
candidate derived ProofSteps
```

を1 API で取得可能にした。

---

# Phase 5-25：one-round state expansion

candidate derived steps を current state に追加する
one-round inference を導入。

---

# Phase 5-26：duplicate-aware merge

equal conclusion を knowledge state に重複追加しない
merge semantics を導入。

---

# Phase 5-27：genuinely new delta

1 round で本当に新規追加される `ProofStep` のみを取得する
API を導入。

---

# Phase 5-28：automatic fixed-point iteration

新しい step がなくなるまで round を自動反復する
fixed-point inference を導入。

derived step を later round の premise として利用可能になった。

---

# Phase 5-29：per-round history / structured run result

`InferenceRunResult` を導入。

```text
final state
round history
productive round count
```

を構造化。

---

# Phase 5-30：max_rounds / termination reason

`max_rounds` と、

```text
FIXED_POINT
MAX_ROUNDS
```

を導入。

round limit termination と fixed-point termination を区別。

---

# Phase 5-31：structured per-round result

`InferenceRoundResult` を導入。

run-level と round-level information を分離。

---

# Phase 5-32：per-round InferenceMatch tracing

各 productive round について、
どの `InferenceMatch` が存在したかを保存。

---

# Phase 5-33：candidate / duplicate-rejection tracing

round result に、

```text
candidate_steps
duplicate_rejected_steps
```

を追加。

```text
match
↓
candidate
↓
accepted / duplicate
```

を観測可能にした。

---

# Phase 5-34：InferenceApplicationResult

match と candidate の対応を、

```text
InferenceApplicationResult
```

という object-level relationship にした。

---

# Phase 5-35：acceptance status / rejection reason

`InferenceApplicationResult` に、

```text
accepted
rejection_reason
```

を追加。

rejection reason:

```text
ALREADY_KNOWN
SAME_ROUND_DUPLICATE
```

を区別可能にした。

---

# Phase 5-36：all valid premise assignments

greedy first assignment から、
deterministic backtracking による exhaustive assignment search へ変更。

導入:

```text
find_all_matching_premises()
find_inference_matches_for_rule()
```

`find_matching_premises()` / `find_inference_match()` は
first-result compatibility API として維持。

この時点では、assignment enumeration はまだ主に
outer pattern condition に基づいていた。

---

# Phase 5-37：PatternVariable

`PatternVariable` を導入。

pattern の可変部分を文字列 placeholder ではなく
structured object として表現可能にした。

---

# Phase 5-38：VariableBinding

`VariableBinding` を導入。

```text
PatternVariable
→
actual value
```

を explicit object として保持。

---

# Phase 5-39：pattern value matching

`match_pattern_value()` を導入。

- variable pattern → binding
- equal literal → success / no binding
- different literal → failure

という最小 pattern matching semantics を確立。

---

# Phase 5-40：relation pattern matching

`match_relation_pattern()` により、
`Relation` の lhs / rhs / relation type を
structured に match できるようにした。

---

# Phase 5-41：binding merge / repeated-variable consistency

`merge_variable_bindings()` を導入。

同じ variable の、

```text
same value
```

は統合、

```text
different value
```

は conflict として reject。

1 relation pattern 内で同じ variable が複数回現れる場合も
consistency を確認可能になった。

---

# Phase 5-42：match_relation_pattern() への binding consistency 統合

relation pattern matching 自体が、
lhs / rhs から生成された bindings を統合し、
repeated variable conflict を reject するようになった。

---

# Phase 5-43：PremisePattern に relation_pattern

`PremisePattern.relation_pattern` を追加。

outer condition:

```text
proof_rule
statement_type
relation_type
```

に加えて、
conclusion の内容を structured `Relation` pattern で指定可能にした。

---

# Phase 5-44：premise matching から binding を返す API

`match_premise_pattern()` を導入・整理し、
boolean ではなく binding tuple を返せるようにした。

`matches_premise_pattern()` は compatibility boolean view とした。

---

# Phase 5-45：複数 premise binding 統合 API

`match_inference_rule_bindings()` により、
明示的に与えた複数 steps について
premise-level bindings を統合。

shared variable conflict を rule-level mismatch として reject。

---

# Phase 5-46：find_all_matching_premises() shared binding consistency

backtracking premise search の途中で、
shared bindings を逐次 merge するようにした。

binding conflict branch は prune し、
別 candidate へ backtrack。

これにより exhaustive search が、

```text
type-compatible combinations
```

から、

```text
binding-consistent combinations
```

へ進んだ。

---

# Phase 5-47：InferenceMatch.bindings

`InferenceMatch` に bindings を保持。

matching phase で得た variable assignment を
application phase へ明示的に引き渡せるようにした。

---

# Phase 5-48：binding lookup

`lookup_variable_binding()` を導入。

variable から actual bound value を取得可能にした。

---

# Phase 5-49：pattern value substitution

`substitute_pattern_value()` を導入。

variable pattern を bound value へ置換。

literal はそのまま保持。

---

# Phase 5-50：Relation pattern substitution

`substitute_relation_pattern()` を導入。

Relation lhs / rhs へ bindings を適用し、
relation metadata を保持。

---

# Phase 5-51：InferenceMatch.bindings から conclusion_pattern を具体化

`substitute_inference_conclusion()` により、
rule の `conclusion_pattern` を match bindings で具体化。

---

# Phase 5-52：apply_inference_match() conclusion_pattern 対応

`apply_inference_match()` が、

```text
conclusion_builder
```

だけでなく、

```text
conclusion_pattern
```

からも candidate conclusion を生成可能になった。

現実装では builder がある場合 builder を優先。

---

# Phase 5-53：conclusion_pattern fixed-point integration

`conclusion_pattern` のみを使う rule を、

- derive
- round
- fixed-point
- history

まで end-to-end で通した。

multi-round conclusion-pattern propagation と
dependency chain preservation も確認。

---

# Phase 5-54：multiple premises + shared bindings + conclusion_pattern

複数 premise の shared bindings を使って
structured conclusion を導く end-to-end integration を確認。

conflicting assignment rejection と、
backtracking による consistent match 発見も確認。

---

# Phase 5-55：single rule / multiple binding assignments

1つの rule が複数 valid bindings を持ち、
それぞれから distinct conclusion を生成できることを確認。

---

# Phase 5-56：multiple premises / multiple shared-binding assignments

複数 premise rule で複数の shared-binding assignment を列挙し、
それぞれ distinct conclusion を生成できることを確認。

---

# Phase 5-57：multiple variables / multiple assignments

1 rule 内の複数 variables が
複数 assignments を通じて正しく独立に binding され、
distinct conclusions を生成することを確認。

---

# Phase 5-58：partially shared variables

複数 premise の一部 variable だけを共有する rule を end-to-end 確認。

shared variable consistency と、
premise-specific variables の独立性を同時に扱えるようになった。

---

# Phase 5-59：shared variable across three premises

1つの shared variable が3 premise にまたがる場合も、
全 premise で consistency が維持されることを確認。

---

# Phase 5-60：multiple shared variables across three premises

複数の shared variables を3 premise 間で伝播させる
より一般的な consistency graph を確認。

---

# Phase 5-61：shared binding graph branch / merge

binding graph が途中で branch し、
後で merge する形の end-to-end inference を確認。

単純 linear chain ではなく、
graph-shaped binding dependency を扱えることを示した。

---

# Phase 5-62：branching / merging graph with multiple final bindings

branch / merge graph から複数 distinct final bindings / conclusions が
生成される場合を確認。

---

# Phase 5-63：multiple rules chained through derived conclusions

rule A が生成した derived conclusion を、
later round で rule B が premise として利用する
multi-rule fixed-point chain を end-to-end 確認。

---

# Phase 5-64：multiple rules propagate multiple binding branches

前段 rule が複数 binding assignments から
複数 intermediate conclusions を生成し、
それぞれが後段 rule に伝播する
multi-branch fixed-point inference を確認。

---

# Phase 5-65：multiple branches merge into a multi-premise rule

Phase 5 の最終 integration test。

複数の前段 branch から生成された intermediate conclusions を、
後段 rule が複数 premises として再び合流させることを確認。

概念的には:

```text
initial branch A
↓
middle A
            \
             merge rule
            /
middle B
↑
initial branch B
```

fixed-point execution の中で、

```text
branch
propagate
merge
derive
terminate
```

が成立することを確認した。

この Phase を、

```text
generic inference engine の基盤完成点
```

とする。

---

# Phase 5-65 時点の current inference pipeline

```text
initial ProofSteps
+
InferenceRules
↓
all premise assignments
↓
relation-pattern matching
↓
PatternVariable bindings
↓
shared binding consistency
↓
InferenceMatch(
  rule,
  premises,
  bindings,
)
↓
conclusion builder / conclusion-pattern substitution
↓
candidate ProofStep
↓
InferenceApplicationResult
↓
acceptance classification
├── accepted
├── ALREADY_KNOWN
└── SAME_ROUND_DUPLICATE
↓
new steps
↓
next productive round
↓
branch / propagate / merge
↓
fixed point
```

---

# Phase 5-65 test verification

今回の documentation review で、
アップロードされた最新:

```text
proof.py
test_inference_rule_pattern.py
```

を同じ isolated directory に置いて、
次を実行した。

```powershell
python -m pytest test_inference_rule_pattern.py -q
```

結果:

```text
423 passed
```

これは inference-rule pattern test file の結果であり、
project 全体の full test suite result ではない。

---

# Phase 5 完了時点の重要な current limitations

以下は Phase 5-36 以前の古い「未実装」記述ではなく、
Phase 5-65 時点でも残る current limitations である。

## ordinary conclusion equality

duplicate identity は ordinary Python equality。

未対応:

```text
canonicalization
normalization
mathematical equivalence
```

## alternative proof storage

alternative applications は execution trace に残るが、
knowledge state に equal conclusion の multiple ProofSteps を
first-class に保持しない。

## recursive general unification

Relation pattern は structured matching できるが、
あらゆる expression / statement type を再帰的に統一する
general unification language ではない。

## unbound conclusion variable

未 binding variable を substitution すると現在は `None` になる。

domain rule 側で必要 variables を premise により bind することを
前提とする。

## combinatorial search

all assignments は combinatorial growth を持つ。

indexing / pruning / agenda optimization はまだ導入しない。

## semantic cycle detection

`max_rounds` は safety bound であり semantic cycle detection ではない。

---

# Phase 5 完了

Phase 5 では最終的に、

```text
proof tracking
+
structured rule representation
+
exhaustive matching
+
shared variable bindings
+
structured conclusion generation
+
multi-round fixed-point inference
+
branching / merging
+
execution tracing
```

を generic engine として統合した。

### 状態

完了

---

# Phase 6：EHP domain inference rules

次 Phase は、

```text
Phase 6: EHP domain inference rules
```

とする。

Phase 6 の主目的:

```text
generic engine を作る
```

から、

```text
実際の EHP mathematics を rule として投入する
```

へ移る。

候補 rule families:

- E/H/P relations
- EHP exactness consequences
- suspension relations
- Hopf invariant relations
- element-order relations
- composition relations
- stable-range results
- Toda relations
- literature-backed theorem rules

基本原則:

```text
new mathematical knowledge
=
new InferenceRule
```

とする。

generic engine の変更は、
real EHP rule が current rule language で表現できないと
実証された場合にのみ行う。

---

# Phase 6-1：EHP exactness inference rule

Phase 6-1 では、既存の EHP exactness の知識を
Phase 5 の generic inference engine から実行できるようにした。

## 実装

新規ファイル:

```text
ehp_rules.py
tests/test_ehp_rules.py
```

追加した factory:

```python
ehp_exactness_inference_rule(exact_step)
```

この rule は次の premise を要求する。

```text
ImageStatement(first_map)
KernelStatement(second_map)
```

builder は既存の `ehp_exactness_proof_step()` を再利用し、生成された
`ExactnessStatement` を conclusion とする。

## ProofStep rule の判断

generic engine の `apply_inference_match()` は derived step に常に、

```text
ProofRule.INFERENCE
```

を設定する。

したがって、Phase 6-1 の rule を generic engine で適用した derived step
も `ProofRule.INFERENCE` を使用する。EHP 固有 rule であることは、

```text
ProofStep.inference_rule
```

から確認できる。

なお、`ehp_exactness_proof_step()` を直接呼び出す既存経路では、従来どおり
`ProofRule.EHP_EXACTNESS` を使用する。

## 設計判断

Phase 5 の generic engine の境界を維持するため、

- `proof.py` は変更しない
- `ehp.py` は変更しない
- 新しい `ProofRule` は追加しない
- EHP-specific branch は generic engine に追加しない

という方針にした。

Phase 6-1 では statement type と proof rule による premise matching
だけを使用する。structured statement matching や任意 EHP segment の
自動選択は導入していない。

## テスト

`tests/test_ehp_rules.py` で次を確認した。

- EHP segment から image step を作成
- kernel step を作成
- EHP rule が applicable
- generic inference による exactness conclusion の生成
- 元の image/kernel step の premise 参照
- `inference_rule` の保持
- `ProofRule.INFERENCE` の設定
- 最初の round での導出
- fixed-point 到達
- duplicate の追加拒否

結果:

```text
専用テスト: 1 passed
全 pytest: 648 passed
```

### 状態

完了
# Phase 6-2：structured statement matching

Phase 6-2 では、Phase 6-1 の EHP exactness rule を特定の
`ExactSequenceStep` に factory-bound した形から一般化するため、
statement 内部 fields を pattern matching する最小基盤を追加した。

## 実装

`proof.py` に次を追加・拡張した。

- `PremisePattern.statement_pattern`
- `match_statement_pattern()`
- dataclass fields を使った field-by-field matching

structured matcher は各 field について既存の
`match_pattern_value()` を呼び出し、生成された bindings を
`merge_variable_bindings()` で統合する。これにより、literal matching、
`PatternVariable` binding、同一 statement 内の repeated binding、複数
premise 間の shared binding consistency を同じ generic mechanism で扱う。

## EHP rule integration

`ehp_rules.py` の `ehp_exactness_inference_rule()` は、既存の

```python
ehp_exactness_inference_rule(exact_step)
```

を維持しつつ、argument-free invocation にも対応した。

argument-free rule は次の内部 patterns を使用する。

```text
ImageStatement(group_map=?first_map)
KernelStatement(group_map=?second_map)
```

matching された maps から `ExactSequenceStep` を作り、既存の
`ehp_exactness_proof_step()` を conclusion construction に再利用する。
この変更でも EHP 固有の分岐や新しい `ProofRule` は generic engine に
追加していない。

## 設計境界

Phase 6-2 では次を実装しない。

- arbitrary EHP segment からの exact pair 自動探索
- EHP sequence 全体の自動構築
- 新しい数学的 EHP theorem
- E/H/P の domain/codomain に基づく index arithmetic

## テスト

structured matching について次を追加・確認した。

- ImageStatement の map binding
- KernelStatement の map binding
- concrete field matching と mismatch rejection
- 既存 binding と矛盾しない場合の成功
- 複数 premise 間の shared binding consistency
- Phase 6-1 exactness inference regression

結果:

```text
focused inference and EHP tests: 428 passed
full project test suite: 652 passed
exit code: 0
git diff --check: clean
```

### 状態

完了


# Phase 6-3：statement conclusion と match guard

Phase 6-3 では、Phase 6-2 で導入した structured statement matching を
conclusion construction まで拡張し、premise の構造的一致だけでは表せない
domain condition を guard として扱えるようにした。

## 実装

`proof.py` に次を追加・拡張した。

- `InferenceRule.conclusion_pattern` に dataclass statement を許可
- `substitute_statement_pattern()`
- dataclass fields の substitution
- `InferenceRule.match_guard`
- premise matching 後の guard evaluation

statement conclusion pattern は各 field を既存の
`substitute_pattern_value()` で置換する。これにより
`ExactnessStatement`、`ImageStatement`、`KernelStatement` などを generic
inference rule の conclusion として扱える。

`match_guard(premises, bindings)` は premise patterns の matching と
binding consistency の後に評価される。guard が false を返す assignment
は `InferenceMatch` から除外されるため、generic engine に domain-specific
な条件分岐を追加せずに追加条件を表現できる。

## EHP rule integration

argument-free `ehp_exactness_inference_rule()` は、Image/Kernel の map を
statement patterns から binding し、次の `ExactnessStatement` conclusion
pattern を使用する。

```text
ExactnessStatement(
  first_map=?first_map,
  second_map=?second_map,
  is_exact=True,
)
```

さらに `ehp_maps_are_consecutive()` を guard から呼び出し、first map の
target と second map の source が一致する map pair だけを受理する。
既存の `ehp_exactness_inference_rule(exact_step)` factory form と direct
proof-step API は維持した。

## 設計境界

Phase 6-3 では次を実装しない。

- arbitrary EHP segment からの exact pair 自動探索
- EHP sequence 全体の自動構築
- 新しい数学的 EHP theorem
- 複雑な E/H/P index arithmetic

## テスト

statement conclusion substitution、guard の accept/reject、guard への
binding 受け渡し、Phase 6-2 structured matching、Phase 6-1 exactness
inference regression を確認した。focused inference and EHP tests は
`441 passed`、full project test suite は `665 passed`、pytest exit code は
`0` だった。

### 状態

完了


# Phase 6-4：Exactness + Image → Kernel structure

Phase 6-4 では、EHP exactness と既知の image structure から second map の
kernel structure を導く rule を追加した。

```text
Exactness(first_map, second_map)
+
Image(first_map, structure)
↓
Kernel(second_map, structure)
```

既存の structured statement pattern と shared bindings のみで表現し、
generic engine は変更していない。

### 状態

完了

---

# Phase 6-5：Exactness + Kernel → Image structure

Phase 6-5 では Phase 6-4 の逆方向を追加した。

```text
Exactness(first_map, second_map)
+
Kernel(second_map, structure)
↓
Image(first_map, structure)
```

Phase 6-4 / 6-5 により、exactness と Image / Kernel structure の相互伝播が
可能になった。

### 状態

完了

---

# Phase 6-6：exactness rule family fixed-point integration

Phase 6-1、6-4、6-5 を同一 fixed-point run に投入し、Image + Kernel から
Exactness が導かれた後、相互伝播 rule が既知 conclusion を再生成しても
duplicate rejection により fixed point に到達することを確認した。

### 状態

完了

---

# Phase 6-7：Exactness → EHP zero composition

EHP exactness から consecutive maps の zero composition を表す
`EHPZeroCompositionStatement` を導出する rule を追加した。

```text
Exactness(first_map, second_map)
↓
EHPZeroCompositionStatement(first_map, second_map)
```

non-exact statement は match しない。

### 状態

完了

---

# Phase 6-8：Image + Kernel → Exactness → zero composition integration

Phase 6-1 と Phase 6-7 を fixed-point inference で接続し、

```text
round 1: Exactness
round 2: EHP zero composition
```

という productive-round chain を確認した。

### 状態

完了

---

# Phase 6-9：EHP zero composition → generic ZERO relation

`EHPZeroCompositionStatement` を generic `Relation` へ変換する bridge rule を
追加した。

```text
EHPZeroCompositionStatement(first_map, second_map)
↓
Composition(second_map, first_map) = 0
```

conclusion は `RelationType.ZERO` を使用する。

### 状態

完了

---

# Phase 6-10：EHP exactness → generic ZERO integration

Image / Kernel facts から、

```text
Exactness
↓
EHP zero composition
↓
generic ZERO relation
```

までを multi-round fixed-point inference で確認した。

### 状態

完了

---

# Phase 6-11：ZERO + equality → ZERO propagation

composition の ZERO relation と、別 expression がその composition に等しい
relation から、別 expression の ZERO relation を導く rule を追加した。

```text
composition = 0
x = composition
↓
x = 0
```

zero-side expression が `Composition` であることを guard で確認する。

### 状態

完了

---

# Phase 6-12：EHP → generic ZERO → propagated ZERO integration

EHP exactness chain から得られた generic ZERO relation を equality premise と
接続し、generic expression の ZERO relation まで到達する multi-round test を
追加した。

### 状態

完了

---

# Phase 6-13：reverse equality ZERO propagation

ZERO expression が equality の lhs に現れる orientation も追加した。

```text
composition = 0
composition = x
↓
x = 0
```

これにより ZERO propagation は equality の両 orientation を扱える。

### 状態

完了

---

# Phase 6-14：equality symmetry

generic equality symmetry rule を追加した。

```text
x = y
↓
y = x
```

non-equality relation は reject する。

### 状態

完了

---

# Phase 6-15：equality symmetry fixed-point verification

symmetry rule 単体を fixed-point execution に通し、reverse equality を1回だけ
追加した後、元 equality / reverse equality の再生成が `ALREADY_KNOWN` として
reject されることを確認した。

### 状態

完了

---

# Phase 6-16：equality transitivity

generic equality transitivity rule を追加した。

```text
x = y
+
y = z
↓
x = z
```

shared middle expression は existing binding consistency により一致を要求する。

### 状態

完了

---

# Phase 6-17：multi-round transitivity closure

3-link equality chain に transitivity を反復し、1 round で得られた equality が
次 round の premise となって chain endpoint equality を導くことを確認した。

### 状態

完了

---

# Phase 6-18：equality equivalence closure

symmetry と transitivity を同じ fixed-point run で実行した。

connected equality component について directed pairwise equalities と reflexive
equalities が導かれ、ordinary conclusion equality と duplicate rejection により
fixed point に到達することを確認した。

独立した equality graph subsystem は導入していない。

### 状態

完了

---

# Phase 6-19：equality closure → ZERO propagation

ZERO relation、複数 equality facts、symmetry、transitivity、ZERO propagation を
同一 run に投入し、derived equality を経由して ZERO が複数 round 伝播する
ことを確認した。

### 状態

完了

---

# Phase 6-20：EHP → equality closure → ZERO propagation integration

EHP domain chain と generic equality closure を統合した。

代表 scenario:

```text
Image(E)
+
Kernel(H)
↓
Exactness(E,H)
↓
EHP zero composition
↓
H ∘ E = 0

 target = intermediate
 H ∘ E = intermediate
↓ symmetry / transitivity
 target = H ∘ E
↓ ZERO propagation
 target = 0
```

EHP-specific facts が generic relation layer に入り、generic reasoning によって
新しい ZERO relation を導けることを end-to-end で確認した。

### 状態

完了

---

# Phase 6-21：Phase 6 representative end-to-end completion

Phase 6 の最終 integration として、主要 rule family を1つの fixed-point
scenario にまとめた。

最終 rule set:

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO relation
ZERO + equality → propagated ZERO
ZERO + reverse equality → propagated ZERO
equality symmetry
equality transitivity
```

representative test:

```text
test_phase6_representative_end_to_end_scenario_reaches_fixed_point
```

この test は次を確認する。

1. Image + Kernel から Exactness が得られる。
2. Exactness から EHP zero composition が得られる。
3. EHP-specific statement から generic composition ZERO relation が得られる。
4. symmetry / transitivity により target と composition の equality が得られる。
5. ZERO propagation により target = 0 が得られる。
6. target ZERO step が premise と source `InferenceRule` を保持する。
7. final state への追加 inference round で `new_steps == ()` となる。
8. exactness / image / kernel propagation を含む全 representative rule family が
   terminal state で既知 conclusion の範囲に閉じる。

Phase 6-21 では production inference code を追加していない。
既存 Phase 5 generic engine と Phase 6 domain rules の組み合わせだけで
completion scenario を表現できたためである。

## Phase 6 completion criteria

Phase 6 は次を満たしたため完了とする。

1. Image + Kernel から Exactness を導出できる。
2. Exactness と Image / Kernel structure を相互伝播できる。
3. Exactness から EHP zero composition を導出できる。
4. EHP zero composition を generic ZERO Relation に変換できる。
5. ZERO を equality の両 orientation で伝播できる。
6. equality symmetry を generic rule として実行できる。
7. equality transitivity を generic rule として実行できる。
8. symmetry + transitivity を fixed point まで反復して equality closure を構築できる。
9. equality closure を利用して ZERO を複数 round 伝播できる。
10. EHP facts から generic equality reasoning を経て final ZERO relation まで到達できる。
11. derived `ProofStep` が premises と `inference_rule` を保持する。
12. representative Phase 6 rule set が genuine fixed point に到達する。
13. generic engine に EHP-specific branch を追加していない。

## Phase 6 の到達点

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

これはすべての EHP / unstable homotopy theorem の実装完了を意味しない。
Phase 6 で完成したのは最初の domain-inference vertical slice である。

## テスト結果

Phase 6-21 完了後に full project test suite を実行した。

```powershell
python -m pytest -v
```

結果:

```text
691 passed in 22.77s
```

691 tests を収集し、failure なしで完了した。

### 状態

完了

---

# Phase 6 完了後の境界

次 Phase は generic engine の speculative refactoring から開始しない。

候補は、実際の新しい mathematical rule family である。

```text
element order
suspension relations
Hopf invariant
stable-range theorem
Toda relations
Toda bracket
Steenrod operations
double EHP
odd-primary-specific rules
```

actual rule を current generic language で表現してみて、不足が実証された
場合だけ generic engine を拡張する。

---

# 今後の記録方針

今後は役割を明確に分ける。

```text
README.md
=
current capabilities / current status

docs/design.md
=
current design decisions

docs/development_log.md
=
chronological history
```

development_log の historical limitation を、
current limitation として再掲しない。

Phase 6 以降の各作業では、

1. mathematical rule の意味
2. rule representation
3. tests
4. generic engine 変更の有無
5. current limitation への影響

を記録する。
