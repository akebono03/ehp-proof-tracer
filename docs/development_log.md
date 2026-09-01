# ehp_proof 開発記録

この文書は Phase 26 完了時点までの開発履歴を、現在の実装と矛盾しない形で整理した改訂版である。

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

Main additions:

```text
GeneratorTypingFact
GeneratorAmbientGroupFact
ETA_3_GENERATOR
ETA_3_TYPING_FACT
ETA_3_AMBIENT_GROUP_FACT
GeneratorFactRepository
GENERATOR_FACT_REPOSITORY
materialize_typed_element()
```

Representative:

```text
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
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

Verified at Phase 25 completion:

```text
tests/test_generator_facts.py
55 passed in 2.25s
```

```text
full suite
1245 passed in 65.71s
```

Post-completion representative probe:

```powershell
python -m probes.probe_phase25_capabilities
```

Visible results:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
η₃ : S⁴ → S³
η₃ ∈ π₄(S³)
```

Phase 25 boundary:

```text
ν′ production typing
ν₇ production typing
repository-derived Eν′ typing
complete ε₃ entry typing
```

were not yet implemented.

### 状態

完了

---

# Phase 26：actual Toda-generator typing expansion

Goal:

```text
{η₃,Eν′,ν₇}_1
```

の3 entry を notation から推測するのではなく、explicit generator facts から typed にし、既存 Toda type-compatibility machinery に接続する。

---

## Phase 26-1：ν′ generator typing fact の最小表現

追加:

```text
NU_PRIME_GENERATOR
NU_PRIME_TYPING_FACT
```

Identity:

```text
GeneratorSymbol(
  family="ν",
  decoration="′",
)
```

Typing:

```text
ν′ : S⁶ → S³
```

At this step the fact existed but was intentionally not yet registered in the production repository.

Verified:

```text
tests/test_generator_facts.py
61 passed in 0.30s
```

```text
full suite
1251 passed in 24.88s
```

### 状態

完了

---

## Phase 26-2：ν₇ generator typing fact の最小表現

追加:

```text
NU_7_GENERATOR
NU_7_TYPING_FACT
```

Identity:

```text
GeneratorSymbol(
  family="ν",
  index=7,
)
```

Typing:

```text
ν₇ : S¹⁰ → S⁷
```

Structural distinction fixed:

```text
ν₇ != ν′
ν₇ != unindexed ν
```

Verified:

```text
tests/test_generator_facts.py
68 passed in 0.38s
```

```text
full suite
1258 passed in 25.09s
```

### 状態

完了

---

## Phase 26-3：ν′ / ν₇ ambient-group fact

追加:

```text
NU_PRIME_AMBIENT_GROUP_FACT
NU_7_AMBIENT_GROUP_FACT
```

Facts:

```text
ν′ ∈ π₆(S³)
ν₇ ∈ π₁₀(S⁷)
```

Boundary maintained:

```text
typing fact
!=
ambient-group fact
```

No cross-family consistency rule was introduced yet.

Verified:

```text
tests/test_generator_facts.py
76 passed in 0.41s
```

```text
full suite
1266 passed in 23.03s
```

### 状態

完了

---

## Phase 26-4：production repository への登録

Updated production repository coverage:

```text
typing facts:
  η₃
  ν′
  ν₇

ambient-group facts:
  η₃
  ν′
  ν₇
```

Now available:

```text
lookup_typing(ν′)
→ NU_PRIME_TYPING_FACT

lookup_typing(ν₇)
→ NU_7_TYPING_FACT
```

```text
lookup_ambient_group(ν′)
→ NU_PRIME_AMBIENT_GROUP_FACT

lookup_ambient_group(ν₇)
→ NU_7_AMBIENT_GROUP_FACT
```

Materialization:

```text
ν′ → S⁶ → S³
ν₇ → S¹⁰ → S⁷
```

Historical "not yet registered" tests from 26-1 to 26-3 were removed when their boundary intentionally changed in 26-4.

Verified:

```text
tests/test_generator_facts.py
76 passed in 0.29s
```

```text
full suite
1266 passed in 23.10s
```

### 状態

完了

---

## Phase 26-5：Eν′ の explicit typing connection

Production code:

```text
変更なし
```

Existing layers were connected explicitly:

```text
NU_PRIME_TYPING_FACT
↓
GENERATOR_FACT_REPOSITORY
↓
ν′ : S⁶ → S³
↓
Suspension
↓
Eν′ : S⁷ → S⁴
```

Boundary:

```text
Suspension(untyped ν′)
→ untyped
```

No recursive repository typing and no `materialize_typed_suspension()` API were added.

Verified:

```text
tests/test_generator_facts.py
81 passed in 0.32s
```

```text
full suite
1271 passed in 25.43s
```

### 状態

完了

---

## Phase 26-6：{η₃,Eν′,ν₇}_1 の entry typing representative

Production code:

```text
変更なし
```

Actual typed entries:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

Constructed:

```text
TodaBracket(
  first=typed η₃,
  second=typed Eν′,
  third=typed ν₇,
  index=1,
)
```

The typed bracket preserves the same generator identities and index as the actual theorem-side notation.

Full bracket structural equality is intentionally not required because typed entries contain source / target data.

Verified:

```text
tests/test_generator_facts.py
85 passed in 0.31s
```

```text
full suite
1275 passed in 23.31s
```

### 状態

完了

---

## Phase 26-7：actual ε₃ bracket の type compatibility 確認

Production code:

```text
変更なし
```

Actual defining compositions:

```text
η₃ ∘ Eν′
Eν′ ∘ ν₇
```

Typing checks:

```text
η₃.source = 4
Eν′.target = 4
```

```text
Eν′.source = 7
ν₇.target = 7
```

Therefore:

```text
{η₃,Eν′,ν₇}_1
→ defining compositions are type-compatible
```

Critical boundary:

```text
type-compatible
!=
composition is zero
!=
Toda bracket is defined
```

Verified:

```text
tests/test_generator_facts.py
89 passed in 0.35s
```

```text
full suite
1279 passed in 23.35s
```

### 状態

完了

---

## Phase 26-8：typing / ambient-group consistency boundary

追加:

```text
GeneratorFactRepository.is_typing_ambient_group_consistent()
```

Semantics:

```text
True
=
both explicit facts exist and agree
```

```text
False
=
both explicit facts exist and disagree
```

```text
None
=
one or both facts are missing
```

Agreement condition:

```text
typing.source == ambient.group_dimension
and
typing.target == ambient.sphere_dimension
```

Production results:

```text
η₃ → True
ν′ → True
ν₇ → True
```

No fact generation and no automatic repair were added.

Verified:

```text
tests/test_generator_facts.py
95 passed in 0.37s
```

```text
full suite
1285 passed in 23.47s
```

### 状態

完了

---

## Phase 26-9：provenance / regression / scope

Production code:

```text
変更なし
```

Regression boundaries fixed:

```text
actual Toda typing chain
↛
generator repository mutation
```

```text
actual Toda typing chain
↛
theorem repository mutation
```

```text
consistency query
↛
new fact generation
```

```text
ν₇ registered
↛
general ν_n automatic typing
```

Current provenance fixed as:

```text
η₃
← ETA_3_TYPING_FACT
```

```text
Eν′
← Suspension
← NU_PRIME_TYPING_FACT
```

```text
ν₇
← NU_7_TYPING_FACT
```

This remains data-path provenance rather than `ProofStep` provenance.

Verified:

```text
tests/test_generator_facts.py
100 passed in 0.39s
```

```text
full suite
1290 passed in 23.16s
```

### 状態

完了

---

## Phase 26-10：Phase 26 完了整理

Phase 26 completion chain:

```text
ETA_3_TYPING_FACT
NU_PRIME_TYPING_FACT
NU_7_TYPING_FACT
+
ambient-group facts
↓
GENERATOR_FACT_REPOSITORY
↓
typed η₃ / ν′ / ν₇
↓
Suspension
↓
typed Eν′
↓
TodaBracket(
  η₃,
  Eν′,
  ν₇,
  index=1
)
↓
existing Toda type-compatibility query
↓
defining compositions are type-compatible
```

Visible mathematical result:

```text
η₃  : S⁴  → S³
Eν′ : S⁷  → S⁴
ν₇  : S¹⁰ → S⁷
```

```text
η₃ ∘ Eν′
Eν′ ∘ ν₇
```

are type-compatible.

Phase 26 does not derive:

```text
η₃ ∘ Eν′ = 0
Eν′ ∘ ν₇ = 0
```

and therefore does not replace the separate Toda definedness premise used by the theorem bridge.

Documentation updated:

```text
README.md
docs/design.md
docs/development_log.md
docs/roadmap.md
```

Representative probe added:

```powershell
python -m probes.probe_phase26_capabilities
```

Final verified regression status:

```text
tests/test_generator_facts.py
100 passed in 0.39s
```

```text
full suite
1290 passed in 23.16s
```

### 状態

完了

---

# Phase 26 completion boundary

Implemented:

```text
ν′ explicit typing / ambient facts
ν₇ explicit typing / ambient facts
production repository registration
production materialization
explicit Eν′ typing via existing Suspension semantics
actual typed η₃ / Eν′ / ν₇ entries
actual indexed ε₃ Toda representative
actual defining-composition type compatibility
typing / ambient consistency query
True / False / None consistency semantics
scope / provenance regression
```

Critical boundaries:

```text
GeneratorSymbol
↛
automatic family typing
```

```text
type compatibility
↛
zero composition
```

```text
type compatibility
↛
Toda definedness
```

```text
consistency query
↛
fact generation
```

```text
generator fact repository
!=
theorem fact repository
```

```text
current generator provenance
!=
ProofStep provenance
```

Current verified status:

```text
tests/test_generator_facts.py
100 passed in 0.39s
```

```text
full suite
1290 passed in 23.16s
```

No failures.

### 状態

完了

---

# Next candidate

A natural next direction is to continue the same actual ε₃ bracket rather than widen generator coverage immediately.

Candidate chain:

```text
typed actual entries
↓
explicit zero-composition facts
↓
Toda definedness
↓
existing theorem fact
↓
ε₃ membership
↓
proof trace
```

Alternative candidates:

```text
generator-fact LiteratureReference
name / generator / dimension validation
external generator table loading
```

Stable homotopy groups and stable Toda brackets remain later layers.

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
