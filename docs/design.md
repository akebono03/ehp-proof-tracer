# ehp_proof 設計メモ

この文書は Phase 8 完了時点の current architecture / semantics /
design boundary を正本としてまとめる。

過去の development log にある「未実装」「今後の課題」は歴史的記述であり、
current specification とは限らない。

---

# 1. 全体アーキテクチャ

依存方向:

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

逆向き依存を作らない。

generic inference engine は個別 theorem の意味を知らない。

algebra layer も、

```text
E
H
P
Suspension
Toda bracket
Hopf invariant
element-order theorem
```

などのホモトピー論的意味を知らない。

基本原則:

```text
new mathematical knowledge
=
new domain InferenceRule
```

generic engine を変更するのは、

```text
actual mathematical rule が
current generic rule language では
正しく表現できない
```

と実証された場合のみとする。

---

# 2. Algebra layer

## 2.1 責務

- finitely generated abelian groups
- relation matrices
- integer lattices
- HNF / SNF
- group homomorphisms
- kernel / image / cokernel
- subgroup
- quotient
- exact sequence
- finite extension candidates

を担当する。

## 2.2 群の一般形

```text
Z^r ⊕ finite torsion
```

として統一的に扱う。

## 2.3 exactness

```text
Im(f) = Ker(g)
```

は subgroup / lattice equality。

```text
B / Im(f) ≅ Im(g)
```

は abstract group isomorphism。

両者を混同しない。

## 2.4 primary decomposition

algebra layer は 2-primary / odd-primary の理論的意味を区別しない。

その区別が必要な theorem reasoning は domain layer の責務。

---

# 3. EHP data layer

EHP layer の責務:

- E/H/P maps の構築
- repository data の読み込み
- generator 対応
- source / target group の選択
- EHP segment の構築

一般群論計算は algebra layer へ委譲する。

---

# 4. Expression layer

Current expression tree:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Composition
└── Suspension
```

generator helpers:

```text
eta(n)
nu(n)
sigma(n)
```

## 4.1 Suspension

`Suspension` は単項 expression constructor:

```python
Suspension(
  expression=x,
)
```

nested form を許可する:

```python
Suspension(
  expression=Suspension(
    expression=x,
  ),
)
```

これは expression structure の表現のみであり、

- dimension shift の妥当性
- stable range
- Freudenthal theorem
- theorem applicability
- normalization

を Expression 自身は判断しない。

## 4.2 Expression layer の非責務

Expression は、

- algebra calculation
- theorem application
- zero 判定
- equality 判定
- order calculation
- canonicalization
- simplification

を担当しない。

---

# 5. Relation / Proof layer

## 5.1 Relation

fields:

```text
lhs
rhs
relation_type
source
note
```

Current `RelationType`:

```text
EQUALITY
ZERO
ORDER
```

## 5.2 EQUALITY

EQUALITY は structural fact として directed representation を保持する。

symmetry / transitivity は object normalization ではなく explicit
InferenceRule で導出する。

## 5.3 ZERO

```text
x = 0
```

は:

```python
Relation(
  lhs=x,
  rhs=Zero(),
  relation_type=RelationType.ZERO,
)
```

で表す。

ZERO は domain-independent shared representation。

EHP / ORDER / Suspension の各 branch が同じ ZERO relation model を使用する。

## 5.4 ORDER

Concrete exact finite order:

```text
ord(α) = n
```

を:

```python
Relation(
  lhs=α,
  rhs=n,
  relation_type=RelationType.ORDER,
)
```

で表す。

`order_relation()` は positive integer validation を行う。

Current ORDER semantics は exact finite order であり、
divisibility fact や infinite order はまだ表現しない。

## 5.5 ProofStep

fields:

```text
conclusion
premises
rule
note
inference_rule
```

derived step の provenance は `premises` と `inference_rule` により保持する。

同じ knowledge state に複数 domain branch が存在しても、
premise chain を共有させない限り provenance は混線しない。

---

# 6. Generic inference engine

Phase 5-65 を generic engine foundation completion point とする。

Engine の責務:

```text
rule の theorem semantics
```

ではなく:

```text
match
bind
apply
deduplicate
iterate
trace
```

である。

Current pipeline:

```text
available ProofSteps
+
InferenceRules
↓
premise assignment search
↓
structured pattern matching
↓
variable bindings
↓
binding consistency
↓
match guard
↓
InferenceMatch
↓
conclusion construction
↓
candidate ProofStep
↓
application classification
↓
accepted new ProofSteps
```

---

# 7. InferenceRule

fields:

```text
name
description
premise_patterns
conclusion_builder
conclusion_pattern
match_guard
```

## 7.1 conclusion_pattern

bindings を nested dataclass fields へ recursive substitution できる。

## 7.2 conclusion_builder

pattern substitution だけでは表現しにくい conclusion construction に使う。

builder と conclusion_pattern が両方ある場合は builder を優先する。

## 7.3 match_guard

structural matching 後に domain-specific validity を追加する optional hook。

generic engine に domain-specific `if` branch を追加しないために用いる。

---

# 8. Matching / binding semantics

## 8.1 PatternVariable

pattern 内の変数を表す。

## 8.2 VariableBinding

```text
PatternVariable → actual value
```

を保持する。

## 8.3 Shared binding consistency

複数 premise で同じ variable が現れる場合、
同じ値へ bind されなければ match を reject する。

## 8.4 Search

`find_all_matching_premises()` は deterministic backtracking で
valid assignments を列挙する。

same available-step index を1 assignment 内で再利用しない。

---

# 9. Fixed-point semantics

Derived conclusion は knowledge state へ追加され、
後続 round で premise として利用できる。

Equal conclusion は ordinary Python equality で duplicate reject される。

## 9.1 FIXED_POINT

productive round がなくなった場合:

```text
InferenceTerminationReason.FIXED_POINT
```

## 9.2 MAX_ROUNDS

`max_rounds` に達した場合:

```text
InferenceTerminationReason.MAX_ROUNDS
```

これは safety-bound termination。

semantic nontermination proof や symbolic cycle detection ではない。

---

# 10. Generic equality / ZERO rules

## 10.1 symmetry

```text
x = y
↓
y = x
```

## 10.2 transitivity

```text
x = y
y = z
↓
x = z
```

## 10.3 generic ZERO propagation

```text
x = 0
y = x
↓
y = 0
```

known-zero expression type を限定しない。

EHP-derived, ORDER-derived, Suspension-derived ZERO を同じ rule で扱える。

---

# 11. Phase 6 EHP rule family

Representative rules:

```text
Image + Kernel → Exactness
Exactness + Image → Kernel
Exactness + Kernel → Image
Exactness → EHP zero composition
EHP zero composition → generic ZERO
```

generic equality / ZERO rules と接続し:

```text
EHP structural facts
↓
EHP domain rules
↓
generic Relation
↓
generic relation reasoning
```

へ移行できる。

generic engine に EHP-specific branch は置かない。

---

# 12. Phase 7 ORDER rule family

Concrete exact-order fact:

```text
ord(α)=n
```

から:

```text
nα=0
```

を導出する。

Rule:

```text
order_implies_zero_multiple_inference_rule()
```

ORDER-derived ZERO は generic ZERO relation であるため、
generic equality closure / ZERO propagation へそのまま接続する。

---

# 13. Phase 8 Suspension rule family

Phase 8 の principal design goal:

```text
Suspension-specific theorem knowledge
```

を:

```text
existing Expression / Relation / InferenceRule infrastructure
```

に載せる。

generic engine の変更は行わない。

## 13.1 Suspension preserves equality

Rule:

```text
suspension_preserves_equality_inference_rule()
```

Semantics:

```text
x = y
↓
E(x) = E(y)
```

conclusion は普通の `RelationType.EQUALITY`。

したがって derived equality は symmetry / transitivity / ZERO propagation
など既存 generic relation rules が利用できる。

## 13.2 Suspension preserves zero

Rule:

```text
suspension_preserves_zero_inference_rule()
```

Semantics:

```text
x = 0
↓
E(x) = 0
```

conclusion は普通の `RelationType.ZERO`。

## 13.3 Suspension preserves zero multiple

Rule:

```text
suspension_preserves_zero_multiple_inference_rule()
```

Semantics:

```text
nα = 0
↓
nE(α) = 0
```

Coefficient は保存し、underlying expression のみ Suspension する。

Rule premise が `Multiple` であることは domain guard で確認する。

## 13.4 Reconnection principle

Suspension-derived facts を Suspension 専用 reasoning silo に閉じ込めない。

Example:

```text
x = y
y = 0
↓
E(x) = E(y)
E(y) = 0
↓
generic ZERO propagation
E(x) = 0
```

重要な boundary:

```text
Suspension creates ordinary Relation facts
```

であり:

```text
Suspension requires a new generic relation engine
```

ではない。

---

# 14. EHP + ORDER + Suspension integration

Representative scenario:

```text
EHP branch                         ORDER branch

Image + Kernel                    ord(α)=n
      ↓                               ↓
Exactness                           nα=0
      ↓                               ↓
EHP zero composition              nE(α)=0
      ↓
Composition(H,E)=0
      ↓
E(Composition(H,E))=0
```

Both branches are accumulated in one proof-step state.

## 14.1 Provenance requirements

EHP suspended result:

```text
image_step
kernel_step
↓
exactness_step
↓
zero_composition_step
↓
ehp_zero_step
↓
suspended_ehp_zero_step
```

ORDER suspended result:

```text
order_step
↓
order_zero_step
↓
suspended_order_zero_step
```

Required invariant:

```text
shared knowledge state
does not imply
shared provenance
```

EHP branch premises must not accidentally include ORDER steps.

ORDER branch premises must not accidentally include EHP structural steps.

No branch-id model is currently required because explicit `ProofStep.premises`
already preserves these dependencies.

---

# 15. Suspension termination semantics

Phase 8-10 formalizes the key termination boundary.

## 15.1 Mathematical repeatability

Suspension preservation may be applied repeatedly:

```text
x = 0
↓
E(x) = 0
↓
E²(x) = 0
↓
E³(x) = 0
↓
...
```

Similarly:

```text
x = y
↓
E(x)=E(y)
↓
E²(x)=E²(y)
↓
...
```

and:

```text
nα=0
↓
nE(α)=0
↓
nE²(α)=0
↓
...
```

These conclusions are structurally distinct.

## 15.2 Duplicate rejection is insufficient

Duplicate detection uses:

```python
candidate.conclusion == known_conclusion
```

Nested Suspension depth changes the dataclass structure.

Therefore:

```text
E(x)
E²(x)
E³(x)
```

are not duplicates.

Hence unrestricted Suspension closure need not reach a finite fixed point.

## 15.3 No artificial rule guard

Do not add:

```text
if expression is already Suspension:
  reject
```

to Suspension theorem rules.

That would incorrectly change mathematical applicability in order to satisfy
an execution concern.

Current separation:

```text
theorem validity
≠
execution policy
```

---

# 16. Inference-scope policy for Suspension

## 16.1 Staged one-round execution

When the intended theorem application is exactly one Suspension level:

```python
run_inference_round(
  suspension_rule,
  available_steps,
)
```

を使う。

A single call only sees the state available at the start of that round.

Therefore:

```text
x=0
```

からその round で生成されるのは:

```text
E(x)=0
```

まで。

`E²(x)=0` は次 Suspension round を明示的に実行しない限り生成しない。

## 16.2 Bounded repeated execution

Repeated Suspension を intentional に実行する場合:

```python
run_inference_until_stable_with_history(
  suspension_rule,
  steps,
  max_rounds=n,
)
```

を使える。

新しい nested conclusions が続く場合:

```text
termination_reason == MAX_ROUNDS
```

を expected behavior とする。

## 16.3 Generic engine boundary

Phase 8 では generic engine に次を追加しない:

- Suspension depth counter
- theorem-specific cycle detector
- expression-depth cap
- "apply once" metadata
- Suspension-specific termination state

actual future requirement が生じた場合のみ別 Phase で検討する。

---

# 17. Phase 8 testing specification

Phase 8 tests are grouped conceptually as:

## 17.1 Expression

- Suspension construction
- nested Suspension representation

## 17.2 Single-rule semantics

- equality preservation
- ZERO preservation
- zero-multiple preservation
- mismatched premise rejection

## 17.3 Cross-rule integration

- ORDER-derived ZERO multiple suspension
- Suspension-derived equality → generic ZERO propagation
- EHP-derived ZERO suspension

## 17.4 Representative integration

- EHP + ORDER + Suspension scenario
- EHP and ORDER suspended conclusions coexist

## 17.5 Provenance regression

- exact premise chain
- exact `inference_rule`
- `ProofRule.INFERENCE`
- no cross-branch premise contamination

## 17.6 Termination regression

Tests formalize:

```text
unrestricted repeated Suspension
→ may remain productive
→ MAX_ROUNDS is expected under bound
```

for:

- EQUALITY
- ZERO
- zero multiple

## 17.7 Scope regression

One round derives one additional Suspension layer.

A second explicit Suspension round derives the next layer.

---

# 18. Phase 8 completion criteria

Phase 8 is complete when all of the following hold:

1. `Suspension` is a first-class Expression.
2. nested Suspension is structurally representable.
3. equality preservation is an `InferenceRule`.
4. ZERO preservation is an `InferenceRule`.
5. zero-multiple preservation is an `InferenceRule`.
6. ORDER-derived ZERO multiple can be suspended.
7. Suspension-derived equality reconnects to generic ZERO propagation.
8. EHP-derived ZERO can be suspended.
9. EHP and ORDER branches coexist with Suspension reasoning.
10. representative branch provenance is fixed by regression tests.
11. repeated Suspension is recognized as potentially unbounded.
12. bounded repeated execution returns `MAX_ROUNDS`.
13. active rule scope controls explicit Suspension depth.
14. no artificial "already suspended" theorem restriction is introduced.
15. no Suspension-specific generic-engine branch is introduced.
16. full regression suite passes.

Current verified full suite:

```text
721 passed in 22.16s
```

---

# 19. Phase 8 non-goals

Phase 8 does not implement:

- automatic dimension shift validation
- domain/codomain tracking on Expression
- Freudenthal suspension theorem
- stable-range isomorphism rules
- stable-range epimorphism rules
- automatic stabilization detection
- suspension depth planning
- canonical `E^n` representation
- expression normalization
- theorem-aware equality
- desuspension
- automatic group-level order preservation
- Hopf invariant theorem family
- Toda composition theorem family
- Toda bracket
- Steenrod operations
- double EHP
- odd-primary theorem family

---

# 20. Current limitations

## 20.1 Conclusion identity

ordinary Python equality.

No theorem-aware canonical equivalence.

## 20.2 Alternative proofs

same conclusion の multiple candidate derivations は trace に残り得るが、
knowledge state は first accepted step を保持する。

## 20.3 Pattern language

structured Relation / dataclass statement matching は可能。

arbitrary recursive symbolic unification は未導入。

## 20.4 Unbound substitution

unbound `PatternVariable` は `None` へ substitute される。

domain rule design で必要 variable を bind する。

## 20.5 Search performance

exhaustive assignment は combinatorial growth を持つ。

未導入:

- indexing
- pruning
- memoization
- semi-naive evaluation
- agenda / worklist optimization
- rule priority

## 20.6 Termination

arbitrary symbolic rule family の termination proof は行わない。

`max_rounds` は safety bound。

Phase 8 の Suspension family はこの limitation を具体的に示す最初の
domain example である。

---

# 21. Phase 9 boundary

Phase 9 は speculative generic-engine refactoring ではなく、
actual mathematical theorem family から開始する。

Phase 8 の Suspension representation を直接利用できる自然な候補:

```text
Freudenthal / stable-range reasoning
```

その他の候補:

- Hopf-invariant relations
- Toda composition relations
- literature-backed theorem rules
- Toda brackets
- Steenrod operations
- double EHP
- odd-primary-specific theorem rules

Phase 9 でも:

```text
domain theorem
↓
InferenceRule
↓
existing generic engine
```

を最初に試す。

generic engine の拡張は必要性が実証された場合のみ行う。

---

# 22. Testing principle

domain rule family を追加するときは:

1. expression / representation test
2. single-rule semantic test
3. invalid premise test
4. multi-round integration
5. generic-rule reconnection
6. provenance test
7. representative scenario
8. termination / scope boundary if relevant
9. full regression

を基本順序とする。

---

# 23. Documentation policy

```text
README.md
=
current capabilities / current status

docs/design.md
=
current architecture / semantics / design boundaries

docs/development_log.md
=
chronological implementation history
```

historical limitation は historical statement として保持する。

current specification は latest README / design を優先する。
