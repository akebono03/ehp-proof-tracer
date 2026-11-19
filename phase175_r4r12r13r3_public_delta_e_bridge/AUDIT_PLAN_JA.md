# Phase 175 R4R12R13R3 監査計画

## 対象

- 既存ファイル `phase165_r52_r9_shared_math.py`：`shared_expansion_provider` に限定接続。関数の全文を実環境の `output/shared_expansion_provider_FULL.py` に書き出す。
- 新規 `phase175_r4r12r13r3_public_delta_e_bridge/provider.py`：`screened_toda58_available`、`delta_free_coordinate_proposals`、`build_public_delta_e_provider`。
- 新規 `installer.py`：`render`、`plan`、`install`。
- 新規 `audit.py`：`git`、`preflight`、`inspect`、`run`、`main`。
- 新規 `tests/test_provider.py`：限定テスト5件。
- その他：`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`run.ps1`、`__init__.py`。

## 出典・一般推論

Toda (5.8) は既存の出典付き GIVEN を前提とする。式を再登録しない。先行群の DB 行と既存一般型を目標として用いるが、DB 行のみを証明としない。

R13R2 の Δ 単射と E 全射は一般規則としてそのまま再利用する。位相・次元と型が一致しない場合には候補を出さない。誤った π₉⁹=0 を導入しない。

## 実行と境界

DryRun と本実行のそれぞれで限定 pytest 10件（R13R2 5件 + R13R3 5件）。全体 pytest は実施しない。公開接続は目標群の完成証明を保証しない。次段階で R13R2 3前提の再帰的 ProofStep と E の生成元像の閉包を確認する。
