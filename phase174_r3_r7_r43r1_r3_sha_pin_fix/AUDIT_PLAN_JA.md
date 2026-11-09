# R43R1 実装前監査・方針

- ユーザーログの最初の失敗は R43 DryRun の `Reviewed source differs: phase174_r3_r7_r3_ehp_zero_rule/rule.py`。
- GitHub `develop` の `phase174_r3_r7_r3_ehp_zero_rule/rule.py` は Git blob SHA `8834cbefbfca5bcca18dc01f072c9738a05f7bdc`（40桁）。
- R43 の `source_guard.py` は `8834cbefbfca18dc01f072c9738a05f7bdc`（35桁）となり、`5bcca` が欠落している。
- R43 の関連規則 R3・R5・R37 とテスト、R42 統合履歴、R43 既存 Source Guard を確認済み。

## 変更対象

- 既存ファイル `phase174_r3_r7_r43_public_ehp_map_property_wiring/source_guard.py` の定数 `PINS` の対象 SHA 1件のみ。
- 新規 `phase174_r3_r7_r43r1_r3_sha_pin_fix/install.py` の関数：`git`, `normalize`, `sha256`, `git_blob`, `reviewed_source_blob`, `replacement_contract`, `verify_checkout`, `install`, `main`。
- 新規 `phase174_r3_r7_r43r1_r3_sha_pin_fix/tests/test_fix.py` のテスト関数5件。

数学的な規則、既存の `verify_checkout()` の検証方法、推論 Provider、本番コードは変更しない。Source-first（出典優先）・First Successful Proof Search（初成功で終了）は維持する。

## 完了条件

1. R43R1 Source Guard と DryRun が PASS。
2. 既存の R43 の Source Guard・DryRun・通常監査が PASS。
3. R43R1 と R43 の限定 pytest が全件 PASS。
4. `phase165_r52_r9_shared_math.py` 以外に tracked diff が発生しない。
5. Web の公開根が未完成であることは引き続き明示し、全体 pytest は Phase 終盤まで行わない。

## 次の工程との境界

R43R1 は R43 の固定ハッシュ訂正だけ。R44 の再帰探索・Web 確認や上側 Δ の全射性の証明を先取りしない。
