# ehp_proof 設計メモ

この文書は Phase 24 完了時点の current architecture / semantics /
design boundary を正本としてまとめる。

過去の development log にある「未実装」「今後の課題」は historical
statement であり、current specification とは限らない。

---

# 1. 全体アーキテクチャ

```text
literature-backed theorem facts / repository
        ↓
homotopy / EHP domain inference rules
        ↓
generic proof / inference engine
        ↓
proof-level expression / scalar / set / subgroup / modulo /
indeterminacy / Toda statements
        ↓
homotopy / EHP data layer
        ↓
finitely generated abelian-group algebra
        ↓
integer linear algebra
```

基本原則:

```text
new mathematical knowledge
=
new domain InferenceRule
```

ただし Phase 24 のような knowledge supply layer は、新しい数学的推論を
追加せず、既存 statement / ProofStep / InferenceRule に fact を供給する。

generic engine を変更するのは actual mathematical rule が current rule
language では正しく表現できないと実証された場合のみ。

---

# 2. Algebra layer

責務:

- finitely generated abelian groups
- relation matrices
- integer lattices
- HNF / SNF
- homomorphisms
- kernel / image / cokernel
- subgroup / quotient
- exact sequence

群は:

```text
Z^r ⊕ finite torsion
```

として扱う。

proof-level Toda index / iterated suspension / generator notation /
indeterminacy semantics / theorem applicability / theorem repository semantics は
algebra layer に埋め込まない。

---

# 3. Expression layer

Current tree:

```text
Expression
├── Zero
├── HomotopyElement
├── Multiple
├── Sum
├── Composition
├── MapApplication
├── Suspension
└── IteratedSuspension
```

Separate structural objects:

```text
MapSymbol
ScalarSymbol
GeneratorSymbol
TodaBracket
IndexedTodaBracketData
```

Expression layer は syntax / structure を lossless に保持する。

担当しないもの:

- theorem applicability
- repository lookup
- literature provenance materialization
- scalar solving
- candidate enumeration
- stable-range judgement
- constructor-level source / target validation
- ambient homotopy-group validation
- generator-table lookup
- generator-to-typing inference
- equality / zero proof
- commutative / associative normalization
- repeated-sum expansion
- iterated-suspension normalization
- Toda value selection
- general theorem quantification

---

# 4. Structural equality principle

Python equality は structural equality。

Mathematical equality とは区別する。

Examples:

```text
Sum(alpha,beta)
!=structural
Sum(beta,alpha)
```

```text
Multiple(2,alpha)
!=structural
Sum(alpha,alpha)
```

```text
IteratedSuspension(alpha,1)
!=structural
Suspension(alpha)
```

```text
GeneratorSymbol(family="η",index=3)
!=structural
GeneratorSymbol(family="μ",index=3)
```

```text
TodaBracket(...,index=1)
!=structural
TodaBracket(...,index=None)
```

Phase 24 repository lookup も current narrow form では、この structural
equality を theorem fact identity として再利用する。

数学的に等しい場合は explicit theorem / relation で扱う。

---

# 5. ScalarSymbol semantics

`ScalarSymbol` は symbolic integer syntax。

Uses:

```text
kβ
E^t α
```

Current structural types:

```text
Multiple.coefficient:
  int | ScalarSymbol
```

```text
IteratedSuspension.exponent:
  int | ScalarSymbol
```

`ScalarSymbol("t")` は concrete integer を選択しない。

General symbolic arithmetic object ではない。

---

# 6. Generic inference engine boundary

Engine responsibilities:

```text
match
bind
apply
deduplicate
iterate
trace
```

Termination:

```text
FIXED_POINT
MAX_ROUNDS
```

`max_rounds` は safety bound。

Phase 24 でも generic inference engine は変更しない。

Domain-specific validity は `InferenceRule.match_guard` など domain rule 側に置く。

Repository responsibilities は:

```text
store
validate repository uniqueness
lookup
materialize provenance
create existing-style GIVEN input
```

であり、generic inference engine の責務とは分離する。

---

# 7. Phase 14–17 summary

## Phase 14

```text
α∈A
A⊆B
A=B
α∈Ker(f)
α∈Im(f)
```

Role-aware subgroup reference を保持。

## Phase 15

```text
α+A
α≡β mod A
α+A=β+A
```

Modulo と ordinary equality を区別。

## Phase 16

```text
ScalarSymbol
OddScalarStatement
EvenScalarStatement
ScalarCongruenceStatement
```

General symbolic arithmetic solver は導入しない。

## Phase 17

```text
x∈β+A
x=±α
x∈{kβ+γ | k odd}
```

Partial information を exact value に潰さない。

---

# 8. Phase 18 Toda design

`TodaBracket` は three-fold unstable Toda bracket の structural object。

```text
{a,b,c}
```

Dedicated statements:

```text
TodaBracketDefinedStatement
TodaBracketMembershipStatement
```

Boundary:

```text
definedness
↛
membership
```

```text
membership
↛
exact equality
```

`TodaBracket` 自体は `Expression` ではない。

---

# 9. Phase 19 theorem bridge

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

Actual source notation:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Phase 19 では `_1` を保持できなかった。

この gap が Phase 20 の actual requirement となった。

---

# 10. Phase 20 design

Target:

```text
{a,E^t b,E^t c}_t
```

Current:

```text
TodaBracket.index:
  int | ScalarSymbol | None
```

```text
IteratedSuspension.exponent:
  int | ScalarSymbol
```

```text
IndexedTodaBracketData.suspension_exponent:
  int | ScalarSymbol
```

Key boundary:

```text
IteratedSuspension(α,1)
!=structural
Suspension(α)
```

```text
suspension exponent role
!=
bracket index role
```

`IndexedTodaBracketData.is_consistent()` は pure structural query。

```text
constructible
≠
consistent
```

```text
consistent
≠
theorem applicable
```

---

# 11. Phase 21 typed homotopy-element semantics

Current `HomotopyElement`:

```text
HomotopyElement
  name: str
  dimension: int
  source: int | None
  target: int | None
  generator: GeneratorSymbol | None
```

Phase 21 introduces minimal concrete source / target context without introducing a
universal homotopy type system.

`None` is not a wildcard.

It means that the corresponding concrete typing information is not stored.

---

# 12. Suspension source / target semantics

For:

```text
α : S^m → S^n
```

ordinary suspension exposes:

```text
Eα : S^(m+1) → S^(n+1)
```

Known information shifts by `+1`.

Unknown information remains `None`.

No constructor validation is introduced.

---

# 13. IteratedSuspension typing semantics

For concrete non-negative:

```text
r: int
```

Phase 21 derives:

```text
E^r α : S^(m+r) → S^(n+r)
```

For:

```text
ScalarSymbol("t")
```

Phase 21 does not create symbolic dimension expressions.

Therefore concrete typing query returns:

```text
source=None
target=None
```

for symbolic exponent.

Negative exponents remain structurally constructible but do not produce concrete
source / target typing.

---

# 14. Composition compatibility semantics

Current:

```text
Composition.is_type_compatible() -> bool
```

checks the required source / target boundary.

The predicate returns `True` only when both required dimensions are concrete and
equal.

Current `False` intentionally combines:

```text
known mismatch
unknown typing
unsupported typing
```

Critical:

```text
Composition(...)
```

remains constructible even when incompatible.

---

# 15. Toda entry compatibility semantics

For:

```text
{a,b,c}
```

current pure query:

```text
TodaBracket.are_defining_compositions_type_compatible()
```

checks:

```text
a∘b
b∘c
```

Both must be confirmed compatible.

Critical separation:

```text
entry compatibility
≠
ZERO composition
```

and:

```text
entry compatibility
≠
Toda definedness
```

---

# 16. Phase 22 generator design

`GeneratorSymbol` は generator identity / notation の最小構造。

```text
GeneratorSymbol
  family: str
  index: int | None
  decoration: str | None
```

`GeneratorSymbol` は `Expression` ではない。

Examples:

```text
ν
ν′
barν
η₃
μ₃
ι₇
```

All fields participate in ordinary dataclass structural equality.

```text
η₃ != η₄
η₃ != μ₃
ν != ν′
ν′ != barν
```

`index=None` と `decoration=None` は wildcard ではない。

---

# 17. HomotopyElement generator connection

Current shape:

```text
HomotopyElement
  name
  dimension
  source
  target
  generator
```

Role separation:

```text
GeneratorSymbol
=
generator identity / notation

HomotopyElement
=
homotopy expression + dimension / source / target context
```

Critical:

```text
generator notation
↛
automatic typing
```

Existing helpers:

```text
eta()
nu()
sigma()
```

は backward compatible のため legacy form のまま。

---

# 18. Suspension / generator role separation

For:

```text
Eν′
```

storage is:

```text
Suspension(
  expression=
    HomotopyElement(
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
    ),
)
```

The operation `E` is not folded into generator identity.

Thus:

```text
generator identity
!=
homotopy operation
```

---

# 19. Phase 23 design goal

Phase 23 の目的は、indexed Toda theorem fact を structural representation
から実際の membership inference へ接続すること。

対象は2種類に分ける。

```text
A. canonical indexed form
   {a,E^t b,E^t c}_t

B. specific literature form
   ε₃ ∈ {η₃,Eν′,ν₇}_1
```

この2つを無理に同じ validity representation に統合しない。

---

# 20. Indexed theorem fact semantics

既存:

```text
TodaBracketMembershipTheoremStatement
```

を再利用する。

新しい indexed theorem statement hierarchy は作らない。

Statement が保持する:

```text
element
bracket
source
note
```

`bracket` は `TodaBracket` なので:

```text
index
GeneratorSymbol
Suspension / IteratedSuspension
```

を含む bracket 全体を lossless に保持できる。

---

# 21. Bracket index match

Theorem matching は whole-bracket structural equality を使う。

したがって:

```text
{a,b,c}_1 == {a,b,c}_1
{a,b,c}_1 != {a,b,c}_2
{a,b,c}_1 != {a,b,c}
```

`index=None` は wildcard ではない。

---

# 22. Generator structure match

`HomotopyElement.generator` が structural equality に参加するため、
theorem bracket と definedness bracket の generator identity も
whole-bracket equality に含まれる。

Difference examples:

```text
family mismatch
index mismatch
decoration mismatch
```

Same display name でも generator field が異なれば structural mismatch。

Generator-specific manual theorem matcher は追加しない。

---

# 23. Definedness connection

Narrow theorem bridge:

```text
matching theorem fact
+
matching TodaBracketDefinedStatement
↓
TodaBracketMembershipStatement
```

Boundary:

```text
theorem fact
↛
membership
```

```text
definedness
↛
membership
```

Definedness は independent premise。

---

# 24. Canonical indexed structural consistency guard

Canonical indexed form:

```text
{a,E^t b,E^t c}_t
```

用 rule:

```text
indexed_toda_bracket_membership_from_theorem_inference_rule(
  indexed_data
)
```

は:

```text
indexed_data.is_consistent()
```

を要求する。

This checks:

```text
bracket.second
==
IteratedSuspension(second_base,t)

bracket.third
==
IteratedSuspension(third_base,t)

bracket.index
==
t
```

Critical:

```text
is_consistent() == True
↛
theorem applies by itself
```

---

# 25. Canonical indexed typing guard

Guard はさらに:

```text
indexed_data.bracket
.are_defining_compositions_type_compatible()
```

を要求する。

Current policy:

```text
known mismatch → reject
unknown typing → reject
```

ただし:

```text
type-compatible
↛
ZERO
↛
definedness
```

なので `TodaBracketDefinedStatement` は別 premise のまま。

---

# 26. Canonical guarded bridge

Canonical indexed rule:

```text
matching theorem fact
+
matching definedness
+
indexed structural consistency
+
confirmed entry typing compatibility
↓
indexed Toda membership
```

Theorem / definedness / `indexed_data.bracket` は structural に一致する必要がある。

Theorem source / note は membership に伝播する。

---

# 27. Actual ε₃ literature scenario

Actual notation:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

Current storage:

```text
ε₃
=
GeneratorSymbol(family="ε",index=3)

η₃
=
GeneratorSymbol(family="η",index=3)

ν′
=
GeneratorSymbol(family="ν",decoration="′")

Eν′
=
Suspension(ν′)

ν₇
=
GeneratorSymbol(family="ν",index=7)

_1
=
TodaBracket.index
```

This is lossless.

---

# 28. Why actual ε₃ is not canonical IndexedTodaBracketData

`IndexedTodaBracketData` は:

```text
second = IteratedSuspension(base,t)
third  = IteratedSuspension(base,t)
```

を要求する。

しかし actual ε₃ bracket は:

```text
second = Suspension(ν′)
third  = ν₇
index  = 1
```

である。

Current structural semantics:

```text
Suspension(ν′)
!=
IteratedSuspension(ν′,1)
```

さらに:

```text
ν₇ → ν₆
```

の inverse generator lookup は存在しない。

したがって actual ε₃ theorem を canonical data に無理に変換しない。

---

# 29. Narrow literature bridge responsibility

Actual ε₃ theorem は existing narrow bridge:

```text
specific theorem fact
+
exactly matching definedness
↓
membership
```

を使う。

Specific literature theorem fact 自体が concrete bracket identity を持つため、
canonical symbolic-form consistency model を追加で課さない。

---

# 30. Phase 23 provenance semantics

Derived indexed membership direct premises:

```text
theorem_step
defined_step
```

Unrelated facts are not included.

Theorem:

```text
source
note
```

は derived membership に伝播する。

`IndexedTodaBracketData.is_consistent()` と typing compatibility は
proof-step premise ではなく rule applicability guard。

---

# 31. Indexed / unindexed boundary

Indexed conclusion:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

から unindexed:

```text
ε₃ ∈ {η₃,Eν′,ν₇}
```

を自動生成しない。

```text
index=1
!=structural
index=None
```

---

# 32. Phase 23 completion boundary

Phase 23 completed indexed theorem preservation, structural matching,
definedness dependency, canonical consistency / typing guards, actual ε₃ narrow
bridge, provenance, and indexed / unindexed separation.

Generic inference engine remained unchanged.

---

# 33. Phase 24 design goal

Phase 24 の目的は、Phase 23 まで Python code 上で直接組み立てていた
literature-backed theorem fact を、最小 repository layer から供給できる
ようにすること。

Target dependency:

```text
literature-backed theorem fact
+
LiteratureReference
↓
TheoremFactEntry
↓
TheoremFactRepository
↓
materialized statement
↓
ProofStep.GIVEN
↓
existing InferenceRule
↓
proof graph
```

Critical:

```text
knowledge repository
!=
universal theorem prover
```

```text
stored fact
!=
automatically applicable theorem
```

```text
repository lookup success
!=
membership
```

---

# 34. TheoremFactEntry semantics

Current narrow entry:

```text
TheoremFactEntry
  statement: TodaBracketMembershipTheoremStatement
  reference: LiteratureReference
```

Phase 24 は actual repeated need のある Toda membership theorem fact family
だけを対象とする。

Current entry は universal statement wrapper ではない。

`LiteratureReference` は既存 class を再利用する。

---

# 35. TheoremFactRepository semantics

Current repository:

```text
TheoremFactRepository
  entries: tuple[TheoremFactEntry, ...]
```

Repository は immutable dataclass shape を使う。

Responsibilities:

```text
store facts
reject duplicate structural statements
lookup by structural statement
```

Responsibilities outside repository:

```text
theorem applicability
definedness
Toda membership inference
generic proof iteration
```

---

# 36. Repository identity / duplicate semantics

Current lookup identity は:

```text
entry.statement
```

の structural equality。

新しい fact key / string ID は導入しない。

Duplicate definition:

```text
entry1.statement == entry2.statement
```

なら duplicate。

したがって:

```text
same statement
+
different LiteratureReference
→ duplicate
→ ValueError
```

一方:

```text
different statement
+
same LiteratureReference
```

は許容する。

Reason:

```text
lookup statement
→ provenance source
```

の結果を repository tuple order に依存させないため。

---

# 37. Repository lookup semantics

Current API:

```text
repository.lookup(statement)
```

Behavior:

```text
known structural statement
→ matching TheoremFactEntry

unknown structural statement
→ None

empty repository
→ None
```

Lookup は exact structural identity であり、partial matching / wildcard
matching / generator-family search / bracket-only search ではない。

Wrong bracket index:

```text
_1
!=
_2
```

なので match しない。

---

# 38. Literature provenance materialization

Stored entry:

```text
TheoremFactEntry
├── statement
└── reference
```

では、stored statement の `source` を `None` のまま保持できる。

Method:

```text
TheoremFactEntry.materialize_statement()
```

は新しい theorem statement を作り:

```text
source = entry.reference
```

を設定する。

The stored statement は mutate しない。

Therefore:

```text
stored statement object
!=
materialized statement object
```

while:

```text
element
bracket
note
bracket index
generator structure
```

は保持される。

Repository metadata と proof-facing statement provenance を明示的な変換で
接続する。

---

# 39. Registered ε₃ theorem fact

Production repository representative:

```text
EPSILON_3_TODA_MEMBERSHIP_FACT
```

stores:

```text
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

with:

```text
ε₃ generator = ε, index 3
η₃ generator = η, index 3
ν′ generator = ν, decoration ′
Eν′ = Suspension(ν′)
ν₇ generator = ν, index 7
TodaBracket.index = 1
LiteratureReference(label="Toda")
```

Repository:

```text
THEOREM_FACT_REPOSITORY
```

contains this entry.

Critical:

```text
repository representation
↛
IndexedTodaBracketData conversion
```

```text
repository representation
↛
inverse generator lookup
```

---

# 40. ProofStep.GIVEN connection

`TheoremFactEntry.to_proof_step()` reuses existing:

```text
toda_bracket_membership_theorem_proof_step()
```

Chain:

```text
entry
↓
materialize_statement()
↓
source-backed theorem statement
↓
existing theorem proof-step helper
↓
ProofStep.GIVEN
```

Result semantics:

```text
rule = GIVEN
premises = ()
inference_rule = None
```

No new `ProofStep` semantics are introduced.

No repository-specific proof rule is introduced.

---

# 41. Repository theorem vs membership

Important boundary:

```text
repository fact
↓
ProofStep.GIVEN
```

means a theorem statement is known.

It does not mean:

```text
TodaBracketMembershipStatement
```

has already been proved.

The existing bridge still requires:

```text
theorem GIVEN
+
matching definedness
↓
membership
```

Therefore:

```text
repository fact
≠
membership
```

```text
lookup success
≠
theorem applicability
```

---

# 42. Phase 24 representative inference

Actual representative:

```text
THEOREM_FACT_REPOSITORY
↓
lookup ε₃ theorem
↓
TheoremFactEntry
↓
to_proof_step()
↓
theorem GIVEN
+
{η₃,Eν′,ν₇}_1 defined
↓
existing Toda theorem bridge
↓
ε₃ ∈ {η₃,Eν′,ν₇}_1
```

No new inference rule is needed.

The actual ε₃ bridge remains the narrow literature bridge from Phase 23.

---

# 43. Phase 24 provenance semantics

Derived membership direct premises remain:

```text
theorem_step
defined_step
```

A repository may contain other distinct theorem facts.

An unrelated repository-derived GIVEN step:

```text
↛
membership provenance
```

The theorem literature reference is propagated through:

```text
entry.reference
↓
materialized statement.source
↓
theorem GIVEN conclusion
↓
derived membership.source
```

Stored repository data itself remains unchanged.

---

# 44. Phase 24 inference-scope / termination boundary

Repository integration does not add recursive generation rules.

Representative scope:

```text
theorem GIVEN
+
definedness GIVEN
↓
membership
↓
FIXED_POINT
```

The matching membership appears once under ordinary inference deduplication.

No repository-to-repository generation occurs.

No theorem fact is synthesized from membership.

No automatic repository iteration is introduced.

Generic inference engine remains unchanged.

---

# 45. Phase 24 completion criteria

1. `TheoremFactRepository` is first-class.
2. empty repository is representable.
3. `TheoremFactEntry` is first-class.
4. entry stores existing `TodaBracketMembershipTheoremStatement`.
5. entry stores existing `LiteratureReference`.
6. actual ε₃ theorem fact is production data.
7. actual ε₃ structured generator identity is preserved.
8. actual bracket index `1` is preserved.
9. `Suspension(ν′)` remains ordinary Suspension.
10. no canonical `IndexedTodaBracketData` conversion.
11. repository structural lookup exists.
12. known lookup returns one entry.
13. unknown structural lookup returns `None`.
14. empty lookup returns `None`.
15. wrong-index lookup does not match.
16. duplicate structural statement is rejected.
17. same statement with another source is still duplicate.
18. no fact-key / ID system is introduced.
19. `materialize_statement()` attaches literature provenance.
20. stored statement is not mutated.
21. materialized statement preserves theorem structure.
22. `to_proof_step()` creates `ProofStep.GIVEN`.
23. existing Toda theorem proof-step helper is reused.
24. theorem step has no premises.
25. theorem step is not itself membership.
26. repository theorem + matching definedness derives membership.
27. actual ε₃ indexed membership remains lossless.
28. membership provenance is theorem step + definedness step.
29. unrelated repository fact is excluded from provenance.
30. literature source propagates to membership.
31. matching membership is not duplicated.
32. representative reaches genuine `FIXED_POINT`.
33. no repository-specific inference rule.
34. no universal theorem language.
35. no external table loader.
36. no automatic generator typing.
37. generic inference engine unchanged.
38. focused repository regression PASS.
39. Toda regression PASS.
40. full regression PASS.

Verified:

```text
tests/test_theorem_facts.py
15 passed
```

```text
tests/test_toda_rules.py
66 passed
```

```text
full suite
1190 passed in 61.30s
```

---

# 46. Phase 24 non-goals

Not implemented:

- repository support for arbitrary heterogeneous theorem families,
- universal `Statement` repository schema,
- fact key / fact ID,
- lookup by string key,
- multiple literature references for one structural theorem statement,
- external JSON / YAML knowledge table loader,
- automatic repository loading into a `Proof`,
- automatic inference execution after lookup,
- general theorem quantification,
- theorem variable substitution beyond existing inference patterns,
- generator table lookup,
- automatic generator typing,
- name / generator validation,
- ambient homotopy-group validation,
- stem validation,
- stable / unstable generator classification,
- general indexed Toda definedness theorem system,
- `Suspension` / `IteratedSuspension` normalization,
- inverse generator lookup,
- stable homotopy-group model,
- stable Toda bracket,
- higher Toda bracket.

---

# 47. Next design boundary

Natural next candidate:

```text
Phase 25
Generator typing / ambient-group facts
```

Purpose:

```text
GeneratorSymbol
+
explicit generator fact / table
↓
source / target / ambient-group knowledge
↓
existing typed HomotopyElement / theorem validity machinery
```

Important:

```text
GeneratorSymbol.index
↛
automatic typing
```

until explicit generator facts are supplied.

Phase 25 should first identify an actual generator fact requirement and add the
minimum storage / query / statement connection needed for that requirement.

Potential later dependency:

```text
generator typing / ambient-group facts
↓
general theorem representation
  only when actual quantified theorem need appears
↓
stable homotopy representation
↓
stable Toda bracket
```

---

# 48. Testing principle

For each new mathematical layer:

1. representation
2. structural distinction
3. validity / applicability
4. invalid-case behavior
5. integration
6. provenance if inference exists
7. representative scenario
8. termination / scope boundary
9. full regression

Structural-only Phase では存在しない inference / provenance を先取りしない。

---

# 49. Documentation policy

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

Current specification は latest README / design を優先する。
