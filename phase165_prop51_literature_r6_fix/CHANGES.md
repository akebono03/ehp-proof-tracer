# Phase 165 R6 修正版

- 修正対象：`phase165_prop51_claim_order.py` の `ordered_prop51_items()` における第4項の区分。
- 修正対象：`phase165_r52_r13_reference_registration.py` の `build_adopted_prop51_reference()` の登録結果に第4項の独立 Assertion を追加。
- 新規：`phase165_prop51_literature_r6_fix/install.py`（構造検査とバックアップ、再実行可能）。
- テスト：`test_prop51_literature.py` 全3件と既存の `test_phase165_r52_r13_reference_registration.py`。
- 既存の文献由来 `GIVEN` 4項目に影響しない。第4項を自己証明の根拠として使用しない。
- 全体 pytest は実施しない。
