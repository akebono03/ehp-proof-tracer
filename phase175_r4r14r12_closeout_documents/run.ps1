param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase175_r4r14r12_closeout_documents.build_documents --dry-run
    } else {
        python -B -m phase175_r4r14r12_closeout_documents.build_documents
    }
    if ($LASTEXITCODE -ne 0) { throw 'R4R14R12 document generation failed' }
    if (-not $DryRun) {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase175_r4r14r12_closeout_documents/tests
        if ($LASTEXITCODE -ne 0) { throw 'R4R14R12 focused tests failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'R4R14R12 git diff check failed' }
        Write-Output 'R4R14R12_OUTPUT=phase175_r4r14r12_closeout_documents/output/'
        Write-Output 'R4R14R12_FULL_PYTEST=NOT_RUN'
        Write-Output '(END)'
    }
} finally {
    Pop-Location
}
