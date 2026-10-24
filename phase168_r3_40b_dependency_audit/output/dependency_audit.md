# Phase 168 R3-40B — 依存関係と表示順序の監査

読み取り専用。新しい命題・引用・表示規則は導入しない。

| 対象 | Steps | 論理依存の逆転 (Projection) | 未解決前提 | 編集上の順序不一致 |
|---|---:|---:|---:|---:|
| pi3_2 | 18 | 0 | 0 | 0 |
| pi4_3 | 25 | 0 | 0 | 0 |
| pi5_4 | 10 | 1 | 0 | 1 |
| pi6_5 | 10 | 0 | 0 | 1 |

## 読み方

- 論理依存の逆転：既存の ProofStep.premises を表示順が逆転したもの。非表示ステップを含む場合は別途確認する。
- 編集上の順序不一致：出典群・Toda 同型・輸送結果・生成元の表示について、検証可能な箇所だけ比較したもの。数学的な誤りと同一視しない。
- Proof Tree の論理依存だけでは、独立な生成元恒等式の自然な文章位置までは決まらない。
- Reference はモデルの citation に従い、推論規則名だけから新たに付与しない。

## pi3_2

- 全ステップ数: 18
- 表示可能なステップ数: 14
- 論理依存逆転: []
- 未解決の前提: []
- 表示順: [0, 1, 2, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17]
- Toda 輸送に関係する順序チェック: []

### 表示可能ステップの概要

- #0: TodaPrimaryGroupZeroStatement — \pi_{i}^{1} = 0
- #1: TodaPrimaryGroupZeroStatement — \pi_{2}^{1} = 0
- #4: MapInjective — 完全性より, $H: \pi_{3}^{2}\to \pi_{3}^{3}$ は単射である.
- #5: Relation — \pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}
- #6: Relation — \pi_{1}^{1} = \mathbb{Z}\{\iota_{1}\}
- #7: Relation — \pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}
- #8: GeneratorSuspension — $E(\iota_{1})=\iota_{2}$.
- #9: TodaSuspensionIsomorphismStatement — $E: \pi_{1}^{1}\to \pi_{2}^{2}$ は同型.
- #11: TodaDeltaZeroStatement — 完全性より, $\operatorname{Im}\Delta=\ker E=0$ なので, $\Delta: \pi_{3}^{3}\to \pi_{1}^{1}$ は零写像である.
- #13: MapSurjective — 完全性より, $H: \pi_{3}^{2}\to \pi_{3}^{3}$ は全射である.
- #14: MapIsomorphism — 単射性と全射性より, $H: \pi_{3}^{2}\to \pi_{3}^{3}$ は同型である.
- #15: Relation — \pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}
- #16: GeneratorImage — $H(\eta_{2})=\iota_{3}$.
- #17: Relation — \pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}

## pi4_3

- 全ステップ数: 25
- 表示可能なステップ数: 12
- 論理依存逆転: []
- 未解決の前提: []
- 表示順: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 21, 20, 22, 23, 24]
- Toda 輸送に関係する順序チェック: []

### 表示可能ステップの概要

- #3: GeneratorSuspension — $E(\eta_{2})=\eta_{3}$.
- #5: Relation — \pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}
- #6: Relation — \pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}
- #7: TodaDeltaImageUpToSignStatement — \Delta\left(\iota_{5}\right) = \pm 2\eta_{2}
- #8: TodaDeltaImageFreeCyclicStatement — これより, $\operatorname{Im}\Delta=\mathbb{Z}\{2\eta_{2}\}$.
- #11: EHPImageEqualsKernelStatement — 完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ.
- #12: SuspensionKernelFreeCyclicStatement — 完全性より, $\ker E=\mathbb{Z}\{2\eta_{2}\}$.
- #16: TodaPrimaryGroupZeroStatement — \pi_{4}^{5} = 0
- #17: MapSurjective — 完全性より, $E: \pi_{3}^{2}\to \pi_{4}^{3}$ は全射である.
- #21: Relation — \pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}
- #20: QuotientIsomorphismStatement — 全射性と核の決定から, 準同型定理より $\pi_{4}^{3}\cong \pi_{3}^{2}/\mathbb{Z}\{2\eta_{2}\}$.
- #24: Relation — \pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}

## pi5_4

- 全ステップ数: 10
- 表示可能なステップ数: 5
- 論理依存逆転: [[3, 4]]
- 未解決の前提: []
- 表示順: [0, 1, 2, 4, 5, 6, 7, 3, 8, 9]
- Toda 輸送に関係する順序チェック: [{"map_step": 7, "map_exponent": 1, "source_group_index": 5, "transported_group_index": 8, "generator_image_indices": [3], "named_group_indices": [9], "source_before_isomorphism": "PASS", "isomorphism_before_transport": "PASS", "transport_before_generator_images": [{"step": 3, "status": "FAIL"}], "transport_before_named_group": [{"step": 9, "status": "PASS"}]}]

### 表示可能ステップの概要

- #5: Relation — \pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}
- #7: Toda45IsomorphismStatement — $(n,m,k)=(3,4,1)$ に適用すると, $E: \pi_{4}^{3}\to \pi_{5}^{4}$ は同型である.
- #3: GeneratorSuspension — $E(\eta_{3})=\eta_{4}$.
- #8: Relation — \pi_{5}^{4} = \mathbb{Z}/2\{E\eta_{3}\}
- #9: Relation — \pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}

## pi6_5

- 全ステップ数: 10
- 表示可能なステップ数: 5
- 論理依存逆転: []
- 未解決の前提: []
- 表示順: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
- Toda 輸送に関係する順序チェック: [{"map_step": 7, "map_exponent": 2, "source_group_index": 5, "transported_group_index": 8, "generator_image_indices": [3], "named_group_indices": [9], "source_before_isomorphism": "PASS", "isomorphism_before_transport": "PASS", "transport_before_generator_images": [{"step": 3, "status": "FAIL"}], "transport_before_named_group": [{"step": 9, "status": "PASS"}]}]

### 表示可能ステップの概要

- #3: GeneratorSuspension — $E(\eta_{4})=\eta_{5}$.
- #5: Relation — \pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}
- #7: Toda45IsomorphismStatement — $(n,m,k)=(3,5,1)$ に適用すると, $E^{2}: \pi_{4}^{3}\to \pi_{6}^{5}$ は同型である.
- #8: Relation — \pi_{6}^{5} = \mathbb{Z}/2\{E^{2}\eta_{3}\}
- #9: Relation — \pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}

## この監査から先の設計判断

1. ProofStep.premises の論理的な前後関係は壊さない。
2. 出典となる群構造・Toda (4.5) の特殊化・輸送先の群・生成元の同定という表示上の関係は、Proof Tree に実在するノードを参照して明示的に検証する。
3. 特定の群番号や指数に依存した分岐を一般的な順序付けに混入させない。
4. 次の Phase で共通表示順序へ置換するときは、既存の3群の固定基準テストと pi6_5 の検証を限定実行する。

全体 pytest は実行しない。
