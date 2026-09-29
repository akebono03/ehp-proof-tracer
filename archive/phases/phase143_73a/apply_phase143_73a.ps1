$ErrorActionPreference = "Stop"

$repo = (Get-Location).Path
$renderer = Join-Path $repo "toda_group_proof_narrative_renderer.py"
$test = Join-Path $repo "tests\test_phase143_73a_internal_statement_narrative.py"

if (-not (Test-Path $renderer)) {
  throw "toda_group_proof_narrative_renderer.py was not found."
}

$text = [System.IO.File]::ReadAllText($renderer)

if ($text -notmatch "from scalar_rules import \(") {
  $anchor = "from repository_element_presentation import ("
  $idx = $text.IndexOf($anchor)
  if ($idx -lt 0) {
    throw "Import insertion anchor was not found."
  }

  $import = @"
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
"@

  $text = $text.Insert($idx, $import)
}

if ($text -notmatch "  TodaEtaFamilyDefinitionStatement,") {
  $anchor = "  TodaDeltaZeroStatement,"
  $idx = $text.IndexOf($anchor)
  if ($idx -lt 0) {
    throw "TodaEtaFamilyDefinitionStatement import anchor was not found."
  }

  $text = $text.Insert(
    $idx,
    "  TodaEtaFamilyDefinitionStatement,`r`n"
  )
}

$labelAnchor = @"
  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return "σ-family の定義"

  return None
"@

if ($text.Contains($labelAnchor)) {
  $labelReplacement = @"
  if isinstance(
    statement,
    TodaEtaFamilyDefinitionStatement,
  ):
    return "η-family の定義"

  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return "σ-family の定義"

  return None
"@
  $text = $text.Replace(
    $labelAnchor,
    $labelReplacement
  )
}
elseif ($text -notmatch "TodaEtaFamilyDefinitionStatement,\s*\r?\n  \):\s*\r?\n    return `"η-family の定義`"") {
  throw "Narrative label insertion anchor was not found."
}

$latexAnchor = @"
  statement = proof_step.conclusion

  try:
"@

if ($text.Contains($latexAnchor)) {
  $latexReplacement = @"
  statement = proof_step.conclusion

  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.left
      )
      + r" \ge "
      + render_toda_expression_latex(
        statement.right
      )
    )

  try:
"@
  $text = $text.Replace(
    $latexAnchor,
    $latexReplacement
  )
}
elseif ($text -notmatch "ScalarGreaterEqualStatement") {
  throw "Narrative LaTeX insertion anchor was not found."
}

[System.IO.File]::WriteAllText(
  $renderer,
  $text,
  [System.Text.UTF8Encoding]::new($false)
)

$testContent = @'
from expression import (
  ScalarSymbol,
)
from proof import (
  ProofRule,
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_rules import (
  toda_eta_family_definition_statement,
)


def test_phase143_73a_scalar_greater_equal_statement_renders_as_latex():
  n = ScalarSymbol(
    name="n",
  )

  step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    _render_group_proof_narrative_fact(
      step
    )
    == r"$n \ge 5$"
  )


def test_phase143_73a_eta_family_definition_uses_human_readable_label():
  n = ScalarSymbol(
    name="n",
  )

  step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        n
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    _render_group_proof_narrative_fact(
      step
    )
    == "η-family の定義"
  )
'@

[System.IO.File]::WriteAllText(
  $test,
  $testContent,
  [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Phase 143-73A applied."
Write-Host "Changed: toda_group_proof_narrative_renderer.py"
Write-Host "Added:   tests\test_phase143_73a_internal_statement_narrative.py"
