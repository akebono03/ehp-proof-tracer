$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159-R1-7b repair9 - semantic-closure exactness source"
Write-Host "=============================================================="

$RepoRoot = (Get-Location).Path
$PhaseDir = Join-Path $RepoRoot "phase159_r1_7b_repair9_semantic_closure_source"
$env:PYTHONPATH = "$RepoRoot;$RepoRoot\tests"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host "Repository root: $RepoRoot"
  Write-Host ""

  Write-Host "[1/6] Apply repair9"
  python (Join-Path $PhaseDir "apply_phase159_r1_7b_repair9.py")
  if ($LASTEXITCODE -ne 0) {
    throw "repair9 apply failed"
  }

  Write-Host ""
  Write-Host "[2/6] Syntax preflight"
  python -m py_compile `
    ".\toda_group_proof_narrative_renderer.py" `
    ".\tests\test_phase157_r20_repair37_short_exact_after_map_support.py" `
    ".\tests\test_phase159_r1_7b_exact_sequence_display_order.py"
  if ($LASTEXITCODE -ne 0) {
    throw "syntax preflight failed"
  }

  Write-Host ""
  Write-Host "[3/6] Semantic-closure exactness smoke check"
  @'
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
    _phase159_r1_7b_exactness_step_latex,
    _phase159_r1_7b_inline_exactness_latex,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_rules import TodaProp42ExactnessStatement

report = build_standard_toda_report(n=4, k=7)
group_result = report.candidates[0].source_candidate.group_result
replay = build_toda_group_result_proof_replay(group_result, max_depth=2)
presentation = build_toda_group_proof_presentation(replay)
closure = build_toda_group_proof_narrative_semantic_closure_presentation(
    presentation
)

exactness_latex = [
    _phase159_r1_7b_exactness_step_latex(node.proof_step)
    for node in closure.nodes
    if isinstance(node.proof_step.conclusion, TodaProp42ExactnessStatement)
]

target = (
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}"
)

if target not in exactness_latex:
    print("Closure exactness candidates:")
    for latex in exactness_latex:
        print(repr(latex))
    raise SystemExit(
        "missing typed H-Delta exactness in semantic closure"
    )

inline = (
    r"$\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}$."
)

if _phase159_r1_7b_inline_exactness_latex(inline) is None:
    raise SystemExit(
        "inline '$...$.' exactness parser failed"
    )

print("semantic-closure H-Delta exactness: OK")
print("runtime '$...$.' inline parser: OK")
'@ | python -
  if ($LASTEXITCODE -ne 0) {
    throw "semantic-closure smoke check failed"
  }

  Write-Host ""
  Write-Host "[4/6] Focused tests"
  python -m pytest -q `
    ".\tests\test_phase159_r1_7b_exact_sequence_display_order.py" `
    ".\tests\test_phase157_r20_repair37_short_exact_after_map_support.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase148_rc2_3_exactness_exposure.py" `
    ".\tests\test_phase148_rc2_3_repair_r1.py"
  if ($LASTEXITCODE -ne 0) {
    throw "focused tests failed"
  }

  Write-Host ""
  Write-Host "[5/6] Render pi_6^3 / pi_11^4 verification"
  @'
from pathlib import Path

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay

output_dir = (
    Path(
        "phase159_r1_7b_repair9_semantic_closure_source"
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
  Write-Host "[6/6] Completion"
  Write-Host "Focused tests passed."
  Write-Host "Repository-wide pytest intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
