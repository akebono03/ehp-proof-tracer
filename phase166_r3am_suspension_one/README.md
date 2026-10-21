# Phase 166 R3-AM: Suspension exponent one

## 変更対象

- `toda_human_readable_renderer.py`: `render_toda_expression_latex()` 全体の置換（`IteratedSuspension` 分岐のみ内容変更）
- `tests/test_suspension_one.py`: 新規3テスト。importを含む全文を同梱

`apply.py` は AST から変更前の関数全体を取得し、該当分岐だけ置換したうえで、変更後の関数**全文**を `render_toda_expression_latex_full.py.txt` に出力する。現在の実装が一致しない場合は適用しない。既存 import の変更なし。バックアップを作成。

`IteratedSuspension(expression, 1)` の TeX は `E` とする。指数 2 以上の `E^{m}` は従来どおり。証明探索・命題台帳・Goalの構造は変更しない。

限定 pytest: `python -m pytest -q phase166_r3am_suspension_one/tests/test_suspension_one.py`

完了条件: 対象2群で `E^{1}` が出ず、一般の懸垂指数を維持する。次の作業は112群のブラウザ表示監査。全体 pytest は Phase 最後に実施。
