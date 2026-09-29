from pathlib import Path


TARGET_DIR_NAME = (
  "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
)

OLD_FUNCTION = r'''function Test-FoundationAtCommit {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha
  )

  $objectName = "${Sha}:$FoundationPath"
  & git cat-file -e $objectName 2>$null
  $exitCode = $LASTEXITCODE

  if ($exitCode -eq 0) {
    return $true
  }

  return $false
}
'''

NEW_FUNCTION = r'''function Test-FoundationAtCommit {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Sha
  )

  $objectName = "${Sha}:$FoundationPath"
  $stderrPath = Join-Path $env:TEMP (
    "ehp_r25_11_r6_r1_cat_file_"
    + $PID
    + ".stderr.txt"
  )
  $oldErrorActionPreference = $ErrorActionPreference

  try {
    $ErrorActionPreference = "Continue"
    & git cat-file -e $objectName 2>$stderrPath
    $exitCode = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldErrorActionPreference
  }

  if ($exitCode -eq 0) {
    if (Test-Path $stderrPath) {
      Remove-Item $stderrPath -Force -ErrorAction SilentlyContinue
    }

    return $true
  }

  if ($exitCode -eq 1) {
    if (Test-Path $stderrPath) {
      Remove-Item $stderrPath -Force -ErrorAction SilentlyContinue
    }

    return $false
  }

  $stderrText = ""

  if (Test-Path $stderrPath) {
    $stderrLines = Get-Content -Path $stderrPath -Encoding UTF8
    $stderrText = $stderrLines -join " "
    Remove-Item $stderrPath -Force -ErrorAction SilentlyContinue
  }

  throw (
    "git cat-file failed for "
    + $Sha
    + " with exit code "
    + $exitCode
    + ": "
    + $stderrText
  )
}
'''


def main():
  repo_root = Path.cwd()
  target_dir = repo_root / TARGET_DIR_NAME
  locator = target_dir / "locate_historical_190.ps1"

  if not locator.is_file():
    raise SystemExit(
      f"missing locator: {locator}"
    )

  source = locator.read_text(
    encoding="utf-8-sig"
  )

  count = source.count(
    OLD_FUNCTION
  )

  if count != 1:
    raise SystemExit(
      "expected exactly one old "
      "Test-FoundationAtCommit function, "
      f"found {count}"
    )

  updated = source.replace(
    OLD_FUNCTION,
    NEW_FUNCTION,
    1,
  )

  locator.write_text(
    updated,
    encoding="utf-8-sig",
  )

  print(
    "R25-11-R6-R1-R2-R1-R2 native Git error handling repair applied."
  )
  print(
    "Changed locator function: Test-FoundationAtCommit."
  )
  print(
    "Production changes: none."
  )
  print(
    "Existing project tests changed: none."
  )
  print(
    "Expected historical population remains 190."
  )
  print(
    "Existing population cache is preserved."
  )


if __name__ == "__main__":
  main()
