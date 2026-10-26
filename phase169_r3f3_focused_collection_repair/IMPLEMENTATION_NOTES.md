# Phase 169 R3F3 — pytest収集エラー修正

## 前回の失敗

R3F2 の限定 pytest に旧テスト `phase161_r4_literature_premise_matching/tests/test_phase161_r4_literature_premise_matching.py` を指定した。しかし旧テストの import 先 `tests.test_phase59_n3_ehp_chain` は現行 GitHub HEAD `2e0b466ee6a91f891ca6b101794b1bd6bca0b970` には存在しない。このため、数学的推論の検査前に pytest 収集が停止した。ガード付き自動復元は成功した。

## 変更対象

配布ファイル `run.ps1`、`README.md`、`IMPLEMENTATION_NOTES.md` を更新した。`apply.py` はフェーズ表記のみ R3F3 へ更新した。

本番コードの変更内容は R3F2 と同一で、以下の2関数を全体としてパッケージ内に収録する。import 節は変更しない。

- `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 全文：`full_functions/shared_expansion_provider.py`。
- `phase165_r14_r5_ehp_connection.py` の新規 `expand_registered_ehp_terminal_goal()` 全文：`full_functions/expand_registered_ehp_terminal_goal.py`。追加位置は `audit_ehp_connection()` 直前。
- 新規テスト8関数全文：`tests/test_phase169_r3f_ehp_terminal_subgoals.py`。

## 限定 pytest

`run.ps1` は以下の3ファイルを実行する。

1. `phase169_r3f3_focused_collection_repair/tests/test_phase169_r3f_ehp_terminal_subgoals.py`
2. `phase165_r14_r5_ehp_connection/test_phase165_r14_r5_ehp_connection.py`
3. `tests/test_phase161_r3_backward_goal_schema.py`

旧 Phase 161 R4 テストは削除・変更せず、収集対象から除外する。R3E1 の既存回帰テストには「終端 Goal に候補がないこと」を固定した検査が含まれ、今回の R3F によって前提が変更されるため、同テストファイルも限定実行しない。代わりに `audit.py` が実際の文献順で選別された文脈における双方の終端候補、既存同型性の推論、`INFERENCE` 前提条件を確認する。

## 完了条件

`R3F3_FOCUSED_PYTEST_EXIT_CODE=0`、`R3F3_AUDIT_EXIT_CODE=0`、`R3F3_COMPLETE`。`H(ν')=η₅` と Proposition 5.1 の複合命題は未証明の Goal であり、証明済みの GIVEN に置き換えない。$\pi_5^3$ を `complete` にしない。全体 pytest は Phase 169 終了時だけ実施する。

## 次 Phase との境界

R3G で2つの終端下位 Goal に引用上の実際の証明経路が存在するか調査する。R3F3 は新たな文献や数学的事実を創作しない。
