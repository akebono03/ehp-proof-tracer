param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Root = (Resolve-Path (Join-Path $Package '..')).Path
$GitRoot = (& git -C $Root rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Not a Git repository' }
$ResolvedGitRoot = [IO.Path]::GetFullPath($GitRoot).TrimEnd([char]'\', [char]'/')
$ResolvedRoot = [IO.Path]::GetFullPath($Root).TrimEnd([char]'\', [char]'/')
if ($ResolvedGitRoot -ine $ResolvedRoot) { throw 'Extract ZIP at repository root' }

Write-Output 'PHASE173_R15R17_DOCS_SCOPE=FIVE_FULL_MARKDOWN_FILES_ONLY'
Write-Output 'PHASE173_R15R17_DOCS_GIT_RESET_CLEAN_STAGE_COMMIT=NONE'
Write-Output 'PHASE173_R15R17_DOCS_FULL_PYTEST=False'

& git -C $Root -c core.quotepath=false fetch origin develop
if ($LASTEXITCODE -ne 0) { throw 'git fetch failed' }

Push-Location $Root
try {
    Write-Output '=== PHASE173 R15R17 DOCUMENT PATCH CONTRACT TESTS ==='
    & python -B -m pytest -q -p no:cacheprovider '.\phase173_r15r17_document_checkpoint\tests\test_docs_builder.py'
    if ($LASTEXITCODE -ne 0) { throw 'Focused document test failed' }

    if ($DryRun) {
        & python -B -m phase173_r15r17_document_checkpoint.docs_builder --repo $Root --package $Package
    } else {
        & python -B -m phase173_r15r17_document_checkpoint.docs_builder --repo $Root --package $Package --apply
    }
    if ($LASTEXITCODE -ne 0) { throw 'Document generation failed' }
} finally {
    Pop-Location
}
