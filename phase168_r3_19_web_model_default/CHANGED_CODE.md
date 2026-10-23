# Phase 168 R3-19 変更内容

## 変更対象

- `web_group_proof.py` の `build_standard_web_group_proof_view()` 全体（import の変更なし）
- `tests/test_phase168_r3_19_web_model_default.py` の3関数（新規、全文収録）
- `phase168_r3_6_standard_web_entry/tests/test_phase168_r3_6_standard_web_entry.py` の `test_r36_default_pi32_preserves_long_form()`（旧経路を明示して確認、テスト全文は既存ファイル内）
- `run.ps1` と `patch.py`（配置先は ZIP 内の専用フォルダ）

パッチを実行すると、変更後の関数全文を `build_standard_web_group_proof_view_FULL.py` に出力する。変更前の `web_group_proof.py` は `backup/web_group_proof.py` に保存する。

変更点は `citation_source` の既定値 `legacy` → `model` と、その説明 docstring の修正のみ。既存 API の引数名や明示的な `legacy` 経路は維持する。

## 限定 pytest

`python -m pytest -q phase168_r3_19_web_model_default/tests/test_phase168_r3_19_web_model_default.py`

## 完了条件

通常 Web が明示指定なしで model Renderer を通ること、旧経路を明示指定可能であること、trace 出力が変更されないこと。

## 次工程との境界

R3-20 以降で EHP 完全性の文章化、その他型付き文章化、Reference の統一を行う。旧経路の削除と全体 pytest はまだ実施しない。
