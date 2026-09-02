# ehp_proof 開発記録

この文書は EHP Proof Tracer の時系列の実装履歴を記録する。

```text
各 Phase の「未実装」「次の課題」
=
その Phase 時点の historical statement
```

current specification は `README.md` / `docs/design.md` を優先する。

---

# Phase 1–17 概要

Phase 1: finite abelian-group calculations.

Phase 2: structured subgroup calculations.

Phase 3: quotient / exact sequence / extension.

Phase 4: presentation-based finitely generated abelian groups.

Phase 5: generic proof / inference engine foundation.

Phase 6: EHP domain inference foundation.

Phase 7: element-order reasoning.

Phase 8: Suspension reasoning.

Phase 9: Freudenthal / stable-range reasoning.

Phase 10: composition reasoning.

Phase 11: generalized Hopf-invariant reasoning.

Phase 12: additive expression / reasoning.

Phase 13: homomorphism reasoning.

Phase 14: set / subgroup reasoning.

Phase 15: coset / modulo reasoning.

Phase 16: symbolic scalar constraints.

Phase 17: indeterminacy.

### 状態

完了

---

# Phase 18–24 概要

Phase 18:
Toda bracket minimum representation.

追加:

```text
TodaBracket
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

Phase 19:
Toda bracket membership / first theorem bridge.

Phase 20:
Indexed unstable Toda notation.

追加:

```text
TodaBracket.index
IndexedTodaBracketData
IteratedSuspension
```

Phase 21:
Typed homotopy elements / source-target context.

Phase 22:
Structured `GeneratorSymbol`.

Phase 23:
Indexed Toda theorem / validity connection.

Phase 24:
Theorem fact / knowledge-table integration.

### 状態

完了

---

# Phase 25：generator typing / ambient-group facts

追加:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
materialize_typed_element()
```

代表:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
```

### 状態

完了

---

# Phase 26：actual Toda-generator typing expansion

production generator coverage:

```text
η₃
ν′
ν₇
```

typing:

```text
η₃ : S⁴ → S³
ν′ : S⁶ → S³
ν₇ : S¹⁰ → S⁷
```

Suspension:

```text
ν′
↓
Eν′ : S⁷ → S⁴
```

actual bracket:

```text
{η₃,Eν′,ν₇}_1
```

### 状態

完了

---

# Phase 27：corrected actual ε₃ Toda-definedness / end-to-end inference

primitive knowledge:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
```

corrected rule:

```text
a ∘ Eb = 0
b ∘ c = 0
Ec = d
↓
{a,Eb,d}_1 is defined
```

actual result:

```text
η₃ ∘ Eν′ = 0
ν′ ∘ ν₆ = 0
Eν₆ = ν₇
↓
{η₃,Eν′,ν₇}_1 is defined
```

さらに theorem fact と接続:

```text
Toda theorem fact
+
derived definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

### 状態

完了

---

# Phase 28：map-property equality-reflection foundation

目的:

```text
f(a)=f(b)
+
f is injective / isomorphism
↓
a=b
```

追加:

```text
InjectiveMapStatement
IsomorphismStatement
isomorphism_implies_injective_inference_rule()
injective_map_reflects_equality_inference_rule()
```

### 状態

完了

---

# Phase 29：actual H map facts / typing

production identity:

```text
HOPF_MAP = MapSymbol(name="H")
```

追加:

```text
MapTypingFact
MapIsomorphismFact
MapIsomorphismFactRepository
HOPF_MAP_TYPING_FACT
HOPF_MAP_ISOMORPHISM_FACT
MAP_ISOMORPHISM_FACT_REPOSITORY
```

actual chain:

```text
production H isomorphism fact
↓
ProofStep.GIVEN Isomorphism(H)
↓
Injective(H)
+
H(a)=H(b)
↓
a=b
```

### 状態

完了

---

# Phase 30：Toda Prop.2.2 右側公式

対象:

```text
H(a∘Eb)=H(a)∘Eb
```

当初は existing generalized Hopf machinery を利用して:

```text
H(a)=β
↓
H(a∘Eb)=β∘Eb
```

と:

```text
H(a)=β
↓ symmetry
β=H(a)
↓ staged right composition
β∘Eb=H(a)∘Eb
```

を作り、transitivity で:

```text
H(a∘Eb)=H(a)∘Eb
```

まで閉じた。

この実装で:

```text
HopfInvariantStatement
actual-H bridge
equality symmetry
right-composition congruence
transitivity
```

の接続を確認した。

当時の final regression:

```text
full provenance
mismatched-middle rejection
different-right-factor rejection
unrelated equality exclusion
round-level deduplication
terminal transitivity regression
staged right-composition boundary
```

### Phase 32 実装中の設計修正

Phase 32 の検討時に、この β 経由経路は Toda Prop.2.2 本体を別の既知事実から証明しているのではなく、Prop.2.2 の内容を concrete Hopf value へ一度 specialize して元へ戻していることを確認した。

したがって Phase 30 も direct theorem 方式へ修正した。

追加:

```text
toda_prop22_right_inference_rule()
```

current theorem semantics:

```text
a, b
↓ Toda Prop.2.2
H(a∘Eb)=H(a)∘Eb
```

```text
premises = ()
```

β-based path は削除せず:

```text
specialization / integration / consistency regression
```

として保持する。

direct theorem と β path の最終 conclusion が一致することを確認した。

修正後 focused:

```text
tests/test_phase30_prop22.py
25 passed
```

### 状態

完了

---

# Phase 31：SmashProduct minimum representation

目的:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

に必要な `c∧c` を表現する。

追加:

```text
SmashProduct(Expression)
  left
  right
```

確認:

```text
a∧b
c∧c
E(c∧c)
```

を structural に保持可能。

boundary:

```text
representation
!=
typing
!=
theorem knowledge
```

current:

```text
SmashProduct has no source / target
E(c∧c).source = None
E(c∧c).target = None
```

Barratt–Hilton は未実装。

Phase 31 完了時:

```text
full suite
1466 passed
```

### 状態

完了

---

# Phase 32：Toda Prop.2.2 左側公式

対象:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

---

## Phase 32-1：formula structural representation

production code 変更なし。

既存:

```text
Composition
Suspension
SmashProduct
MapApplication
Relation
```

を組み合わせて左公式を lossless に表現可能であることを確認した。

focused:

```text
6 tests
```

### 状態

完了

---

## Phase 32-2：HopfInvariantStatement / actual-H equality distinction

確認:

```text
HopfInvariantStatement
!=
actual H Relation
```

`HopfInvariantStatement` は map identity を直接保持しない。

actual H equality は:

```text
MapApplication(
  map=HOPF_MAP,
  expression=...
)
```

を明示する。

### 状態

完了

---

## Phase 32-3：left composition law statement minimum representation

追加:

```text
HopfLeftCompositionLawStatement
  alpha
  beta
  gamma
```

この時点では direct Toda theorem ではなく、generalized Hopf value を concrete `β` へ接続するための中間 statement として導入した。

### 状態

完了

---

## Phase 32-4：generalized left-composition specialization

追加:

```text
hopf_left_composition_law_inference_rule()
hopf_left_composition_formula_inference_rule()
```

経路:

```text
H(a)=β
+
c
↓
HopfLeftCompositionLawStatement(a,β,c)
↓
H((Ec)∘a)=E(c∧c)∘β
```

### 状態

完了

---

## Phase 32-5：β=H(a) connection

追加:

```text
equality_preserved_under_left_composition_inference_rule()
```

経路:

```text
H(a)=β
↓ actual-H bridge
H(a)=β
↓ symmetry
β=H(a)
↓ staged left composition
E(c∧c)∘β=E(c∧c)∘H(a)
```

left-composition congruence は expression growth を生むため staged one-shot rule とした。

### 状態

完了

---

## Phase 32-6：transitivity closure

二枝:

```text
H((Ec)∘a)=E(c∧c)∘β
```

```text
E(c∧c)∘β=E(c∧c)∘H(a)
```

から:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

を equality transitivity で導出。

この時点では end-to-end integration として成功した。

focused:

```text
29 passed
```

full suite:

```text
1498 passed
```

### 状態

完了

---

## Phase 32-7：typing / scope boundary regression

確認:

```text
SmashProduct(c,c)
→ source / target を自動生成しない
```

```text
E(c∧c).source = None
E(c∧c).target = None
```

さらに:

```text
left law は explicit c を要求
left formula specialization は law statement を要求
c∧c は arbitrary known expression へ自動簡約しない
```

focused:

```text
34 passed
```

full suite:

```text
1503 passed
```

### 状態

完了

---

## Phase 32-8：representative executable probe

追加:

```text
probes/probe_phase32_capabilities.py
```

当初は β-based integration chain を表示した。

実行により:

```text
full provenance preserved = True
actual H map preserved = True
```

および typing / scope boundary を確認した。

### 状態

完了

---

# Phase 32 設計レビュー：direct theorem 化

Phase 32-8 後、数学的意味を再確認した。

結論:

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

は Toda Prop.2.2 左側そのものであり、`H(a)=β` は theorem premise ではない。

したがって β を経由して formula 自体へ戻す設計を canonical theorem representation とするのは不自然であると判断した。

修正方針:

```text
Toda Prop.2.2
↓
direct proof-level equality
```

を主経路とする。

β path は specialization / integration regression として残す。

---

## direct theorem rule の追加

追加:

```text
toda_prop22_left_inference_rule(
  alpha,
  gamma,
)
```

結論:

```text
H((E gamma)∘alpha)
=
E(gamma∧gamma)∘H(alpha)
```

premises:

```text
()
```

actual H identity:

```text
EHP_H_MAP
```

を conclusion builder で直接使用する。

---

## canonical H identity regression

最初の direct theorem test では:

```text
MapSymbol(name="H") is MapSymbol(name="H")
```

が False となる問題が発見された。

原因:

```text
conclusion_pattern
```

による dataclass 再構築で canonical `EHP_H_MAP` identity が保持されなかったため。

修正:

```text
conclusion_builder
```

で production `EHP_H_MAP` を直接返す。

修正後:

```text
lhs H is HOPF_MAP
rhs H is HOPF_MAP
```

を object identity で確認できるようになった。

focused:

```text
tests/test_phase32_prop22.py
38 passed
```

full suite:

```text
1507 passed
```

---

# Phase 30 direct theorem 化

Phase 32 の design correction に合わせ、Phase 30 右側も同じ direct theorem semantics へ修正した。

追加:

```text
toda_prop22_right_inference_rule()
```

結論:

```text
H(a∘Eb)=H(a)∘Eb
```

premises:

```text
()
```

canonical actual H identity を conclusion builder で保持。

β-based historical chain は integration / specialization regression として維持。

修正途中、`tests/test_phase30_prop22.py` の import 更新時に:

```text
derive_inference_round_result
```

の import が落ち、既存 Phase 30-7 test が NameError になった。

production logic の失敗ではなく、既存 import の欠落であったため import を復元。

修正後:

```text
tests/test_phase30_prop22.py
25 passed
```

full suite:

```text
1511 passed
```

### 状態

完了

---

## Phase 32-9：final regression

direct theorem を Phase 32 の正式な最終仕様として representative regression に固定した。

確認:

```text
premises == ()
```

```text
H((Ec)∘a)=E(c∧c)∘H(a)
```

```text
lhs H is HOPF_MAP
rhs H is HOPF_MAP
```

```text
Ec structure preserved
E(c∧c) structure preserved
```

```text
SmashProduct typing remains unimplemented
```

focused:

```text
tests/test_phase32_prop22.py
39 passed
```

関連:

```text
tests/test_phase30_prop22.py
25 passed

tests/test_hopf_rules.py
31 passed

tests/test_map_facts.py
54 passed
```

full suite:

```text
1512 passed in 63.58s
```

No failures.

### 状態

完了

---

# Phase 32-10：Phase 32 完了整理

Phase 32 completion result:

```text
Toda Prop.2.2 right
H(a∘Eb)=H(a)∘Eb
```

```text
Toda Prop.2.2 left
H((Ec)∘a)=E(c∧c)∘H(a)
```

の双方を direct theorem rule として actual H identity を保持した proof-level equality で表現・適用可能になった。

Phase 32 canonical capability:

```text
a, c
↓
Toda Prop.2.2
↓
H((Ec)∘a)=E(c∧c)∘H(a)
```

human-readable probe:

```powershell
python -m probes.probe_phase32_capabilities
```

確認:

```text
premises: none
lhs correct = True
rhs correct = True
actual H map preserved = True
```

typing boundary:

```text
SmashProduct has source: False
SmashProduct has target: False
E(c∧c).source = None
E(c∧c).target = None
```

generic inference engine:

```text
変更なし
```

final verified status:

```text
full suite
1512 passed in 63.58s
```

No failures.

### 状態

完了

---

# Phase 32 completion boundary

Phase 32 で完成:

```text
Toda Prop.2.2
right + left
```

未実装:

```text
SmashProduct typing
SmashProduct algebra / normalization
Barratt-Hilton Prop.3.1
symbolic (-1)^n expression
symbolic sign parity reduction
actual H((2ι₂)η₂) calculation
H((2ι₂)η₂)=H(4η₂)
(2ι₂)η₂=4η₂
```

次の mathematical dependency:

```text
Toda Prop.2.2 COMPLETE
↓
Barratt-Hilton に必要な最小 prerequisite
↓
Toda Prop.3.1
↓
actual H calculation
↓
Phase 29 equality reflection
```

---

# 次の Phase

推奨:

```text
Phase 33
Barratt-Hilton prerequisite minimum representation
```

第一候補:

```text
symbolic scalar expression
(-1)^n
```

と parity reduction。

ただし、actual Toda Prop.3.1 の式をもう一度確認し、既存 `IteratedSuspension` で不足する typing / exponent 表現がある場合は、その concrete need を優先する。

---

# 文書運用方針

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

historical limitation と current limitation を混同しない。
