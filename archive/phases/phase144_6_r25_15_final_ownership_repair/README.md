# Phase 144-6 R25-15 Final Ownership Repair

## 変更対象

- `toda_group_proof_narrative_argument_multi_renderer.py`
  - rejected R25-13 の rollback のみ。
- `toda_group_proof_narrative_contribution_ordering.py`
  - `_group_key` 全体を semantic statement identity に戻す。

## 修正理由

表示文字列は presentation concern であり、proof contribution の semantic identity ではない。
rendered text を group key に使うと、異なる内部 statement が同じ表示を持つ場合に
ownership が PARTICIPATING / DETACHED argument 間で移動し得る。

group key を statement type + `repr(conclusion)` + provider keys に戻し、
proof structure の identity と表示形式を分離する。

## テスト順

1. R25-15 semantic identity test
2. depth=2 definition regression
3. pi_6^3 generic production route
4. six-group final completion invariants
5. 上記が全て PASS の場合だけ Phase-final full pytest

full pytest は Phase の最後として一度だけ実行する。
