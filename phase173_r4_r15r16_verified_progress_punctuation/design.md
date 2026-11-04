# R15R16 設計

## 目的

未完成の記名生成元証明であっても, 別個に検証された抽象群証明書の中間段階を表示する. 完成・未完成は同じ Web の共通 Renderer へ流れる. 文章の句読点を ASCII のコンマとピリオドに統一し, 文末ピリオドで行を区切る.

## 責務

- `CertifiedAbstractStructure.proof_step`: 既存の検証済み抽象推論根. 前提4個は当該推論規則の `match_guard` で認定済み.
- `phase173_r4_r15r9_shared_abstract_renderer/projection.py`: 検証済み前提を出典表示名と数学的式に射影し, 複数の中間段階と抽象群の結論を表示する. 群・次元・生成元ごとの表示専用分岐は追加しない.
- `phase173_r4_r15r13_unified_presentation/layout.py`: 正規化済み Markdown の文章部分だけで句読点と改行を共通化する. 数式, コード, 文献番号は保護する.

## 制約

1. 証明済みの抽象群構造から記名生成元の証明完成を推論しない.
2. 出典表示名は証明木に付属した `LiteratureReference` を読む. 出典番号の新規採番は行わない.
3. 証明木の内容, Citation, open goals, diagnostics, public status は変更しない.
4. 従来の生 Markdown API は互換性を保つ. Web 表示でのみ句読点と改行を統一する.
5. 全体 pytest は Phase 終了時だけ行う.

## 次工程との境界

R15R16 は検証済みの途中経過の表示と句読点処理だけを扱う. 抽象群側の Reference を標準の `ProofNarrativeModel.citations` に統合する改修, 生成元の証明規則の拡張, 未解決 Goal の統合表示は行わない.
