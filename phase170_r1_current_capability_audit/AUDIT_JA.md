# Phase 170 R1 監査仕様

対象は `phase165_r55_nk_only_goal.py::search_group_from_registered_goal` から始まる本番経路。`ProofStep` と実際の前提関係、`phase168_r3_4_link_bridge.py` の Citation、`phase168_r3_41p13_trust_boundary/verification.py` の検証結果、共通 Renderer の結果を別々に記録する。

標準対象は $\pi_4^2,\pi_5^3,\pi_6^4$。ほかの stem は有限個の標本であり、全登録群の完全性分布ではない。

`data/sphere.csv` と `data/sphere_relation2.csv` は該当行の存在を確認する。DB 行が存在しても、その出典が Proof Tree の Root に到達していなければ「証明で使用した」とみなさない。`HyoujiGen.csv` と `TBtable.csv` は R1 では件数と列名の確認にとどめ、詳しい利用状況は R2 で監査する。

**変更対象** は監査パッケージの `audit.py`、`run.ps1`、`tests/test_audit_contract.py`、`README.md`、`AUDIT_JA.md`、`__init__.py` の新規ファイルのみ。既存のクラス・関数・import は変更しない。

**完了条件** はレビュー済み Git HEAD・主要本体ファイルの確認、全対象の検索実行、ProofStep・未解決 Goal・Citation・Trust の報告、Git tracked/index 不変、限定 pytest の PASS。数学的に未完成と判定された群があっても、監査としては正しい結果になり得る。

**次段階との境界**：R1 では新しい数学的規則・個別 Definition・DB エントリを追加しない。R2 では群構造・関係式・生成元・Toda 命題と本番探索の接続の有無を詳細に監査する。全体 pytest は Phase 170 終了時だけ実行する。
