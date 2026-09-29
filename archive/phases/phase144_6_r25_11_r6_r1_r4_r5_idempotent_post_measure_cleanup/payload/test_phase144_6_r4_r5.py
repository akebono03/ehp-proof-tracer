from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent
LOCATOR = PHASE_DIR / "locate_historical_190.ps1"


def _remove_source():
  source = LOCATOR.read_text(encoding="utf-8-sig")
  start = source.index("function Remove-TemporaryWorktree {")
  end = source.index("function Read-PopulationCache {")
  return source[start:end]


def test_phase144_6_r4_r5_cleanup_rechecks_registration_after_remove_failure():
  source = _remove_source()

  assert "function Get-RegisteredAuditWorktreeState {" in source
  assert "$stillRegistered = Get-RegisteredAuditWorktreeState" in source
  assert "if ($stillRegistered)" in source
  assert "$removeExitCode = $LASTEXITCODE" in source


def test_phase144_6_r4_r5_cleanup_treats_unregistered_residue_idempotently():
  source = _remove_source()

  assert "function Remove-StaleAuditWorktreePath {" in source
  assert '$expectedLeaf = ".phase144_6_r25_11_r6_r1_worktree"' in source
  assert "Remove-StaleAuditWorktreePath" in source
  assert "refusing unregistered path cleanup outside audit worktree" in source


def test_phase144_6_r4_r5_preserves_prune_and_collector_native_repairs():
  source = LOCATOR.read_text(encoding="utf-8-sig")

  assert "& git worktree prune --expire now 1>$null 2>$null" in source
  assert "$pruneExitCode = $LASTEXITCODE" in source
  assert "$collectorOldErrorActionPreference = $ErrorActionPreference" in source
  assert "$collectorExitCode = $LASTEXITCODE" in source
  assert source.count("function Read-PopulationCache {") == 1
  assert "$Expected = 190" in source
