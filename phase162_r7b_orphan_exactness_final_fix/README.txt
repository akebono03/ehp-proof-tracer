Phase 162 R7-B: orphan exactness introduction - final public boundary fix

Diagnosis: the earlier cleanup ran during the contribution renderer, before the
final public narrative was assembled. The integration regression still found
orphaned introductions. This patch runs the already-tested cleanup on the
finished non-stable public narrative, leaving the stable-specialized path alone.

Changed production file: toda_group_proof_narrative_renderer.py
Changed: imports from toda_group_proof_narrative_contribution_renderer (add
suppress_toda_group_proof_narrative_dangling_connectors) and FINAL definition
of render_toda_group_proof_narrative_markdown.

Unchanged: proof trees, inference rules, citations, and the existing R7-B helper.

Run in PowerShell from repository root:
Expand-Archive -Path "$HOME\Downloads\phase162_r7b_orphan_exactness_final_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r7b_orphan_exactness_final_fix\run.ps1"

Focused tests only. Do not run the full suite until Phase 162 completion.
