Phase 165 R12-R19: Existing eta-family definition audit (read-only).

Scope: inspect TodaEtaFamilyDefinitionStatement / toda_eta_family_definition_statement(3)
and whether actual unified-registry proof links have FIXED_STATEMENT origin,
GIVEN proof rule, matching assertion content, and a literature locator.
Do not fabricate a new η definition, cite an unverified equation, or claim
that E(η₂)=η₃ is certified merely because a definition object exists.
No changes to old production code. No full pytest.

Run from project root:
  Expand-Archive -Path "$HOME\Downloads\phase165_r12_r19_eta_definition_audit.zip" -DestinationPath . -Force
  powershell -ExecutionPolicy Bypass -File ".\phase165_r12_r19_eta_definition_audit\run.ps1"

Completion criterion: 3 targeted tests pass, audit_result.json records the actual
registry contents. Later phase must derive a ProofStep from a valid existing
definition and certify it before closing π₄³.
