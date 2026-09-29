from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent
LOCATOR = PHASE_DIR / "locate_historical_190.ps1"


def _remove_source():
  source = LOCATOR.read_text(encoding="utf-8-sig")
  start = source.index("function Remove-TemporaryWorktree {")
  end = source.index("function Read-PopulationCache {")
  return source[start:end]


def test_phase144_6_r4_r5_r1_preserves_legacy_registration_initialization():
  source = _remove_source()

  assert "$isRegistered = $false" in source
  assert "$isRegistered = Get-RegisteredAuditWorktreeState" in source


def test_phase144_6_r4_r5_r1_preserves_idempotent_recheck():
  source = _remove_source()

  assert "$stillRegistered = Get-RegisteredAuditWorktreeState" in source
  assert "if ($stillRegistered)" in source
  assert "Remove-StaleAuditWorktreePath" in source


def test_phase144_6_r4_r5_r1_preserves_historical_baseline_contracts():
  source = LOCATOR.read_text(encoding="utf-8-sig")

  assert "& git worktree prune --expire now 1>$null 2>$null" in source
  assert "$collectorExitCode = $LASTEXITCODE" in source
  assert "function Read-PopulationCache {" in source
  assert "$Expected = 190" in source
