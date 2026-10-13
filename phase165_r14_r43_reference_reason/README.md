# Phase 165 R43

## 変更対象
- `toda_group_proof_narrative_renderer.py`：末尾の `render_toda_group_proof_narrative_markdown` 関数全文を置換し、共通補完関数を呼ぶ。既存の stable transport 分岐は保持。
- `phase165_r14_r43_reference_reason.py`：新規。`_reference_rows`、`_exactness_reason_rows`、`enrich_common_narrative` の関数全文。
- `test_phase165_r14_r43_reference_reason.py`：新規テスト5件。
- `install.py`、`run.ps1`：配置と対象テストを実行。既存ファイルのバックアップを作成。

## 実装方針
実在する ProofStep の葉に付与された Reference locator のみ採用する。空の「使用する結果」を補い、対応する完全性命題が前提にある推論についてのみ短い数学的理由を補う。専用の群別の証明文章は書かず、共通 Renderer の既存出力を保存する。

## 完了条件
文献3箇所の参照欄、完全性に基づく理由3件、既存の型付き文章表示の維持を対象 pytest 5件で検査。

## 境界
Phase 165 全体 pytest は実行しない。その他の群・安定輸送表示は改変しない。
