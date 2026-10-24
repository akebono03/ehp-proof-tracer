Phase 168 R3-39G pre-implementation baseline audit.
This package changes no repository source file.
Use from repository root:
Expand-Archive -Path "$HOME\Downloads\phase168_r3_39g_step_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_39g_step_audit\run.ps1"
Requires the repository's phase168_r3_38_frozen_fulltext_audit and phase168_r3_39f_frozen_comparison packages.
Output is written to phase168_r3_39g_step_audit/output.
