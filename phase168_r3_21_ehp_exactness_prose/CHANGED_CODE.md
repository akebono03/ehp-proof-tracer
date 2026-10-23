# 変更対象

- `phase168_r3_5_model_renderer.py`: `render_model_backed_narrative_markdown` の関数全文置換。import は関数内に追加し、ファイル先頭の import は変更なし。
- 新規 `tests/test_phase168_r3_21_ehp_exactness_prose.py`: テスト3関数と import 全文を収録。
- 関数全文: `render_model_backed_narrative_markdown_FULL.py`。

## 完了条件

既に証明された `EHPImageEqualsKernelStatement` が `Im Delta = ker E` と表示されること。未証明の等式は追加しない。限定 pytest のみ実行。

## 次工程の境界

核の具体的な決定・準同型定理・群構造の文章化は次工程。Reference の重複処理、探索、全体テストは今回変更しない。
