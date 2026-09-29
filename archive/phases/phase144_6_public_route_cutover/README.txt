Phase 144-6 Public Route Cutover
================================

目的
----
R5-43-11D までに完成した contribution-aware generic Narrative renderer を、
pi_6^3 の user-visible production route に接続する。

変更対象
--------
1. toda_group_proof_narrative_renderer.py
   - import:
     render_toda_group_proof_narrative_multi_argument_with_contributions_markdown
   - render_toda_group_proof_narrative_markdown()
     pi_6^3 branch の最終 renderer 呼び出しのみ切替

2. tests/test_phase144_6_public_route_cutover.py
   - 新規 focused regression

変更しない
----------
- main.py
- web_group_proof.py
- proof core
- ProofStep / InferenceRule / TodaProofEdge
- pi_8^5 / pi_15^8 等の既存 public route
- legacy helper の削除
- docs

理由
----
CLI と Web は既に render_toda_group_proof_narrative_markdown() を共有しているため、
public entry point 内の pi_6^3 branch を切り替えれば両方へ反映される。

実行
----
PowerShell で repository root に移動してから:

Expand-Archive `
  -Path "$HOME\Downloads\phase144_6_public_route_cutover.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_public_route_cutover\run_phase144_6_public_route_cutover.ps1"

focused regression が PASS した結果を確認後、Phase 144-6 最終 full suite へ進む。

この ZIP 自体では full suite は実行しない。
