from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GENERIC = ROOT / "toda_group_proof_generic_narrative_renderer.py"
BODY = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"
TEST = ROOT / "tests" / "test_phase150_rc4_5e_2_short_exact_derivation_reason.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )
  return text.replace(old, new, 1)


def update_generic_renderer() -> None:
  text = GENERIC.read_text(encoding="utf-8")

  anchor = '''def _generic_narrative_dependency_labels(
'''
  helper = '''def _generic_short_exact_sequence_reason_prose(
  presentation: TodaGroupProofPresentation,
  exactness_step: ProofStep,
) -> str | None:
  short_exact_sequence_latex = (
    _generic_short_exact_sequence_latex(
      presentation,
      exactness_step,
    )
  )

  if short_exact_sequence_latex is None:
    return None

  return (
    "この完全性と、左の写像が単射、"
    "右の写像が全射であることより、"
    "次の短完全列を得る."
  )


'''
  if "def _generic_short_exact_sequence_reason_prose(" not in text:
    text = replace_once(
      text,
      anchor,
      helper + anchor,
      "insert short-exact reason helper",
    )

  old = '''    if short_exact_sequence_latex is not None:
      lines.append(
        "この完全性と両端の写像の性質より, "
        "次の短完全列を得る."
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + short_exact_sequence_latex
        + "$"
      )
      lines.append(
        ""
      )
'''
  new = '''    if short_exact_sequence_latex is not None:
      reason_prose = (
        _generic_short_exact_sequence_reason_prose(
          presentation,
          proof_step,
        )
      )

      if reason_prose is None:
        raise ValueError(
          "short exact sequence reason prose "
          "must exist when the sequence exists"
        )

      lines.append(
        reason_prose
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + short_exact_sequence_latex
        + "$"
      )
      lines.append(
        ""
      )
'''
  if old in text:
    text = replace_once(
      text,
      old,
      new,
      "generic proof short-exact prose",
    )
  elif new not in text:
    raise RuntimeError(
      "generic proof short-exact prose: expected old or new block"
    )

  GENERIC.write_text(text, encoding="utf-8")


def update_argument_body_renderer() -> None:
  text = BODY.read_text(encoding="utf-8")

  old_import = '''from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
)
'''
  new_import = '''from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
)
'''
  if old_import in text:
    text = replace_once(
      text,
      old_import,
      new_import,
      "argument body import",
    )
  elif new_import not in text:
    raise RuntimeError(
      "argument body import: expected old or new import"
    )

  old = '''    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .DERIVED_SHORT_EXACT_SEQUENCE
    ):
      lines.append(
        "この完全性と両端の写像の性質より, "
        "次の短完全列を得る."
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + contribution.latex
        + "$"
      )
      lines.append(
        ""
      )
      continue
'''
  new = '''    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .DERIVED_SHORT_EXACT_SEQUENCE
    ):
      reason_prose = (
        _generic_short_exact_sequence_reason_prose(
          presentation,
          contribution.proof_step,
        )
      )

      if reason_prose is None:
        raise ValueError(
          "derived short exact sequence must have "
          "typed reason prose"
        )

      lines.append(
        reason_prose
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + contribution.latex
        + "$"
      )
      lines.append(
        ""
      )
      continue
'''
  if old in text:
    text = replace_once(
      text,
      old,
      new,
      "argument body short-exact prose",
    )
  elif new not in text:
    raise RuntimeError(
      "argument body short-exact prose: expected old or new block"
    )

  BODY.write_text(text, encoding="utf-8")


def write_test() -> None:
  TEST.write_text(
    '''import inspect

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_reason_prose,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


def _pi6_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )


def test_phase150_rc4_5e_2_builds_short_exact_reason_from_typed_contract():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _pi6_data()

  reason_proses = tuple(
    _generic_short_exact_sequence_reason_prose(
      presentation,
      node.proof_step,
    )
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  expected = (
    "この完全性と、左の写像が単射、"
    "右の写像が全射であることより、"
    "次の短完全列を得る."
  )

  assert expected in reason_proses
  assert None in reason_proses


def test_phase150_rc4_5e_2_reason_is_visible_before_short_exact_sequence():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _pi6_data()

  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  reason = (
    "この完全性と、左の写像が単射、"
    "右の写像が全射であることより、"
    "次の短完全列を得る."
  )
  sequence = (
    "$0\\\\longrightarrow \\\\pi_{5}^{2}"
    "\\\\xrightarrow{E} \\\\pi_{6}^{3}"
    "\\\\xrightarrow{H} \\\\pi_{6}^{5}"
    "\\\\longrightarrow 0$"
  )

  assert rendered.count(reason) == 1
  assert sequence in rendered
  assert rendered.index(reason) < rendered.index(sequence)
  assert "この完全性と両端の写像の性質より" not in rendered


def test_phase150_rc4_5e_2_helper_has_no_target_or_rule_name_special_case():
  import toda_group_proof_generic_narrative_renderer as module

  source = inspect.getsource(
    module._generic_short_exact_sequence_reason_prose
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
    "inference_rule",
    ".rule",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
''',
    encoding="utf-8",
  )


def main() -> None:
  update_generic_renderer()
  update_argument_body_renderer()
  write_test()
  print("RC4-5E-2 minimal implementation applied.")
  print("Changed production files:")
  print("  toda_group_proof_generic_narrative_renderer.py")
  print("  toda_group_proof_narrative_argument_body_renderer.py")
  print("Added test:")
  print("  tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py")


if __name__ == "__main__":
  main()
