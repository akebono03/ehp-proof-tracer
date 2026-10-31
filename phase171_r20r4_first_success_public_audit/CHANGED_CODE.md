# Changed code (complete replaceable units)

## Files and symbols

1. `phase171_r20r4_first_success_public_audit/audit.py`: replace the complete `EXPECTED_HEADS` constant with `REVIEWED_SOURCE_BLOBS`; replace the complete `preflight()` function.
2. `phase171_r20r4_first_success_public_audit/run.ps1`: not changed from R20R4R1; included whole for extraction.
3. Existing production and tests: no change. No import changes in `audit.py`.

## New constant (at the former EXPECTED_HEADS location)

```python
# Reviewed GitHub content blobs (not commit/HEAD IDs).
# Source: akebono03/ehp-proof-tracer @ 788261264e63d202b9e9bfe819212f12e0d0134e.
REVIEWED_SOURCE_BLOBS = {
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r9_shared_math.py": "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac",
}
```

## Full preflight() function

```python
def preflight() -> dict:
    """Check the reviewed search/provider bytes, regardless of newer commit ID.

    Use Git's read-only hash-object with the path-specific clean filters so
    Windows checkout line endings do not trigger false source mismatches.
    Never repair or reset the worktree. A source mismatch is fatal.
    """
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    if branch != "develop":
        raise RuntimeError("R20R4 requires develop; no branch will be changed")

    observed_blobs: dict[str, str] = {}
    for relative_path, reviewed_blob in REVIEWED_SOURCE_BLOBS.items():
        path = ROOT / relative_path
        if not path.is_file():
            raise RuntimeError("required production file is missing: " + relative_path)
        command = [
            "git", "hash-object", "--path=" + relative_path,
            relative_path,
        ]
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, check=True,
        )
        observed_blob = result.stdout.strip()
        observed_blobs[relative_path] = observed_blob
        if observed_blob != reviewed_blob:
            raise RuntimeError(
                "production source differs from reviewed GitHub blob: "
                + relative_path + " expected=" + reviewed_blob
                + " actual=" + observed_blob
                + "; no files modified"
            )

    source = (ROOT / "phase165_r3_recursive_search.py").read_text(encoding="utf-8")
    if (
        "def reconstruct_registered_goal(" not in source
        or "first accepted proof wins" not in source
        or "ambiguous registered direct references" not in source
        or "expected a verified registered derivation" not in source
    ):
        raise RuntimeError("reviewed R20R2 first-successful proof search is unavailable")

    return {
        "branch": branch,
        "head": head,
        "reviewed_source_blobs": observed_blobs,
        "tracked_before": git("status", "--porcelain", "--untracked-files=no"),
    }
```

## Full run.ps1 (unchanged from R20R4R1)

```powershell
param(
    [switch]$DryRun,
    [switch]$RightOnly,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root

$Audit = Join-Path $PSScriptRoot 'audit.py'
if (-not (Test-Path -LiteralPath $Audit)) {
    throw 'R20R4 audit.py is missing'
}

if ($DryRun) {
    & python -m phase171_r20r4_first_success_public_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R4 dry-run failed' }
    return
}

if (-not $SkipTests) {
    Write-Output 'PHASE171_R20R4_FOCUSED_PYTEST_START'
    & python -m pytest -q -p no:cacheprovider `
        'phase171_r2j_r4_r9_r7_public_cyclic_root/tests/test_audit.py::test_generic_source_anchored_root_is_a_premise_proposal_only' `
        'phase171_r2j_r4_r9_r8_public_cardinality/tests/test_audit.py::test_end_groups_yield_only_one_typed_backward_obligation'
    if ($LASTEXITCODE -ne 0) { throw 'R20R4 focused pytest failed' }
    Write-Output 'PHASE171_R20R4_FOCUSED_PYTEST=PASS'
}

if ($RightOnly) {
    & python -m phase171_r20r4_first_success_public_audit.audit --right-only
} else {
    & python -m phase171_r20r4_first_success_public_audit.audit
}
if ($LASTEXITCODE -ne 0) { throw 'R20R4 read-only audit failed' }

```

No new test or production function is introduced. The pytest node IDs are listed in IMPLEMENTATION_NOTES_JA.md.
