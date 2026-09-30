from pathlib import Path

REFERENCES = Path("toda_group_proof_narrative_references.py")
RENDERER = Path("toda_group_proof_narrative_renderer.py")
TEST = Path("tests/test_phase150_rc4_7a_cross_group_reference_normalization.py")


def replace_once(text, old, new, label):
  if old not in text:
    raise RuntimeError(f"target not found: {label}")
  if text.count(old) != 1:
    raise RuntimeError(f"target is not unique: {label}")
  return text.replace(old, new, 1)


def patch_references():
  text = REFERENCES.read_text(encoding="utf-8")
  text = replace_once(
    text,
    "from dataclasses import dataclass\n",
    "from dataclasses import dataclass\nimport re\n",
    "references import",
  )
  old = '''def extract_toda_group_proof_step_literature_reference(
  proof_step: ProofStep,
) -> LiteratureReference | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")
  if proof_step.inference_rule is None:
    return None
  return proof_step.inference_rule.literature_reference
'''
  new = r'''def _infer_toda_group_proof_literature_reference_from_rule_name(
  rule_name: str,
) -> LiteratureReference | None:
  if not isinstance(rule_name, str):
    raise TypeError("rule_name must be a str")

  named_match = re.match(
    r"^Toda (Proposition|Lemma|Theorem|Equation) ([0-9]+(?:\.[0-9]+)*)\b",
    rule_name,
  )
  if named_match is not None:
    kind, number = named_match.groups()
    locator = f"{kind} {number}"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  parenthesized_match = re.match(
    r"^Toda \(([0-9]+(?:\.[0-9]+)*)\)\b",
    rule_name,
  )
  if parenthesized_match is not None:
    number = parenthesized_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  bare_equation_match = re.match(
    r"^Toda ([0-9]+\.[0-9]+)\b",
    rule_name,
  )
  if bare_equation_match is not None:
    number = bare_equation_match.group(1)
    locator = f"({number})"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )

  return None


def extract_toda_group_proof_step_literature_reference(
  proof_step: ProofStep,
) -> LiteratureReference | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")

  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  if inference_rule.literature_reference is not None:
    return inference_rule.literature_reference

  return _infer_toda_group_proof_literature_reference_from_rule_name(
    inference_rule.name
  )
'''
  text = replace_once(text, old, new, "reference extraction")
  REFERENCES.write_text(text, encoding="utf-8")


def patch_renderer():
  text = RENDERER.read_text(encoding="utf-8")
  old_import = '''from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
'''
  new_import = '''from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''
  text = replace_once(text, old_import, new_import, "renderer imports")

  old_sig = '''def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
) -> None:
'''
  new_sig = '''def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
  reference_marker_by_step_id: dict[int, str] | None = None,
) -> None:
'''
  text = replace_once(text, old_sig, new_sig, "append signature")

  old_fact = '''    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
'''
  new_fact = '''    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    premise_reference_marker = (
      None
      if reference_marker_by_step_id is None
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
'''
  text = replace_once(text, old_fact, new_fact, "premise marker")

  old_recursive = '''      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
      )
'''
  new_recursive = '''      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
        reference_marker_by_step_id,
      )
'''
  text = replace_once(text, old_recursive, new_recursive, "recursive marker")

  old_leaf = '''      lines.append(
        (
          lead
          + "、"
          + premise_fact
          + "を用いる。"
        )
      )
'''
  new_leaf = '''      lines.append(
        (
          lead
          + "、"
          + (
            premise_reference_marker
            if premise_reference_marker is not None
            else premise_fact
          )
          + "を用いる。"
        )
      )
'''
  text = replace_once(text, old_leaf, new_leaf, "leaf reference")

  old_lines = '''  lines = [
    "# Group proof narrative",
    "",
    theorem + "を用いる。",
    "",
  ]

  root_edges = (
'''
  new_lines = '''  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )
  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }

  lines = [
    "# Group proof narrative",
    "",
    theorem + "を用いる。",
    "",
  ]

  if reference_section:
    lines.extend(
      (
        "## 使用する結果",
        "",
        reference_section,
        "",
        "## 証明",
        "",
      )
    )

  root_edges = (
'''
  text = replace_once(text, old_lines, new_lines, "fallback reference section")

  old_root_call = '''    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
    )
'''
  new_root_call = '''    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
      reference_marker_by_step_id,
    )
'''
  text = replace_once(text, old_root_call, new_root_call, "root marker")
  RENDERER.write_text(text, encoding="utf-8")


def write_test():
  TEST.write_text(r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)


def _render_group(n: int, k: int) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_complete_toda_group_result_proof_replay(
    group_result
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase150_rc4_7a_pi10_4_numbers_normalized_references(
):
  rendered = _render_group(4, 6)
  assert "## 使用する結果" in rendered
  assert "Proposition 5.11" in rendered
  assert "Proposition 5.6" in rendered
  assert "(5.6)" in rendered
  assert "Lemma 5.4" in rendered
  assert "[R1]" in rendered


def test_phase150_rc4_7a_pi12_5_numbers_normalized_references(
):
  rendered = _render_group(5, 7)
  assert "## 使用する結果" in rendered
  assert "Proposition 5.15" in rendered
  assert "Lemma 5.13" in rendered
  assert "Proposition 5.11" in rendered
  assert "[R1]" in rendered


def test_phase150_rc4_7a_pi16_9_numbers_normalized_references(
):
  rendered = _render_group(9, 7)
  assert "## 使用する結果" in rendered
  assert "Proposition 5.15" in rendered
  assert "Lemma 5.14" in rendered
  assert "Theorem 3.6" in rendered
  assert "[R1]" in rendered


def test_phase150_rc4_7a_pi15_8_special_renderer_is_unchanged(
):
  rendered = _render_group(8, 7)
  assert "Toda Proposition 4.4 の分解同型" in rendered
  assert "直和因子の順序を入れ替えると," in rendered
''', encoding="utf-8")


def main():
  patch_references()
  patch_renderer()
  write_test()
  print("Phase 150 RC4-7A applied.")
  print("Changed: toda_group_proof_narrative_references.py")
  print("Changed: toda_group_proof_narrative_renderer.py")
  print("Added: tests/test_phase150_rc4_7a_cross_group_reference_normalization.py")


if __name__ == "__main__":
  main()
