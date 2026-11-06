# Phase 174 R3-R7-R6 監査計画

## 出発点

R3-R7-R5R1 は 94 件の限定 pytest PASS、独立 Hopf 単射性候補 1 件、公開 `ImageZero(E)` 候補 0 件で終了した。`E: π₁₀⁵ → π₁₁⁶` の像の零性は未証明である。

## 一般則

有限巡回群 `G = Z/m{g}`、`m ≥ 2` と群準同型 `E: G → H` について、`E(g) = 0` が証明されれば `im(E) = 0` となる。実装では次の独立 Goal を要求する。

1. `Relation(G, FiniteCyclicGroup(m,g), EQUALITY)`：群構造の証明。
2. `GeneratorImage(E,g,Zero())`：生成元の像が型付き零元であることの証明。

どちらかが未証明なら完成させない。既存データベースの群表示はあくまで Goal 候補である。

## 出典

Toda Chapter V Proposition 5.9 の採用転写に、`π₁₀⁵ = Z/2{ν₅η₈²}`、`E(ν₅η₈²)=ν₆η₉η₁₀=0`、`Eπ₁₀⁵=0` が記される。これらは出典テキストの記述確認であって、新しい GIVEN 登録や検証済み ProofStep を意味しない。

## 変更境界

変更は新規 `phase174_r3_r7_r6_cyclic_generator_zero_image/` のみ。実装・監査・テスト・PowerShell を収める。共有 Proof Search、Web、Renderer、既存の 5 文書は変更しない。

## PASS 条件

Source Guard、過去の R5 実測 JSON の検査、別プロセスに分けた限定 pytest、独立一般則の子 Goal、公開 provider の候補数の記録が成立すること。全体 pytest は Phase 174 の終了時だけ実施する。

次段階では、生成元の懸垂像が零である Goal の具体的な出典付き導出を検討する。本段階では結論を GIVEN にしない。
