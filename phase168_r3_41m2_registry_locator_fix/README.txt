Phase 168 R3-41M2 — concise Renderer and corrected registered eta locator.

Use this INSTEAD of phase168_r3_41m_concise_renderer.zip, not after it.

From repository root in PowerShell:
  Expand-Archive -Path "$HOME\Downloads\phase168_r3_41m2_registry_locator_fix.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41m2_registry_locator_fix\run.ps1"

Guarded transaction updates 6 existing files; all are restored byte-for-byte on failure.
It does not run full pytest, only focused tests. Upload output/review_bundle.zip on success.
