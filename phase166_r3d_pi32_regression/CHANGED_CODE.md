# Phase 166 R3-D 変更内容

## 変更対象

- 新規 `phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py`：6件の回帰テスト。追加位置は新規テストファイル。
- 新規 `phase166_r3d_pi32_regression/run.ps1`：対象限定テストの実行。
- 新規 `README.md`：英語で実行方法を説明。
- 新規 `CHANGED_CODE.md`：変更記録。

本番コード・既存テスト・既存 API は変更しない。新規テスト関数はファイル内に全文収録し、import もすべて収録。テストは `search_group_from_registered_goal` と公開 Web view を直接呼び出し、完全証明、文献参照、EHP 完全列、各導出、最終結論を検査する。

## 完了条件

6件 PASS し、公開 Web 表示でも `generic-complete-proof` が維持されること。全体 pytest は Phase 166 終了時のみ。R3-E の π4^3・π5^3 は未着手。
