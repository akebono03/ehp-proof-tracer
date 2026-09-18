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

# 3. 過去の代表 probe

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

## 4.1 出典 / 定理

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

## 4.2 結果

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

## 4.3 上流結果

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

## 4.4 導出要素

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

## 4.5 証明形式の導出

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

この表示は 現在の Phase 66 代表 probe の hand-authored presentation layer である。

---

## 4.6 機械的 provenance

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

## 4.8 GIVEN / INFERENCE 境界

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

## 4.9 表現境界

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

## 4.10 オブジェクト provenance 境界

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

## 4.11 代表 probe

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

## 4.12 回帰テスト状況

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

# 5. 自動証明 narrative 生成 との関係

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

# 6. 永続 Proof Repository との境界

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

# 7. 現在の証明記録境界

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

# 8. Phase 66 完了記録

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

代表 probe:

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

