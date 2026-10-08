Phase 162 R5-6 dependency audit renderer repair

Changes:
- Only the read-only audit script and its PowerShell runner are included.
- Unsupported mathematical statement renderers are represented by their type, rule, and renderer error; never invent or suppress mathematical facts.
- Paths to root and whether they cross a fixed Reference boundary are reported.
- Production files, proof DAG, and tests are not changed.

Run from your repository root:
  Expand-Archive -Path "$HOME\Downloads\phase162_r5_6_dependency_audit_render_repair.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r5_6_dependency_audit_render_repair\run_phase162_r5_6_dependency_audit.ps1"

No full pytest suite is run.
