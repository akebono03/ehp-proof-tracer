$ErrorActionPreference = "Stop"

$repo = (Get-Location).Path
$renderer = Join-Path $repo "toda_group_proof_narrative_renderer.py"
$test = Join-Path $repo "tests\test_phase143_73a_internal_statement_narrative.py"

if (-not (Test-Path $renderer)) {
  throw "toda_group_proof_narrative_renderer.py was not found."
}

$lines = [System.Collections.Generic.List[string]]::new()
[System.IO.File]::ReadAllLines($renderer) | ForEach-Object {
  [void]$lines.Add($_)
}

function Find-LineIndex {
  param(
    [System.Collections.Generic.List[string]]$Items,
    [string]$ExactText,
    [int]$StartIndex = 0
  )

  for ($i = $StartIndex; $i -lt $Items.Count; $i++) {
    if ($Items[$i] -eq $ExactText) {
      return $i
    }
  }

  return -1
}

# Add ScalarGreaterEqualStatement import immediately before repository import.
if (-not ($lines -contains "  ScalarGreaterEqualStatement,")) {
  $idx = Find-LineIndex $lines "from repository_element_presentation import ("
  if ($idx -lt 0) {
    throw "repository_element_presentation import anchor was not found."
  }

  $block = @(
    "from scalar_rules import (",
    "  ScalarGreaterEqualStatement,",
    ")"
  )

  for ($j = $block.Count - 1; $j -ge 0; $j--) {
    $lines.Insert($idx, $block[$j])
  }
}

# Add TodaEtaFamilyDefinitionStatement to the existing toda_rules import.
if (-not ($lines -contains "  TodaEtaFamilyDefinitionStatement,")) {
  $idx = Find-LineIndex $lines "  TodaDeltaZeroStatement,"
  if ($idx -lt 0) {
    throw "TodaDeltaZeroStatement import anchor was not found."
  }

  $lines.Insert(
    $idx + 1,
    "  TodaEtaFamilyDefinitionStatement,"
  )
}

function Replace-Function {
  param(
    [System.Collections.Generic.List[string]]$Items,
    [string]$FunctionName,
    [string]$NextFunctionName,
    [string[]]$Replacement
  )

  $start = Find-LineIndex $Items ("def " + $FunctionName + "(")
  if ($start -lt 0) {
    throw ("Function start not found: " + $FunctionName)
  }

  $next = Find-LineIndex $Items ("def " + $NextFunctionName + "(") ($start + 1)
  if ($next -lt 0) {
    throw ("Next function start not found: " + $NextFunctionName)
  }

  $removeCount = $next - $start
  $Items.RemoveRange(
    $start,
    $removeCount
  )

  for ($j = $Replacement.Count - 1; $j -ge 0; $j--) {
    $Items.Insert(
      $start,
      $Replacement[$j]
    )
  }
}

$labelFunction = @'
def _group_proof_narrative_statement_label(
  statement,
) -> str | None:
  if isinstance(
    statement,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  ):
    return (
      "Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係"
    )

  if isinstance(
    statement,
    Toda48Pi16_9OrderAndE4InjectiveStatement,
  ):
    return (
      "π₁₆⁹ の位数 16 と E⁴ の単射性"
    )

  if isinstance(
    statement,
    Toda52CompositionIsomorphismStatement,
  ):
    return "Toda (5.2) の η₂ 合成同型"

  if isinstance(
    statement,
    Toda53NuPrimeBracketSpecializationStatement,
  ):
    return (
      "ν′ に対する Lemma 5.2 の Toda bracket 特殊化"
    )

  if isinstance(
    statement,
    Toda55NuFamilyFiniteDimensionalStatement,
  ):
    return (
      "Toda (5.5) の ν-family 有限次元結果"
    )

  if isinstance(
    statement,
    Toda56Nu4DecompositionIsomorphismStatement,
  ):
    return "Toda (5.6) の ν₄ 分解同型"

  if isinstance(
    statement,
    Toda56Nu4DecompositionStatement,
  ):
    return "Toda (5.6) の ν₄ 分解"

  if isinstance(
    statement,
    TodaDeltaZeroStatement,
  ):
    return "Δ 写像が零写像であること"

  if isinstance(
    statement,
    TodaEtaFamilyDefinitionStatement,
  ):
    return "η-family の定義"

  if isinstance(
    statement,
    TodaHopfInvariantInjectiveStatement,
  ):
    return "Hopf 写像の単射性"

  if isinstance(
    statement,
    TodaIteratedSuspensionInjectiveStatement,
  ):
    return "E²: π₆³ → π₈⁵ の単射性"

  if isinstance(
    statement,
    TodaLemma513Statement,
  ):
    return (
      "Toda Lemma 5.13 の σ‴ に関する結果"
    )

  if isinstance(
    statement,
    TodaLemma514Sigma8Statement,
  ):
    return (
      "Toda Lemma 5.14 の σ₈ に関する結果"
    )

  if isinstance(
    statement,
    TodaLemma514SigmaPrimeStatement,
  ):
    return "Toda Lemma 5.14 の σ′ に関する結果"

  if isinstance(
    statement,
    TodaLemma54Statement,
  ):
    return "Toda Lemma 5.4 の結果"

  if isinstance(
    statement,
    TodaProp51FiniteDimensionalStatement,
  ):
    return (
      "Toda Proposition 5.1 の有限次元結果"
    )

  if isinstance(
    statement,
    TodaProp511FiniteDimensionalStatement,
  ):
    return (
      "Toda Proposition 5.11 の有限次元結果"
    )

  if isinstance(
    statement,
    TodaProp515Pi12_5HopfIsomorphismStatement,
  ):
    return (
      "π₁₂⁵ の位数 2 の Hopf 像への同型"
    )

  if isinstance(
    statement,
    TodaProp56FiniteDimensionalStatement,
  ):
    return (
      "Toda Proposition 5.6 の有限次元結果"
    )

  if isinstance(
    statement,
    TodaProp56Pi8_5QuotientStatement,
  ):
    return (
      "π₈⁵ / E²π₆³ が位数 2 であること"
    )

  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return "σ-family の定義"

  return None


'@ -split "`r?`n"

$latexFunction = @'
def _render_group_proof_narrative_latex(
  proof_step: ProofStep,
) -> str | None:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

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
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = None

  if latex is not None:
    return latex

  return (
    render_toda_proof_statement_latex(
      statement
    )
  )


'@ -split "`r?`n"

Replace-Function `
  $lines `
  "_group_proof_narrative_statement_label" `
  "_render_group_proof_narrative_latex" `
  $labelFunction

Replace-Function `
  $lines `
  "_render_group_proof_narrative_latex" `
  "_render_group_proof_narrative_fact" `
  $latexFunction

[System.IO.File]::WriteAllLines(
  $renderer,
  $lines,
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

Write-Host "Phase 143-73A R2 applied."
Write-Host "Changed: toda_group_proof_narrative_renderer.py"
Write-Host "Added:   tests\test_phase143_73a_internal_statement_narrative.py"
