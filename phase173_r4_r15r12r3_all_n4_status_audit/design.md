# Phase 173 R4-R15R12R3：全33群の読み取り専用監査設計

## 目的

`data/sphere.csv` の n=4 に明記された k=1〜33 を対象に、登録済み群構造と、実際の証明探索・公開 Web の検証結果を分離して報告する。k≥8 の26群について、証明済み／抽象構造のみ／未完成／実行エラーを実測で区別する。

## 既存コードの事前確認

GitHub `develop` HEAD `715dff58df263c419cdcb45c51a1fa169a87de45` の以下を確認した。

- `phase165_r55_nk_only_goal.py`: `search_group_from_registered_goal`
- `phase169_r10e4_ordered_db_prior/db_prior.py`: `exact_prior_database_result`
- `web_group_proof.py`: `build_standard_web_group_proof_view`、完成時の Trust Boundary（証明検査）
- `phase165_r52_r3_web_adapter.py`: Model-backed Web 経路
- `phase168_r3_3_proof_narrative_model.py` と `phase168_r3_5_model_renderer.py`: Proof Tree に基づく引用・表示と未解決 Goal の表示
- `phase173_r4_r10_general_toda56_core/core.py`: 抽象群と記名生成元の対応に関するそれぞれの必要条件を判定
- `phase173_r4_r15r7_source_first_abstract_certificate/search.py` と `phase173_r4_r15r8_public_abstract_sidecar/attach.py`: 記名生成元を完成扱いにしない独立抽象群証明
- `phase173_r4_r15r12_reference_correction/tests/test_integration.py`、`phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py`: 完成群と未完成群を区別する既存の限定テスト

## 変更・追加対象

既存ファイル、既存クラス、既存関数・既存テストは**変更しない**。新規ディレクトリ `phase173_r4_r15r12r3_all_n4_status_audit/` のみ追加する。

- `audit.py`: `discover_registered_n4`, `classify_observed_status`, `compact_text`, `view_text`, `inspect_registered_group`, `make_summary`, `render_markdown`, `main` を新規追加
- `tests/test_contract.py`: `test_registered_n4_uses_only_explicit_sphere_csv_rows`, `test_status_contract_never_promotes_unproven_named_generators`, `test_summary_keeps_abstract_only_separate_from_named_complete` を新規追加
- `run.ps1`: HEAD / Blob Source Guard、DryRun、読み取り専用全件実行
- `README.md`（英語）、`design.md`（日本語）、`SOURCE_CODE.md`（完全なコード全文）

## 判定条件

`NAMED_COMPLETE` は Search COMPLETE、conclusionあり、open goals 0、公開 Web `generic-complete-proof` かつ `partial_result=False` の同時成立時のみ。

`ABSTRACT_ONLY_NAMED_PENDING` は未完成・公開 Web partial と独立証明済み抽象群構造の併存時のみ。記名生成元は未証明のまま維持する。

`NAMED_PENDING_NO_ABSTRACT` は未完成で独立抽象群構造の証明を確認できない場合。

また `abstract_input_compatible` と `named_generator_shape_compatible` は必要条件の一致だけを表し、それだけで完成証明とはしない。

`INCONSISTENT_SEARCH_WEB` と `NOT_VERIFIED_ERROR` は実行上・検査上の不整合であり、数学的な未証明とは区別する。

## Phase 境界

R15R12R3 は監査だけを行う。R15R13 の見出し重複の修正、未解決 Goal の数式対応、証明探索の追加規則は実装しない。全体 pytest は Phase 173 の終了時だけ実施する。
