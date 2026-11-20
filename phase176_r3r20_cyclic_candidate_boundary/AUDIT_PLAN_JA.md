# Phase 176 R3R20 巡回構造の候補境界監査

## 変更対象

新規 `phase176_r3r20_cyclic_candidate_boundary/` の `audit.py`（`inspect_source`, `capture`, `checked_git_root`, `report_file`, `execute`, `main`）、`tests/test_audit.py` の3テスト、`run.ps1`、本ドキュメント、README のみ。既存コードは変更しない。

## 内容

根の巡回構造 Goal の候補が0件である理由を、既存の Hopf lift と有限位数経路の入力候補から切り分ける。特に `eligible_eta_hopf_chains` と `specialize_registered_higher_stem` の対象一致数を個別に出力する。後者が0件でも、別の経路が数学的に不可能とまでは断定しない。

`expand_cited_double_cyclic_root` は位数4の出典付き二倍関係を要求するため、位数2の今回の根へ直接使えるとは想定しない。これは既存規則の適用条件の監査であり、新たな一般規則を導入しない。

## テストと完了条件

`python -B -m pytest -q -p no:cacheprovider phase176_r3r20_cyclic_candidate_boundary/tests/test_audit.py` を限定実行。DryRun・本実行の両方が PASS し、型付き根 Goal の候補数、Hopf chain 数、対象群の出典付き specialization 数が取得できたら完了。全体 pytest は Phase 終了時のみ。
