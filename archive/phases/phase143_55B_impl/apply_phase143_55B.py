from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  if old not in text:
    if new in text:
      return text
    raise RuntimeError(
      f"expected {label} was not found"
    )
  return text.replace(
    old,
    new,
    1,
  )


def update_body_renderer() -> None:
  path = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"
  text = path.read_text(
    encoding="utf-8",
  )

  old_import = """from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _render_generic_narrative_proof_block,
)
"""
  new_import = """from toda_group_proof_generic_narrative_renderer import (
  _generic_narrative_dependency_labels,
  _generic_narrative_sentence_lead,
  _render_generic_narrative_proof_block,
  _render_generic_narrative_step,
)
from proof import (
  ProofStep,
)
"""
  text = replace_once(
    text,
    old_import,
    new_import,
    "body renderer import block",
  )

  marker = """def render_toda_group_proof_narrative_argument_body_markdown(
"""
  helper = SOURCE.joinpath(
    "body_renderer_helpers.txt"
  ).read_text(
    encoding="utf-8",
  )
  if helper not in text:
    if marker not in text:
      raise RuntimeError(
        "body renderer function marker was not found"
      )
    text = text.replace(
      marker,
      helper + marker,
      1,
    )

  old_signature_tail = """  connector_before_block_id: int | None = None,
  connector_text: str | None = None,
) -> str:
"""
  new_signature_tail = """  connector_before_block_id: int | None = None,
  connector_text: str | None = None,
  conclusion_step: ProofStep | None = None,
) -> str:
"""
  text = replace_once(
    text,
    old_signature_tail,
    new_signature_tail,
    "body renderer signature tail",
  )

  old_validation_marker = """  if (
    connector_before_block_id is None
  ) != (
    connector_text is None
  ):
    raise ValueError(
      "connector_before_block_id and connector_text "
      "must be provided together"
    )

  block_index_by_identity = {
"""
  new_validation_marker = """  if (
    connector_before_block_id is None
  ) != (
    connector_text is None
  ):
    raise ValueError(
      "connector_before_block_id and connector_text "
      "must be provided together"
    )

  if (
    conclusion_step is not None
    and not isinstance(
      conclusion_step,
      ProofStep,
    )
  ):
    raise TypeError(
      "conclusion_step must be a ProofStep or None"
    )

  if (
    conclusion_step is not None
    and connector_before_block_id is None
  ):
    raise ValueError(
      "conclusion_step requires connector placement"
    )

  block_index_by_identity = {
"""
  text = replace_once(
    text,
    old_validation_marker,
    new_validation_marker,
    "body renderer connector validation",
  )

  old_non_exact = """      block_lines = tuple(
        _render_generic_narrative_proof_block(
          presentation,
          blocks,
          block_index,
          show_dependency_labels=False,
          suppress_provenance_only=True,
        )
      )

    if not block_lines:
      continue

    if (
      not connector_inserted
      and connector_before_block_id is not None
      and id(
        block
      )
      == connector_before_block_id
    ):
      lines.append(
        connector_text
      )
      lines.append(
        ""
      )
      connector_inserted = True

    lines.extend(
      block_lines
    )
"""
  # tolerate formatter style used by 53B-R where equality may be on same line
  if old_non_exact not in text:
    old_non_exact = """      block_lines = tuple(
        _render_generic_narrative_proof_block(
          presentation,
          blocks,
          block_index,
          show_dependency_labels=False,
          suppress_provenance_only=True,
        )
      )

    if not block_lines:
      continue

    if (
      not connector_inserted
      and connector_before_block_id is not None
      and id(
        block
      ) == connector_before_block_id
    ):
      lines.append(
        connector_text
      )
      lines.append(
        ""
      )
      connector_inserted = True

    lines.extend(
      block_lines
    )
"""

  new_non_exact = """      reordered_block = block

      if (
        conclusion_step is not None
        and connector_before_block_id is not None
        and id(
          block
        ) == connector_before_block_id
        and conclusion_step in block.steps
      ):
        reordered_block = (
          _reorder_toda_group_proof_narrative_block_conclusion_step_last(
            block,
            conclusion_step,
          )
        )

      render_blocks = blocks

      if reordered_block is not block:
        render_blocks = (
          blocks[
            :block_index
          ]
          + (
            reordered_block,
          )
          + blocks[
            block_index + 1:
          ]
        )

      block_lines = tuple(
        _render_generic_narrative_proof_block(
          presentation,
          render_blocks,
          block_index,
          show_dependency_labels=False,
          suppress_provenance_only=True,
        )
      )

    if not block_lines:
      continue

    if (
      not connector_inserted
      and connector_before_block_id is not None
      and id(
        block
      ) == connector_before_block_id
    ):
      if (
        conclusion_step is not None
        and conclusion_step in block.steps
        and block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        block_lines = (
          _insert_toda_group_proof_narrative_connector_before_conclusion_step(
            block_lines,
            conclusion_step,
            connector_text,
          )
        )
      else:
        block_lines = (
          connector_text,
          "",
        ) + block_lines

      connector_inserted = True

    lines.extend(
      block_lines
    )
"""
  text = replace_once(
    text,
    old_non_exact,
    new_non_exact,
    "body renderer block rendering section",
  )

  path.write_text(
    text,
    encoding="utf-8",
  )
  print(
    f"updated {path}"
  )


def update_multi_renderer() -> None:
  path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
  text = path.read_text(
    encoding="utf-8",
  )

  old_import = """from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
)
"""
  new_import = """from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
"""
  text = replace_once(
    text,
    old_import,
    new_import,
    "multi renderer arguments import",
  )

  old_connector = """    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )

    body = (
"""
  new_connector = """    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )
    conclusion_step = (
      None
      if connector is None
      else extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    body = (
"""
  text = replace_once(
    text,
    old_connector,
    new_connector,
    "multi renderer connector section",
  )

  old_call_tail = """        connector_text=connector,
      )
    )
"""
  new_call_tail = """        connector_text=connector,
        conclusion_step=conclusion_step,
      )
    )
"""
  text = replace_once(
    text,
    old_call_tail,
    new_call_tail,
    "multi renderer body call tail",
  )

  path.write_text(
    text,
    encoding="utf-8",
  )
  print(
    f"updated {path}"
  )


def copy_file(
  source_relative: str,
  destination_relative: str,
) -> None:
  source = SOURCE / source_relative
  destination = ROOT / destination_relative
  destination.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copyfile(
    source,
    destination,
  )
  print(
    f"updated {destination}"
  )


def main() -> None:
  update_body_renderer()
  update_multi_renderer()
  copy_file(
    "tests/test_phase143_55b_conclusion_step_ordering.py",
    "tests/test_phase143_55b_conclusion_step_ordering.py",
  )


if __name__ == "__main__":
  main()
