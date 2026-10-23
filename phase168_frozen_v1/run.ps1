$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Target = Join-Path $Project 'phase168_narrative_baseline_frozen'
New-Item -ItemType Directory -Force -Path $Target | Out-Null
$Files = @('pi3_2_original.txt','pi4_3_original.txt','pi5_4_original.txt','README.md','BASELINE_POLICY.md','SHA256SUMS.txt')
foreach ($Name in $Files) {
  $Source = Join-Path $PSScriptRoot $Name
  $Dest = Join-Path $Target $Name
  if (Test-Path $Dest) {
    if ((Get-FileHash $Source -Algorithm SHA256).Hash -ne (Get-FileHash $Dest -Algorithm SHA256).Hash) {
      throw "Baseline differs; refusing overwrite: $Dest"
    }
    Write-Host "UNCHANGED: $Dest"
  } else {
    Copy-Item -LiteralPath $Source -Destination $Dest
    Write-Host "SAVED: $Dest"
  }
}
Write-Host 'Frozen baseline saved. References are not frozen. No pytest was run.'
