$ErrorActionPreference = "Stop"

$repoRoot = (Get-Location).Path
$testPath = Join-Path $repoRoot "tests\test_phase143_72a_negative_scalar_product_latex.py"

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
      name="x",
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
    == r"E^{n - 4}x"
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
      name="x",
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
    == r"E^{m - n}x"
  )


def test_phase143_72a_preserves_negative_integer_scalar_sum_rendering():
  n = ScalarSymbol(
    "n"
  )

  expression = IteratedSuspension(
    expression=HomotopyElement(
      name="x",
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
    == r"E^{n - 4}x"
  )
'@

Set-Content -Path $testPath -Value $testContent -Encoding UTF8

Write-Host "Phase 143-72A R4 test repair applied."
Write-Host "Updated: tests\test_phase143_72a_negative_scalar_product_latex.py"
Write-Host "Renderer was not changed."
