$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$BundleDir = Join-Path $RepoRoot "phase167_r4_3_homomorphism_theorem"

Write-Host "=== Phase 167 R4-3: patch ==="
python (Join-Path $BundleDir "patch.py")

Write-Host ""
Write-Host "=== Phase 167 R4-3: limited pytest ==="
python -m pytest `
  (Join-Path $BundleDir "test_phase167_r4_3_homomorphism_theorem.py") `
  -q

Write-Host ""
Write-Host "=== Phase 167 R4-3: source phrase audit ==="
python -c "from pathlib import Path; s=Path('toda_group_proof_narrative_renderer.py').read_text(encoding='utf-8'); assert '全射性と核の決定から, 第一同型定理より $' not in s; assert s.count('全射性と核の決定から, 準同型定理より $') == 1; print('SOURCE_AUDIT_OK')"

Write-Host ""
Write-Host "Phase 167 R4-3 limited verification completed."
Write-Host "Full pytest is intentionally NOT run in this bundle."
