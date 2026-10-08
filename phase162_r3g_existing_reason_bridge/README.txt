Phase 162 R3-G: existing reason reuse audit

This package adds a new independent adapter without changing R3-F or the public
narrative renderer. It reuses the existing premise-validated reason builders:
  _exactness_to_map_property_reason
  _exactness_to_kernel_reason
and the existing reason sentence renderer.

The other previous typed reason kinds require a separate contract audit; this
package does not classify them as solved or implement duplicates.

Run in the repository root after R3-F:
  Expand-Archive -Path "$HOME\Downloads\phase162_r3g_existing_reason_bridge.zip" -DestinationPath . -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r3g_existing_reason_bridge\run_phase162_r3g.ps1"

Only focused tests run. Full suite is not run. The trace is not a proof certificate.
