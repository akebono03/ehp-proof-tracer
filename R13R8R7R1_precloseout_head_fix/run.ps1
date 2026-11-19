param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root
$baseline = 'b5a0b13884f6f0af527034d8c8bcd47b90c7cc97'
$head = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Cannot read Git HEAD' }
Write-Output "R13R8R7R1_LOCAL_HEAD=$head"
Write-Output "R13R8R7R1_GITHUB_BASELINE=$baseline"
$objects = @(
    @{Path='phase168_r3_37c_reference_projection.py'; Blob='a4140294f53c62972c35dd67fbfdfa1430232cae'},
    @{Path='phase168_r3_5_model_renderer.py'; Blob='f77616cf4ccc734954754e6e5d3a8d8b550dfef1'}
)
foreach ($entry in $objects) {
    $file = $entry.Path
    if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Missing production file: $file" }
    $headBlob = (git rev-parse "HEAD:$file").Trim()
    if ($LASTEXITCODE -ne 0) { throw "Cannot read committed blob: $file" }
    if ($headBlob -ne $entry.Blob) { throw "Committed production blob diverges from verified GitHub develop: $file ($headBlob)" }
    $indexBlob = (git rev-parse ":$file").Trim()
    if ($LASTEXITCODE -ne 0) { throw "Cannot read staged blob: $file" }
    if ($indexBlob -ne $entry.Blob) { throw "Staged production change: $file" }
    $workingBlob = (git hash-object -- $file).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Cannot hash working file: $file" }
    if ($workingBlob -ne $entry.Blob) { throw "Working production file differs from verified GitHub develop: $file" }
    $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $file).Path)
    $lf = 0; $crlf = 0
    for ($i = 0; $i -lt $bytes.Length; $i++) {
        if ($bytes[$i] -eq 10) {
            $lf++
            if ($i -gt 0 -and $bytes[$i - 1] -eq 13) { $crlf++ }
        }
    }
    Write-Output "R13R8R7R1_SOURCE_BLOB=PASS $file"
    Write-Output "R13R8R7R1_EOL=$file LF=$lf CRLF=$crlf"
    if ($crlf -gt 0 -and $crlf -ne $lf) { throw "Mixed CRLF/LF in $file" }
}
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'Unstaged git diff --check failed' }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'Staged git diff --check failed' }
if ($DryRun) {
    Write-Output 'R13R8R7R1_GATE=PASS_DRYRUN_VERIFIED_SOURCE_BLOBS'
    exit 0
}
$test = 'phase175_r4r12r13r8r6_binding_contract/tests/test_contract.py'
if (-not (Test-Path -LiteralPath $test -PathType Leaf)) { throw "Missing focused test: $test" }
python -m pytest -q $test
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
Write-Output 'R13R8R7R1_GATE=PASS_SOURCE_BLOBS_AND_FOCUSED_TESTS'
