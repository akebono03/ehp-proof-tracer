$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-7b repair5 - normalizer call fix"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PhaseDir = Join-Path $RepoRoot "phase159_r1_7b_repair5_normalizer_call_fix"
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/5] Apply repair5"
  python (Join-Path $PhaseDir "apply_phase159_r1_7b_repair5.py")
  if ($LASTEXITCODE -ne 0) {
    throw "repair5 apply failed"
  }

  Write-Host ""
  Write-Host "[2/5] Syntax preflight"
  python -m py_compile `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase157_r20_repair37_short_exact_after_map_support.py" `
    ".\tests\test_phase159_r1_7b_exact_sequence_display_order.py"
  if ($LASTEXITCODE -ne 0) {
    throw "syntax preflight failed"
  }

  Write-Host ""
  Write-Host "[3/5] Verify normalizer call is present"
  @'
import ast
from pathlib import Path

path = Path("toda_group_proof_narrative_renderer.py")
source = path.read_text(encoding="utf-8-sig")
tree = ast.parse(source)

contract = next(
    node
    for node in tree.body
    if (
        isinstance(node, ast.FunctionDef)
        and node.name
        == "_phase158_normalize_public_narrative_contract"
    )
)

calls = [
    node
    for node in contract.body
    if (
        isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id
        == "_phase159_r1_7b_normalize_public_exact_sequences"
    )
]

if len(calls) != 1:
    raise SystemExit(
        "expected exactly one R1-7b normalizer call, "
        f"found {len(calls)}"
    )

print("R1-7b normalizer call count: 1")
'@ | python -
  if ($LASTEXITCODE -ne 0) {
    throw "normalizer call verification failed"
  }

  Write-Host ""
  Write-Host "[4/5] Focused tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_7b_exact_sequence_display_order.py" `
    ".\tests\test_phase157_r20_repair37_short_exact_after_map_support.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py"
  if ($LASTEXITCODE -ne 0) {
    throw "focused tests failed"
  }

  Write-Host ""
  Write-Host "[5/5] Render verification"
  @'
from pathlib import Path

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)

output_dir = (
    Path(
        "phase159_r1_7b_repair5_normalizer_call_fix"
    )
    / "verification_output"
)
output_dir.mkdir(
    parents=True,
    exist_ok=True,
)

for label, n, k in (
    ("pi6_3", 3, 3),
    ("pi11_4", 4, 7),
):
    report = build_standard_toda_report(
        n=n,
        k=k,
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

    (
        output_dir
        / f"{label}.md"
    ).write_text(
        rendered,
        encoding="utf-8",
    )

    print("=" * 78)
    print(label)
    print("=" * 78)
    print(rendered)
'@ | python -
  if ($LASTEXITCODE -ne 0) {
    throw "verification render failed"
  }

  Write-Host ""
  Write-Host "Focused tests passed."
  Write-Host "Repository-wide pytest intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
