param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $root
$expected = 'b5a0b13884f6f0af527034d8c8bcd47b90c7cc97'
$head = (git rev-parse HEAD).Trim()
Write-Output "R13R8R7_LOCAL_HEAD=$head"
if ($head -ne $expected) { throw "HEAD mismatch: expected $expected" }
$files = @('phase168_r3_37c_reference_projection.py','phase168_r3_5_model_renderer.py')
foreach ($file in $files) {
  if (-not (Test-Path $file)) { throw "Missing $file" }
  $changed = @(git diff --name-only HEAD -- $file)
  if ($changed.Count -gt 0) { throw "Production file modified: $file" }
  $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $file).Path)
  $crlf = 0; $lf = 0
  for ($i=0; $i -lt $bytes.Length; $i++) {
    if ($bytes[$i] -eq 10) { $lf++; if ($i -gt 0 -and $bytes[$i-1] -eq 13) { $crlf++ } }
  }
  Write-Output "R13R8R7_EOL=$file LF=$lf CRLF=$crlf"
  if ($crlf -gt 0 -and $crlf -lt $lf) { throw "Mixed EOL: $file" }
}
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed' }
if ($DryRun) { Write-Output 'R13R8R7_GATE=PASS_DRYRUN_LOCAL_GUARDS'; exit 0 }
python -m pytest -q phase175_r4r12r13r8r6_binding_contract/tests/test_contract.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Output 'R13R8R7_GATE=PASS_LOCAL_GUARDS_AND_FOCUSED_TESTS'
