# ehp_proof 設計メモ

この文書は Phase 6-3 完了時点の「現在の設計」を正本としてまとめる。

過去の各 Phase で書かれた設計メモには、その当時は正しかった
「未実装」「今後の課題」という記述が多数ある。

本改訂版では、

```text
現在の設計原則
```

と、

```text
歴史的な実装順序
```

を分離する。

現在の仕様判断では、この文書の「現在の設計」を優先する。

---

# 1. 全体アーキテクチャ

基本の依存方向は次とする。

```text
EHP domain inference rules
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

特に、

```text
algebra.py
```

は、

```text
E
H
P
Toda bracket
Hopf invariant
```

などのホモトピー論的意味を知らない。

また generic inference engine も、

```text
EHP-specific theorem
```

そのものを知らない。

---

# 2. integer linear algebra と algebra 層

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

有限群については、全元列挙方式を削除しない。

その役割は、

```text
reference implementation
```

である。

presentation-based calculation と独立に計算し、
cross-check に利用する。

## 2.4 exactness

完全性:

```text
Im(f) = Ker(g)
```

は、中間群内の部分群 / lattice の一致として判定する。

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

などの区別は上位層の責務とする。

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

# 4. Relation / Proof 層

## 4.1 Relation

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

など、単純な expression equality 以外の statement を
将来扱う可能性があるためである。

## 4.2 LiteratureReference

文献 metadata を、

```text
label
author
title
year
locator
```

として構造化する。

数学的 relation の provenance と、
ProofStep の実行上の note は別概念とする。

## 4.3 ProofStep

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

## 4.4 ProofRule

現在の主な category:

```text
GIVEN
RELATION
INFERENCE
EXACTNESS
EHP_EXACTNESS
KERNEL_COMPUTATION
IMAGE_COMPUTATION
COKERNEL_COMPUTATION
```

`ProofRule` と `InferenceRule` は別概念である。

```text
ProofRule
=
ProofStep の大分類

InferenceRule
=
具体的な数学的推論規則
```

## 4.5 Proof

`Proof` は、

```text
conclusion
steps
```

を持つ。

依存関係は `ProofStep.premises` で保持する。

Phase 5-65 時点では、独立した DAG class は必須ではない。

---

# 5. Expression 層

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

を担当しない。

`HomotopyElement` と `GroupElement` は別クラスとする。

---

# 6. RelationRepository / formatter

Relation repository は、

```text
known Relation の保存・検索
```

を担当する。

relation application や inference は担当しない。

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
どの rule が valid か
```

を知ることではなく、

```text
与えられた rule を
どのように match / bind / apply / iterate するか
```

を担当することである。

したがって engine に、

```python
if rule_is_ehp:
  ...
```

のような domain-specific branch を入れない。

---

# 8. InferenceRule

現在の構造:

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

主に互換性・柔軟な conclusion construction のために残す。

## 8.2 conclusion_pattern

structured `Relation` または dataclass statement pattern に bindings を
代入して conclusion を生成できる。

statement pattern の field substitution は
`substitute_statement_pattern()` を通じて行う。

## 8.3 builder と pattern の両立

両方が指定された場合、現実装では builder が優先される。

この precedence は current API semantics として明示する。

## 8.4 match_guard

`match_guard` は optional callable であり、次の引数を受け取る。

```text
matched premises
bindings
```

premise pattern の構造的一致と binding merge が成功した後に評価され、
false を返す assignment は `InferenceMatch` として採用しない。
domain-specific な追加条件を generic engine の分岐なしに表現するために
使用する。

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

外側 category matching と、
内部 `Relation` pattern matching を併用できる。

`statement_pattern` は dataclass-based statement の内部 fields を
structured に match するための domain-independent pattern である。
各 field は literal または `PatternVariable` にできる。

empty pattern は任意の step に match する。

---

# 10. PatternVariable / VariableBinding

## 10.1 PatternVariable

pattern 内の変数を表す。

構造的 equality は `name` による。

空文字列や非文字列の name は許可しない。

## 10.2 VariableBinding

```text
PatternVariable
→
value
```

を明示的 object として保持する。

value は任意型を許す。

---

# 11. Pattern matching

## 11.1 match_pattern_value()

pattern が `PatternVariable` なら binding を生成する。

literal なら ordinary equality を要求する。

## 11.2 match_relation_pattern()

`Relation` の、

```text
lhs
rhs
relation_type
```

を構造的に match する。

同じ variable が lhs / rhs などに繰り返し現れる場合は、
binding consistency を要求する。

## 11.3 match_statement_pattern()

`match_statement_pattern()` は dataclass instance の fields を順番に
比較する。

```text
statement pattern
        ↓
dataclass fields
        ↓
match_pattern_value()
        ↓
merge_variable_bindings()
```

pattern と value の dataclass type が一致しない場合は match failure と
する。各 field の `PatternVariable` は既存の `VariableBinding` に変換し、
同じ variable の異なる値は reject する。

この最小基盤は全 object tree を再帰的に unification するものではなく、
statement dataclass の直接 fields を対象とする。

## 11.4 substitute_statement_pattern()

`substitute_statement_pattern()` は dataclass statement の各 field に
`substitute_pattern_value()` を適用し、同じ statement type の具体化された
instance を返す。これにより `ExactnessStatement` などを
`InferenceRule.conclusion_pattern` として利用できる。

## 11.5 merge_variable_bindings()

同一 variable に対して、

```text
same value
```

なら統合できる。

```text
different value
```

なら conflict として `None` を返す。

binding order は最初に現れた order を基本に維持する。

---

# 12. match_premise_pattern()

`PremisePattern` と `ProofStep` を match し、

```text
match failure
```

なら `None`、

```text
match success
```

なら binding tuple を返す。

boolean compatibility API:

```text
matches_premise_pattern()
```

は、

```text
binding tuple is not None
```

として実装される。

---

# 13. 複数 premise の shared binding

## 13.1 match_inference_rule_bindings()

explicitly supplied steps と premise patterns を順番に match し、
全 premise の bindings を merge する。

shared variable conflict があれば rule match 全体を reject する。

## 13.2 意味

例えば、

```text
premise 1:
x → y

premise 2:
y → z
```

で、

```text
premise 1 の y
```

と、

```text
premise 2 の y
```

は同じ値でなければならない。

これにより type-compatible combination ではなく、
binding-consistent combination を選択できる。

---

# 14. Exhaustive premise assignment

canonical search API:

```text
find_all_matching_premises()
```

とする。

## 14.1 search semantics

- ordered assignment
- pattern order を維持
- available step order を維持
- deterministic depth-first backtracking
- 1 assignment 内では同じ available-step index を再利用しない
- structurally equal な別 entry は index が別なら別候補になり得る
- empty-premise rule は1つの empty assignment
- no assignment は empty tuple

## 14.2 shared binding pruning

search の途中で binding conflict が発生した assignment は、
その branch を打ち切る。

backtracking により後続 candidate を試す。

したがって Phase 5-36 時点の単なる combinatorial enumeration から、
Phase 5-46 以降は binding-consistent exhaustive search へ進んでいる。

## 14.3 compatibility APIs

```text
find_matching_premises()
```

は first assignment compatibility view。

```text
find_inference_match()
```

は first `InferenceMatch` compatibility view。

canonical all-match APIs は、

```text
find_inference_matches_for_rule()
find_inference_matches()
```

である。

---

# 15. InferenceMatch

現在の構造:

```text
inference_rule
premises
bindings
```

bindings default は empty tuple。

matching phase で得られた binding information を
application phase へ明示的に引き渡す。

---

# 16. Substitution

## 16.1 lookup_variable_binding()

variable に対応する value を取得する。

binding conflict がある入力は invalid とする。

## 16.2 substitute_pattern_value()

variable は lookup した value へ置換する。

literal はそのまま返す。

未 binding variable は現実装では `None` になる。

## 16.3 substitute_relation_pattern()

Relation の lhs / rhs に substitution を適用し、
metadata:

```text
relation_type
source
note
```

を保持する。

## 16.4 substitute_inference_conclusion()

`InferenceMatch` の bindings を、
rule の `conclusion_pattern` へ適用する。

---

# 17. apply_inference_match()

application semantics:

1. `conclusion_builder` があれば callable validation 後に使用。
2. builder がなければ `conclusion_pattern` を substitution。
3. どちらもなければ error。

生成する step:

```text
ProofRule.INFERENCE
```

を使用し、

```text
premises = matched premises
inference_rule = source rule
```

を保持する。

---

# 18. Application trace

1 application を、

```text
InferenceApplicationResult
├── match
├── candidate_step
├── accepted
└── rejection_reason
```

として表す。

raw application 時点では、

```text
accepted = None
rejection_reason = None
```

であり、
classification 後に決定される。

---

# 19. Duplicate semantics

current duplicate identity は、

```python
candidate_step.conclusion == known_conclusion
```

である。

## 19.1 ALREADY_KNOWN

round 開始前に同じ conclusion が存在した場合。

## 19.2 SAME_ROUND_DUPLICATE

同じ round の先行 application が同じ conclusion を
accepted 済みの場合。

## 19.3 first-candidate-wins

knowledge state には、equal conclusion に対する
最初の accepted `ProofStep` のみを追加する。

alternative applications は execution trace には残る。

---

# 20. InferenceRoundResult

現在の構造:

```text
InferenceRoundResult
├── new_steps
├── matches
├── candidate_steps
├── duplicate_rejected_steps
└── application_results
```

conceptual pipeline:

```text
current state
+
rules
↓
all matches
↓
all applications
↓
candidate steps
↓
classification
├── accepted
└── rejected
↓
InferenceRoundResult
```

---

# 21. Fixed-point inference

## 21.1 run_inference_round()

1 round 分の genuinely new steps を current state に追加する。

## 21.2 run_inference_until_stable()

simple API。

最終 state の `tuple[ProofStep, ...]` を返す。

## 21.3 run_inference_until_stable_with_history()

detailed API。

```text
InferenceRunResult
├── steps
├── round_results
├── termination_reason
├── round_history
└── round_count
```

## 21.4 productive-round semantics

`round_results` に保存するのは productive round のみ。

fixed point を確認した final empty check は保存しない。

## 21.5 round_history

`round_results[*].new_steps` の compatibility view とする。

## 21.6 max_rounds

productive-round upper bound。

```text
None
```

または non-negative integer。

bool は int subclass だが明示的に reject する。

## 21.7 termination reason

```text
FIXED_POINT
MAX_ROUNDS
```

を区別する。

`MAX_ROUNDS` は fixed point を意味しない。

---

# 22. Multi-binding / multi-premise semantics

Phase 5 後半で次を end-to-end 確認した。

- single rule / multiple binding assignments
- multiple premises / multiple shared-binding assignments
- multiple variables
- partially shared variables
- one shared variable across three premises
- multiple shared variables across three premises

これにより、

```text
one rule
↓
multiple mathematically consistent assignments
↓
multiple distinct conclusions
```

を扱える。

---

# 23. Branch / merge semantics

generic engine は linear chain に限定しない。

検証済み graph:

```text
branch
↓
multiple middle conclusions
↓
merge
↓
later conclusion
```

さらに、

```text
multiple rules
↓
multiple branches
↓
fixed-point propagation
↓
multi-premise merge
```

まで end-to-end で確認した。

Phase 5-65 は、

```text
multiple branches
↓
intermediate conclusions
↓
later multi-premise rule
↓
branch merge
↓
fixed point
```

を generic-engine completion test とする。

---

# 24. Proof dependency preservation

derived `ProofStep` は matched premises をそのまま保持する。

したがって、

```text
initial facts
↓
round 1 intermediate steps
↓
round 2 final step
```

の場合も、
final step から intermediate step、
intermediate step から initial step へ依存を辿れる。

---

# 25. Current limitations

ここは過去 Phase の「当時の制限」ではなく、
Phase 5-65 時点の current limitations とする。

## 25.1 mathematical equivalence

duplicate detection / literal matching は ordinary Python equality。

未対応:

- canonicalization
- expression normalization
- mathematical equivalence
- theorem-aware equivalence

## 25.2 alternative proof storage

application trace には alternative derivations が残る。

しかし knowledge state に、

```text
one conclusion → multiple ProofSteps
```

を first-class に保存しない。

## 25.3 general recursive pattern language

Relation および dataclass statement の direct fields には
structured pattern support があるが、
任意の nested object tree に対する一般 recursive unification engine
ではない。

全 Expression / Statement tree を対象とした
一般 recursive unification engine ではない。

## 25.4 unbound conclusion variables

未 binding `PatternVariable` の substitution は `None`。

Phase 6 domain rules では、
conclusion に必要な variable が premise で必ず bind されるよう
rule design する。

必要なら後に strict validation を追加する。

## 25.5 performance

exhaustive assignment は combinatorial growth を持つ。

未導入:

- indexing
- pruning
- memoization
- semi-naive evaluation
- agenda / worklist optimization
- rule priority

Phase 6 の real rule set で必要性を観測してから最適化する。

## 25.6 semantic cycle detection

`max_rounds` は safety bound であり、
semantic cycle detector ではない。

---

# 26. Phase 5 completion criteria

Phase 5 は次を満たしたため generic-engine foundation completed とする。

1. structured proof / relation model
2. structured inference-rule metadata
3. multiple premise patterns
4. exhaustive premise assignments
5. deterministic backtracking
6. pattern variables
7. variable bindings
8. repeated-variable consistency
9. shared bindings across premises
10. bindings stored on `InferenceMatch`
11. conclusion substitution
12. multiple binding assignments
13. multiple distinct derived conclusions
14. application-level execution trace
15. duplicate-rejection reasons
16. one-round knowledge expansion
17. fixed-point execution
18. bounded execution
19. multi-round dependency preservation
20. multiple-rule propagation
21. branch generation
22. branch merge
23. multi-premise branch merge
24. fixed-point end-to-end integration

---

# 27. Phase 6 design principle

Phase 6 は、

```text
generic engine をさらに一般化する phase
```

ではなく、

```text
EHP domain inference rules を実装する phase
```

とする。

基本方針:

```text
新しい数学知識
=
新しい InferenceRule
```

と考える。

engine を変更するのは、

```text
実際の EHP rule が
現在の generic rule language では正しく表現できない
```

と確認できた場合のみ。

---

## 27.1 Phase 6-1：EHP exactness inference rule

EHP 固有の inference rule は、generic engine と分離して、

```text
ehp_rules.py
```

に置く。

Phase 6-1 の factory:

```python
ehp_exactness_inference_rule(exact_step)
```

は対象の `ExactSequenceStep` を保持し、次の premise を順序付きで
要求する。

```text
ImageStatement(first_map)
KernelStatement(second_map)
```

premise matching には既存の `ProofRule` と statement type の matching
を使用する。conclusion は既存の `ehp_exactness_proof_step()` を再利用
して構築する。

直接 `ehp_exactness_proof_step()` を呼び出した場合の step は
`ProofRule.EHP_EXACTNESS` を持つ。一方、generic engine の
`apply_inference_match()` を経由した derived step は、既存仕様により
`ProofRule.INFERENCE` を持つ。EHP 固有 rule の情報は
`ProofStep.inference_rule` から追跡できる。

Phase 6-1 の依存方向は次のとおりである。

```text
ehp_rules.py
        ↓
proof.py
ehp.py
algebra.py
```

`proof.py` に EHP 固有分岐を追加しない。

Phase 6-1 では次を導入しない。

- 任意 EHP segment の自動選択
- 新しい `ProofRule` enum 値
- generic engine の EHP-specific branch

## 27.2 Phase 6-2：structured statement matching

Phase 6-2 では、Phase 6-1 の premise matching を statement type だけから
statement 内部 fields まで拡張した。

`PremisePattern.statement_pattern` に `ImageStatement` や
`KernelStatement` の dataclass instance を指定できる。例えば、

```python
first_map = PatternVariable("first_map")
PremisePattern(
        statement_type=ImageStatement,
        statement_pattern=ImageStatement(
                group_map=first_map,
                structure=PatternVariable("image_structure"),
        ),
)
```

のように `group_map` を binding できる。

複数 premise の matching では、各 premise の field bindings を既存の
`merge_variable_bindings()` で統合する。したがって Image と Kernel の
patterns で同じ variable を使用すれば、両者が同じ map を参照すること
を generic engine の shared-binding semantics で保証できる。

EHP rule は `ehp_rules.py` に保持し、Phase 6-2 で argument-free factory を導入した。
現在の実装では Phase 6-3 の拡張により、matched maps は conclusion_pattern の substitution に使用され、map pair の妥当性は match_guard で検証される。
Phase 6-1 の引数付き factory form と既存の direct proof-step API は維持する。

Phase 6-2 の境界:

- arbitrary EHP segment からの exact pair 自動探索は行わない
- EHP sequence 全体の自動構築は行わない
- E/H/P の index arithmetic は扱わない
- generic engine に EHP-specific branch を追加しない

## 27.3 Phase 6-3：statement conclusion と match guard

Phase 6-3 では、structured statement support を premise matching だけで
なく conclusion construction にも拡張した。

`InferenceRule.conclusion_pattern` は `Relation` に加えて dataclass
statement を保持できる。`substitute_pattern_value()` は dataclass fields
を再帰的に置換し、`substitute_statement_pattern()` は statement pattern
用の明示的 API として提供する。

また `InferenceRule.match_guard` を追加した。guard は premise matching
後の `premises` と `bindings` を受け取り、domain condition を検査する。
guard が false の場合、その assignment は除外される。

argument-free EHP exactness rule は `ExactnessStatement(first_map,
second_map, True)` を conclusion pattern とし、Image/Kernel の maps が
consecutive であることを guard で確認する。Phase 6-1 の factory-bound
形式、direct proof-step API、既存の generic inference semantics は維持
する。

この phase でも arbitrary EHP segment discovery、full EHP sequence
construction、複雑な index arithmetic は実装しない。

# 28. Phase 6 candidates

候補:

- E/H/P に関する既知 relation
- EHP exactness consequences
- suspension relations
- Hopf invariant relations
- element order relations
- composition relations
- stable-range theorems
- Toda relations
- literature-backed theorem rules

将来、

```text
Toda bracket
Steenrod operation
double EHP
odd-primary data
```

へ拡張しても、
generic engine と algebra layer の境界は維持する。

---

# 29. Documentation policy

今後の文書運用では、

```text
README
=
現在できること

design.md
=
現在採用している設計

development_log.md
=
各時点で何を変更したか
```

と役割を分離する。

過去の development log に、

```text
まだ未実装
次の課題
```

と書いてあっても、
それは historical statement である。

current status は README / design の最新版を正とする。
