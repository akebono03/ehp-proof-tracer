# ehp_proof 開発記録

この文書は Phase 25 完了時点までの開発履歴を、現在の実装と矛盾しない形で整理した改訂版である。

```text
各 Phase の「未実装」「次の課題」
=
その Phase 時点の historical statement
```

current specification は README.md / docs/design.md を優先する。

---

# Phase 1–17 summary

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

Representative Phase 17 forms:

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Verified Phase 17 full suite:

```text
1024 passed in 66.01s
```

### 状態

完了

---

# Phase 18：Toda bracket minimum representation

追加:

```text
TodaBracket
TodaBracketMembershipStatement
TodaBracketDefinedStatement
```

Verified:

```text
full suite
1048 passed in 61.09s
```

### 状態

完了

---

# Phase 19：Toda bracket membership / first theorem bridge

追加:

```text
TodaBracketMembershipTheoremStatement
```

Bridge:

```text
matching theorem fact
+
matching bracket definedness
↓
Toda bracket membership
```

Verified:

```text
full suite
1064 passed in 61.64s
```

### 状態

完了

---

# Phase 20：Indexed unstable Toda notation

追加:

```text
TodaBracket.index
IndexedTodaBracketData
IteratedSuspension
IndexedTodaBracketData.is_consistent()
```

Verified:

```text
full suite
1098 passed in 61.30s
```

### 状態

完了

---

# Phase 21：Typed homotopy elements / source-target context

追加:

```text
HomotopyElement.source
HomotopyElement.target
Composition.is_type_compatible()
TodaBracket.are_defining_compositions_type_compatible()
```

Verified:

```text
full suite
1125 passed in 22.75s
```

### 状態

完了

---

# Phase 22：Structured Generator Representation

追加:

```text
GeneratorSymbol
  family
  index
  decoration
```

Critical:

```text
generator notation
↛
automatic source / target typing
```

Verified:

```text
full suite
1153 passed in 24.83s
```

### 状態

完了

---

# Phase 23：Indexed Toda theorem / validity connection

Specific actual bridge:

```text
ε₃ theorem fact
+
exactly matching definedness
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Verified:

```text
full suite
1175 passed in 22.96s
```

### 状態

完了

---

# Phase 24：Theorem fact / knowledge-table integration

追加:

```text
TheoremFactEntry
TheoremFactRepository
EPSILON_3_TODA_MEMBERSHIP_FACT
THEOREM_FACT_REPOSITORY
```

Verified:

```text
tests/test_theorem_facts.py
15 passed
```

```text
full suite
1190 passed in 61.30s
```

### 状態

完了

---

# Phase 25：Generator typing / ambient-group facts

Critical principle:

```text
GeneratorSymbol.index
↛
automatic typing
```

Typing is supplied only from explicit registered facts.

---

## Phase 25-1：generator typing fact の最小表現

追加:

```text
GeneratorTypingFact
  generator
  source
  target
```

Representative:

```text
η₃ : S⁴ → S³
```

Verified:

```text
tests/test_generator_facts.py
6 passed
```

```text
full suite
1196 passed in 64.54s
```

### 状態

完了

---

## Phase 25-2：GeneratorSymbol と source / target fact の接続

追加:

```text
GeneratorTypingFact.matches_generator()
```

Exact structural identity.

Verified:

```text
tests/test_generator_facts.py
12 passed in 0.85s
```

```text
full suite
1202 passed in 61.04s
```

### 状態

完了

---

## Phase 25-3：ambient homotopy group fact の最小表現

追加:

```text
GeneratorAmbientGroupFact
  generator
  group_dimension
  sphere_dimension
```

Representative:

```text
η₃ ∈ π₄(S³)
```

Verified:

```text
tests/test_generator_facts.py
18 passed in 0.55s
```

```text
full suite
1208 passed in 67.35s
```

### 状態

完了

---

## Phase 25-4：η₃ generator fact の representative

Production representative:

```text
ETA_3_GENERATOR
ETA_3_TYPING_FACT
ETA_3_AMBIENT_GROUP_FACT
```

Verified:

```text
tests/test_generator_facts.py
24 passed in 1.77s
```

```text
full suite
1214 passed in 68.81s
```

### 状態

完了

---

## Phase 25-5：generator fact repository の最小接続

追加:

```text
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
```

Lookup:

```text
lookup_typing()
lookup_ambient_group()
```

Verified:

```text
tests/test_generator_facts.py
30 passed in 0.98s
```

```text
full suite
1220 passed in 64.41s
```

### 状態

完了

---

## Phase 25-6：fact lookup → typed HomotopyElement

追加:

```text
GeneratorFactRepository.materialize_typed_element()
```

Chain:

```text
untyped HomotopyElement
+
matching GeneratorTypingFact
↓
new typed HomotopyElement
```

Verified:

```text
tests/test_generator_facts.py
36 passed in 4.34s
```

```text
full suite
1226 passed in 73.20s
```

### 状態

完了

---

## Phase 25-7：Toda entry typing への representative connection

Production code:

```text
変更なし
```

Representative integration:

```text
GeneratorSymbol
↓
GeneratorTypingFact
↓
GeneratorFactRepository
↓
materialize_typed_element()
↓
typed HomotopyElement entries
↓
TodaBracket
↓
are_defining_compositions_type_compatible()
```

Verified:

```text
tests/test_generator_facts.py
40 passed in 1.69s
```

```text
full suite
1230 passed in 65.74s
```

### 状態

完了

---

## Phase 25-8：mismatch / unknown / duplicate boundary

Repository uniqueness:

```text
same generator + two typing facts
→ ValueError
```

```text
same generator + two ambient-group facts
→ ValueError
```

Cross-family one-per-family coexistence is allowed.

Existing / partial typing is not overwritten or implicitly completed.

Verified:

```text
tests/test_generator_facts.py
48 passed in 1.91s
```

```text
full suite
1238 passed in 63.30s
```

### 状態

完了

---

## Phase 25-9：provenance / regression / scope

Production code:

```text
変更なし
```

Fixed:

```text
lookup returns registered fact identity
unrelated facts do not affect η₃ materialization
HomotopyElement.name is not a lookup key
ambient-group fact alone does not materialize typing
materialization does not mutate repository
materialization does not modify theorem repository
```

Current provenance:

```text
typed element
← materialize_typed_element()
← registered GeneratorTypingFact
← GeneratorFactRepository
```

Verified:

```text
tests/test_generator_facts.py
55 passed in 2.25s
```

```text
full suite
1245 passed in 65.71s
```

### 状態

完了

---

# Phase 25 completion boundary

Implemented:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
ETA_3_GENERATOR
ETA_3_TYPING_FACT
ETA_3_AMBIENT_GROUP_FACT
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
exact structural generator lookup
duplicate rejection per fact family
unknown lookup boundary
non-mutating typed-element materialization
already-typed / partial-typing protection
Toda compatibility integration
scope / repository-separation regression
```

Main chain:

```text
GeneratorSymbol
+
explicit generator fact
↓
GeneratorFactRepository
↓
exact structural lookup
↓
GeneratorTypingFact
↓
materialize_typed_element()
↓
typed HomotopyElement
↓
existing Toda type-compatibility machinery
```

Important boundaries:

```text
GeneratorSymbol.index
↛
automatic typing
```

```text
HomotopyElement.name
↛
generator lookup
```

```text
GeneratorAmbientGroupFact
↛
source / target materialization
```

```text
typing fact
!=
ambient-group fact
```

```text
generator repository
!=
theorem repository
```

```text
lookup / materialization
↛
generic inference engine
```

Current verified status at Phase 25 completion:

```text
tests/test_generator_facts.py
55 passed in 2.25s
```

```text
full suite
1245 passed in 65.71s
```

No failures.

### 状態

完了

---

# Phase 25 post-completion representative capability demo

Phase 25完了後、各 Phase の数学的成果を人間が実行して確認できる形にするため、representative probe を導入した。

Probe:

```text
probes/probe_phase25_capabilities.py
```

Run from project root as a module:

```powershell
python -m probes.probe_phase25_capabilities
```

Direct execution:

```powershell
python probes/probe_phase25_capabilities.py
```

では project root が import path に入らず、

```text
ModuleNotFoundError: No module named 'expression'
```

となるため、module execution を標準とする。

Representative regression run:

```powershell
python -m pytest tests/test_theorem_facts.py -q
python -m pytest tests/test_generator_facts.py -q
python -m pytest -q
```

Observed:

```text
15 passed in 0.08s
55 passed in 0.24s
1245 passed in 23.45s
```

Representative mathematical inference demonstrated:

```text
THEOREM_FACT_REPOSITORY
↓
EPSILON_3_TODA_MEMBERSHIP_FACT
↓
literature-backed ProofStep.GIVEN
+
{η₃,Eν′,ν₇}_1 defined
↓
Toda bracket membership inference rule
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
↓
FIXED_POINT
```

Representative Phase 25 generator-knowledge demonstration:

```text
untyped η₃
+
ETA_3_GENERATOR
↓
GENERATOR_FACT_REPOSITORY.lookup_typing()
↓
η₃ : S⁴ → S³
↓
materialize_typed_element()
↓
new typed HomotopyElement
```

Ambient group lookup also displays:

```text
η₃ ∈ π₄(S³)
```

Non-mutation is visible:

```text
original source = None
original target = None
new source = 4
new target = 3
```

The same probe explicitly displays the Phase 25 boundary:

```text
ν′ production typing
ν₇ production typing
repository-derived Eν′ typing
complete production typing of all ε₃ Toda entries
```

are not yet implemented.

Therefore the current state is:

```text
actual Toda membership inference
+
explicit generator typing materialization
```

both work independently, but:

```text
generator facts
↓
all ε₃ Toda entry typing
↓
definedness
↓
theorem applicability
↓
membership
```

is not yet one complete end-to-end proof.

### 方針

今後、可能な Phase では完了整理に以下を含める:

```text
focused pytest
full regression
representative probe command
human-readable mathematical result
what became possible in this Phase
what remains outside the Phase boundary
```

Probe は production API / existing inference engine を実際に使い、テスト専用の別ロジックで数学的結果を偽装しない。

### 状態

記録完了

---

# Phase 26 candidate

Natural next candidate:

```text
Phase 26
Generator fact provenance / actual Toda-generator typing expansion
```

Candidate actual requirements:

```text
LiteratureReference-backed generator typing fact
ν′ / ν₇ production typing facts
typing / ambient-group consistency validation
explicit nested Suspension typing
```

The next Phase should choose one actual mathematical need first.

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
