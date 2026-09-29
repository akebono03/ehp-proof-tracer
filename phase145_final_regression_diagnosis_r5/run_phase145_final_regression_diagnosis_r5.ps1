$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 145 Final Regression Diagnosis R5"
Write-Host "Locate the three unresolved canonical test dependencies"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Archive changes: none"
Write-Host "=============================================================="

$targets = @(
    "test_phase143_19_method_evidence.py",
    "test_phase75_515_pi15_8_final_group.py",
    "test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"
)

Write-Host ""
Write-Host "A. Repository root"
Write-Host "--------------------------------------------------------------"
Write-Host (Get-Location).Path
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD

Write-Host ""
Write-Host "B. Physical file search in current worktree"
Write-Host "--------------------------------------------------------------"
foreach ($name in $targets) {
    Write-Host ""
    Write-Host "TARGET: $name"

    $matches = Get-ChildItem `
        -Path "." `
        -Filter $name `
        -File `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue |
        Sort-Object FullName

    if ($matches.Count -eq 0) {
        Write-Host "  physical matches: NONE"
    }
    else {
        Write-Host "  physical matches: $($matches.Count)"
        foreach ($match in $matches) {
            Write-Host "  $($match.FullName)"
        }
    }
}

Write-Host ""
Write-Host "C. Git index / tracked-path search"
Write-Host "--------------------------------------------------------------"
$tracked = @(git ls-files)
foreach ($name in $targets) {
    Write-Host ""
    Write-Host "TARGET: $name"

    $matches = @(
        $tracked |
        Where-Object {
            [System.IO.Path]::GetFileName($_) -eq $name
        }
    )

    if ($matches.Count -eq 0) {
        Write-Host "  git ls-files matches: NONE"
    }
    else {
        Write-Host "  git ls-files matches: $($matches.Count)"
        foreach ($match in $matches) {
            Write-Host "  $match"
        }
    }
}

Write-Host ""
Write-Host "D. Git HEAD tree search"
Write-Host "--------------------------------------------------------------"
$headTree = @(git ls-tree -r --name-only HEAD)
foreach ($name in $targets) {
    Write-Host ""
    Write-Host "TARGET: $name"

    $matches = @(
        $headTree |
        Where-Object {
            [System.IO.Path]::GetFileName($_) -eq $name
        }
    )

    if ($matches.Count -eq 0) {
        Write-Host "  HEAD matches: NONE"
    }
    else {
        Write-Host "  HEAD matches: $($matches.Count)"
        foreach ($match in $matches) {
            Write-Host "  $match"
        }
    }
}

Write-Host ""
Write-Host "E. Git history path-name search"
Write-Host "--------------------------------------------------------------"
foreach ($name in $targets) {
    Write-Host ""
    Write-Host "TARGET: $name"

    $historyMatches = @(
        git log --all --name-only --pretty=format: |
        Where-Object {
            $_ -and ([System.IO.Path]::GetFileName($_) -eq $name)
        } |
        Sort-Object -Unique
    )

    if ($historyMatches.Count -eq 0) {
        Write-Host "  history path matches: NONE"
    }
    else {
        Write-Host "  history path matches: $($historyMatches.Count)"
        foreach ($match in $historyMatches) {
            Write-Host "  $match"
        }
    }
}

Write-Host ""
Write-Host "F. Archive directory inventory around likely phases"
Write-Host "--------------------------------------------------------------"
$archiveRoots = @(
    ".\archive\phases",
    ".\archive\phases\phase75",
    ".\archive\phases\phase143",
    ".\archive\phases\phase144"
)

foreach ($root in $archiveRoots) {
    Write-Host ""
    Write-Host "ROOT: $root"
    if (Test-Path $root) {
        Get-ChildItem `
            -Path $root `
            -File `
            -Recurse `
            -Force `
            -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -in $targets
        } |
        Sort-Object FullName |
        ForEach-Object {
            Write-Host "  $($_.FullName)"
        }
    }
    else {
        Write-Host "  directory absent"
    }
}

Write-Host ""
Write-Host "G. Canonical path existence"
Write-Host "--------------------------------------------------------------"
foreach ($name in $targets) {
    $canonical = Join-Path ".\tests" $name
    Write-Host "$canonical : $(Test-Path $canonical)"
}

Write-Host ""
Write-Host "H. Relevant import references still present"
Write-Host "--------------------------------------------------------------"
foreach ($name in $targets) {
    $module = [System.IO.Path]::GetFileNameWithoutExtension($name)
    Write-Host ""
    Write-Host "MODULE: tests.$module"

    $references = Get-ChildItem `
        -Path ".\tests" `
        -Filter "*.py" `
        -File `
        -ErrorAction SilentlyContinue |
    Select-String `
        -SimpleMatch `
        -Pattern "tests.$module" `
        -ErrorAction SilentlyContinue

    if ($null -eq $references -or $references.Count -eq 0) {
        Write-Host "  import references: NONE"
    }
    else {
        foreach ($reference in $references) {
            Write-Host "  $($reference.Path):$($reference.LineNumber): $($reference.Line.Trim())"
        }
    }
}

Write-Host ""
Write-Host "I. Concise git status for tests/archive"
Write-Host "--------------------------------------------------------------"
git status --short -- tests archive/phases

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 145 Final Regression Diagnosis R5: COMPLETE"
Write-Host "No repository files were modified by this diagnosis."
Write-Host "Do NOT run repository-wide pytest yet."
Write-Host "=============================================================="
