param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r54_public_http_narrative_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R54 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R54_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r54_public_http_narrative_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R54 in-process HTTP audit failed' }
    $Groups = @(
        @{Name='R54_STATIC'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_static.py'},
        @{Name='R54_PARSER'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_html_parser.py'},
        @{Name='R54_GUARD'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_guard.py'},
        @{Name='R54_HTTP'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_http.py'},
        @{Name='R53_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_public.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R54_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R54 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R54_RUN=PASS'
    Write-Output 'PHASE174_R3R7R54_PRODUCTION_FILES_CHANGED=0'
    Write-Output 'PHASE174_R3R7R54_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
