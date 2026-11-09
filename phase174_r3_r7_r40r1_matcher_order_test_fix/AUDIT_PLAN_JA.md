# Phase 174 R3-R7-R40R1 — 修正監査

## 状況と再現

R40 本実行は数学的推論の検査と Source Guard が PASS したが、`R40_RULE` の `test_direct_given_for_generator_zero_is_rejected` において `find_inference_matches_for_rule(rule, (independent, db)) == ()` が失敗した。

GitHub `develop` にある `proof.py` の `_find_all_matching_premise_bindings` は、`PremisePattern` ごとに使用可能な `ProofStep` を走査し、必要な前提の型・内容に対応付ける。入力順序が逆でも、正しい前提を `(db, independent)` として返す。前提を逆順に渡しただけで拒否されるという従来のテスト期待は誤り。

## 変更対象

`phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py` の **`test_direct_given_for_generator_zero_is_rejected()` だけ**を変更する。他の関数、import、数学的規則およびドキュメントは変更しない。

## 修正条件

- `db` と偽装 `forged` の組は、入力順序にかかわらず拒否する。
- `db` のみの不完全な入力を拒否する。
- 正しい `(independent, db)` には照合が1件あり、返された前提は規則順の `(db, independent)` である。
- 実際の `ProofRule`、`verified_db_step`、R40 の監査、R38/R39 には変更を加えない。

## 出典・状態の保全

既存 R40 の `source_guard.verify_checkout()` を最初に実行し、さらに `rule.py`、`audit.py`、`source_guard.py`、`run.ps1` のレビュー済み内容を SHA256 で照合する。対象テストは元の内容または同じ修正版のみ許可する。Git の管理する既存変更を上書きしない。

## テストと完了条件

R40R1 の限定テスト4件および R40 元来の `run.ps1`（R40 と関連テストの限定 pytest）が PASS した場合に限り、R40R1 完了とする。全体 pytest は実施しない。R40 は隔離推論であり、公開 Provider 接続と最終ルート証明は後続 Phase に残す。
