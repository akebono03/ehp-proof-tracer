Phase 162 R3-H: existing-reason reuse inventory (read-only)

Run in repository root after Phase 162 R3-G:

  Expand-Archive -Path "$HOME\Downloads\phase162_r3h_reason_inventory.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r3h_reason_inventory\run_phase162_r3h.ps1"

Files copied: new audit module, CLI, and focused tests only.
No production ProofStep, reason builders, or public renderer changes.
No full test suite.

Output under phase162_r3h_output:
  reason_inventory_audit.json
  unexplained_step_inventory.json
  reason_inventory_groups.json

Categories:
 DIRECT_REUSE_READY: existing direct-premise validated builder + nonempty reason prose
 MATCHED_BUT_RENDER_UNAVAILABLE: builder matches but prose unavailable
 AMBIGUOUS_OR_INVALID_DIRECT_MATCH: conflicts or premise identity invalid
 GENERIC_RESULT_LABEL_ONLY: existing broad final-result kind but no verified direct rule
 NO_DIRECT_MATCH_REVIEW_REQUIRED: no direct builder match; may still have contextual reasons

Never interpret NO_DIRECT_MATCH_REVIEW_REQUIRED as proof of a missing implementation.
