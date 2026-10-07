$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-7b repair12 - connector prefix fix"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PhaseDir = Join-Path $RepoRoot "phase159_r1_7b_repair12_connector_prefix_fix"
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/5] Apply repair12"
  python (Join-Path $PhaseDir "apply_phase159_r1_7b_repair12.py")
  if ($LASTEXITCODE -ne 0) {
    throw "repair12 apply failed"
  }

  Write-Host ""
  Write-Host "[2/5] Syntax preflight"
  python -m py_compile `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase159_r1_7b_repair11_inline_connector.py" `
    ".\tests\test_phase159_r1_7b_exact_sequence_display_order.py"
  if ($LASTEXITCODE -ne 0) {
    throw "syntax preflight failed"
  }

  Write-Host ""
  Write-Host "[3/5] Focused tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_7b_repair11_inline_connector.py" `
    ".\tests\test_phase159_r1_7b_exact_sequence_display_order.py" `
    ".\tests\test_phase157_r20_repair37_short_exact_after_map_support.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase148_rc2_3_exactness_exposure.py" `
    ".\tests\test_phase148_rc2_3_repair_r1.py"
  if ($LASTEXITCODE -ne 0) {
    throw "focused tests failed"
  }

  Write-Host ""
  Write-Host "[4/5] Render pi_11^4 verification"
  @'
from toda_calculation_facade import (
    build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)

report = build_standard_toda_report(
    n=4,
    k=7,
)
group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
)
replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
)
presentation = build_toda_group_proof_presentation(
    replay
)
rendered = render_toda_group_proof_narrative_markdown(
    presentation
)

print(rendered)

h_delta = (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
)
e_h = (
    "\\[\n"
    r"\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}."
    "\n\\]"
)
surjectivity = (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$"
    " は全射."
)

if h_delta not in rendered:
    raise SystemExit(
        "H-Delta exactness display is missing"
    )

if e_h not in rendered:
    raise SystemExit(
        "E-H exactness display is missing"
    )

if surjectivity not in rendered:
    raise SystemExit(
        "Delta surjectivity line is missing"
    )

if rendered.index(h_delta) > rendered.index(
    surjectivity
):
    raise SystemExit(
        "H-Delta exactness appears after Delta surjectivity"
    )

print(
    "pi_11^4 H-Delta / E-H display and ordering: OK"
)
'@ | python -
  if ($LASTEXITCODE -ne 0) {
    throw "pi11_4 verification failed"
  }

  Write-Host ""
  Write-Host "[5/5] Completion"
  Write-Host "Phase 159-R1-7b focused checks passed."
  Write-Host "Repository-wide pytest intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
