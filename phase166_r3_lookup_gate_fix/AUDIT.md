# Phase 166 R3 — 直接型付き参照の資格判定統一

## 現行コードの監査

- `phase165_r3_recursive_search.py` の `typed_reference` は従来 `GIVEN` と型一致だけで引用資格を判断していた。
- `typed_reference_ordered` は `phase165_r52_r15_ordered_citation.ordered_typed_reference_steps` を使用し、`assess_phase164_r2_citation` を通過する。
- `legacy` は `find_eligible_goal_candidates` を使用する。

## 変更対象（限定）

- `phase165_r3_recursive_search.py`: `_typed_reference_steps` 全体、`reconstruct_registered_goal` 内 `typed_reference` 分岐の呼出し部分（関数全文は ZIP 同梱の実コードを参照）。
- 新規 `phase166_r3_lookup_gate_fix/install.py`：事前条件検査・バックアップ・最小置換。
- 新規 `phase166_r3_lookup_gate_fix/test_gate.py`：12個のパラメータ化された回帰例。

## 完了条件

3モードで未審査、metadata_only、文献順違反を拒否し、独立審査済みの適格な既存 GIVEN を許可する。R3の内部証明資格の全監査は別途継続。

## 次 Phase との境界

関係式 Repository の探索への接続は R4、群構造データの照合は R5、全体 pytest は R10 とする。
