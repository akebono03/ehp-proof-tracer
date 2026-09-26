$ErrorActionPreference = "Stop"

$repo = (Get-Location).Path
$multi = Join-Path $repo "toda_group_proof_narrative_argument_multi_renderer.py"
$body = Join-Path $repo "toda_group_proof_narrative_argument_body_renderer.py"
$testTarget = Join-Path $repo "tests\test_phase143_71a_eta_definition_visibility.py"

if (-not (Test-Path $multi) -or -not (Test-Path $body)) {
  throw "Run this script from the ehp-proof-tracer repository root."
}

$multiSource = Get-Content -Raw -Encoding UTF8 $multi
$bodySource = Get-Content -Raw -Encoding UTF8 $body

$oldMultiArgumentsImport = @'
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
'@

$newMultiArgumentsImport = @'
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
'@

$oldMultiRulesImport = @'
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
'@

$newMultiRulesImport = @'
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)
'@

$oldLocalBody = @'
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    header = (
'@

$newLocalBody = @'
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    context_hidden_step_ids = frozenset(
      id(
        proof_step
      )
      for block in local_body_blocks
      for proof_step in block.steps
      if (
        argument.role
        is not TodaGroupProofNarrativeArgumentRole
        .ESTABLISH_DEFINITION
        and isinstance(
          proof_step.conclusion,
          TodaEtaFamilyDefinitionStatement,
        )
      )
    )

    header = (
'@

$oldBodyCallTail = @'
        conclusion_step=conclusion_step,
        direct_derivation_premises=direct_derivation_premises,
      )
'@

$newBodyCallTail = @'
        conclusion_step=conclusion_step,
        direct_derivation_premises=direct_derivation_premises,
        context_hidden_step_ids=context_hidden_step_ids,
      )
'@

$oldBodySignature = @'
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ] = (),
) -> str:
'@

$newBodySignature = @'
  direct_derivation_premises: tuple[
    ProofStep,
    ...,
  ] = (),
  context_hidden_step_ids: (
    frozenset[
      int
    ]
    | None
  ) = None,
) -> str:
'@

$oldBodyValidationAnchor = @'
  for premise_step in direct_derivation_premises:
    if not isinstance(
      premise_step,
      ProofStep,
    ):
      raise TypeError(
        "direct_derivation_premises must contain only "
        "ProofStep objects"
      )

  block_index_by_identity = {
'@

$newBodyValidationAnchor = @'
  for premise_step in direct_derivation_premises:
    if not isinstance(
      premise_step,
      ProofStep,
    ):
      raise TypeError(
        "direct_derivation_premises must contain only "
        "ProofStep objects"
      )

  if (
    context_hidden_step_ids is not None
    and not isinstance(
      context_hidden_step_ids,
      frozenset,
    )
  ):
    raise TypeError(
      "context_hidden_step_ids must be "
      "a frozenset or None"
    )

  if context_hidden_step_ids is not None:
    for step_id in context_hidden_step_ids:
      if (
        not isinstance(
          step_id,
          int,
        )
        or isinstance(
          step_id,
          bool,
        )
      ):
        raise TypeError(
          "context_hidden_step_ids must contain "
          "only integers"
        )

  block_index_by_identity = {
'@

$oldDisplaySteps = @'
      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          id(
            proof_step
          ) not in redundant_direct_premise_step_ids
          and (
            id(
              proof_step
            ) not in relocated_direct_premise_ids
            or (
              conclusion_step is not None
              and conclusion_step in block.steps
            )
          )
        )
      )
'@

$newDisplaySteps = @'
      display_steps = tuple(
        proof_step
        for proof_step in block.steps
        if (
          (
            context_hidden_step_ids is None
            or id(
              proof_step
            ) not in context_hidden_step_ids
          )
          and id(
            proof_step
          ) not in redundant_direct_premise_step_ids
          and (
            id(
              proof_step
            ) not in relocated_direct_premise_ids
            or (
              conclusion_step is not None
              and conclusion_step in block.steps
            )
          )
        )
      )
'@

foreach ($pair in @(
  @($oldMultiArgumentsImport, $newMultiArgumentsImport),
  @($oldMultiRulesImport, $newMultiRulesImport),
  @($oldLocalBody, $newLocalBody),
  @($oldBodyCallTail, $newBodyCallTail)
)) {
  if (-not $multiSource.Contains($pair[0])) {
    throw "Expected multi-renderer source block not found."
  }
  $multiSource = $multiSource.Replace($pair[0], $pair[1])
}

foreach ($pair in @(
  @($oldBodySignature, $newBodySignature),
  @($oldBodyValidationAnchor, $newBodyValidationAnchor),
  @($oldDisplaySteps, $newDisplaySteps)
)) {
  if (-not $bodySource.Contains($pair[0])) {
    throw "Expected body-renderer source block not found."
  }
  $bodySource = $bodySource.Replace($pair[0], $pair[1])
}

Set-Content -Path $multi -Value $multiSource -Encoding UTF8
Set-Content -Path $body -Value $bodySource -Encoding UTF8

Copy-Item `
  (Join-Path $PSScriptRoot "tests\test_phase143_71a_eta_definition_visibility.py") `
  $testTarget `
  -Force

Write-Host "Phase 143-71A files applied."
