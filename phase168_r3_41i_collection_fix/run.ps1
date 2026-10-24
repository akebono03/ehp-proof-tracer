$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Target = Join-Path $Project "phase168_r3_41i_renderer_closure_audit\run.ps1"
$Output = Join-Path $PSScriptRoot "output"
$Backup = Join-Path $Output "run.ps1.before"
$Report = Join-Path $Output "collection_fix_report.txt"
$ReferenceRunner = Join-Path $PSScriptRoot "full_files\phase168_r3_41i_renderer_closure_audit\run.ps1"
$PackageTest = Join-Path $PSScriptRoot "tests\test_collection_fix.py"
$AuditBundle = Join-Path $Project "phase168_r3_41i_renderer_closure_audit\output\review_bundle.zip"

New-Item -ItemType Directory -Force -Path $Output | Out-Null
if (-not (Test-Path -LiteralPath $Target -PathType Leaf)) {
    throw "R3-41I runner not found: $Target"
}

$Watched = @(
    "web_group_proof.py",
    "phase165_r52_r4_flask_bridge.py",
    "phase165_r52_r3_web_adapter.py",
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_29_order_projection.py",
    "phase168_narrative_baseline_frozen\pi3_2_original.txt",
    "phase168_narrative_baseline_frozen\pi4_3_original.txt",
    "phase168_narrative_baseline_frozen\pi5_4_original.txt"
)
$BeforeHashes = @{}
foreach ($Relative in $Watched) {
    $Source = Join-Path $Project $Relative
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Required source/baseline not found: $Source"
    }
    $BeforeHashes[$Relative] = (Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash
}

$OriginalBytes = [System.IO.File]::ReadAllBytes($Target)
$OriginalHash = (Get-FileHash -LiteralPath $Target -Algorithm SHA256).Hash
$Decoder = [System.Text.UTF8Encoding]::new($false, $true)
$Encoder = [System.Text.UTF8Encoding]::new($false)
$OriginalText = $Decoder.GetString($OriginalBytes)
$Needle = 'python -m pytest -q `'
$Replacement = 'python -m pytest -q --import-mode=importlib `'
$Changed = $false
$Successful = $false
$ErrorMessage = ""

Push-Location $Project
try {
    python -m pytest -q --import-mode=importlib $PackageTest
    if ($LASTEXITCODE -ne 0) {
        throw "Collection-fix package tests failed."
    }

    if ($OriginalText.Contains($Replacement)) {
        Write-Host "R3-41I runner already uses --import-mode=importlib."
    }
    elseif ($OriginalText.Contains($Needle)) {
        $UpdatedText = $OriginalText.Replace($Needle, $Replacement)
        [System.IO.File]::WriteAllBytes($Backup, $OriginalBytes)
        $Changed = $true
        [System.IO.File]::WriteAllBytes($Target, $Encoder.GetBytes($UpdatedText))
        Write-Host "PATCHED $Target"
        Write-Host "BACKUP $Backup"
    }
    else {
        throw "Unexpected R3-41I run.ps1 format; no patch applied."
    }

    $ExpectedRunnerText = [System.IO.File]::ReadAllText($ReferenceRunner, $Decoder)
    $ActualRunnerText = [System.IO.File]::ReadAllText($Target, $Decoder)
    if (($ActualRunnerText -replace "`r`n", "`n") -ne ($ExpectedRunnerText -replace "`r`n", "`n")) {
        # The runner is allowed to contain harmless local changes, but must
        # preserve exactly the three intended focused tests and the audit entrypoint.
        $Required = @(
            'phase168_r3_41i_renderer_closure_audit\tests\test_audit.py',
            'phase168_r3_39f_frozen_comparison\tests\test_audit.py',
            'phase168_r3_19_web_model_default\tests\test_phase168_r3_19_web_model_default.py',
            'python -m phase168_r3_41i_renderer_closure_audit.audit'
        )
        foreach ($Part in $Required) {
            if (-not $ActualRunnerText.Contains($Part)) {
                throw "Unexpected runner: required limited audit target missing: $Part"
            }
        }
    }

    powershell -NoProfile -ExecutionPolicy Bypass -File $Target
    if ($LASTEXITCODE -ne 0) {
        throw "R3-41I audit runner returned $LASTEXITCODE"
    }

    foreach ($Relative in $Watched) {
        $AfterHash = (Get-FileHash -LiteralPath (Join-Path $Project $Relative) -Algorithm SHA256).Hash
        if ($AfterHash -ne $BeforeHashes[$Relative]) {
            throw "Read-only verification failed: $Relative changed"
        }
    }
    if (-not (Test-Path -LiteralPath $AuditBundle -PathType Leaf)) {
        throw "R3-41I review bundle not found: $AuditBundle"
    }
    $Successful = $true
    Write-Host "R3-41I scoped audit complete. Full pytest NOT run."
    Write-Host "UPLOAD_BUNDLE $AuditBundle"
}
catch {
    $ErrorMessage = $_.Exception.Message
    if ($Changed) {
        [System.IO.File]::WriteAllBytes($Target, $OriginalBytes)
        Write-Warning "R3-41I run.ps1 restored from the exact original bytes."
    }
}
finally {
    Pop-Location
    $State = if ($Successful) { "SUCCESS" } else { "FAILED (runner rolled back if modified)" }
    $CurrentHash = (Get-FileHash -LiteralPath $Target -Algorithm SHA256).Hash
    $Lines = @(
        "Phase 168 R3-41I collection fix",
        "Result: $State",
        "Only intended runner change: add --import-mode=importlib",
        "Runner before SHA256: $OriginalHash",
        "Runner after SHA256: $CurrentHash",
        "Source/baseline snapshot: nine watched files",
        "Repository-wide pytest: NOT RUN",
        "Audit bundle: $AuditBundle",
        "Error: $ErrorMessage"
    )
    $Lines | Set-Content -LiteralPath $Report -Encoding UTF8
    Write-Host "COLLECTION_FIX_REPORT $Report"
}
if (-not $Successful) {
    throw "R3-41I collection fix / audit failed: $ErrorMessage"
}
