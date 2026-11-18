# Phase 175 R4R12R11 監査計画

## 対象

- 新規 `phase175_r4r12r11_ehp_surjectivity_frontier/audit.py`：`git`、`describe`、`valid_zero_goal`、`inspect`、`run`、`main` を追加する。
- 新規 `tests/test_audit.py`：4件の限定テストを追加する。
- 新規 `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`__init__.py`。
- 既存ファイル・既存クラス・既存関数・既存 import は変更しない。

## 数学的注意

(5.11) は再証明しない。既存 R10R1 が登録した文献与件を利用する。

EHP 完全性から $E:\pi_8^4\to\pi_9^5$ の全射性を主張する際、$\pi_9^9=0$ を前提にする既存の候補は使用できない。実際 $\pi_9^9\cong\mathbb Z$ である。

今回の監査では $H$ の像に関する一般的な定理を追加しない。$E$ の全射性と生成元像はそれぞれ独立した未解決義務として維持する。

## 完了条件

- 共有・単独の2 Orientation が同じく得られる。
- 6義務のうち Δ 像、EHP 完全性、E 全射性、E 生成元像の候補と前提を出力する。
- 零群を要求する候補と、その対象群が diagonal である事実を可視化する。
- 実際の再帰証明・本番ファイルの変更・新規 GIVEN・新規数学規則・全体 pytest は実施しない。
- Gate: `PASS_R11_EHP_SURJECTIVITY_FRONTIER_AUDITED_NOT_COMPLETE`。
