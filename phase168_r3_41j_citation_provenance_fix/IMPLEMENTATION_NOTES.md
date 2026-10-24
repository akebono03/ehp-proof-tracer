# Phase 168 R3-41J — 変更一覧と境界

## 変更対象

- 本体: `phase168_r3_5_model_renderer.py`
- 変更関数: `render_model_backed_narrative_markdown()`（関数全体を同梱）
- 本体ファイルの最上位 import: 変更なし
- 関数内 import: `GeneratorSuspension`、`_eta_pair`、`TodaEtaFamilyGeneralDefinition`、`TodaProp42GeneralExactnessStatement` を追加
- 関数内の新規局所関数: `cited_general_ancestor_numbers()`（既存関数内部、`body_by_step` の直後）
- 新規限定テスト: `tests/test_phase168_r3_41j_citation_provenance.py`（全体を同梱）
- 本文生成の変更: 型付き ProofStep の前提として実際に出現する GIVEN に紐づく Reference 番号を、統合された EHP 完全列および η 系列の GeneratorSuspension に表示

## 不変事項

- 型付き Backward Search / Proof Tree / Proof Narrative Model / Reference 台帳を変更しない。
- 命題名の文字列探索から Reference を補わない。
- 固定基準の本文、出典の原文、証明対象の群構造を変更しない。
- `legacy` 経路と未完成証明の表示を変更しない。
- 新たな群専用文章、命題、証明ステップは作成しない。

## 実行する限定 pytest

`run.ps1` から `--import-mode=importlib` を使用し、次の4ファイルだけを実行する。

1. `phase168_r3_41j_citation_provenance_fix/tests/test_phase168_r3_41j_citation_provenance.py`
2. `phase168_r3_41i_renderer_closure_audit/tests/test_audit.py`
3. `phase168_r3_26a_after_r3_25a/tests/test_phase168_r3_26_projection.py`
4. `phase168_r3_19_web_model_default/tests/test_phase168_r3_19_web_model_default.py`

その後、R3-41I 監査を本パッケージの `output` に対して再実行する。以前の R3-41I 監査出力は上書きしない。

## 完了条件

- 限定 pytest がすべて PASS。
- 3群の `references_not_explicitly_tagged_in_proof` がすべて空。
- 3群の `missing_benchmark_explanations` と `missing_body_locators` がすべて空。
- Web の既存経路契約9項目がすべて True。
- 実装と固定基準は監査中に変化しない。
- 実行に失敗した場合は本体ファイルを事前バックアップからバイト単位で復元する。

## 次作業との境界

- 「導出により」の言い換え、冗長な中間記述の抑制、説明の詳しさの調整は今回変更しない。
- 新規証明探索機能、有限巡回群構造の未解決課題は別 Phase で扱う。
- 固定基準との文章全体の一致は引き続き人手監査を要する。
- 全体 pytest は Phase 168 終了時にのみ実行する。
