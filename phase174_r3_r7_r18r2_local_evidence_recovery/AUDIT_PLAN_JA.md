# Phase 174 R3-R7-R18R2 監査計画

## 現象

`C:\Users\user\AppData\Local\EHPProofTracerAudit\phase174_r3_r7_r17\typed_map_public_audit.json` が存在せず、R18R1 は Source Guard の改行コード修正を適用できても R18 DryRun の前提監査に失敗した。R17 の証跡は以前の Windows アカウント側で生成されたため、現在の `LOCALAPPDATA` には存在しない。

## 変更ファイル・関数

- `phase174_r3_r7_r18_delta_image_surjectivity/audit.py`
  - `validate_prior_r17`：関数全体を置換。import、他の関数は不変。
- `phase174_r3_r7_r18r2_local_evidence_recovery/patch.py`：新規ファイル。変更対象と完全一致ハッシュを確かめる適用・復元機構。
- `phase174_r3_r7_r18r2_local_evidence_recovery/audit.py`：新規ファイル。R18 の本実行レポートと数学的境界を再検証。
- `phase174_r3_r7_r18r2_local_evidence_recovery/tests/test_evidence.py`, `tests/test_audit.py`：新規限定テスト。
- `run.ps1`：新規。`-DryRun` と本実行、失敗時の復元。

## 証拠の扱い

存在する監査 JSON は phase / gate / 新規 GIVEN / 全体 pytest の状態を検査する。不正な JSON はそのまま失敗とする。欠けている JSON があれば R17 `inspect_public_map_display()` を**実際に実行**し、公開 Root 候補、Delta 候補、循環的な同型候補、Web LaTeX、証明完成の不在を再検証する。旧 Gate の成功を捏造しない。R17R1 のテストソースは R18 の既存 Source Guard により Git Blob と一致することを確かめ、本実行では旧 Phase 173 の限定テストも実行する。

## 完了条件

- GitHub HEAD / ソース改行 / 改変対象が監査済み範囲内であること。
- R18R1 の改行修正も通過していること。
- R17 過去 JSON の有無にかかわらず正しい公開境界を再確認すること。
- 不正な JSON / 循環した証明 / 意図しない `GIVEN` を拒否すること。
- R18 の `PASS_ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY_FRONTIER` を実測確認すること。
- `PASS_R18_LIVE_R17_BOUNDARY_REVALIDATED_NO_PRIOR_JSON_COPY` が出ること。
- 新規数学的規則 0、結論直接 GIVEN 0、全体 pytest 未実施。R19 の公開接続は対象外。
