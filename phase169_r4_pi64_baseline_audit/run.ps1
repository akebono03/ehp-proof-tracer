$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$package = $PSScriptRoot
Push-Location $root
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_ADDOPTS = '-p no:cacheprovider'
try {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw 'python is required'
    }
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'git is required'
    }
    $branch = (git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git branch check failed' }
    Write-Host "R4_GIT_BRANCH=$branch"
    if ($branch -ne 'develop') { throw 'R4 audit requires local develop; no changes made' }
    $head = (git rev-parse HEAD).Trim()
    Write-Host "R4_GIT_HEAD=$head"
    if ($head -ne 'ff08b601badf339457ff524ca21847b5d6a67ef5') {
        Write-Warning 'Local HEAD differs from the GitHub develop HEAD verified when ZIP was built. Review report and source before relying on findings.'
    }
    $beforeWorktree = @(git diff --name-only)
    $beforeIndex = @(git diff --cached --name-only)
    try {
        python -m pytest -q `
            (Join-Path $package 'tests\test_r4_audit.py') `
            (Join-Path $root 'phase169_r3o_toda45_composite_transport\tests\test_r3o_toda45_composite_transport.py')
        if ($LASTEXITCODE -ne 0) { throw 'R4 focused pytest failed' }
        python -m phase169_r4_pi64_baseline_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R4 audit failed; inspect output\audit.json' }
    }
    finally {
        $afterWorktree = @(git diff --name-only)
        $afterIndex = @(git diff --cached --name-only)
        if (($beforeWorktree -join "`n") -cne ($afterWorktree -join "`n") -or
            ($beforeIndex -join "`n") -cne ($afterIndex -join "`n")) {
            Write-Error 'Tracked Git changes detected during audit. Inspect git diff immediately.'
        }
    }
    Write-Host 'R4_AUDIT_ONLY=True'
    Write-Host 'R4_PRODUCTION_MODIFIED=False'
    Write-Host 'R4_FULL_PYTEST_RUN=False'
    Write-Host "R4_REPORT=$(Join-Path $package 'output\audit.md')"
} finally {
    Pop-Location
}
