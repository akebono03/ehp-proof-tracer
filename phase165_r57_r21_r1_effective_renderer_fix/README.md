# Phase 165 R57-R21-R1 effective renderer fix

This patch corrects a failed R57-R21 install that left the old renderer effective at runtime. It replaces the last top-level function definition and verifies the loaded source. It does not change mathematical rules or proof search. Run `run.ps1` from PowerShell after extracting to the project root. Run only targeted pytest.
