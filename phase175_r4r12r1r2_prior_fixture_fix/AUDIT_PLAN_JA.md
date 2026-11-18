# Phase 175 R4R12R1R2 — 監査計画

## 原因

R4R12R1R1 は追跡キャッシュの検証まで成功したが、R4R12 の既存テスト `test_prior_success_is_not_a_root_proof_certificate` が失敗した。

`audit.validate_prior()` は R4R11 実行時の歴史的 HEAD `abf619040d52aa9fd61c5bca60db81e28912e24d` を要求する。R4R12 の現在の HEAD は `344fc101fdfcce49ec80f867f80a0614d96c214e` であり、テスト用の `prior_success_report()` が `audit.HEAD` を代入するのは誤り。

## 変更対象

- `phase175_r4r12_public_two_summand_quotient/tests/test_audit.py` の `prior_success_report()` に含まれる `preflight.head` を、R4R11 の歴史的 HEAD に変更する。それ以外の箇所は変更しない。
- 補正パッケージの新規 `patch.py` に `git()`、`checked_paths()`、`patch_fixture()`、`main()` を実装する。
- 補正パッケージの `tests/test_patch.py` に5件の限定回帰テストを追加する。

## 検証と境界

- 修正前の旧 HEAD / 現行 HEAD を区別して保持し、HEAD 履歴検証を維持する。
- 未承認の追跡ファイル変更は拒否する。
- 先行レポート、一般数学規則、GIVEN、共有探索本体は変更しない。
- DryRun ではファイルを書き換えない。実行後に既存 R4R12 DryRun と本実行を実施する。
- 期待 Gate: `PASS_R4R12_TWO_SUMMAND_QUOTIENT_ROOT_CANDIDATE_PI95_PENDING`。
- 全体 pytest は Phase の終わりまで行わず、群の完成証明も本補正の対象外。
