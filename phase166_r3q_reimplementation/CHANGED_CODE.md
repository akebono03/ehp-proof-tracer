# Phase 166 R3-Q 再実装

## 変更対象

- `phase165_r55_nk_only_goal.py`
  - 新規 `_r3q_publication_boundary()`：既存 `search_group_from_registered_goal()` の直前に追加。
  - `search_group_from_registered_goal()`：関数全体を置換。
- 新規 `phase166_r3q_reimplementation/tests/test_phase166_r3q_reimplementation.py`：限定テスト5件、必要 import を全文収録。
- 新規 `apply.py`、`run.ps1`、`README.md`、`CHANGED_CODE.md`。

import の変更なし。既存 API の引数は変更しない。クラスの変更なし。関数の全文は `apply.py` の `HELPER` と `FUNCTION` に省略なしで収録し、実行時にもバックアップ先 `NEW_FUNCTIONS.py.txt` に全文を出力する。

## 方針

証明目標は従来の登録命題／明示的 Relation から決める。本文中に同じ目標 Relation を含み、掲載位置と構成位置が両方登録された FIXED_STATEMENT が一つだけ存在するときに限り、その主張を文献掲載順の境界として指定する。先行可否は既存の `precedes_citing_assertion()` のみが決める。

一致主張がない場合・複数ある場合・位置が欠落する場合は、未確認の位置や仮 ID を作成せず、現行 Web の通常探索の入口を維持する。これは順序適用の完全化ではなく、安全な部分接続である。

## テスト

`python -m pytest -q phase166_r3q_reimplementation/tests/test_phase166_r3q_reimplementation.py phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py`

限定テストで $\pi_3^2$ の完全証明を守る。$\pi_4^3$ と $\pi_5^4$ については、現行データで順序境界を確定できるか別途確認が必要。全体 pytest は Phase 166 終了時のみ。
