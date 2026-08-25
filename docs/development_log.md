# ehp_proof 開発記録

この文書は Phase 5-65 時点までの開発履歴を、
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
