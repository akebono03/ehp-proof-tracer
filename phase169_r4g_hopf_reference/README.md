# Phase 169 R4G — Source-verified Hopf-fibration Reference

This narrowly scoped patch adds the existence of Hopf fibrations for dimensions 2, 4 and 8—explicitly recorded immediately before Toda's Proposition 4.4—to the already cited Proposition 4.4 Reference body. The patch verifies the Chapter IV source file's Git blob and the preceding passage before registering the extended typed source statement.

It intentionally does **not** create a separate citation, assert a new proof leaf, modify the Proposition 4.4 injection inference, or change the existing 18-step completed proof. The exact earlier location is clearly identified within the existing Reference.

Extract the ZIP to the repository root and run in Windows PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r4g_hopf_reference.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4g_hopf_reference\run.ps1"
```

The runner verifies the develop branch, validates the exact pre-patch files, writes complete replacements and backups in `output`, runs **focused** pytest checks, and audits the actual public Narrative. It restores the two source files if validation fails. The full pytest suite is deliberately not run.
