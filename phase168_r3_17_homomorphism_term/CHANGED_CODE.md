# 変更対象

- `toda_group_proof_narrative_renderer.py`：関数 `render_toda_group_proof_narrative_markdown` 内の重複挿入防止条件のみ変更。import は変更しません。
- `tests/test_phase168_r3_17_homomorphism_term.py`：新規テスト3関数。
- `apply.py`：既存コードの厳密一致確認、バックアップ、完全な変更後関数の書き出し。

既存の公開関数は大きいため、`run.ps1` の実行時に**現在の実コードから変更後の関数全体を切り出し**、`output/render_toda_group_proof_narrative_markdown_FULL.py` に省略なく出力します。変更していない import 部分も `output/imports_and_prefix_FULL.py` に出力します。ZIP にはテストファイルと実行スクリプトの全文が含まれます。

修正する条件は `if "準同型定理" not in "\\n\\n".join(paragraphs):` です。条件だけを修正し、既存の「全射性と核の決定から, 準同型定理より」という本文は維持します。
