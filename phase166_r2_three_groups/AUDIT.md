# Phase 166 R2 — 3群の命題対応監査

## 対象

- $\pi_3^2$：Proposition 5.1 / `pi3_2_group_relation`
- $\pi_4^3$：Proposition 5.1 / `higher_eta_group_relation`
- $\pi_5^3$：Proposition 5.3 / `pi5_3_group_relation`

## 変更対象

新規 `phase166_r2_three_groups/` の `audit.py`（`read_rows`・`inspect`・`main`）、`test_audit.py`（4関数）、`run.ps1`、本書、`README.md`、監査用 CSV のみ。既存クラスと関数は変更しない。

## 検査

群の `(n,k)`・登録生成元文字列・次数データ・`Element` ID と、命題台帳内の参照 ID・個別主張 ID・構成要素キーを照合する。未知 ID・欠落群・誤った構成要素は fail closed とする。

## 境界

台帳の `TodaFixedStatementComponent` は数学的な群構造文そのものではない。対応はメタデータ候補であり、群構造・位数・生成性の証明や `ProofStep` の生成を意味しない。R3 の資格判定と R6〜R8 の証明生成を先取りしない。

## pytest と完了条件

`python -m pytest -q phase166_r2_three_groups/test_audit.py` の限定4件が成功し、対象3群の命題 ID を取得でき、承認数と ProofStep 追加数が0であること。全体 pytest は R10 に限定する。
