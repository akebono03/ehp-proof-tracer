# Phase 169 R3Z — 変更対象と実行時の全文ファイル

- 変更対象：`phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown()` だけ。
- 新規テストファイル：`tests/test_r3z_reference_only_generic_eta.py`。必要な import と全テスト関数を収録。
- 新規監査ファイル：`audit.py`。全関数と import を収録。
- 既存のモジュールレベル import、クラス、既存 API は不変更。

既存 Renderer 本体は約458行あり、ユーザーの現行チェックアウトを厳密に保持するため、ZIP に一部を再定義した古いコピーは含めません。`install.py` はその場で AST を用いて **関数全文**を生成して置き換え、次のファイルに出力します。

1. `output/render_model_backed_narrative_markdown_FULL.py`：変更後の関数全文
2. `output/phase168_r3_5_model_renderer.py.FULL.py`：変更後のモジュール全文
3. `output/phase168_r3_5_model_renderer.py.before`：元のファイルのバイト単位バックアップ

新規処理の全文は `install.py` の `ADDITION` に収録しています。今回の Phase に必要な抑制だけを行います。途中失敗時には原ファイルを復元します。
