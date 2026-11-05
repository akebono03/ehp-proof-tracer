# Phase 174 R1R1 — 既存テスト契約の限定修正

## 変更対象
- 既存 `test_phase165_r55_nk_only_goal.py` の全文置き換え。
- import 部分を全文更新（`phase166_r3af_goal_adapter` を追加）。
- 変更するテスト関数は次の4件のみ。
  - `test_r55_discovers_group_goal_inside_fixed_typed_composite`
  - `test_r55_calls_canonical_search_with_registered_goal_not_given`
  - `test_r55_no_candidates_fails_closed`
  - `test_r55_multiple_candidates_do_not_guess`
- 新規 `phase174_r1r1_test_contract_correction/run.ps1`（追加位置はルート直下）。
- 新規 `phase174_r1r1_test_contract_correction/README.md`。
- 本番コード・主要5文書は無変更。

## 失敗4件の理由と処置
1. `n=3,k=1` には現行 DB 由来の型付き Goal 候補がある。旧「候補なし」の期待を候補の型・群次元の検証に変更。
2. 古い `SimpleNamespace` fixture には `assertion_id` 等がない。引用解決だけを単体テストで分離し、実際の探索への委譲と未証明維持を検査。
3. DB 候補がある群で「候補なし」を検査するのは不適切。DB Goal 選択をモックで無効化して `fail-closed`（失敗時に証明しない）を確認。
4. DB の一意候補が優先される場合、合成レジストリの多候補枝には到達しない。DB 候補をモックで無効化し、本来の曖昧候補枝を確認。

## 完了条件
- 元の4テストをすべて実行（スキップ・削除しない）。
- 元の R1 Runner による 3群の Goal 監査が PASS。
- 限定 pytest が全 PASS。
- Git index が維持され、本番コードの Source Guard が PASS。

## 境界
Phase 174 R2（数学的出典検証）および R3（共通型付き推論）は開始しない。
全体 pytest は Phase 174 の末尾まで実施しない。
