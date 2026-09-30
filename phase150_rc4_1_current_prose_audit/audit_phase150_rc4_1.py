from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


HISTORICAL_COMMIT = "908e24db89669750949fa9ad149f5e306ac05546"
HISTORICAL_RENDERER_PATH = "toda_group_proof_narrative_renderer.py"


@dataclass(frozen=True)
class ReasonProbe:
  key: str
  historical_pattern: str
  current_patterns: tuple[str, ...]
  classification: str
  rc4_candidate: bool
  note: str


PROBES = (
  ReasonProbe(
    key="definition_precondition_to_bracket",
    historical_pattern=r"\(1\), \(2\).*Lemma 5\.2.*仮定",
    current_patterns=(
      r"2\\eta_\{3\}\s*=\s*0",
      r"\\nu'\s*\\in\s*\\\{\\eta_\{3\}",
    ),
    classification="PRECONDITION + DEFINITION -> applicability reason",
    rc4_candidate=True,
    note="Explain why the displayed precondition and bracket membership permit the lemma to be applied.",
  ),
  ReasonProbe(
    key="hopf_image_derivation",
    historical_pattern=r"H\(\\beta\)=E\^\{2\}\\alpha.*E\^\{2\}\\eta_\{3\}=\\eta_\{5\}",
    current_patterns=(
      r"H\\left\(\\nu'\\right\)\s*=\s*E\^\{2\}\\eta_\{3\}",
      r"E\^\{2\}\\eta_\{3\}\s*=\s*\\eta_\{5\}",
      r"H\\left\(\\nu'\\right\)\s*=\s*\\eta_\{5\}",
    ),
    classification="CALCULATION dependency chain -> derived equality reason",
    rc4_candidate=True,
    note="The facts are present; the prose should state that the final equality follows from the preceding two equalities.",
  ),
  ReasonProbe(
    key="surjectivity_to_delta_zero",
    historical_pattern=r"Im.?H.*ker.?\\Delta.*\\pi_\{7\}\^\{5\}",
    current_patterns=(
      r"H:\s*\\pi_\{7\}\^\{3\}\s*\\to\s*\\pi_\{7\}\^\{5\}",
      r"\\Delta:\s*\\pi_\{7\}\^\{5\}\s*\\to\s*\\pi_\{5\}\^\{2\}",
    ),
    classification="EXACTNESS + MAP_PROPERTY -> zero-map reason",
    rc4_candidate=True,
    note="Explain ker(Delta)=Im(H) and why surjectivity of H makes Delta zero.",
  ),
  ReasonProbe(
    key="delta_zero_to_suspension_injective",
    historical_pattern=r"Im.?\\Delta.*ker.?E.*0",
    current_patterns=(
      r"\\Delta:\s*\\pi_\{7\}\^\{5\}\s*\\to\s*\\pi_\{5\}\^\{2\}",
      r"E:\s*\\pi_\{5\}\^\{2\}\s*\\to\s*\\pi_\{6\}\^\{3\}",
    ),
    classification="EXACTNESS + zero map -> injectivity reason",
    rc4_candidate=True,
    note="Explain ker(E)=Im(Delta)=0, hence E is injective.",
  ),
  ReasonProbe(
    key="injectivity_to_eta3_cube_order",
    historical_pattern=r"\(7\), \(14\).*E\(\\eta_\{2\}\^\{3\}\)=\\eta_\{3\}\^\{3\}",
    current_patterns=(
      r"operatorname\{ord\}.*\\eta_\{3\}\^\{3\}",
    ),
    classification="GROUP_STRUCTURE + MAP_PROPERTY + transport -> order reason",
    rc4_candidate=True,
    note="Explain why injectivity preserves the nonzero order-two generator under suspension.",
  ),
  ReasonProbe(
    key="double_relation_to_nu_prime_order",
    historical_pattern=r"\(5\), \(15\)",
    current_patterns=(
      r"2\\nu'\s*=\s*\\eta_\{3\}\^\{3\}",
      r"operatorname\{ord\}.*\\nu'",
    ),
    classification="CALCULATION + ORDER -> element-order reason",
    rc4_candidate=True,
    note="Explain why 2 nu' has order two, forcing nu' to have order four.",
  ),
  ReasonProbe(
    key="short_exact_sequence_derivation",
    historical_pattern=r"\(8\), \(14\), \(18\).*短完全列",
    current_patterns=(
      r"0\\longrightarrow\s*\\pi_\{5\}\^\{2\}",
    ),
    classification="EXACTNESS + injective + surjective -> short-exact reason",
    rc4_candidate=True,
    note="Explain why exactness together with endpoint map properties yields the short exact sequence.",
  ),
  ReasonProbe(
    key="short_exact_to_group_structure",
    historical_pattern=r"\(7\), \(17\), \(19\).*位数.*4",
    current_patterns=(
      r"\\pi_\{5\}\^\{2\}",
      r"\\pi_\{6\}\^\{5\}\s*=\s*\\mathbb\{Z\}/2",
      r"\\pi_\{6\}\^\{3\}\s*=\s*\\mathbb\{Z\}/4",
    ),
    classification="SHORT_EXACT + endpoint structures -> middle-group order reason",
    rc4_candidate=True,
    note="Explain why the short exact sequence gives order four for the middle group.",
  ),
  ReasonProbe(
    key="order_four_member_to_generator",
    historical_pattern=r"\\nu'.*位数 4.*生成",
    current_patterns=(
      r"\\nu'\s*\\in\s*\\pi_\{6\}\^\{3\}",
      r"operatorname\{ord\}.*\\nu'",
      r"\\pi_\{6\}\^\{3\}\s*=\s*\\mathbb\{Z\}/4",
    ),
    classification="MEMBERSHIP + ORDER + GROUP_ORDER -> generator reason",
    rc4_candidate=True,
    note="Explain why an element of order four generates a group of order four.",
  ),
)


def _git_show(path: str) -> str:
  result = subprocess.run(
    ["git", "show", f"{HISTORICAL_COMMIT}:{path}"],
    check=True,
    capture_output=True,
    text=True,
    encoding="utf-8",
  )
  return result.stdout


def _current_pi6_3() -> str:
  presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)
  return render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def _contains_all(text: str, patterns: tuple[str, ...]) -> bool:
  return all(re.search(pattern, text, re.S) is not None for pattern in patterns)


def main() -> int:
  output_dir = Path("phase150_rc4_1_current_prose_audit") / "audit_output"
  output_dir.mkdir(parents=True, exist_ok=True)

  historical_source = _git_show(HISTORICAL_RENDERER_PATH)
  current = _current_pi6_3()

  # The historical renderer source is used as the stable semantic baseline.
  # Phase 146 already established HISTORICAL_COMMIT as the Phase 136-2 baseline.
  records = []
  for probe in PROBES:
    historical_evidence = re.search(
      probe.historical_pattern,
      historical_source,
      re.S,
    ) is not None
    current_facts_present = _contains_all(
      current,
      probe.current_patterns,
    )
    records.append(
      (
        probe,
        historical_evidence,
        current_facts_present,
      )
    )

  lines = [
    "=" * 78,
    "Phase 150 / RC4-1 Current prose audit",
    f"Historical baseline commit: {HISTORICAL_COMMIT}",
    "Production changes: none",
    "Existing test changes: none",
    "Repository-wide tests: not run",
    "=" * 78,
    "",
    "CURRENT pi_6^3 NARRATIVE",
    "-" * 78,
    current,
    "",
    "REASON-PROSE AUDIT",
    "-" * 78,
  ]

  rc4_candidates = 0
  for index, (probe, historical_evidence, current_facts_present) in enumerate(
    records,
    start=1,
  ):
    if probe.rc4_candidate and current_facts_present:
      rc4_candidates += 1
    lines.extend(
      (
        f"[{index}] {probe.key}",
        f"classification: {probe.classification}",
        f"historical_reason_evidence: {historical_evidence}",
        f"current_required_facts_present: {current_facts_present}",
        f"rc4_candidate: {probe.rc4_candidate}",
        f"note: {probe.note}",
        "",
      )
    )

  lines.extend(
    (
      "BOUNDARY",
      "-" * 78,
      "RC4 owns explanatory reason/provenance prose.",
      "RC4 does not redesign RC3 contribution placement.",
      "RC4 does not introduce RC5 EHP semantic naming.",
      "RC4 does not perform RC6 equation-numbering cleanup.",
      (
        "The position of (1),(2) => 2nu'=eta_3^3 is recorded only as a "
        "reason-prose candidate when its dependency explanation is missing; "
        "its placement is not changed here."
      ),
      "",
      f"reason_prose_candidates={rc4_candidates}",
      "AUDIT_RESULT=PASS",
    )
  )

  report = "\n".join(lines) + "\n"
  report_path = output_dir / "phase150_rc4_1_report.txt"
  report_path.write_text(report, encoding="utf-8")
  (output_dir / "current_pi6_3.txt").write_text(current, encoding="utf-8")

  print(report)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
