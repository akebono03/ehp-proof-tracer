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

if ($multiSource.Contains("context_hidden_step_ids")) {
  throw "71A appears to be already partially applied to multi renderer. Stop and inspect before retrying."
}
if ($bodySource.Contains("context_hidden_step_ids")) {
  throw "71A appears to be already partially applied to body renderer. Stop and inspect before retrying."
}

# 1. Add argument role import after the existing argument class import.
$needle = "  TodaGroupProofNarrativeArgument,`r`n  extract_toda_group_proof_narrative_argument_conclusion_step,"
if (-not $multiSource.Contains($needle)) {
  $needle = "  TodaGroupProofNarrativeArgument,`n  extract_toda_group_proof_narrative_argument_conclusion_step,"
}
if (-not $multiSource.Contains($needle)) {
  throw "Could not locate TodaGroupProofNarrativeArgument import."
}
$replacement = $needle.Replace(
  "  extract_toda_group_proof_narrative_argument_conclusion_step,",
  "  TodaGroupProofNarrativeArgumentRole,`n  extract_toda_group_proof_narrative_argument_conclusion_step,"
)
$multiSource = $multiSource.Replace($needle, $replacement)

# 2. Add TodaEtaFamilyDefinitionStatement import immediately after presentation import.
$marker = @'
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
'@
$markerCrLf = $marker -replace "`n", "`r`n"
if ($multiSource.Contains($markerCrLf)) {
  $marker = $markerCrLf
} elseif (-not $multiSource.Contains($marker)) {
  throw "Could not locate TodaGroupProofPresentation import."
}
$addition = $marker + @'
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)
'@
$multiSource = $multiSource.Replace($marker, $addition)

# 3. Insert context visibility calculation after local_body_blocks construction.
$anchor = "    header = (`r`n"
if (-not $multiSource.Contains($anchor)) {
  $anchor = "    header = (`n"
}
if (-not $multiSource.Contains($anchor)) {
  throw "Could not locate header construction."
}
$visibility = @'
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

'@
if ($anchor.Contains("`r`n")) {
  $visibility = $visibility -replace "`n", "`r`n"
}
$multiSource = $multiSource.Replace($anchor, $visibility + $anchor)

# 4. Pass the hidden IDs to the body renderer.
$callNeedle = "        direct_derivation_premises=direct_derivation_premises,`r`n      )"
if (-not $multiSource.Contains($callNeedle)) {
  $callNeedle = "        direct_derivation_premises=direct_derivation_premises,`n      )"
}
if (-not $multiSource.Contains($callNeedle)) {
  throw "Could not locate body renderer call tail."
}
$lineEnding = if ($callNeedle.Contains("`r`n")) { "`r`n" } else { "`n" }
$callReplacement = (
  "        direct_derivation_premises=direct_derivation_premises," +
  $lineEnding +
  "        context_hidden_step_ids=context_hidden_step_ids," +
  $lineEnding +
  "      )"
)
$multiSource = $multiSource.Replace($callNeedle, $callReplacement)

# 5. Extend body renderer signature.
$sigNeedle = "  ] = (),`r`n) -> str:"
if (-not $bodySource.Contains($sigNeedle)) {
  $sigNeedle = "  ] = (),`n) -> str:"
}
if (-not $bodySource.Contains($sigNeedle)) {
  throw "Could not locate body renderer signature tail."
}
$lineEnding = if ($sigNeedle.Contains("`r`n")) { "`r`n" } else { "`n" }
$sigReplacement = (
  "  ] = ()," + $lineEnding +
  "  context_hidden_step_ids: (" + $lineEnding +
  "    frozenset[" + $lineEnding +
  "      int" + $lineEnding +
  "    ]" + $lineEnding +
  "    | None" + $lineEnding +
  "  ) = None," + $lineEnding +
  ") -> str:"
)
$bodySource = $bodySource.Replace($sigNeedle, $sigReplacement)

# 6. Validate context_hidden_step_ids before block lookup.
$validationAnchor = "  block_index_by_identity = {`r`n"
if (-not $bodySource.Contains($validationAnchor)) {
  $validationAnchor = "  block_index_by_identity = {`n"
}
if (-not $bodySource.Contains($validationAnchor)) {
  throw "Could not locate block_index_by_identity."
}
$validation = @'
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

'@
if ($validationAnchor.Contains("`r`n")) {
  $validation = $validation -replace "`n", "`r`n"
}
$bodySource = $bodySource.Replace(
  $validationAnchor,
  $validation + $validationAnchor
)

# 7. Add context visibility to the existing display-step filter.
$displayNeedle = @'
        if (
          id(
            proof_step
          ) not in redundant_direct_premise_step_ids
'@
$displayNeedleCrLf = $displayNeedle -replace "`n", "`r`n"
if ($bodySource.Contains($displayNeedleCrLf)) {
  $displayNeedle = $displayNeedleCrLf
} elseif (-not $bodySource.Contains($displayNeedle)) {
  throw "Could not locate display_steps filter."
}
$displayReplacement = @'
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
'@
if ($displayNeedle.Contains("`r`n")) {
  $displayReplacement = $displayReplacement -replace "`n", "`r`n"
}
$bodySource = $bodySource.Replace(
  $displayNeedle,
  $displayReplacement
)

Set-Content -Path $multi -Value $multiSource -Encoding UTF8
Set-Content -Path $body -Value $bodySource -Encoding UTF8

Copy-Item `
  (Join-Path $PSScriptRoot "tests\test_phase143_71a_eta_definition_visibility.py") `
  $testTarget `
  -Force

Write-Host "Phase 143-71A-R files applied."
