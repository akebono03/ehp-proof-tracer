# 変更対象

- `phase165_r57_r8_eta_specialization.py`
  - `specialized_eta_group_goal_candidates()` — `n < 4` で空の候補を返す。
  - `expand_registered_eta_specialization()` — `n < 4` で空の候補を返す。
- 新規 `phase165_prop51_range_r2_candidate_skip/test_candidate_skip.py`
  - 5件の対象テスト。$n=3$ の候補不生成、$n=4$ の成功、登録メタデータを検証する。

命題台帳と推論検証器の既存の $n\ge4$ 制限は変更しない。新たな推論規則は追加しない。

## 完了条件

対象テストが PASS し、$n=3$ で適用条件の例外が Web Query に漏れないことを実画面で確認する。EHP 内部証明の完成は別作業。
