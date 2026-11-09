# Phase 174 R3-R7-R30R1：Provider 欠落修正

## 前提監査

ユーザー環境の R30 DryRun で `ImportError: cannot import name 'has_certified_prop27_leaf'` を確認。
配布済み R30 ZIP 内の `provider.py` が 0 バイトであることを実ファイルで確認。
関連する `audit.py`、`install.py`、`tests/test_wiring.py`、R28 `registration.py`、R29 `provider.py` を点検。

## 変更対象のファイル・関数

- `phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py`：空ファイルを全置換。
  - `_reviewed_position()` を新設。
  - `register_positioned_prop27()` を新設。
  - `has_certified_prop27_leaf()` を新設。
  - `expand_public_cited_prop27_goal()` を新設。
- 同ディレクトリの `run.ps1`：全体を置換し、インストール前の限定テストを追加。
- `tests/test_provider_contract.py`：`tests/test_wiring.py` の隣に新設。
- `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`：全文更新。

既存 `phase165_r52_r9_shared_math.py` を書き換える処理自体は、元の R30 `install.py` を変更しない。
Source Guard 通過、事前限定テスト PASS の後にのみ、本実行で既存2関数を書き換える。

## 出典および数学的契約

- R28 の原文 SHA256 照合を再利用する。
- 掲載順序は既存の Phase 163 manifest の `toda:Proposition 2.7` と `toda:tex:ch2:0018` の正確な対応からのみ取得する。
- source-first スクリーニング後、一般命題の唯一の固定出典リンクが存在するときだけ逆向き候補を提供。
- 個別 `n=6` GIVEN を追加しない。証明の可否は既存 `reconstruct_registered_goal()` が判断。
- Web HTTP と Δ 全射性はこの修正の範囲外。

## 完了条件

DryRun PASS、本実行の事前・事後限定 pytest PASS、公開共通探索の検査 PASS。
全体 pytest は Phase 最終工程まで行わない。
R31 は Δ 全射性に必要な数学的橋渡しと HTTP 表示の検査を行う。
