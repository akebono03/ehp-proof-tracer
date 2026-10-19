# Phase 165 R6 テスト整理記録

## 今回の変更対象

- 削除: `tests/test_phase164_r7_statement_resolution.phase164_r7_r1_backup.py`（バックアップ名付きの旧テスト）
- 維持: `tests/test_phase164_r7_statement_resolution.py`（現行の対応テスト）
- 追加: `phase165_r6_safe_test_cleanup/run.ps1`, `rollback.ps1`, `README.md`, `decision.md`

クラス・関数・import の変更はありません。旧群別規則や Renderer は復活しません。

## 根拠

現行 GitHub にバックアップ名付きテストと通常版が別々に存在することを確認。バックアップ名付きファイルは pytest の収集で不正なモジュール名として扱われ、エラーを生じていた。通常版テストは維持する。なお、両者の内容が完全に一致するとはみなしていないため、削除済みファイルはローカルの監査結果ディレクトリに保存する。

## 検証と境界

実行する targeted pytest: `python -m pytest -q tests/test_phase164_r7_statement_resolution.py`

今回の完了条件は、削除対象の退避とハッシュ照合、通常版の targeted pytest が成功すること。全体 pytest は Phase 終了時のみ実施。259件の旧 probe 経由エラーと残りの収集エラーは未解決のまま継続監査する。Phase 165 の終了判定は保留。
