# Phase 173 R4-R15R11 設計記録

## 対象と目的

R15R10 で確認した `MODEL_HAS_ABSTRACT=False` に対応する。対象は共通 Narrative Model（証明文章モデル）のデータ受け渡しと表示であり、証明探索・既存 DB・新しい数学規則は対象外。

## 既存コードの監査

GitHub `develop` HEAD `7e9e00f42e8b125480cd2928b0ee7ec2c5269d3a` と関連モジュール・既存テストを確認した。

- `PartialProofResult.abstract_structure` は `CertifiedAbstractStructure` によって検証済み。
- `ProofNarrativeModel` は従来 `abstract_structure` を持たない。
- `phase165_r52_r3_web_adapter.py` はモデル/互換 Renderer の後で抽象節を追加する。
- `phase168_r3_5_model_renderer.py` は既存の Model-backed Narrative を生成する。
- 旧 R15R9 のモデル経由、Legacy（従来互換）、Trace（証明手順）の挙動を維持する。

## 変更対象（4ファイル）

1. `phase168_r3_3_proof_narrative_model.py`：`ProofNarrativeModel` クラス、`build_proof_narrative_model` 関数、import。
2. `phase168_r3_5_model_renderer.py`：既存 `render_model_backed_narrative_markdown` 関数全体を置換。関数内で Model の検証済み抽象節を生成し、後付けの別 Renderer を増やさない。
3. `phase173_r4_r15r9_shared_abstract_renderer/projection.py`：`render_certified_abstract_section` 関数全体、`_render_abstract_claim` と `render_certified_abstract_model_section` の新規追加（既存関数の直後）。
4. `phase165_r52_r3_web_adapter.py`：`build_partial_web_group_proof_view` 関数全体を置換。既存 import は不変。

## 数学的境界

`CertifiedAbstractStructure` の型付き証明をそのまま Model に引き渡す。出典を再探索しない。記名生成元等式を仮定として追加しない。`status`、`conclusion`、`open_goals`、`references` は元の検索結果のままとする。通常 Web は引き続き `generic-partial-proof` とし、未解決 Goal は消さない。

## テスト／完了条件

DryRun で4ファイルのコード整合性と AST（抽象構文木）を検証。実適用後は限定 pytest で抽象群表示が重複しないことと完成証明の維持を確認する。`MODEL_HAS_ABSTRACT=True`、`ABSTRACT_SECTION_COUNT=1`、`NAMED_PENDING=True` が両方の対象群で得られ、Web Adapter に専用分岐がないことを条件とする。

## 次工程との境界

今回の Model 統合は抽象節の単一生成に限る。抽象 ProofStep の Citation（引用）を既存の記名生成元証明用 Reference にどのように統合するかは、別途証拠範囲を監査してから判断する。完成判定の一般化や未証明の生成元同定は先取りしない。

## R15R11R1 HEAD 整合性修正（2026-11-03）

- GitHub `develop` HEAD が `8bfa1394` から `7e9e00f4` に進行。
- 比較結果：追加1コミットは R15R10 の監査パッケージのみ。本番対象4ファイルは変更されていない。
- 現行4ファイルの Git Blob SHA を再取得し、既存 `EXPECTED_BLOBS` の4件と完全一致。
- `patch.py` と `run.ps1` の期待 HEAD を `7e9e00f4` に更新。既存の変換関数・対象ファイル・数学的意味・限定 pytest は変更しない。
- `run.ps1` にはローカル HEAD 整合性を明示する検査と `HEAD_LINEAGE=PASS` の出力を追加。
- ローカル HEAD の差異がある場合は停止する。自動的な reset、checkout、pull はしない。
- R15R11R1 は HEAD 修正工程であり、Phase 173 の完了工程ではない。

## R15R11R2 — 再適用時の fail-closed 修正（2026-11-03）

- **実測障害**：`test_patch_is_fail_closed_on_repetition_and_crlf` が「DID NOT RAISE RuntimeError」で失敗。DryRun 中のため本番ファイル変更なし。
- **根本原因**：`_patch_model_renderer()` の置換後文字列に、置換前アンカー `incomplete = result.status ...` と終端の Goal 文が残るため、2回目も置換できてしまう。証明モデル一致検査を二重挿入する可能性があった。
- **変更対象**：`phase173_r4_r15r11_model_abstract_integration/patch.py` の `_replace_once()` 全体、および `tests/test_static.py` の新規テスト関数1件。新規テストは既存の繰り返し適用テストに加えて、問題の重複を単独再現する。
- **修正内容**：`after in source` の場合、アンカー検索に先立って `RuntimeError` で拒否する。既存のアンカー件数検査および CRLF 対応を変更しない。
- **本番変更なし**：提案済みの4ファイルに対する変換内容、数学的論理、参照、Status、公開 Web Adapter の挙動を変更しない。
- **HEAD・Blob**：HEAD `7e9e00f4` と既存4つの Git Blob SHA を維持。Source Guard を省略しない。
- **検証**：局所再現・再適用拒否・CRLF・構文検査、そしてユーザー環境で既存の `test_static.py` を再実行。全体 pytest は Phase 173 終了時のみ。
- **次工程境界**：R15R11 の元来の Model 統合の限定 pytest と Web 監査は、修正版の DryRun を PASS した後にのみ実施する。R15R11 の完了は現段階で宣言しない。
