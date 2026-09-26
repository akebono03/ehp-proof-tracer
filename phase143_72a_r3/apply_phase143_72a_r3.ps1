$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$rendererPath = Join-Path $repoRoot "toda_human_readable_renderer.py"
$testPath = Join-Path $repoRoot "tests\test_phase143_72a_negative_scalar_product_latex.py"

if (-not (Test-Path $rendererPath)) {
  throw "toda_human_readable_renderer.py not found. Run from repository root."
}

$lines = Get-Content -Encoding UTF8 $rendererPath

$start = -1
$end = -1

for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -eq "def _render_scalar_latex(") {
    $start = $i
    break
  }
}

if ($start -lt 0) {
  throw "_render_scalar_latex start was not found. No files were changed."
}

for ($i = $start + 1; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -eq "def _render_generator_symbol_latex(") {
    $end = $i
    break
  }
}

if ($end -lt 0) {
  throw "_render_scalar_latex end boundary was not found. No files were changed."
}

$newFunction = @'
def _render_scalar_latex(
  value,
) -> str:
  if isinstance(
    value,
    bool,
  ):
    raise TypeError(
      "scalar bool is not supported"
    )

  if isinstance(
    value,
    int,
  ):
    return str(
      value
    )

  if isinstance(
    value,
    ScalarSymbol,
  ):
    return _render_unicode_math_name_latex(
      value.name
    )

  if isinstance(
    value,
    ScalarSum,
  ):
    if (
      isinstance(
        value.right,
        int,
      )
      and not isinstance(
        value.right,
        bool,
      )
      and value.right < 0
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          -value.right
        )
      )

    if (
      isinstance(
        value.right,
        ScalarProduct,
      )
      and value.right.left == -1
    ):
      return (
        _render_scalar_latex(
          value.left
        )
        + " - "
        + _render_scalar_latex(
          value.right.right
        )
      )

    return (
      _render_scalar_latex(
        value.left
      )
      + " + "
      + _render_scalar_latex(
        value.right
      )
    )

  if isinstance(
    value,
    ScalarProduct,
  ):
    return (
      _render_scalar_latex(
        value.left
      )
      + r"\,"
      + _render_scalar_latex(
        value.right
      )
    )

  if isinstance(
    value,
    ScalarPower,
  ):
    return (
      "{"
      + _render_scalar_latex(
        value.base
      )
      + "}^{"
      + _render_scalar_latex(
        value.exponent
      )
      + "}"
    )

  raise TypeError(
    "unsupported scalar value for LaTeX rendering"
  )


'@ -split "`r?`n"

$before = @()
if ($start -gt 0) {
  $before = $lines[0..($start - 1)]
}

$after = $lines[$end..($lines.Count - 1)]

Copy-Item $rendererPath "$rendererPath.phase143_72a_r3.bak" -Force

$output = @()
$output += $before
$output += $newFunction
$output += $after

Set-Content -Path $rendererPath -Value $output -Encoding UTF8

$testContent = @'
from expression import (
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)


def test_phase143_72a_renders_negative_constant_product_in_scalar_sum_as_subtraction():
  n = ScalarSymbol(
    "n"
  )

  expression = IteratedSuspension(
    expression=HomotopyElement(
      name="η",
      dimension=4,
    ),
    exponent=ScalarSum(
      left=n,
      right=ScalarProduct(
        left=-1,
        right=4,
      ),
    ),
  )

  assert (
    render_toda_expression_latex(
      expression
    )
    == r"E^{n - 4}\eta"
  )


def test_phase143_72a_renders_negative_symbolic_product_in_scalar_sum_as_subtraction():
  m = ScalarSymbol(
    "m"
  )
  n = ScalarSymbol(
    "n"
  )

  expression = IteratedSuspension(
    expression=HomotopyElement(
      name="η",
      dimension=4,
    ),
    exponent=ScalarSum(
      left=m,
      right=ScalarProduct(
        left=-1,
        right=n,
      ),
    ),
  )

  assert (
    render_toda_expression_latex(
      expression
    )
    == r"E^{m - n}\eta"
  )


def test_phase143_72a_preserves_negative_integer_scalar_sum_rendering():
  n = ScalarSymbol(
    "n"
  )

  expression = IteratedSuspension(
    expression=HomotopyElement(
      name="η",
      dimension=4,
    ),
    exponent=ScalarSum(
      left=n,
      right=-4,
    ),
  )

  assert (
    render_toda_expression_latex(
      expression
    )
    == r"E^{n - 4}\eta"
  )
'@

Set-Content -Path $testPath -Value $testContent -Encoding UTF8

Write-Host "Phase 143-72A R3 applied."
Write-Host "Changed: toda_human_readable_renderer.py"
Write-Host "Added:   tests\test_phase143_72a_negative_scalar_product_latex.py"
