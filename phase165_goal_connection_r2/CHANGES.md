# Phase 165：型付き Goal 接続 R2

## 変更対象

- `phase165_r55_nk_only_goal.py`：`search_group_from_registered_goal()` 関数全文を置換
- `web_group_proof.py`：`build_standard_web_group_proof_view()` 関数全文を置換
- 新規 `test_goal_connection.py`：対象テスト3件
- 新規 `install.py`、`run.ps1`：バックアップ付きの導入器

import の追加・変更はありません。クラスは変更しません。関数の置換全文は `install.py` の `search` と `web` に収録しています。

## 完了条件

型付き Goal が文献台帳を経由せず共有探索に届くこと、不一致の Goal を拒否すること、既存の n,k 専用経路を維持すること。

## 次の境界

Web UI に型付き Goal を入力・引継ぎする経路と、EHP による数学的証明の構築は別作業です。全体 pytest は Phase 終了時のみ行います。
