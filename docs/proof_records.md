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

Phase 66-6 完了時点:

```text
Phase 66-2 focused       12 passed
Phase 66-3 focused       19 passed
Phase 66-4 focused       18 passed
Phase 66-5 focused       22 passed
Phase 66-6 focused       20 passed

repository-wide:
3932 passed in 34.87s
```

Phase 66-7 / 66-8 の focused tests と final regression は、それぞれの実行後に completion documentation で更新する。

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

Phase 66-8 で正式記録を開始した result:

```text
Toda Equation (5.8)

Δ(ι₉)
=
±(2ν₄-Eν′)
=
±[ι₄,ι₄]
```

次の proof record は、今後の concrete Toda calculation の representative probe 完成時に追加する。

過去 Phase の backfill は必要に応じて別途行う。
