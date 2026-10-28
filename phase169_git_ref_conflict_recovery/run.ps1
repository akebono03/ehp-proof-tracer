param(
    [switch]$Repair
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Invoke-GitOrFail {
    param(
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )
    $lines = @(& git @Arguments 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw ("Git command failed (exit {0}): git {1}; output: {2}" -f `
            $LASTEXITCODE, ($Arguments -join ' '), ($lines -join ' | '))
    }
    return $lines
}

function Resolve-GitDirectory {
    $pathLines = @(Invoke-GitOrFail -Arguments @('rev-parse', '--git-dir'))
    if ($pathLines.Count -ne 1) {
        throw 'Could not determine one Git directory.'
    }
    $path = [string]$pathLines[0]
    if (-not [System.IO.Path]::IsPathRooted($path)) {
        $path = Join-Path (Get-Location).Path $path
    }
    $absolutePath = [System.IO.Path]::GetFullPath($path)
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Container)) {
        throw "Git directory is not a directory: $absolutePath"
    }
    return $absolutePath
}

function Get-ConflictedRefCopies {
    param([Parameter(Mandatory = $true)][string]$GitDirectory)
    $result = @()
    foreach ($relativeParent in @('refs\heads', 'refs\remotes\origin')) {
        $parent = Join-Path $GitDirectory $relativeParent
        if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
            continue
        }
        foreach ($entry in @(Get-ChildItem -LiteralPath $parent -File -Force)) {
            if ($entry.Name -notmatch '^develop \([^)]*競合コピー[^)]*\)$') {
                continue
            }
            $relativeRef = ($relativeParent -replace '\\', '/') + '/' + $entry.Name
            # A valid reference must never be relocated. The log's conflicted
            # name contains a space, which is forbidden by Git ref syntax.
            $null = & git check-ref-format $relativeRef 2>$null
            if ($LASTEXITCODE -eq 0) {
                throw "Ref name unexpectedly valid; refusing: $relativeRef"
            }
            $result += [pscustomobject]@{
                Source = $entry.FullName
                Relative = ($relativeParent + '\' + $entry.Name)
                GitRef = $relativeRef
                Sha256 = (Get-FileHash -LiteralPath $entry.FullName -Algorithm SHA256).Hash
            }
        }
    }
    return @($result)
}

$gitDirectory = Resolve-GitDirectory
$branch = ((Invoke-GitOrFail -Arguments @('branch', '--show-current')) -join '').Trim()
if ($branch -ne 'develop') {
    throw "Expected develop branch. Actual: $branch"
}
$localCommit = ((Invoke-GitOrFail -Arguments @('rev-parse', '--verify', 'refs/heads/develop^{commit}')) -join '').Trim()
$remoteCommit = ((Invoke-GitOrFail -Arguments @('rev-parse', '--verify', 'refs/remotes/origin/develop^{commit}')) -join '').Trim()
if ($localCommit -notmatch '^[0-9a-f]{40}$' -or $remoteCommit -notmatch '^[0-9a-f]{40}$') {
    throw 'Normal develop ref or origin/develop ref did not resolve to a valid commit.'
}

$found = @(Get-ConflictedRefCopies -GitDirectory $gitDirectory)
Write-Output ("GIT_REF_RESCUE_MODE=" + $(if ($Repair) { 'REPAIR' } else { 'DRY_RUN' }))
Write-Output "GIT_REF_RESCUE_GIT_DIR=$gitDirectory"
Write-Output "GIT_REF_RESCUE_NORMAL_DEVELOP=$localCommit"
Write-Output "GIT_REF_RESCUE_NORMAL_ORIGIN_DEVELOP=$remoteCommit"
Write-Output "GIT_REF_RESCUE_CONFLICT_COUNT=$($found.Count)"
foreach ($item in $found) {
    Write-Output "GIT_REF_RESCUE_CONFLICT=$($item.Relative) SHA256=$($item.Sha256)"
}
if (-not $Repair) {
    Write-Output 'GIT_REF_RESCUE_DRY_RUN=PASS'
    Write-Output 'To back up and relocate only these invalid copies, run: .\run.ps1 -Repair'
    exit 0
}
if ($found.Count -eq 0) {
    Write-Output 'GIT_REF_RESCUE_NO_ACTION=PASS'
    exit 0
}
if ($found.Count -gt 2) {
    throw 'Unexpected number of conflicted ref copies. No changes performed.'
}

# Backups are saved outside the project and outside its Dropbox folder.
$backupRoot = Join-Path $HOME ('ehp-git-ref-conflict-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss-ffff'))
if (Test-Path -LiteralPath $backupRoot) {
    throw "Backup already exists: $backupRoot"
}
New-Item -ItemType Directory -Path $backupRoot -ErrorAction Stop | Out-Null
$moved = @()
try {
    foreach ($item in $found) {
        $destination = Join-Path $backupRoot $item.Relative
        $destinationParent = Split-Path -Parent $destination
        New-Item -ItemType Directory -Path $destinationParent -Force -ErrorAction Stop | Out-Null
        if (Test-Path -LiteralPath $destination) {
            throw "Backup destination already exists: $destination"
        }
        # Move rather than delete: the exact original bytes stay recoverable.
        [System.IO.File]::Move($item.Source, $destination)
        $moved += [pscustomobject]@{ Source = $item.Source; Destination = $destination }
        if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $item.Sha256) {
            throw "Backup checksum mismatch: $destination"
        }
        Write-Output "GIT_REF_RESCUE_MOVED=$($item.Relative)"
    }
    # Preserve the original valid references throughout the operation.
    $postLocal = ((Invoke-GitOrFail -Arguments @('rev-parse', '--verify', 'refs/heads/develop^{commit}')) -join '').Trim()
    $postRemote = ((Invoke-GitOrFail -Arguments @('rev-parse', '--verify', 'refs/remotes/origin/develop^{commit}')) -join '').Trim()
    if ($postLocal -ne $localCommit -or $postRemote -ne $remoteCommit) {
        throw 'Normal Git branch pointers changed; rolling back the relocation.'
    }
    $manifest = [ordered]@{
        mode = 'REPAIR'
        branch = $branch
        normal_develop = $localCommit
        normal_origin_develop = $remoteCommit
        git_directory = $gitDirectory
        moved = @($found | ForEach-Object { [ordered]@{relative = $_.Relative; sha256 = $_.Sha256} })
        instructions = 'Move the backup file(s) back to the original paths only if recovery is required.'
    }
    $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $backupRoot 'manifest.json') -Encoding UTF8
    Write-Output "GIT_REF_RESCUE_BACKUP=$backupRoot"
    Write-Output 'GIT_REF_RESCUE_RESULT=PASS'
    Write-Output 'Next: git fetch origin develop; git status -sb'
} catch {
    $caught = $_
    for ($position = $moved.Count - 1; $position -ge 0; $position--) {
        $entry = $moved[$position]
        if ((Test-Path -LiteralPath $entry.Destination -PathType Leaf) -and
            -not (Test-Path -LiteralPath $entry.Source)) {
            [System.IO.File]::Move($entry.Destination, $entry.Source)
        }
    }
    throw $caught
}
