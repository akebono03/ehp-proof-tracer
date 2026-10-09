# Phase 163 R1 棚卸し総括（暫定）

## 判定

**登録方式の棚卸しは一区切り。全登録命題数の確定は未達成。** この文書は R1A〜R1I の実行ログとしてユーザーが提示した情報を集約したもの。完全性を保証しない。

## 静的監査

| 監査 | 結果 |
|---|---|
| R1A | 候補4,932箇所、769ファイル、構文解析エラー0 |
| R1B | 本体候補1,034箇所、テスト候補2,520箇所、優先候補115箇所 |
| R1C | 25ファイル、登録関連115箇所、エラー0 |
| R1D | Statement型定義162箇所、明示キー8箇所、重複キー候補0 |
| R1E | Entry生成21箇所（ProofRepositoryEntry 20、TheoremFactEntry 1）、明示キーなし13箇所 |
| R1F | 未解決ゲート6、数学的命題総数は未確定 |

## 実行時監査

| 監査 | Repository | 登録実体数 |
|---|---|---:|
| R1G | THEOREM_FACT_REPOSITORY | 1 |
| R1G | 標準 ProofRepository（テスト fixture により生成） | 4 |
| R1H | MAP_ISOMORPHISM_FACT_REPOSITORY | 1 |
| R1H | GENERATOR_FACT_REPOSITORY.typing_facts | 3 |
| R1H | GENERATOR_FACT_REPOSITORY.ambient_group_facts | 3 |
| R1I | ZERO_COMPOSITION_FACT_REPOSITORY | 2 |

実行時に確認した実体の延べ数は14。異種データの合計であり、文献命題数・ユニーク Statement 数ではない。

## R2 へ引き継ぐ区分

- 文献の固定 Statement（命題と個別主張）
- ProofRepositoryEntry に記録された ProofStep
- Map / Generator / Composition の補助 Fact
- InferenceRuleCatalog で管理される推論規則（文献命題数には含めない）

## 未確認事項

1. factory が動的に生成する登録の網羅性
2. 文献上の命題IDと Statement ID の対応
3. 重複・特殊化・一般形の同一性判定
4. 文献の掲載順と各主張の証明完了位置（R3）
5. fixed statement と proof-internal の分類
6. 依存関係と参照の適格性（R5）

## 境界とテスト

既存コード・API・テストには変更なし。既存 ProofStep を維持する。R2 では台帳のデータ構造を設計するが Backward Search と Renderer の変更は行わない。全体 pytest は Phase 終了時まで保留。
