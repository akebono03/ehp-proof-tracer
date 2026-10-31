# Phase 172 R1：AUDIT_ONLY（監査計画）

## 対象と境界

対象は $\pi_6^3=\mathbb Z/4\{\nu'\}$ の完成済み証明の表示経路に限定する。既存の証明探索・数学的規則・出典・Proof Tree・Renderer・既存テストを一切変更しない。今後の R2〜R5 の修正を先取りしない。

## GitHub における事前確認

2026年10月31日、GitHub `akebono03/ehp-proof-tracer` の `develop` を指定して、共通 Renderer、ProofNarrativeModel、Web Adapter、Phase 171 の完成証明整形処理、関連テストの内容と blob SHA を確認した。引継ぎに記録された Phase 171 最終コミットは `a64edd93e0df561b0970d482c6b2bd0ec72b2344`。リポジトリ履歴には後続の `845508ddf8f3bc30fa8a51349c065c7551eb893a`（マージ）も存在するが、全リポジトリ履歴は `develop` の先端そのものを保証しない。実行時に `git ls-remote origin refs/heads/develop` とローカル HEAD を照合する。

確認済みの現行経路：`web_group_proof.build_standard_web_group_proof_view()` → `search_group_from_registered_goal()` → `verify_proof_tree_for_narrative()` → `build_linked_proof_narrative_model()` → `render_model_backed_narrative_markdown()` → `build_partial_web_group_proof_view()`。後段で `verified_order_four_summary()`、`suppress_exact_duplicate_body_lines()`、`format_complete_proof_sentences()` が使用される。

## 監査用追加ファイル

- `phase172_r1_renderer_audit/audit.py`：新規関数 `git`, `get_git_value`, `preflight`, `safe_repr`, `math_fragments`, `display_categories`, `locate_premises`, `build_step_inventory`, `align_body_lines`, `duplicate_inventory`, `capture_canonical_proof`, `report_directory`, `save_json`, `formatted_findings`, `run_focused_tests`, `main` を追加。
- `phase172_r1_renderer_audit/run.ps1`：PowerShell Runner を追加。
- `phase172_r1_renderer_audit/tests/test_audit.py`：診断に関する4件の単体テストを追加。
- `phase172_r1_renderer_audit/__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md` を追加。

**変更する既存ファイル、既存クラス、既存メソッド、既存 import：なし。** 新規ファイルはすべてリポジトリ直下の上記ディレクトリに配置する。

## 出力と監査項目

1. 監査対象ソースの Git blob と状態、ローカル・リモート HEAD。
2. 完成 Web view の key、Proof Tree の根と祖先、各 ProofStep の型・結論・前提・Citation 番号。
3. Web 証明全文と構造化描画行、Reference の locator・statement bodies・紐づく ProofStep。
4. 懸垂 $E(\eta_5)=\eta_6$ の重複候補、Hopf 関係の説明、全射性、`DB prior` などの出典表記。
5. 同一行と同一数式の反復は区別して記録する。数式一致だけで不要な重複や証明の唯一性を宣言しない。

## Gate と次工程

R1 完了条件は Reviewed content PASS、実際の Proof Search `complete`、未解決 Goal 0、Trust Boundary PASS、Web `generic-complete-proof`、Reference 8件、出力ファイル生成、既存ソース変更0。任意の限定 pytest に失敗した場合は報告し、全体 pytest は実行しない。

R2〜R5 は監査された実際の文・ProofStep と Reference の対応を確認してから変更範囲を決める。R6 の Phase 末尾のみ全体 pytest を実行する。
