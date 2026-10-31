param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OriginalNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$OriginalPluginAutoload = $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD
$OriginalReport = $env:EHP_R20R2R2_PROBE_REPORT
$TestPath = '.\phase165_r52_r15_ordered_citation\test_phase165_r52_r15_ordered_citation.py'
$First = $TestPath + '::test_ordered_reference_requires_only_prior_order'
$Second = $TestPath + '::test_ordered_reference_integrates_with_backward_search'

Push-Location $Root
try {
    if ((& git branch --show-current).Trim() -ne 'develop') {
        throw 'Expected develop branch; no changes made.'
    }
    if (-not (Test-Path -LiteralPath $TestPath -PathType Leaf)) {
        throw 'Existing ordered citation test file was not found.'
    }
    if (-not (Test-Path -LiteralPath '.\phase165_r52_r15_ordered_citation.py' -PathType Leaf)) {
        throw 'Production ordered citation module was not found.'
    }
    if (-not (Test-Path -LiteralPath '.\phase165_r3_recursive_search.py' -PathType Leaf)) {
        throw 'Production recursive search module was not found.'
    }
    Write-Host 'PHASE171_R20R2R2_MODE=AUDIT_ONLY'
    Write-Host ('PHASE171_R20R2R2_HEAD=' + ((& git rev-parse HEAD).Trim()))
    Write-Host 'PHASE171_R20R2R2_SOURCE_CHANGES=0'
    if ($DryRun) {
        Write-Host 'PHASE171_R20R2R2_DRY_RUN=PASS'
        return
    }
    $Output = Join-Path $PSScriptRoot ('output\' + (Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'))
    New-Item -ItemType Directory -Path $Output -Force | Out-Null
    Write-Host ('PHASE171_R20R2R2_REPORT_DIR=' + $Output)
    $env:PYTHONDONTWRITEBYTECODE = '1'

    $Modes = @(
        @{ Name = 'prepend'; ImportMode = 'prepend'; DisablePlugins = $false },
        @{ Name = 'importlib'; ImportMode = 'importlib'; DisablePlugins = $false },
        @{ Name = 'prepend_no_external_plugins'; ImportMode = 'prepend'; DisablePlugins = $true }
    )
    foreach ($Mode in $Modes) {
        $env:EHP_R20R2R2_PROBE_REPORT = Join-Path $Output ($Mode.Name + '.jsonl')
        if ($Mode.DisablePlugins) {
            $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
        } else {
            if ($null -eq $OriginalPluginAutoload) {
                Remove-Item Env:PYTEST_DISABLE_PLUGIN_AUTOLOAD -ErrorAction SilentlyContinue
            } else {
                $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = $OriginalPluginAutoload
            }
        }
        Write-Host ('PHASE171_R20R2R2_TEST_MODE=' + $Mode.Name)
        & python -B -m pytest -q -s -p no:cacheprovider `
            -p phase171_r20r2r2_pytest_context_probe.probe_plugin `
            ('--import-mode=' + $Mode.ImportMode) `
            $First $Second
        $ExitCode = $LASTEXITCODE
        Write-Host ('PHASE171_R20R2R2_TEST_EXIT_' + $Mode.Name + '=' + $ExitCode)
        if (-not (Test-Path -LiteralPath $env:EHP_R20R2R2_PROBE_REPORT -PathType Leaf)) {
            Write-Host ('PHASE171_R20R2R2_PROBE_MISSING_' + $Mode.Name + '=TRUE')
        }
    }
    Write-Host 'PHASE171_R20R2R2_DIAGNOSTIC_FINISHED=TRUE'
    Write-Host ('PHASE171_R20R2R2_REPORT_DIR=' + $Output)
    & git status -sb
    & git diff --stat
}
finally {
    if ($null -eq $OriginalNoBytecode) {
        Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue
    } else {
        $env:PYTHONDONTWRITEBYTECODE = $OriginalNoBytecode
    }
    if ($null -eq $OriginalPluginAutoload) {
        Remove-Item Env:PYTEST_DISABLE_PLUGIN_AUTOLOAD -ErrorAction SilentlyContinue
    } else {
        $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = $OriginalPluginAutoload
    }
    if ($null -eq $OriginalReport) {
        Remove-Item Env:EHP_R20R2R2_PROBE_REPORT -ErrorAction SilentlyContinue
    } else {
        $env:EHP_R20R2R2_PROBE_REPORT = $OriginalReport
    }
    Pop-Location
}
