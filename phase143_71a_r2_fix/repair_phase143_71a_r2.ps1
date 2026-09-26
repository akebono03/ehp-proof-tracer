$ErrorActionPreference = "Stop"

$repo = (Get-Location).Path
$target = Join-Path $repo "toda_group_proof_narrative_argument_multi_renderer.py"

if (-not (Test-Path $target)) {
  throw "Run this script from the ehp-proof-tracer repository root."
}

$source = Get-Content -Raw -Encoding UTF8 $target

$broken = ")from toda_rules import ("
$fixed = ")`r`nfrom toda_rules import ("

if ($source.Contains($broken)) {
  $source = $source.Replace($broken, $fixed)
  Set-Content -Path $target -Value $source -Encoding UTF8
  Write-Host "Repaired missing import newline."
} elseif ($source.Contains(")`r`nfrom toda_rules import (") -or $source.Contains(")`nfrom toda_rules import (")) {
  Write-Host "Import newline is already correct."
} else {
  throw "Expected broken or repaired import boundary was not found. Stop and inspect the file."
}

python -m py_compile `
  ".\toda_group_proof_narrative_argument_multi_renderer.py" `
  ".\toda_group_proof_narrative_argument_body_renderer.py"

if ($LASTEXITCODE -ne 0) {
  throw "Python syntax check failed."
}

Write-Host "Phase 143-71A-R2 syntax repair complete."
