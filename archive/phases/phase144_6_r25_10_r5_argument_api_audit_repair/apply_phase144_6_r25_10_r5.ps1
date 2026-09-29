$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$AuditDir = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit"
$AuditPath = Join-Path $AuditDir "audit_phase144_6_r25_10.py"

if (-not (Test-Path $AuditPath)) {
  throw "R25-10 audit script not found: $AuditPath"
}

$content = Get-Content -Raw -Encoding UTF8 $AuditPath

$old = 'for i,x in enumerate(a): print(f"  argument[{i}] role={x.role.value} conclusion={x.conclusion_block_id}")'
$new = 'for i,x in enumerate(a): print(f"  argument[{i}] role={x.role.value} conclusion_block_role={x.conclusion_block.role.value} conclusion_steps={len(x.conclusion_block.steps)}")'

if ($content.Contains($old)) {
  $content = $content.Replace($old, $new)
  Set-Content -Path $AuditPath -Value $content -Encoding UTF8
  Write-Host "R25-10-R5 audit harness repair applied."
}
elseif ($content.Contains($new)) {
  Write-Host "R25-10-R5 audit harness repair already applied."
}
else {
  throw "Expected R25-10 Section F line was not found. No file was changed."
}

Write-Host "Production code changes: none."
Write-Host "Existing test changes: none."
