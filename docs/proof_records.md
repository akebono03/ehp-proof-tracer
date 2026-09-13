# EHP Proof Tracer — Proof Records

この文書は、EHP Proof Tracer が実際に導出し、representative probe で人間向けに表示した代表的な数学的証明を記録する。

目的は、単なる実装履歴ではなく、

- 何を証明したか
- どの derived result を使ったか
- どの文献 statement に対応するか
- `GIVEN` と `INFERENCE` の境界がどこにあるか
- machine provenance がどの Phase へ遡るか
- representative probe がどのように人間向けに表示するか

を、長期的に追跡可能な形で残すことである。

現在の `Proof-style derivation` は、`ProofStep` graph から自動生成された証明文ではない。各 Phase で確認済みの machine provenance と数学的依存関係に基づいて、probe 側に hand-authored presentation layer として記述している。

将来 automatic proof narrative generation を実装するとき、この文書に蓄積した representative proof を human-reviewed golden reference として利用する。

---

# 1. この文書の役割

既存ドキュメントとの責務分担は次のとおり。

```text
README.md
  現在何ができるか

docs/design.md
  なぜその表現・設計なのか

docs/development_log.md
  いつ何を実装したか

docs/roadmap.md
  今後どの能力を実装するか

docs/code_reference.md
  どの module / class / function が何を担当するか

docs/proof_records.md
  実際にどの数学的結果を、
  どの provenance と proof-style display で導出したか
```

`docs/proof_records.md` は persistent proof repository ではない。

```text
ProofStep object persistence
proof graph database
derived fact database
automatic theorem search
automatic theorem replay cache
```

はこの文書の責務ではない。

この文書は人間向けの curated proof record である。

---

# 2. 記録フォーマット

今後の各 representative proof は、可能な限り次の形式で記録する。

```text
1. Source / theorem
2. Result
3. Hypotheses / upstream results
4. Derived ingredients
5. Proof-style derivation
6. Machine provenance
7. Literature
8. GIVEN / INFERENCE boundary
9. Representation boundary
10. Representative probe
11. Regression status
```

すべての Phase で全項目が必要とは限らないが、automatic proof narrative generation の display schema を観察するため、できる限り同じ順序を保つ。

---

# 3. Earlier representative probes

Phase 66-8 から正式な proof record を開始する。

それ以前にも代表的な proof-style probe は存在する。

```text
Phase 60
  Toda Lemma 5.4
  ν₄∈π_7^4
  H(ν₄)=ι₇
  2Eν₄=E²ν′

Phase 61
  Toda Lemma 5.5
  Toda bracket transport

Phase 62
  Toda (5.5)
  ν-family
  2ν_n=E^(n-3)ν′
  4ν_n=η_n³

Phase 63
  Toda (5.6)
  π_(i-1)^3 ⊕ π_i^7 ≅ π_i^4

Phase 65
  Toda Proposition 5.6
  π_5^2=Z/2{η₂³}
  π_6^3=Z/4{ν′}
  π_7^4=Z{ν₄}⊕Z/4{Eν′}
  π_(n+3)^n=Z/8{ν_n}, n≥5
```

Phase 66-8 ではこれらを全面的に backfill しない。

過去 Phase の proof record 化は、必要になった時点で別 Phase または documentation task として行う。

---

# 4. Toda Equation (5.8)

## 4.1 Source / theorem

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Equation (5.8)
```

対象式:

```text
Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄]
```

---

## 4.2 Result

Phase 66 では Equation (5.8) を次の3つの first-class derived statement に分解して統合する。

```text
Δ(ι₉)=±(2ν₄-Eν′)

[ι₄,ι₄]=±(2ν₄-Eν′)

Δ(ι₉)=±[ι₄,ι₄]
```

最終的にこれらを literature-aware aggregate:

```text
Toda58EquationStatement
```

へ統合する。

aggregate 自身は:

```text
ProofRule.INFERENCE
```

である。

---

## 4.3 Upstream results

### Phase 65 branch

Phase 65 で derived:

```text
π_7^4
=
Z{ν₄} ⊕ Z/4{Eν′}
```

この decomposition から Equation (5.8) の positive representative:

```text
2ν₄-Eν′
```

を既存 expression tree:

```text
Sum(
  Multiple(2, ν₄),
  Multiple(-1, Eν′),
)
```

として保持する。

### Phase 60 branch

Phase 60 Toda Lemma 5.4 で Whitehead correction data:

```text
[ι₄,ι₄]

H[ι₄,ι₄]=(-1)^u 2ι₇

E[ι₄,ι₄]=0
```

を derived provenance として保持している。

Phase 66 では、この既存 `[ι₄,ι₄]` object を再利用する。

---

## 4.4 Derived ingredients

Phase 66-3:

```text
π_7^4=Z{ν₄}⊕Z/4{Eν′}
        ↓
Toda Equation (5.8)
        ↓
Δ(ι₉)=±(2ν₄-Eν′)
```

Phase 66-4:

```text
Δ(ι₉)=±(2ν₄-Eν′)
+
Phase 60 Whitehead correction data
        ↓
Toda Equation (5.8)
        ↓
[ι₄,ι₄]=±(2ν₄-Eν′)
```

Phase 66-5:

```text
Δ(ι₉)=±(2ν₄-Eν′)

[ι₄,ι₄]=±(2ν₄-Eν′)

same positive representative
        ↓
Δ(ι₉)=±[ι₄,ι₄]
```

Phase 66-7:

```text
Phase 66-3 result
+
Phase 66-4 result
+
Phase 66-5 result
        ↓
Toda58EquationStatement
        INFERENCE
```

---

## 4.5 Proof-style derivation

Representative human-readable derivation:

```text
Phase 65:
π_7^4 = Z{ν₄} ⊕ Z/4{Eν′}

Therefore the Toda (5.8) representative
2ν₄-Eν′
is available in π_7^4.

Toda Equation (5.8):
Δ(ι₉)=±(2ν₄-Eν′).

Phase 60:
the Whitehead square [ι₄,ι₄]
is already available with its
Whitehead correction provenance.

Toda Equation (5.8):
[ι₄,ι₄]=±(2ν₄-Eν′).

Both derived up-to-sign statements
use the same positive representative:

2ν₄-Eν′.

Therefore:

Δ(ι₉)=±[ι₄,ι₄].

Hence:

Δ(ι₉)
=
±(2ν₄-Eν′)
=
±[ι₄,ι₄].
```

この表示は current Phase 66 representative probe の hand-authored presentation layer である。

---

## 4.6 Machine provenance

最終 provenance graph の主要 branch:

```text
Phase 65
π_7^4=Z{ν₄}⊕Z/4{Eν′}
        │
        ↓
Phase 66-3
Δ(ι₉)=±(2ν₄-Eν′)
        │
        ├─────────────────────┐
        │                     │
Phase 60                      │
Whitehead correction data     │
[ι₄,ι₄]                       │
        │                     │
        ↓                     │
Phase 66-4                    │
[ι₄,ι₄]=±(2ν₄-Eν′)           │
        │                     │
        └──────────┬──────────┘
                   ↓
Phase 66-5
Δ(ι₉)=±[ι₄,ι₄]
        │
        │
Phase 66-3 + 66-4 + 66-5
        ↓
Phase 66-7
Toda58EquationStatement
```

Phase 66-6 regression で確認する provenance invariants:

```text
final → Phase 66-3
final → Phase 66-4

Phase 66-3 → Phase 65 π_7^4
Phase 66-4 → Phase 60 Whitehead data

graph is acyclic
final conclusion is absent from ancestors
upstream branches do not depend on final
```

---

## 4.7 Literature

Phase 66-7 aggregate に保持する literature metadata:

```text
Author:
  H. Toda

Title:
  Composition Methods in Homotopy Groups of Spheres

Year:
  1962

Label:
  Toda (5.8)

Locator:
  Equation (5.8)

Statement:
  Δ(ι₉)=±(2ν₄-Eν′)=±[ι₄,ι₄].
```

文献情報は `LiteratureStatement` / `LiteratureReference` を用いて保持する。

literature metadata は generic inference engine に theorem knowledge を追加するものではない。

---

## 4.8 GIVEN / INFERENCE boundary

Phase 66 の Equation (5.8) spine:

```text
Phase 66-3
Δ(ι₉)=±(2ν₄-Eν′)
INFERENCE

Phase 66-4
[ι₄,ι₄]=±(2ν₄-Eν′)
INFERENCE

Phase 66-5
Δ(ι₉)=±[ι₄,ι₄]
INFERENCE

Phase 66-7
Toda58EquationStatement
INFERENCE
```

禁止する shortcut:

```text
Phase 65 π_7^4 を GIVEN に差し替える
→ Phase 66-3 reject

Phase 66-3 result を GIVEN に差し替える
→ Phase 66-4 / Phase 66-5 / aggregate path で reject

Phase 60 Whitehead correction data を GIVEN に差し替える
→ Phase 66-4 reject

Phase 66-4 result を GIVEN に差し替える
→ Phase 66-5 / aggregate path で reject

Phase 66-5 result を GIVEN に差し替える
→ Phase 66-7 aggregate reject
```

Equation (5.8) の最終 theorem aggregate を `GIVEN` として投入しない。

---

## 4.9 Representation boundary

Phase 66 で追加しないもの:

```text
generic PlusMinus expression
generic sign variable
generic sign solver
generic equality modulo sign
generic up-to-sign transitivity
generic subtraction node
generic Whitehead-square theorem
generic Delta/Whitehead bridge
generic theorem aggregate framework
generic literature registry
```

`2ν₄-Eν′` は既存 AST:

```text
Sum(
  left=Multiple(
    coefficient=2,
    expression=ν₄,
  ),
  right=Multiple(
    coefficient=-1,
    expression=Eν′,
  ),
)
```

で保持する。

`Δ(ι₉)=±x` は既存:

```text
TodaDeltaImageUpToSignStatement
```

で保持する。

`[ι₄,ι₄]=±x` は Equation (5.8) 専用:

```text
Toda58WhiteheadSquareUpToSignStatement
```

で保持する。

generic ± algebra は導入しない。

---

## 4.10 Object provenance boundary

Phase 66 の bridge / aggregate は可能な限り upstream conclusion object を再利用する。

```text
ν₄
→ upstream Phase 65 / Phase 60 provenance を維持

Eν′
→ Phase 66-3 の直接 π_7^4 premise 内 generator を利用

[ι₄,ι₄]
→ Phase 60 Whitehead correction object を再利用

Δ map
→ Phase 66-3 object を Phase 66-5 まで再利用

ι₉
→ Phase 66-3 object を Phase 66-5 まで再利用

Toda58EquationStatement fields
→ Phase 66-3 / 66-4 / 66-5 conclusion object をそのまま保持
```

structural equality と Python object identity は区別する。

---

## 4.11 Representative probe

実行:

```powershell
python -m probes.probe_phase66_capabilities
```

表示項目:

```text
Toda Equation (5.8) result

Proof-style derivation

Provenance / integration

Literature statements used

Proof record

Phase 66 completion boundary
```

代表 result:

```text
Δ(ι₉)
=
±(2ν₄-Eν′)
=
±[ι₄,ι₄]
```

probe 内の proof-style derivation は presentation-only であり、automatic proof narrative generation ではない。

---

## 4.12 Regression status

Phase 66 completion 時点:

```text
Phase 66-2 focused       12 passed
Phase 66-3 focused       19 passed
Phase 66-4 focused       18 passed
Phase 66-5 focused       22 passed
Phase 66-6 focused       20 passed
Phase 66-7 focused       21 passed
Phase 66-8 focused       17 passed

Phase 66 focused total:
129 passed

repository-wide:
3970 passed in 31.96s
```

Phase 66-7 / 66-8 の focused tests と final repository-wide regression まで確認済み。

---

# 5. Automatic proof narrative generation との関係

現在:

```text
ProofStep graph
+
Expression structure
+
InferenceRule provenance
+
LiteratureStatement
+
hand-authored representative probe
+
human-reviewed proof_records.md
```

将来:

```text
ProofStep graph
        ↓
dependency path selection
        ↓
proof-chain compression / grouping
        ↓
equation-chain generation
        ↓
literature citation insertion
        ↓
rule-specific narrative templates
        ↓
console / Markdown / LaTeX
```

`docs/proof_records.md` に蓄積した representative proofs は、将来の generator が満たすべき display / narrative expectation を観察するための corpus とする。

ただし Phase 66 では automatic generator を実装しない。

---

# 6. Persistent Proof Repository との境界

`docs/proof_records.md` は persistent proof repository ではない。

現在の `ProofStep` provenance は基本的に in-memory であり、別 process では通常 builder / inference を再実行する。

```text
@lru_cache(maxsize=1)
```

は同一 Python process 内の deterministic object graph reuse のために使う。

将来の persistent repository では別途:

```text
proof result identity
statement schema
dependency edge
literature metadata
version / derivation compatibility
serialization
query
replay / validation
```

を設計する必要がある。

Proof record documentation はその repository schema を先取りしない。

---

# 7. Current proof-record boundary

正式な human-reviewed proof record は現在3件。

```text
Phase 66
Toda Equation (5.8)

Δ(ι₉)
=
±(2ν₄-Eν′)
=
±[ι₄,ι₄]


Phase 67
Toda Lemma 5.7

E²α∈2ι₅∘π_(i+2)(S⁵)
→
E(η₂∘α)=0

特に:
E(η₂∘ν′)=0
Δ(ν₅)=±(η₂∘ν′)


Phase 68
Toda Proposition 5.8
finite-dimensional result

π_6^2=Z/4{η₂ν′}
π_7^3=Z/2{ν′η₆}
π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}
π_9^5=Z/2{ν₅η₈}
π_(n+4)^n=0, n≥6
```

過去 Phase 60–65 の全面 backfill は行わない。

必要になった時点で separate documentation task として追加する。
---

# 8. Phase 66 completion record

Phase 66 は COMPLETE。

verified representative result:

```text
Δ(ι₉)
=
±(2ν₄-Eν′)
=
±[ι₄,ι₄]
```

theorem spine:

```text
Phase 66-3  INFERENCE
Phase 66-4  INFERENCE
Phase 66-5  INFERENCE
Phase 66-7  INFERENCE
```

final aggregate:

```text
Toda58EquationStatement
not GIVEN
```

representative probe:

```powershell
python -m probes.probe_phase66_capabilities
```

focused Phase 66 regression:

```text
129 passed
```

repository-wide regression:

```text
3970 passed in 31.96s
```

この record は Phase 66 completion 時点の human-reviewed golden reference とする。

---

# 9. Toda Lemma 5.7

## 9.1 Source / theorem

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Lemma 5.7
```

対象 statement:

```text
α∈π_i(S³)

E²α ∈ 2ι₅∘π_(i+2)(S⁵)
        ↓
E(η₂∘α)=0
```

特に:

```text
E(η₂∘ν′)=0

Δ(ν₅)=±(η₂∘ν′)
```

---

## 9.2 Result

Phase 67 では Toda Lemma 5.7 を次の concrete capability に分解して導出した。

```text
general:
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
→
E(η₂∘α)=0

special:
E²ν′ ∈ 2ι₅∘π_8(S⁵)

E(η₂∘ν′)=0

π_6^2=Z/4{η₂∘ν′}

Δ(ν₅)=±(η₂∘ν′)
```

最終 special conclusion:

```text
Δ(ν₅)=±(η₂∘ν′)
```

は:

```text
TodaDeltaImageUpToSignStatement
```

として保持する。

---

## 9.3 Hypothesis representation

Lemma 5.7 の hypothesis:

```text
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
```

は Phase 67 専用:

```text
TodaLemma57TwoIota5ImageMembershipStatement
```

で保持する。

field:

```text
element
source_group
```

generic:

```text
ImageMembership
existential witness
map image object
composition image algebra
```

は導入しない。

general theorem test では hypothesis を `GIVEN` として投入できる。

ν′ specialization では同じ statement を upstream result から `INFERENCE` として導出し、general Lemma 5.7 rule を再利用する。

---

## 9.4 General proof branch

Phase 67-3:

```text
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
        ↓
E²(η₂∘α)=η₄∘E²α
```

Phase 55 / Proposition 5.1 consequence:

```text
2η₄=0
```

hypothesis と合わせて:

```text
E²(η₂∘α)=0
```

Phase 67-4:

```text
E²(η₂∘α)=0
        ↓
Toda Lemma 4.5, n=3
        ↓
E(η₂∘α)=0
```

Lemma 4.5 は generic all-n zero-reflection rule にはせず、今回必要な n=3 branch のみを実装した。

---

## 9.5 ν′ specialization

Phase 60 Toda Lemma 5.4:

```text
2Eν₄=E²ν′
```

ν-family definition:

```text
ν₅=Eν₄
```

したがって:

```text
E²ν′
=
2ν₅
∈
2ι₅∘π_8(S⁵)
```

Phase 67-5 ではこれを:

```text
TodaLemma57TwoIota5ImageMembershipStatement
ProofRule.INFERENCE
```

として導出する。

general Lemma 5.7 branch を再利用して:

```text
E(η₂∘ν′)=0
```

を得る。

ν′ 用に general proof を複製しない。

---

## 9.6 π_6^2 calculation

Phase 56 Toda (5.2):

```text
η₂∘- : π_i^3 ≅ π_i^2
```

Phase 65 Toda Proposition 5.6:

```text
π_6^3=Z/4{ν′}
```

concrete transport:

```text
π_6^2
=
Z/4{η₂∘ν′}
```

結果は `ProofRule.INFERENCE`。

generic finite-cyclic generator transport framework は追加しない。

---

## 9.7 Delta consequence

Toda (4.4) の concrete exact segment:

```text
π_8^5 ─Δ→ π_6^2 ─E→ π_7^3
```

Phase 67-5:

```text
E(η₂∘ν′)=0
```

Phase 67-6:

```text
π_6^2=Z/4{η₂∘ν′}
```

したがって generator の像が zero なので、この concrete cyclic group 上で E は zero。

exactness より:

```text
Im Δ
=
Ker E
=
π_6^2
```

したがって:

```text
Δ:π_8^5→π_6^2
```

は surjective。

Phase 65:

```text
π_8^5=Z/8{ν₅}
```

なので:

```text
π_6^2
=
<Δ(ν₅)>
```

一方:

```text
π_6^2
=
Z/4{η₂∘ν′}
```

だから Toda の sign convention で:

```text
Δ(ν₅)=±(η₂∘ν′)
```

を得る。

---

## 9.8 Proof-style derivation

Representative human-readable derivation:

```text
Assume

E²α ∈ 2ι₅∘π_(i+2)(S⁵).

Then

E²(η₂∘α)
=
η₄∘E²α.

Since 2η₄=0,

E²(η₂∘α)=0.

Toda Lemma 4.5, n=3 gives

E(η₂∘α)=0.


Now take α=ν′.

Toda Lemma 5.4 gives

2Eν₄=E²ν′.

Since ν₅=Eν₄,

E²ν′ ∈ 2ι₅∘π_8(S⁵).

Hence

E(η₂∘ν′)=0.


Toda (5.2) and Proposition 5.6 give

π_6^2
=
Z/4{η₂∘ν′}.

Using exactness of

π_8^5 ─Δ→ π_6^2 ─E→ π_7^3,

and E(η₂∘ν′)=0,

Δ is surjective.

Proposition 5.6 gives

π_8^5=Z/8{ν₅}.

Therefore

π_6^2=<Δ(ν₅)>.

Since

π_6^2=Z/4{η₂∘ν′},

we obtain

Δ(ν₅)=±(η₂∘ν′).
```

この proof-style derivation は hand-authored presentation layer である。

---

## 9.9 Machine provenance

主要 branch:

```text
Phase 60
Toda Lemma 5.4
2Eν₄=E²ν′
        │
        ↓
Phase 67-5
E²ν′ ∈ 2ι₅∘π_8(S⁵)
        │
        ↓
Phase 67-3 / 67-4
E(η₂∘ν′)=0
        │
        ├───────────────────────┐
        │                       │
Phase 56                       │
Toda (5.2)                     │
        │                       │
        + Phase 65             │
          Prop.5.6             │
        │                       │
        ↓                       │
Phase 67-6                     │
π_6^2=Z/4{η₂∘ν′}              │
        │                       │
        └──────────┬────────────┘
                   │
Toda (4.4)         │
exactness          │
                   ↓
Phase 67-7
Δ surjective
        │
        + Phase 65
          π_8^5=Z/8{ν₅}
        │
        ↓
Δ(ν₅)=±(η₂∘ν′)
```

Phase 67-8 regression で:

```text
final reaches ν′ hypothesis branch
final reaches E(η₂ν′)=0 branch
final reaches π_6^2 branch
final reaches exactness branch
final reaches Δ-surjectivity branch
final reaches Proposition 5.6

graph is acyclic
final is not its own ancestor
final conclusion absent from ancestors
upstream branches do not depend on final
```

を確認する。

---

## 9.10 Phase 66 independence

Toda source ordering では Lemma 5.7 は Equation (5.8) の後に現れる。

しかし machine proof dependency は:

```text
Phase 56
Phase 60
Phase 65
Toda (4.4)
Phase 67 internal branches
```

で完結する。

Phase 66:

```text
Toda58EquationStatement
```

は final ancestor graph に存在しない。

したがって:

```text
source ordering
!=
machine proof dependency
```

を維持している。

---

## 9.11 GIVEN / INFERENCE boundary

GIVEN:

```text
general symbolic Lemma 5.7 hypothesis
  when testing the general theorem

Toda (4.4) structural exactness window
```

INFERENCE:

```text
2η₄=0

E²(η₂∘α)=η₄∘E²α

E²(η₂∘α)=0

E(η₂∘α)=0

E²ν′ image hypothesis

E(η₂∘ν′)=0

π_6^2=Z/4{η₂∘ν′}

Toda (4.4) exactness statement

Δ surjective

π_8^5=Z/8{ν₅}
through Proposition 5.6

Δ(ν₅)=±(η₂∘ν′)
```

最終 theorem consequence を `GIVEN` として再投入しない。

---

## 9.12 Representation boundary

Phase 67 で追加しないもの:

```text
generic ImageMembership
generic existential witness
generic image algebra
generic suspension-composition normalizer
generic Lemma 4.5 all-n reflection
generic finite-cyclic generator transport
generic cyclic-image solver
generic sign solver
generic ± algebra
generic exactness solver
automatic proof narrative generation
persistent Proof Repository
```

必要な concrete theorem semantics のみ実装する。

---

## 9.13 Representative probe

実行:

```powershell
python -m probes.probe_phase67_capabilities
```

表示:

```text
Toda Lemma 5.7 result

Proof-style derivation

Provenance / integration

Literature / source

Proof record

Phase 67 completion boundary
```

representative result:

```text
E²α ∈ 2ι₅∘π_(i+2)(S⁵)
⇒
E(η₂∘α)=0

In particular:

E(η₂∘ν′)=0

Δ(ν₅)=±(η₂∘ν′)
```

probe の derivation は presentation-only。

automatic proof narrative generation ではない。

---

## 9.14 Regression status

Phase 67 completion:

```text
Phase 67-5 focused      17 passed
Phase 67-6 focused      17 passed
Phase 67-7 focused      19 passed
Phase 67-8 focused      19 passed
Phase 67-9 probe        21 passed

repository-wide:
4102 passed in 32.75s
```

代表 provenance output:

```text
E²ν′ image hypothesis derived = True
E(η₂∘ν′)=0 derived = True
π_6^2=Z/4{η₂∘ν′} derived = True
Toda (4.4) exactness derived = True
Δ surjective derived = True
Toda Proposition 5.6 aggregate derived = True
Δ(ν₅)=±(η₂∘ν′) derived = True
final result is GIVEN = False
all final premises are INFERENCE = True
Toda (4.4) structural window remains GIVEN = True
Phase 66 dependency used = False
fixed point = True
```

この record は Phase 67 completion 時点の human-reviewed golden reference とする。
---

# 10. Toda Proposition 5.8

## 10.1 Source / theorem

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 5.8
```

Phase 68 で正式記録するのは finite-dimensional part:

```text
π_6^2=Z/4{η₂ν′}
π_7^3=Z/2{ν′η₆}
π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}
π_9^5=Z/2{ν₅η₈}
π_(n+4)^n=0
(n≥6)
```

stable statement:

```text
(G_4;2)=0
```

はこの record には含めない。

---

## 10.2 Result

Phase 68 final aggregate:

```text
TodaProp58FiniteDimensionalStatement
```

保持する5 branch:

```text
π_6^2 = Z/4{η₂ν′}

π_7^3 = Z/2{ν′η₆}

π_8^4
=
Z/2{ν₄η₇}
⊕
Z/2{Eν′η₇}

π_9^5 = Z/2{ν₅η₈}

π_(n+4)^n = 0
(n≥6)
```

aggregate 自身は:

```text
ProofRule.INFERENCE
```

である。

---

## 10.3 Upstream results

主要 upstream:

```text
Phase 46
Toda (4.5)
stable-range finite-dimensional suspension isomorphism

Phase 60
Toda Lemma 5.4
ν₄∈π_7^4
H(ν₄)=ι₇
2Eν₄=E²ν′

Phase 62
ν-family
2ν_n=E^(n-3)ν′

Phase 63
Toda (5.6)
π_(i-1)^3⊕π_i^7≅π_i^4

Phase 65
Toda Proposition 5.6
Equation (5.7)
π_7^4=Z{ν₄}⊕Z/4{Eν′}
π_8^5=Z/8{ν₅}

Phase 66
Toda (5.8)
Δ(ι₉)=±(2ν₄-Eν′)

Phase 67
Toda Lemma 5.7
E(η₂ν′)=0
π_6^2=Z/4{η₂ν′}
```

---

## 10.4 π_7^3 derivation

Phase 67:

```text
π_6^2=Z/4{η₂ν′}
E(η₂ν′)=0
```

concrete exactness:

```text
π_6^2 --E--> π_7^3 --H--> π_7^5
```

より:

```text
H injective.
```

Phase 65 Equation (5.7):

```text
H(ν′η₆)=η₅²
```

Proposition 5.3:

```text
π_7^5=Z/2{η₅²}
```

したがって:

```text
H surjective.
```

よって:

```text
H:π_7^3→π_7^5
isomorphism
```

であり:

```text
π_7^3=Z/2{ν′η₆}.
```

---

## 10.5 π_8^4 derivation

Toda (5.6), `i=8`:

```text
π_7^3⊕π_8^7≅π_8^4
(α,β)↦Eα+ν₄β
```

Phase 68:

```text
π_7^3=Z/2{ν′η₆}
```

Proposition 5.1:

```text
π_8^7=Z/2{η₇}
```

concrete suspension bridge:

```text
E(ν′η₆)=Eν′η₇
```

したがって:

```text
π_8^4
=
Z/2{ν₄η₇}
⊕
Z/2{Eν′η₇}.
```

---

## 10.6 Δ(η₉) derivation

Phase 66:

```text
Δ(ι₉)=±(2ν₄-Eν′)
```

Toda Proposition 2.5 の concrete composition consequence:

```text
Δ(η₉)
=
±((2ν₄-Eν′)η₇).
```

Phase 68 の `π_8^4` decomposition から両 direct summand は order two。

したがって:

```text
2ν₄η₇=0
```

かつ `Eν′η₇` の sign は irrelevant。

よって:

```text
Δ(η₉)=Eν′η₇.
```

---

## 10.7 π_9^5 derivation

Phase 66:

```text
Δ(ι₉)=±(2ν₄-Eν′)
```

Phase 65:

```text
π_7^4
=
Z{ν₄}
⊕
Z/4{Eν′}
```

positive representative は free component に `2ν₄` を持つので:

```text
Δ:π_9^9→π_7^4
```

は injective。

exactness:

```text
π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

から:

```text
H=0.
```

さらに exactness:

```text
π_8^4 --E--> π_9^5 --H--> π_9^9
```

から:

```text
E:π_8^4→π_9^5
```

は surjective。

Phase 68:

```text
Δ(η₉)=Eν′η₇
```

により:

```text
ker(E)
=
Z/2{Eν′η₇}.
```

したがって `π_8^4` の第一 summand が quotient に残り:

```text
π_9^5
=
Z/2{E(ν₄η₇)}.
```

concrete suspension bridge:

```text
E(ν₄η₇)=ν₅η₈
```

より:

```text
π_9^5=Z/2{ν₅η₈}.
```

---

## 10.8 Toda (5.9)

Phase 60:

```text
H(ν₄)=ι₇
```

から Phase 68 concrete Hopf bridge:

```text
H(η₃ν₄)=η₅².
```

Phase 65:

```text
H(ν′η₆)=η₅².
```

Phase 68 で既に:

```text
H:π_7^3→π_7^5
```

は injective / isomorphism。

したがって:

```text
η₃ν₄=ν′η₆.
```

これが Toda (5.9)。

machine proof は source proof の追加 order argument を必要とせず、独立導出済み Hopf isomorphism を再利用する。

---

## 10.9 η_nν_(n+1)=0

Toda (5.9):

```text
η₃ν₄=ν′η₆
```

を double suspension:

```text
η₅ν₆=E²ν′η₈.
```

Phase 62 / ν-family:

```text
2ν₅=E²ν′.
```

Phase 68:

```text
π_9^5=Z/2{ν₅η₈}.
```

したがって:

```text
η₅ν₆
=
2ν₅η₈
=
0.
```

suspension transport:

```text
η_nν_(n+1)=0
(n≥5).
```

---

## 10.10 ν_nη_(n+3)=0

まず `n=6` specialization:

```text
η₆ν₇=0.
```

Toda Proposition 3.1 の Barratt-Hilton formulas を:

```text
α=η₂
β=ν₄
p=2
q=4
k=1
h=3
```

へ specialize すると raw structural formulas は:

```text
η₂∧ν₄=-η₆ν₇

η₂∧ν₄=+ν₆η₉.
```

したがって `η₆ν₇=0` から sign に依存せず:

```text
ν₆η₉=0.
```

ここでは generic sign normalizer を追加しない。

family transport により:

```text
ν_nη_(n+3)=0
(n≥6).
```

---

## 10.11 π_10^6=0 と higher transport

concrete exact sequence:

```text
π_9^5 --E--> π_10^6 --H--> π_10^11
```

foundation:

```text
π_10^11=0.
```

したがって:

```text
E:π_9^5→π_10^6
```

は surjective。

Phase 68:

```text
π_9^5=Z/2{ν₅η₈}.
```

その suspended generator は:

```text
ν₆η₉.
```

しかし既に:

```text
ν₆η₉=0.
```

したがって:

```text
π_10^6=0.
```

Toda (4.5):

```text
E^(n-6):
π_10^6
≅
π_(n+4)^n
```

for `n≥6`。

よって:

```text
π_(n+4)^n=0
(n≥6).
```

---

## 10.12 Proof-style derivation

Representative human-readable derivation:

```text
[1] π_6^2

Phase 67:
E(η₂ν′)=0
Δ(ν₅)=±η₂ν′
↓
π_6^2=Z/4{η₂ν′}


[2] π_7^3

Eπ_6^2=0
↓
H:π_7^3→π_7^5 injective

H(ν′η₆)=η₅²
π_7^5=Z/2{η₅²}
↓
H surjective
↓
H isomorphism
↓
π_7^3=Z/2{ν′η₆}


[3] π_8^4

Toda (5.6), i=8:
π_7^3⊕π_8^7≅π_8^4

π_7^3=Z/2{ν′η₆}
π_8^7=Z/2{η₇}
E(ν′η₆)=Eν′η₇
↓
π_8^4
=
Z/2{ν₄η₇}
⊕
Z/2{Eν′η₇}


[4] π_9^5

Toda (5.8):
Δ(ι₉)=±(2ν₄-Eν′)
↓
Δ:π_9^9→π_7^4 injective
↓
H:π_9^5→π_9^9 zero
↓
E:π_8^4→π_9^5 surjective

Δ(η₉)=Eν′η₇
↓
ker(E)=Z/2{Eν′η₇}

π_8^4
=
Z/2{ν₄η₇}
⊕
Z/2{Eν′η₇}
↓
π_9^5=Z/2{E(ν₄η₇)}

E(ν₄η₇)=ν₅η₈
↓
π_9^5=Z/2{ν₅η₈}


[5] π_(n+4)^n

Toda (5.9):
η₃ν₄=ν′η₆
↓ E²
η₅ν₆=E²ν′η₈

2ν₅=E²ν′
π_9^5=Z/2{ν₅η₈}
↓
η₅ν₆=0
↓
η_nν_(n+1)=0
(n≥5)

n=6:
η₆ν₇=0

Toda Proposition 3.1:
η₂∧ν₄ represents
-η₆ν₇
and
+ν₆η₉
↓
ν₆η₉=0
↓
ν_nη_(n+3)=0
(n≥6)

π_9^5=Z/2{ν₅η₈}
E:π_9^5→π_10^6 surjective
ν₆η₉=0
↓
π_10^6=0

Toda (4.5):
E^(n-6):π_10^6≅π_(n+4)^n
↓
π_(n+4)^n=0
(n≥6)
```

この表示は Phase 68 probe の hand-authored presentation layer を human-reviewed record として固定したもの。

automatic proof narrative generation ではない。

---

## 10.13 Machine provenance

主要 spine:

```text
Phase 67
π_6^2=Z/4{η₂ν′}
        │
        ↓
Phase 68-3
π_7^3=Z/2{ν′η₆}
        │
        ↓
Phase 68-4
π_8^4
        │
        ├─────────────────────┐
        │                     │
Phase 66                     │
Toda (5.8)                   │
        │                     │
        ↓                     │
Phase 68-5                   │
Δ(η₉)=Eν′η₇                 │
        │                     │
        └──────────┬──────────┘
                   ↓
Phase 68-6
π_9^5=Z/2{ν₅η₈}
        │
        │
Phase 68-7
Toda (5.9)
        │
        ↓
Phase 68-8
η_nν_(n+1)=0
        │
        ↓
Phase 68-9
ν_nη_(n+3)=0
        │
        ↓
Phase 68-10
π_(n+4)^n=0
        │
        └───────────────────┐

π_6^2
π_7^3
π_8^4
π_9^5
π_(n+4)^n=0
n≥6
        │
        ↓
Phase 68-11
TodaProp58FiniteDimensionalStatement
```

Phase 68-12 regression で:

```text
final reaches all five mathematical branches
branches do not depend on final
final is not its own ancestor
final conclusion absent from ancestors
```

を確認する。

---

## 10.14 Source-order / dependency boundary

Phase 66 Toda (5.8) は:

```text
π_7^3 branch
π_8^4 branch
```

の ancestor ではない。

一方:

```text
π_9^5
higher zero branch
```

では必要な downstream dependency として存在する。

また Toda (5.9):

```text
η₃ν₄=ν′η₆
```

は `π_7^3` を利用して derived されるが、`π_7^3` の ancestor には戻らない。

したがって:

```text
source ordering
!=
machine proof dependency
```

を Phase 68 でも維持する。

---

## 10.15 GIVEN / INFERENCE boundary

GIVEN:

```text
structural exactness windows
foundational zero groups where required
n≥6 applicability
family / structural definitions where they are theorem hypotheses
```

aggregate direct scope:

```text
n≥6
GIVEN
```

INFERENCE:

```text
π_6^2=Z/4{η₂ν′}

π_7^3=Z/2{ν′η₆}

π_8^4
=
Z/2{ν₄η₇}
⊕
Z/2{Eν′η₇}

Δ(η₉)=Eν′η₇

π_9^5=Z/2{ν₅η₈}

η₃ν₄=ν′η₆

η_nν_(n+1)=0

ν_nη_(n+3)=0

π_10^6=0

π_(n+4)^n=0

TodaProp58FiniteDimensionalStatement
```

final aggregate を `GIVEN` として投入しない。

---

## 10.16 Representation boundary

Phase 68 では generic framework を増やさず concrete theorem need を局所処理した。

追加しない:

```text
generic shifted-family constructor
generic ScalarExpression family index support
generic η-name normalization
generic sign variable / sign solver
generic smash-product normalization
generic equality modulo sign
generic cyclic-image solver
generic zero-generator group solver
generic zero-group isomorphism transport
generic exactness solver
stable homotopy-group model
```

特に:

```text
η_(n+3)
```

は `ScalarSum(n,3)` を family helper に渡さず theorem-specific local element として保持する。

また:

```text
η₈
η_8
```

の display-name 差は upstream object reuse と structural generator validation で処理する。

---

## 10.17 Literature

Phase 68 aggregate の direct literature:

```text
Author:
  H. Toda

Title:
  Composition Methods in Homotopy Groups of Spheres

Year:
  1962

Label:
  Toda Proposition 5.8

Locator:
  Proposition 5.8

Statement:
  finite-dimensional Proposition 5.8 group calculation
```

proof の内部では既存 provenance を通じて:

```text
Toda (4.5)
Toda (5.6)
Toda (5.8)
Toda (5.9)
Toda Proposition 3.1
Toda Proposition 2.5
```

等へ遡る。

literature metadata は theorem search engine ではない。

---

## 10.18 Representative probe

実行:

```powershell
python -m probes.probe_phase68_capabilities
```

表示:

```text
Toda Proposition 5.8 finite-dimensional result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 68 representative probe boundary
```

representative result:

```text
π_6^2 = Z/4{η₂ν′}
π_7^3 = Z/2{ν′η₆}
π_8^4 = Z/2{ν₄η₇} ⊕ Z/2{Eν′η₇}
π_9^5 = Z/2{ν₅η₈}
π_(n+4)^n = 0  (n ≥ 6)
```

probe 自身も:

```text
The proof-style derivation above is hand-authored presentation code.
It is not yet generated automatically from the ProofStep graph.
```

という境界を明示する。

---

## 10.19 Regression status

Phase 68-13 probe:

```text
26 passed in 1.38s
```

Phase 68 aggregate + provenance + probe:

```text
75 passed in 1.53s
```

repository-wide:

```text
4343 passed in 28.06s
```

Phase 64 の performance stabilization 水準を維持している。

---

## 10.20 Completion record

Phase 68 は COMPLETE。

verified finite-dimensional Proposition 5.8 result:

```text
π_6^2=Z/4{η₂ν′}
π_7^3=Z/2{ν′η₆}
π_8^4=Z/2{ν₄η₇}⊕Z/2{Eν′η₇}
π_9^5=Z/2{ν₅η₈}
π_(n+4)^n=0
(n≥6)
```

final aggregate:

```text
TodaProp58FiniteDimensionalStatement
INFERENCE
```

representative probe:

```powershell
python -m probes.probe_phase68_capabilities
```

repository-wide regression:

```text
4343 passed in 28.06s
```

この record は Phase 68 completion 時点の human-reviewed golden reference とする。

stable:

```text
(G_4;2)=0
```

は別 boundary として deferred のまま。

---


# 11. Toda Equation (5.10)

## 11.1 Source / theorem

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Equation (5.10)
```

statement:

```text
Δ(ι₁₁)=ν₅η₈
```

---

## 11.2 Source proof dependency

EHP segment:

```text
π_11^11 --Δ--> π_9^5 --E--> π_10^6
```

Phase 68 で:

```text
π_10^6=0
```

が derived 済み。

したがって:

```text
E:π_9^5→π_10^6=0
↓
ker(E)=π_9^5
↓ exactness
Im(Δ)=π_9^5
↓
Δ:π_11^11→π_9^5 surjective
```

さらに:

```text
π_11^11=Z{ι₁₁}
π_9^5=Z/2{ν₅η₈}
```

より:

```text
Δ(ι₁₁)=ν₅η₈
```

target は order two なので sign ambiguity はない。

---

## 11.3 Machine prerequisite graph

Phase 69-2:

```text
structural exactness window
GIVEN
        │
        ↓
concrete Proposition 4.2 exactness
INFERENCE
        │
        │
Phase 68-10
π_10^6=0
INFERENCE
        │
        ↓
Δ:π_11^11→π_9^5
surjective
INFERENCE
```

Phase 69-3:

```text
Δ surjective
INFERENCE

π_11^11=Z{ι₁₁}
GIVEN

Phase 68-6
π_9^5=Z/2{ν₅η₈}
INFERENCE
        │
        ↓
Δ(ι₁₁)=ν₅η₈
INFERENCE
```

---

## 11.4 Concrete exactness rule

追加:

```text
toda_eq510_concrete_delta_e_exactness_inference_rule()
```

既存 symbolic Proposition 4.2 rule と concrete integer dimension の structural mismatch を global normalizer で解決せず、今回必要な window のみ theorem-specific に認識する。

---

## 11.5 Δ-surjectivity rule

追加:

```text
toda_eq510_delta_surjective_inference_rule()
```

premises:

```text
π_10^6=0               INFERENCE
concrete exactness      INFERENCE
```

conclusion:

```text
TodaDeltaSurjectiveStatement(
  Δ:π_11^11→π_9^5
)
INFERENCE
```

既存 `TodaDeltaSurjectiveStatement` を再利用する。

---

## 11.6 Generator-image rule

追加:

```text
toda_eq510_delta_iota11_inference_rule()
```

premises:

```text
Δ surjective              INFERENCE
π_11^11=Z{ι₁₁}           GIVEN
π_9^5=Z/2{ν₅η₈}          INFERENCE
```

conclusion:

```text
Δ(ι₁₁)=ν₅η₈
INFERENCE
```

Phase 68 `π_9^5` branch の generator object を直接再利用する。

---

## 11.7 Why equality, not ±

```text
π_9^5=Z/2{ν₅η₈}
```

より:

```text
ν₅η₈=-(ν₅η₈)
```

したがって surjective な Δ による source generator の像は target の唯一の非零元そのものであり:

```text
Δ(ι₁₁)=ν₅η₈
```

を通常の equality として保持できる。

---

## 11.8 GIVEN / INFERENCE boundary

GIVEN:

```text
π_11^11=Z{ι₁₁}
structural exactness window
```

INFERENCE:

```text
π_10^6=0
π_9^5=Z/2{ν₅η₈}
concrete exactness
Δ surjective
Δ(ι₁₁)=ν₅η₈
```

Phase 68 Proposition 5.8 aggregate は prerequisite にしない。

---

## 11.9 Provenance / non-circularity

final direct premises:

```text
Δ surjective
π_11^11=Z{ι₁₁}
π_9^5=Z/2{ν₅η₈}
```

ancestor graph は:

```text
final
→ Phase 69-2 Δ surjective
→ Phase 68-10 π_10^6=0

final
→ Phase 69-2 concrete exactness
→ structural exactness window

final
→ Phase 68-6 π_9^5

final
→ π_11^11 foundational fact
```

Phase 69 regression で:

```text
final is INFERENCE
final not GIVEN
final is not its own ancestor
final conclusion absent from ancestors
Δ-surjectivity does not depend on final
π_9^5 branch does not depend on final
Phase 68 aggregate not direct premise
Phase 68 aggregate not ancestor
```

を確認。

---

## 11.10 Representative proof-style derivation

```text
π_10^6=0

π_11^11 ─Δ→ π_9^5 ─E→ π_10^6
is exact

π_10^6=0
↓
E=0
↓
ker(E)=π_9^5
↓
Im(Δ)=π_9^5
↓
Δ surjective

π_11^11=Z{ι₁₁}
π_9^5=Z/2{ν₅η₈}
↓
Δ(ι₁₁) is the unique nonzero target element
↓
Δ(ι₁₁)=ν₅η₈
```

この表示は Phase 69 probe の hand-authored presentation layer を human-reviewed record として固定したもの。

automatic proof narrative generation ではない。

---

## 11.11 Related source equation

Toda Equation (5.11):

```text
Δ(η₉)=Eν′η₇
```

は Phase 68-5 で machine-derived 済み。

Phase 69 では再実装しない。

---

## 11.12 Representative probe

```powershell
python -m probes.probe_phase69_capabilities
```

---

## 11.13 Regression

focused Phase 69:

```text
79 passed in 1.53s
```

probe focused:

```text
22 passed in 1.18s
```

repository-wide:

```text
4422 passed in 30.54s
```

---

## 11.14 Representation boundary

Phase 69 では追加しない:

```text
stable (G_4;2)=0
generic concrete-dimension normalizer
generic exactness solver
generic cyclic-image solver
generic zero-target solver
generic sign / ± algebra
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

---

## 11.15 Completion record

Phase 69 は COMPLETE。

verified result:

```text
Δ(ι₁₁)=ν₅η₈
```

representative probe:

```powershell
python -m probes.probe_phase69_capabilities
```

repository-wide regression:

```text
4422 passed in 30.54s
```

この record は Phase 69 completion 時点の human-reviewed golden reference とする。

---


---

# 12. Toda Proposition 5.9

## 12.1 Source / theorem

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Proposition 5.9
```

Phase 70 で正式記録する finite-dimensional result:

```text
π_7^2=Z/2{η₂ν′η₆}

π_8^3=Z/2{ν′η₆²}

π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}

π_10^5=Z/2{ν₅η₈²}

π_11^6=Z{Δι₁₃}

π_(n+5)^n=0
(n≥7)
```

stable:

```text
(G_5;2)=0
```

はこの record に含めない。

---

## 12.2 Final aggregate

Phase 70 final aggregate:

```text
TodaProp59FiniteDimensionalStatement
```

aggregate 自身は:

```text
ProofRule.INFERENCE
```

である。

direct premises:

```text
π_7^2 relation                INFERENCE
π_8^3 relation                INFERENCE
π_9^4 relation                INFERENCE
π_10^5 relation               INFERENCE
π_11^6 relation               INFERENCE
π_(n+5)^n=0                   INFERENCE
n≥7                           GIVEN
```

---

## 12.3 Upstream results

主要 upstream:

```text
Phase 46
Toda (4.5)

Phase 60
Toda Lemma 5.4
ν₄ / H(ν₄) / 2Eν₄

Phase 62
ν-family

Phase 63
Toda (5.6)

Phase 65
Toda Proposition 5.6

Phase 68
Toda Proposition 5.8 finite-dimensional branches

Phase 69
Δ(ι₁₁)=ν₅η₈
```

Phase 70 aggregate は upstream theorem aggregate の shortcut を増やさず、各 branch が必要とする actual derived conclusion を provenance 付きで再利用する。

---

## 12.4 π_7^2 branch

derived:

```text
π_7^2=Z/2{η₂ν′η₆}.
```

Phase 70-2 result は:

```text
ProofRule.INFERENCE
```

であり final aggregate の direct premise になる。

---

## 12.5 π_8^3 branch

derived:

```text
π_8^3=Z/2{ν′η₆²}.
```

machine graph は Phase 70-2 branch を upstream に保持する。

---

## 12.6 π_9^4 branch

derived:

```text
π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}.
```

Toda (5.6) decomposition semantics と existing ν / η family provenance を再利用する。

generic direct-sum theorem framework は追加しない。

---

## 12.7 Δ(η₉²) supporting result

Phase 70-5 derives:

```text
Δ(η₉²)=Eν′η₇².
```

and:

```text
E:π_9^4→π_10^5
surjective.
```

These are supporting consequences for the `π_10^5` branch.

They are not ancestors of the already-derived `π_9^4` branch.

---

## 12.8 π_10^5 proof-style derivation

```text
π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}

Δ(η₉²)=Eν′η₇²
↓
ker(E)=Z/2{Eν′η₇²}

E:π_9^4→π_10^5
is surjective

E(ν₄η₇²)=ν₅η₈²
↓
π_10^5=Z/2{ν₅η₈²}.
```

The final group relation is derived as `INFERENCE`.

---

## 12.9 E(ν₅η₈²)=0 / Δ(η₁₁)

Phase 70-7 derives two sibling consequences:

```text
E(ν₅η₈²)=0

Δ(η₁₁)=ν₅η₈².
```

The first is required by the `π_11^6` proof.

The second is recorded as a valid Toda consequence, but is not used to derive `π_10^5` or `π_11^6`.

---

## 12.10 π_11^6 proof-style derivation

Phase 70-7 and Phase 70-6 give:

```text
E(ν₅η₈²)=0

π_10^5=Z/2{ν₅η₈²}.
```

Therefore the concrete E-H exactness branch gives:

```text
H:π_11^6→π_11^11
injective.
```

Phase 69 and Phase 68 supply:

```text
π_11^11=Z{ι₁₁}

π_9^5=Z/2{ν₅η₈}

Δ(ι₁₁)=ν₅η₈.
```

Hence:

```text
ker(
  Δ:π_11^11→π_9^5
)
=
Z{2ι₁₁}.
```

The concrete Toda Proposition 2.7 consequence gives:

```text
H(Δι₁₃)=±2ι₁₁.
```

Therefore:

```text
π_11^6=Z{Δι₁₃}.
```

Important non-circular boundary:

```text
π_12^7=0
```

is not used as a prerequisite for this result.

---

## 12.11 Higher five-stem zero proof-style derivation

From:

```text
π_13^13=Z{ι₁₃}

π_11^6=Z{Δι₁₃}
```

we derive:

```text
Δ:π_13^13→π_11^6
surjective.
```

Using exactness:

```text
π_13^13 --Δ--> π_11^6 --E--> π_12^7
```

the suspension map is zero.

Using:

```text
π_11^6 --E--> π_12^7 --H--> π_12^13
```

and:

```text
π_12^13=0,
```

the same suspension map is surjective.

Hence:

```text
π_12^7=0.
```

Toda (4.5):

```text
E^(n-7):
π_12^7
≅
π_(n+5)^n
```

therefore gives:

```text
π_(n+5)^n=0
(n≥7).
```

---

## 12.12 Machine provenance

Phase 70-11 verifies:

```text
aggregate is INFERENCE
aggregate is not GIVEN

all six mathematical branches are INFERENCE
n≥7 remains GIVEN

aggregate direct premise count = 7

aggregate reaches all six branches
aggregate is not its own ancestor
aggregate conclusion is absent from ancestors
branches do not depend on aggregate
```

Principal ordering:

```text
π_7^2
→
π_8^3
→
π_9^4
→
π_10^5
→
π_11^6
→
π_12^7=0
→
π_(n+5)^n=0.
```

---

## 12.13 Backward-dependency boundary

Regression verifies:

```text
Phase 70-5 E-surjectivity
→ π_10^5
but not → π_9^4

Phase 70-5 Δ(η₉²)
→ π_10^5
but not → π_9^4

Phase 70-7 E(ν₅η₈²)=0
→ π_11^6
but not → π_10^5

Phase 70-7 Δ(η₁₁)=ν₅η₈²
not → π_10^5
not → π_11^6

Phase 69 Δ(ι₁₁)=ν₅η₈
→ π_11^6
but not → π_9^4
and not → π_10^5.
```

Thus:

```text
source ordering
!=
machine proof dependency
```

is preserved.

---

## 12.14 GIVEN / INFERENCE boundary

GIVEN:

```text
n≥7 structural applicability
foundational source group facts where required
structural EHP exactness windows where required
```

INFERENCE:

```text
π_7^2 result
π_8^3 result
π_9^4 result
Δ(η₉²)
E-surjectivity for π_10^5
π_10^5 result
E(ν₅η₈²)=0
Δ(η₁₁)=ν₅η₈²
π_11^6 result
π_12^7=0
π_(n+5)^n=0
TodaProp59FiniteDimensionalStatement
```

No final theorem result is reintroduced as a `GIVEN`.

---

## 12.15 Representation boundary

Phase 70 adds only concrete semantics required by Proposition 5.9.

It does not add:

```text
generic concrete-dimension normalizer
generic exactness solver
generic cyclic-image solver
generic zero-target solver
generic zero-map solver
generic zero-group isomorphism transport
generic sign solver
generic ± algebra
generic η-name normalizer
generic theorem specialization engine
stable homotopy-group model
```

The Phase 70-7 compatibility issue:

```text
η_9
η₉
```

is handled by theorem-specific structural validation rather than global renaming.

---

## 12.16 Literature

Phase 70 aggregate holds:

```text
Author:
  H. Toda

Title:
  Composition Methods in Homotopy Groups of Spheres

Year:
  1962

Label:
  Toda Proposition 5.9

Locator:
  Proposition 5.9
```

Literature metadata remains structured metadata rather than theorem-search semantics.

---

## 12.17 Representative probe

Run:

```powershell
python -m probes.probe_phase70_capabilities
```

The probe displays:

```text
Toda Proposition 5.9 finite-dimensional result
Proof-style derivation
Provenance / integration
Literature statements used
Phase 70 representative probe boundary
```

Representative detailed chains include:

```text
π_10^5
π_11^6
higher five-stem zero
```

The proof-style display remains hand-authored presentation code.

It is not yet automatically generated from the `ProofStep` graph.

---

## 12.18 Regression status

probe focused:

```text
29 passed in 1.52s
```

aggregate + provenance + probe:

```text
93 passed in 1.65s
```

repository-wide:

```text
4752 passed in 30.85s
```

Phase 64 performance stabilization remains effective.

---

## 12.19 Completion record

Phase 70 is COMPLETE.

verified finite-dimensional result:

```text
π_7^2=Z/2{η₂ν′η₆}
π_8^3=Z/2{ν′η₆²}
π_9^4=Z/2{ν₄η₇²}⊕Z/2{Eν′η₇²}
π_10^5=Z/2{ν₅η₈²}
π_11^6=Z{Δι₁₃}
π_(n+5)^n=0
(n≥7)
```

representative probe:

```powershell
python -m probes.probe_phase70_capabilities
```

repository-wide regression:

```text
4752 passed in 30.85s
```

This record is the Phase 70 completion human-reviewed golden reference.

stable:

```text
(G_5;2)=0
```

remains deferred.

# 14. Toda Equation (5.12)

## 14.1 Source / theorem

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Equation (5.12)
```

statement:

```text
Δ:
π_(n+7)^(2n+1)
→
π_(n+5)^n

is injective for n=4,5,6.
```

Phase 71 records exactly the three finite concrete cases:

```text
n=4:
Δ:π_11^9→π_9^4 injective

n=5:
Δ:π_12^11→π_10^5 injective

n=6:
Δ:π_13^13→π_11^6 injective
```

---

## 14.2 Machine result

concrete statement:

```text
TodaDeltaInjectiveStatement
```

aggregate:

```text
Toda512DeltaInjectivityStatement
```

aggregate fields:

```text
n4_injectivity
n5_injectivity
n6_injectivity
literature_statements
```

final aggregate rule:

```text
ProofRule.INFERENCE
```

---

## 14.3 n=4 derivation

source:

```text
Toda Proposition 5.3
π_11^9=Z/2{η₉²}
```

Phase 70:

```text
π_9^4
=
Z/2{ν₄η₇²}
⊕
Z/2{Eν′η₇²}
```

and:

```text
Δ(η₉²)=Eν′η₇².
```

Thus the unique nonzero source element maps to a nonzero order-two summand generator:

```text
η₉²
↦
Eν′η₇².
```

Therefore:

```text
ker(
  Δ:π_11^9→π_9^4
)
=
0.
```

Hence:

```text
Δ:π_11^9→π_9^4
```

is injective.

machine direct premises:

```text
Δ(η₉²)=Eν′η₇²                    INFERENCE
π_9^4 decomposition               INFERENCE
Toda Proposition 5.3 aggregate    INFERENCE
```

final branch:

```text
TodaDeltaInjectiveStatement
ProofRule.INFERENCE
```

---

## 14.4 n=5 derivation

source:

```text
Toda Proposition 5.1
π_12^11=Z/2{η₁₁}
```

Phase 70:

```text
π_10^5=Z/2{ν₅η₈²}
```

and:

```text
Δ(η₁₁)=ν₅η₈².
```

Thus the source generator maps to the target generator:

```text
η₁₁
↦
ν₅η₈².
```

Therefore:

```text
ker(
  Δ:π_12^11→π_10^5
)
=
0.
```

Hence:

```text
Δ:π_12^11→π_10^5
```

is injective.

Important provenance note:

```text
π_12^11=Z/2{η₁₁}
```

comes from the Proposition 5.1 higher η-family:

```text
π_(n+1)^n=Z/2{η_n},
```

not from Proposition 5.3.

machine direct premises:

```text
Δ(η₁₁)=ν₅η₈²                    INFERENCE
π_10^5=Z/2{ν₅η₈²}               INFERENCE
Toda Proposition 5.1 aggregate  INFERENCE
```

final branch:

```text
TodaDeltaInjectiveStatement
ProofRule.INFERENCE
```

---

## 14.5 n=6 derivation

source:

```text
π_13^13=Z{ι₁₃}
```

with:

```text
ProofRule.GIVEN.
```

Phase 70 derives:

```text
π_11^6=Z{Δι₁₃}
```

with:

```text
ProofRule.INFERENCE.
```

By definition of the concrete Δ application:

```text
ι₁₃
↦
Δι₁₃.
```

The source is free cyclic on `ι₁₃` and the target is free cyclic on `Δι₁₃`.

Therefore:

```text
Δ(kι₁₃)
=
kΔι₁₃.
```

If:

```text
Δ(kι₁₃)=0,
```

then freeness of the target implies:

```text
k=0.
```

Hence:

```text
Δ:π_13^13→π_11^6
```

is injective.

machine direct premises:

```text
π_13^13=Z{ι₁₃}   GIVEN
π_11^6=Z{Δι₁₃}   INFERENCE
```

The already-known Phase 70 surjectivity of the same map is not used as a premise for this injectivity branch.

---

## 14.6 Three-case integration

Phase 71 integrates:

```text
n=4 injectivity  INFERENCE
n=5 injectivity  INFERENCE
n=6 injectivity  INFERENCE
```

into:

```text
Toda512DeltaInjectivityStatement
```

using:

```text
toda_512_delta_injectivity_integration_inference_rule()
```

The final aggregate has exactly three direct premises.

No upstream group calculation is re-derived inside the integration rule.

---

## 14.7 Provenance graph

representative top-level graph:

```text
n=4 injectivity
INFERENCE
      \
       \
n=5 injectivity
INFERENCE
         \
          → Toda (5.12) aggregate
         /  INFERENCE
        /
n=6 injectivity
INFERENCE
```

n=4 direct provenance:

```text
Δ(η₉²)=Eν′η₇²
π_9^4 decomposition
Prop.5.3 aggregate
↓
n=4 injectivity
```

n=5 direct provenance:

```text
Δ(η₁₁)=ν₅η₈²
π_10^5=Z/2{ν₅η₈²}
Prop.5.1 aggregate
↓
n=5 injectivity
```

n=6 direct provenance:

```text
π_13^13=Z{ι₁₃}  GIVEN
π_11^6=Z{Δι₁₃}  INFERENCE
↓
n=6 injectivity
```

---

## 14.8 Non-circularity

dedicated Phase 71 regression verifies:

```text
aggregate not ancestor of itself
aggregate conclusion absent from ancestors

n=4 branch not ancestor of itself
n=5 branch not ancestor of itself
n=6 branch not ancestor of itself

no branch depends on aggregate
no branch depends on another Phase 71 branch
```

The aggregate reaches all three branches and their intended upstream dependencies.

---

## 14.9 Applicability rejection

focused tests reject inappropriate instances including:

```text
wrong source map
wrong target map
wrong Delta argument
wrong Delta value
wrong group structure
wrong finite order
wrong generator
incorrect GIVEN / INFERENCE substitution
```

The integration rule also rejects any of the three branches when supplied as `GIVEN`.

---

## 14.10 Literature

Phase 71 aggregate holds:

```text
Author:
  H. Toda

Title:
  Composition Methods in Homotopy Groups of Spheres

Year:
  1962

Label:
  Toda (5.12)

Locator:
  Equation (5.12)
```

statement metadata:

```text
The Delta map from pi_(n+7)^(2n+1)
to pi_(n+5)^n
is injective for n=4, 5, 6.
```

Literature metadata remains structured provenance metadata rather than theorem-search semantics.

---

## 14.11 Representative probe

Run:

```powershell
python -m probes.probe_phase71_capabilities
```

The probe displays:

```text
Toda (5.12) Delta injectivity
Proof-style derivation
Provenance / integration
Literature statements used
Phase 71 representative probe boundary
```

It explicitly reports:

```text
n=4 injectivity derived = True
n=5 injectivity derived = True
n=6 injectivity derived = True

all three Toda (5.12) cases are INFERENCE = True
final aggregate derived = True
final aggregate is GIVEN = False
final premise count = 3

n=4 upstream facts are INFERENCE = True
n=5 upstream facts are INFERENCE = True
n=6 π_13^13 remains GIVEN = True
n=6 π_11^6 is INFERENCE = True

final graph acyclic = True
all three branch graphs acyclic = True
```

The proof-style display remains hand-authored presentation code.

It is not yet automatically generated from the `ProofStep` graph.

---

## 14.12 Regression status

Phase 71-2:

```text
19 passed in 1.61s
```

Phase 71-3:

```text
20 passed in 1.49s
```

Phase 71-4:

```text
19 passed in 1.48s
```

Phase 71-5:

```text
19 passed in 1.43s
```

Phase 71-6:

```text
30 passed in 1.42s
```

Phase 71-7:

```text
27 passed in 1.30s
```

final repository-wide:

```text
4886 passed in 29.25s
```

Phase 64 performance stabilization remains effective.

---

## 14.13 Representation boundary

Phase 71 does not add:

```text
Toda Lemma 5.10
generic Toda-bracket coset algebra
generic modulo-subgroup bracket normalization
generic cyclic-map injectivity solver
generic free-cyclic map injectivity solver
generic theorem specialization engine
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

The three injectivity cases are implemented with theorem-specific concrete guards rather than a generic map-property solver.

---

## 14.14 Completion record

Phase 71 is COMPLETE.

verified result:

```text
Toda (5.12)

Δ:
π_(n+7)^(2n+1)
→
π_(n+5)^n

is injective for n=4,5,6.
```

concrete machine results:

```text
Δ:π_11^9→π_9^4 injective
Δ:π_12^11→π_10^5 injective
Δ:π_13^13→π_11^6 injective
```

aggregate:

```text
Toda512DeltaInjectivityStatement
ProofRule.INFERENCE
```

representative probe:

```powershell
python -m probes.probe_phase71_capabilities
```

repository-wide regression:

```text
4886 passed in 29.25s
```

This record is the Phase 71 completion human-reviewed golden reference.

---

---

# 15. Toda Lemma 5.10

## 15.1 Source / theorem

Literature:

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres
1962
Lemma 5.10
```

Source statement:

```text
Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
∈
π₁₁(S⁶)/2π₁₁(S⁶)
```

Canonical machine reading:

```text
Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶)
```

---

## 15.2 Machine result

Final statement:

```text
TodaLemma510BracketModuloStatement
```

concrete fields:

```text
element       = Δ(ι₁₃)
bracket       = {ν₆,η₉,2ι₁₀}
ambient_group = π₁₁(S⁶)
modulus       = 2
```

proof rule:

```text
ProofRule.INFERENCE
```

The theorem conclusion is not inserted as `GIVEN`.

---

## 15.3 Bracket indeterminacy derivation

Toda proof uses (4.7) and (5.9):

```text
Indeterminacy
=ν₆∘π₁₁(S⁹)+π₁₁(S⁶)∘2ι₁₁
=ν₆∘π₁₁⁹+2π₁₁(S⁶)
```

Machine provenance:

```text
Phase 59 / Proposition 5.3
π₁₁⁹=Z/2{η₉²}

Phase 68
ν₆η₉=0

Phase 70
π₁₁⁶=Z{Δι₁₃}
```

therefore:

```text
ν₆∘π₁₁⁹=0
Indeterminacy=<2Δι₁₃>=2π₁₁(S⁶)
```

Machine statement:

```text
Toda54IndeterminacyGeneratorStatement
```

with generator:

```text
2Δ(ι₁₃)
```

This reuses the existing minimum indeterminacy representation rather than introducing generic Toda-bracket coset algebra.

---

## 15.4 Hopf bracket consequence

Toda proof uses (5.10) and Proposition 2.6.

Machine provenance:

```text
Phase 69
Δ(ι₁₁)=ν₅η₈
```

Concrete Phase 72 consequence:

```text
H{ν₆,η₉,2ι₁₀}
contains
2ι₁₁
```

Machine statement:

```text
TodaLemma510HopfBracketContainsStatement
ProofRule.INFERENCE
```

The factor identity in `ν₅η₈` is checked by `GeneratorSymbol` identity rather than requiring reconstructed display objects to be structurally identical.

---

## 15.5 E-H exactness core

Existing Phase 70 result:

```text
H(Δι₁₃)=±2ι₁₁
```

Existing exact sequence:

```text
π₁₀(S⁵)
--E-->
π₁₁(S⁶)
--H-->
π₁₁(S¹¹)
```

Since the bracket contains an element with Hopf value `2ι₁₁` and `Δι₁₃` has the same Hopf value up to sign, exactness gives the concrete Phase 72 core conclusion:

```text
Δι₁₃
∈
{ν₆,η₉,2ι₁₀}
+Eπ₁₀(S⁵)
```

Machine statement:

```text
TodaLemma510BracketPlusSuspensionImageStatement
ProofRule.INFERENCE
```

---

## 15.6 Suspension-image containment

Existing Phase 70 group structures:

```text
π₁₀⁵=Z/2{ν₅η₈²}
π₁₁⁶=Z{Δι₁₃}
```

For the concrete suspension homomorphism from the finite order-two source to the free cyclic target:

```text
Eπ₁₀(S⁵)⊂2π₁₁(S⁶)
```

Machine statement:

```text
TodaLemma510SuspensionImageInDoubleStatement
ProofRule.INFERENCE
```

No generic finite-subgroup solver or image-subgroup algebra is added.

---

## 15.7 Final modulo integration

Direct premises:

```text
1. Δι₁₃∈bracket+Eπ₁₀(S⁵)
2. Indeterminacy=2π₁₁(S⁶)
3. Eπ₁₀(S⁵)⊂2π₁₁(S⁶)
```

Final inference:

```text
Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶)
```

The final `ProofStep` has exactly these three direct premises.

---

## 15.8 Provenance graph

Representative provenance:

```text
Phase 59 Prop.5.3 ───────────────┐
Phase 68 ν₆η₉=0 ────────────────┼→ indeterminacy branch ─┐
Phase 70 π₁₁⁶ ──────────────────┘                        │
                                                        │
Phase 69 Δι₁₁=ν₅η₈ ─→ Hopf bracket consequence ─┐      │
Phase 70 H(Δι₁₃)=±2ι₁₁ ────────────────────────┼→ core ├→ final
Phase 70 E-H exactness ─────────────────────────┘      │
                                                        │
Phase 70 π₁₀⁵ ─────────────────────────────────┐       │
Phase 70 π₁₁⁶ ─────────────────────────────────┴→ image┘
```

Important negative dependency:

```text
Phase 71 n=6
Δ:π₁₃¹³→π₁₁⁶ injective
```

is not an ancestor of the Lemma 5.10 final proof.

This was explicitly fixed after the source proof was reviewed.

---

## 15.9 Non-circularity

Dedicated Phase 72 regression verifies:

```text
final = INFERENCE
final != GIVEN
final has exactly three direct branch premises
final not self-ancestor
final conclusion absent from ancestors
core branch acyclic
indeterminacy branch acyclic
suspension-image branch acyclic
no branch depends on final
Phase 71 n=6 injectivity absent from ancestry
```

---

## 15.10 Applicability rejection

Focused tests reject:

```text
GIVEN core shortcut
GIVEN indeterminacy shortcut
GIVEN image-containment shortcut
wrong bracket
wrong modulus
wrong ambient group
wrong indeterminacy generator
wrong suspension map
wrong Hopf bracket value
wrong E-H exactness window
```

The implementation is theorem-specific and guarded.

---

## 15.11 Representative probe

Run:

```powershell
python -m probes.probe_phase72_capabilities
```

The probe displays:

```text
Toda Lemma 5.10 result
Proof-style derivation
Representative source objects
Provenance / integration
Phase 72 representative probe boundary
```

Representative status:

```text
final modulo statement derived = True
final modulo statement is GIVEN = False
core branch derived = True
indeterminacy branch derived = True
suspension-image branch derived = True
exact three direct premises = True
final graph acyclic = True
Phase 71 Delta injectivity absent from ancestry = True
```

The proof-style display remains hand-authored presentation code and is not yet generated automatically from the `ProofStep` graph.

---

## 15.12 Regression status

Phase 72-2:

```text
10 passed in 2.67s
```

Phase 72-3 revised focused:

```text
19 passed in 4.29s
```

Phase 72-4:

```text
22 passed in 8.29s
```

Phase 72-5:

```text
31 passed in 4.70s
```

Phase 72-6:

```text
22 passed in 4.39s
```

final repository-wide on the home laptop:

```text
4990 passed in 70.11s
```

The project is developed on two PCs, so wall-clock regression time is compared per machine.

---

## 15.13 Representation boundary

Phase 72 does not add:

```text
generic Toda-bracket coset algebra
generic modulo-subgroup bracket normalization
generic quotient normalizer
generic finite-subgroup solver
generic Hopf-of-bracket calculus
generic image-subgroup solver
automatic proof narrative generation
persistent Proof Repository
stable homotopy-group model
```

The concrete Lemma 5.10 need is handled by narrow theorem-specific statement types and inference guards.

---

## 15.14 Completion record

Phase 72 is COMPLETE.

verified result:

```text
Toda Lemma 5.10

Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶)
```

final:

```text
TodaLemma510BracketModuloStatement
ProofRule.INFERENCE
```

representative probe:

```powershell
python -m probes.probe_phase72_capabilities
```

repository-wide regression:

```text
4990 passed in 70.11s
```

This record is the Phase 72 completion human-reviewed golden reference.

---

# 16. Current proof-record status

正式な curated proof record:

```text
1. Phase 66
   Toda Equation (5.8)

2. Phase 67
   Toda Lemma 5.7

3. Phase 68
   Toda Proposition 5.8 finite-dimensional result

4. Phase 69
   Toda Equation (5.10)

5. Phase 70
   Toda Proposition 5.9 finite-dimensional result

6. Phase 71
   Toda Equation (5.12)
   Delta injectivity for n=4,5,6

7. Phase 72R
   Toda Lemma 5.10 corrected canonical record
   Δ(ι₁₃)∈{ν₆,η₉,2ι₁₀} mod 2π₁₁(S⁶)
   (original Phase 72 record retained as historical first implementation)
```

current model:

```text
proof inference        = automatic
proof provenance       = automatic
literature metadata    = structured where implemented
proof-style narrative  = hand-authored representative probe
proof records          = human curated
persistent repository  = not implemented
```

7件の formal record が蓄積した。Phase 72R では theorem source proof の確認により、最初の dependency 仮説を revision し、実際の proof ancestry を regression で固定する運用も記録された。

次の formal record candidate:

```text
Phase 73
Toda Proposition 5.11
```

まず Proposition 5.11 と中間式 Toda (5.13) の dependency / representation compatibility を確認する。

---

# 17. Phase 72R canonical revision of Proof Record 7

The original Phase 72 proof record is retained above as the historical first implementation.

Phase 72R is now the canonical machine/provenance record for Toda Lemma 5.10.

## 17.1 Source / theorem

```text
H. Toda
Composition Methods in Homotopy Groups of Spheres

Toda Lemma 5.10
Toda Proposition 2.6
Toda Equation (1.15)
Toda Equation (2.11)
Toda Lemma 4.3 / (4.6) / (4.7)
Toda Equation (5.10)
```

## 17.2 Result

```text
Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶)
```

canonical representation:

```text
TodaLemma510BracketModuloStatement
ambient_group=HomotopyGroup(11,6)
modulus=2
ProofRule.INFERENCE
```

## 17.3 Ordinary / 2-primary boundary

```text
HomotopyGroup(i,n)
=
ordinary π_i(S^n)

TodaPrimaryGroup(i,n)
=
Toda π_i^n
=
current 2-primary representation
```

They are not structurally identified.

## 17.4 Ordinary EHP branch

Serre (4.2):

```text
π₁₀(S⁵) finite
```

Toda (2.11), `m=5,i=10`:

```text
π₁₀(S⁵)
 --E-->
π₁₁(S⁶)
 --H-->
π₁₁(S¹¹)
```

ordinary exact.

## 17.5 Proposition 2.6 indexed branch

Take:

```text
α=ν₅
β=η₈
γ=2ι₉.
```

Derived hypotheses:

```text
ν₆η₉=0
η₈∘2ι₉=0
Δ(ι₁₁)=ν₅η₈.
```

Therefore:

```text
H{ν₆,η₉,2ι₁₀}_1
contains 2ι₁₁.
```

Toda (1.15), `n=1,m=0`:

```text
{ν₆,η₉,2ι₁₀}_1
⊂
{ν₆,η₉,2ι₁₀}.
```

Hence:

```text
H{ν₆,η₉,2ι₁₀}
contains 2ι₁₁.
```

Phase 70:

```text
H(Δι₁₃)=±2ι₁₁.
```

Thus ordinary exactness gives:

```text
Δι₁₃
∈
{ν₆,η₉,2ι₁₀}
+
Eπ₁₀(S⁵).
```

## 17.6 Corrected indeterminacy

Serre:

```text
π₁₁(S⁹) finite.
```

Because `ν₆` is 2-primary:

```text
ν₆∘π₁₁(S⁹)
=
ν₆∘π₁₁⁹.
```

This is composition-level reduction only.

Using:

```text
π₁₁⁹=Z/2{η₉²}
ν₆η₉=0
```

derive:

```text
ν₆∘π₁₁(S⁹)=0.
```

Therefore:

```text
Indeterminacy
=
2π₁₁(S⁶).
```

## 17.7 Corrected ordinary suspension image

Serre:

```text
π₁₀(S⁵) finite
↓
Eπ₁₀(S⁵) finite.
```

Phase 70:

```text
π₁₀⁵=Z/2{ν₅η₈²}
E(ν₅η₈²)=0
```

therefore the 2-primary part of the ordinary image vanishes.

Since the image is finite:

```text
Eπ₁₀(S⁵)
```

has odd order, so multiplication by 2 is onto:

```text
Eπ₁₀(S⁵)
⊂
2π₁₁(S⁶).
```

## 17.8 Final proof-style derivation

```text
ν₆η₉=0
η₈∘2ι₉=0
Δ(ι₁₁)=ν₅η₈
        ↓
Proposition 2.6
        ↓
H{ν₆,η₉,2ι₁₀}_1 contains 2ι₁₁
        ↓
Toda (1.15)
        ↓
H{ν₆,η₉,2ι₁₀} contains 2ι₁₁

H(Δι₁₃)=±2ι₁₁
ordinary Toda (2.11)
        ↓
Δι₁₃
∈
{ν₆,η₉,2ι₁₀}
+
Eπ₁₀(S⁵)

ν₆∘π₁₁(S⁹)
=
ν₆∘π₁₁⁹
=
0
        ↓
Indeterminacy
=
2π₁₁(S⁶)

π₁₀(S⁵) finite
+
2-primary image zero
        ↓
Eπ₁₀(S⁵)
⊂
2π₁₁(S⁶)

therefore

Δ(ι₁₃)
∈
{ν₆,η₉,2ι₁₀}
mod 2π₁₁(S⁶).
```

## 17.9 Machine provenance

final direct premises:

```text
TodaLemma510OrdinaryBracketPlusSuspensionImageStatement
TodaLemma510OrdinaryIndeterminacyDoubleStatement
TodaLemma510OrdinarySuspensionImageInDoubleStatement
```

reachable corrected ancestry includes:

```text
Toda211OrdinaryEHPExactnessStatement
TodaLemma510IndexedHopfBracketContainsStatement
TodaLemma510Split115Statement
TodaLemma510Nu6OrdinaryCompositionReductionStatement
TodaLemma510Nu6OrdinaryCompositionZeroStatement
TodaLemma510OrdinarySuspensionImageFiniteStatement
TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement
```

## 17.10 Legacy retirement audit

The canonical final does not reuse these specific historical Phase 72 steps:

```text
legacy core step
legacy indeterminacy step
legacy image step
legacy exactness step
```

and does not use the exact Phase 71 `n=6` injectivity statement:

```text
Δ:π₁₃¹³→π₁₁⁶ injective.
```

This is proof-instance / exact-statement retirement, not type-wide prohibition.

## 17.11 Representative probe

```powershell
python -m probes.probe_phase72_capabilities
```

reports the corrected ordinary semantics and retirement audit.

## 17.12 Regression status

```text
Phase 72R focused:
149 passed in 9.34s

repository-wide:
5117 passed in 113.34s
```

## 17.13 Completion status

Phase 72R is COMPLETE.

Proof Record 7 should now be read canonically through this Phase 72R revision.

The earlier Phase 72 record remains a historical record of the first implementation.

