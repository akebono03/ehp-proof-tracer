from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent

def find_repository_root() -> Path:
  for candidate in (PACKAGE_DIR.parent, Path.cwd()):
    if (
      (candidate / "toda_group_proof_narrative_contribution_renderer.py").is_file()
      and (candidate / "toda_group_proof_narrative_renderer.py").is_file()
      and (candidate / "tests").is_dir()
    ):
      return candidate.resolve()
  raise SystemExit("EHP Proof Tracer repository root was not found.")

def replace_once(text: str, old: str, new: str, label: str) -> str:
  count = text.count(old)
  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, found {count}."
    )
  return text.replace(old, new, 1)

def patch_contribution_renderer(repo: Path) -> None:
  path = repo / "toda_group_proof_narrative_contribution_renderer.py"
  text = path.read_text(encoding="utf-8")
  marker = "def _toda_group_proof_narrative_reference_statement_lines_by_number(\n"

  helper = """def build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  str,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  marker_by_step_id = {}

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )
    marker = (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )

    for proof_step in selected_steps:
      marker_by_step_id[
        id(
          proof_step
        )
      ] = marker

  return marker_by_step_id


"""

  if "def build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(" in text:
    raise SystemExit("R9 reuse-marker helper is already present.")
  if marker not in text:
    raise SystemExit("R9 helper insertion marker not found.")

  path.write_text(
    text.replace(marker, helper + marker, 1),
    encoding="utf-8",
    newline="\n",
  )

def patch_narrative_renderer(repo: Path) -> None:
  path = repo / "toda_group_proof_narrative_renderer.py"
  text = path.read_text(encoding="utf-8")

  old_import = """from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
"""
  new_import = """from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  build_toda_group_proof_narrative_reference_reuse_marker_by_step_id,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
"""
  text = replace_once(text, old_import, new_import, "R9 contribution import")

  start = text.index("def _append_narrative_for_step(\n")
  end = text.index("\ndef _is_phase134_9_pi8_5_presentation(", start)
  old_function = text[start:end]

  new_function = """def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
  reference_marker_by_step_id: dict[int, str] | None = None,
  reference_reuse_marker_by_step_id: dict[int, str] | None = None,
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step
    premise_id = id(
      premise_step
    )
    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    premise_reference_marker = (
      None
      if (
        reference_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
    premise_reference_reuse_marker = (
      None
      if (
        reference_reuse_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_reuse_marker_by_step_id.get(
        premise_id
      )
    )
    lead = (
      _premise_lead(
        index,
        len(
          edges
        ),
      )
    )

    if premise_id in expanded_step_ids:
      if parent_step is presentation.root_step:
        lines.append(
          (
            lead
            + "、すでに得た"
            + premise_fact
            + "を用いる。"
          )
        )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if (
      premise_edges
      and premise_reference_reuse_marker is not None
    ):
      lines.append(
        (
          lead
          + "、"
          + premise_reference_reuse_marker
          + "を用いる。"
        )
      )
    elif premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
        reference_marker_by_step_id,
        reference_reuse_marker_by_step_id,
      )

      lines.append(
        (
          _derivation_lead(
            len(
              premise_edges
            )
          )
          + "、"
          + premise_fact
          + "を得る。"
        )
      )
    else:
      generic_premise_fact = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      inference_rule = (
        premise_step.inference_rule
      )
      generic_fact_is_fallback = (
        (
          inference_rule is not None
          and generic_premise_fact == inference_rule.name
        )
        or generic_premise_fact
        == (
          "`"
          + type(
            premise_step.conclusion
          ).__name__
          + "`"
        )
        or generic_premise_fact == repr(
          premise_step.conclusion
        )
        or generic_premise_fact == str(
          premise_step.conclusion
        )
      )
      reference_plus_semantic_fact = (
        premise_reference_marker is not None
        and not (
          is_toda_group_proof_narrative_provenance_only_statement(
            premise_step.conclusion
          )
        )
        and not generic_fact_is_fallback
      )

      if reference_plus_semantic_fact:
        if (
          generic_premise_fact.startswith("$")
          and generic_premise_fact.endswith("$")
        ):
          lines.append(
            (
              lead
              + "、"
              + premise_reference_marker
              + " により、"
              + generic_premise_fact
              + "を得る。"
            )
          )
        else:
          lines.append(
            (
              lead
              + "、"
              + premise_reference_marker
              + " により、"
              + generic_premise_fact
            )
          )
      else:
        lines.append(
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

    expanded_step_ids.add(
      premise_id
    )

  active_step_ids.remove(
    parent_id
  )

"""

  text = text[:start] + new_function + text[end:]

  old_map = """  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }

  lines = [
"""
  new_map = """  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }
  reference_reuse_marker_by_step_id = (
    build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
      presentation,
      reference_entries,
    )
  )

  lines = [
"""
  text = replace_once(text, old_map, new_map, "R9 reuse marker map")

  old_call = """    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
      reference_marker_by_step_id,
    )
"""
  new_call = """    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
      reference_marker_by_step_id,
      reference_reuse_marker_by_step_id,
    )
"""
  text = replace_once(text, old_call, new_call, "R9 root recursive call")

  path.write_text(text, encoding="utf-8", newline="\n")

def install_test(repo: Path) -> None:
  shutil.copy2(
    PACKAGE_DIR / "tests" / "test_phase153_r9_reference_reuse_derivation_suppression.py",
    repo / "tests" / "test_phase153_r9_reference_reuse_derivation_suppression.py",
  )

def main() -> None:
  repo = find_repository_root()
  backup_dir = repo / "phase153_r9_reference_reuse_derivation_suppression_backup"
  backup_dir.mkdir(exist_ok=True)

  for filename in (
    "toda_group_proof_narrative_contribution_renderer.py",
    "toda_group_proof_narrative_renderer.py",
  ):
    source = repo / filename
    backup = backup_dir / filename
    if not backup.exists():
      shutil.copy2(source, backup)

  patch_contribution_renderer(repo)
  patch_narrative_renderer(repo)
  install_test(repo)

  print("Phase 153-R9 reference reuse / derivation suppression applied.")
  print("Changed:")
  print("  toda_group_proof_narrative_contribution_renderer.py")
  print("  toda_group_proof_narrative_renderer.py")
  print("Added:")
  print("  tests/test_phase153_r9_reference_reuse_derivation_suppression.py")

if __name__ == "__main__":
  main()
