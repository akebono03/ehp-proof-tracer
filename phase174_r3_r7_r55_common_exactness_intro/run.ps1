param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r55_common_exactness_intro.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55 source review failed' }
    python -B -m phase174_r3_r7_r55_common_exactness_intro.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55 guarded patch DryRun failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R55_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r55_common_exactness_intro.patch
    if ($LASTEXITCODE -ne 0) { throw 'R55 guarded renderer install failed' }
    python -B -m phase174_r3_r7_r55_common_exactness_intro.audit
    if ($LASTEXITCODE -ne 0) { throw 'R55 in-process HTTP audit failed' }
    $Groups = @(
        @{Name='R55_PATCH'; Path='phase174_r3_r7_r55_common_exactness_intro/tests/test_patch.py'},
        @{Name='R55_STATIC'; Path='phase174_r3_r7_r55_common_exactness_intro/tests/test_static.py'},
        @{Name='R55_HTTP'; Path='phase174_r3_r7_r55_common_exactness_intro/tests/test_http.py'},
        @{Name='R54_HTTP_REGRESSION'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_http.py'},
        @{Name='R54_HTML_PARSER_REGRESSION'; Path='phase174_r3_r7_r54_public_http_narrative_audit/tests/test_html_parser.py'},
        @{Name='R53_PROOF_REGRESSION'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_public.py'},
        @{Name='R52_PROBE_REGRESSION'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R55_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R55 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R55_RUN=PASS'
    Write-Output 'PHASE174_R3R7R55_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
