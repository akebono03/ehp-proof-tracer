# Phase 173 R15R17 設計

## 対象

現行 GitHub `develop` の `874c6f63ad85374cd19e00e92600c92c5c056cb3` を監査対象とする。このコミットは直前の監査時 `d57fa2e8` に監査用ディレクトリのみを追加し、以下の5本番ファイルの Blob を変更していない。

- `phase168_r3_3_proof_narrative_model.py`: 新関数 `verified_narrative_steps()` を `build_proof_narrative_model()` の直前に追加し、同関数のステップ入力を統合する。
- `phase168_r3_12_body_binding.py`: `build_narrative_body_lines()` の真正性検査を、検索済みステップおよび検証済み証明木の正確な統合列に適合させる。import の全体像を生成する。
- `web_group_proof_common.py`: `_group_proof_statement_latex()` で型付き抽象不変量を汎用数式に整形する。群の次元・生成元・個別定理による専用 Narrative は作らない。
- `phase173_r4_r15r9_shared_abstract_renderer/projection.py`: `render_certified_abstract_model_section()` は同じ検証済みルートが Model のステップに存在する場合、後付け Section を生成しない。
- `phase165_r52_r3_web_adapter.py`: `build_partial_web_group_proof_view()` のステップ表示を、Model が渡された場合は Model のステップ列から構成する。

## 安全境界

`PartialProofResult` は一切変更しない。特に `status`、`conclusion`、`open_goals`、`diagnostics` を保持する。`root_index` は記名証明の完成ルートにのみ対応し、抽象群側の検証済み推論を記名証明の完成ルートに設定しない。

補助証明木は既存の `verified_tree_postorder()` で前提・cycle・推論 guard を検査し、元の `ProofStep` の identity を維持して結合する。Reference は既存 `build_proof_narrative_model()` の Citation 投影が一括で行う。既存 Common Narrative Renderer 本体は変更しない。未解決 Goal は既存 Renderer の本文末尾の処理を使う。

## テストと境界

新規テストは、抽象証明書あり／なし／完成結果、根の型付き数式化、Reference 統合、二重 Renderer 呼出し禁止、モデル改ざん拒否を対象とする。実装後は指定された限定 pytest のみ実施する。全体 pytest は Phase 173 closeout 時だけ実行する。

旧 Phase の独立した抽象群 Section を必須とした歴史的テストには、現行統一表示とは両立しないアサーションが存在する。これらは新契約に沿って更新を要する。古いパッチの Source Guard を無差別に書き換えることはしない。
