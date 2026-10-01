from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    if (
      (
        candidate
        / "toda_group_proof_narrative_references.py"
      ).is_file()
      and (
        candidate
        / "toda_group_proof_narrative_contribution_renderer.py"
      ).is_file()
      and (
        candidate
        / "tests"
      ).is_dir()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, "
      f"found {count}."
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_references(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_references.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  marker = (
    "def filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n"
  )

  helper = '''def filter_toda_group_proof_narrative_reference_entries_by_step_usage(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  used_step_ids: frozenset[
    int
  ],
  root_step: ProofStep,
) -> tuple[
  tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
]:
  if not isinstance(
    entries,
    tuple,
  ):
    raise TypeError(
      "entries must be a tuple"
    )

  if not all(
    isinstance(
      entry,
      TodaGroupProofNarrativeReferenceEntry,
    )
    for entry in entries
  ):
    raise TypeError(
      "entries must contain only "
      "TodaGroupProofNarrativeReferenceEntry objects"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    used_step_ids,
    frozenset,
  ):
    raise TypeError(
      "used_step_ids must be a frozenset"
    )

  if not all(
    isinstance(
      step_id,
      int,
    )
    and not isinstance(
      step_id,
      bool,
    )
    for step_id in used_step_ids
  ):
    raise TypeError(
      "used_step_ids must contain only integers"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      root_step
    )
  )

  used_entries = tuple(
    entry
    for entry in entries
    if (
      entry.reference
      != root_reference
      and any(
        id(
          proof_step
        )
        in used_step_ids
        for proof_step in entry.proof_steps
      )
    )
  )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      used_entries,
      start=1,
    )
  }

  filtered_entries = tuple(
    replace(
      entry,
      number=number_map[
        entry.number
      ],
    )
    for entry in used_entries
  )

  filtered_statement_lines = {
    number_map[
      entry.number
    ]: statement_lines_by_reference_number[
      entry.number
    ]
    for entry in used_entries
    if entry.number in statement_lines_by_reference_number
  }

  return (
    filtered_entries,
    filtered_statement_lines,
  )


'''

  if (
    "def filter_toda_group_proof_narrative_reference_entries_by_step_usage("
    in text
  ):
    raise SystemExit(
      "R11 generic step-usage filter is already present."
    )

  if marker not in text:
    raise SystemExit(
      "R11 insertion marker not found."
    )

  path.write_text(
    text.replace(
      marker,
      helper + marker,
      1,
    ),
    encoding="utf-8",
    newline="\n",
  )


def patch_contribution_renderer(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old_import = '''from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
'''

  new_import = '''from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
'''

  text = replace_once(
    text,
    old_import,
    new_import,
    "R11 argument imports",
  )

  old_ref_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  new_ref_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  text = replace_once(
    text,
    old_ref_import,
    new_ref_import,
    "R11 reference imports",
  )

  marker = (
    "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n"
  )

  helper = '''def build_toda_group_proof_narrative_generic_used_step_ids(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> frozenset[
  int
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )
  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }
  used_step_ids = set()

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    if (
      discourse_roles[
        ordered_position
      ]
      is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED
    ):
      continue

    argument_index = source_index_by_identity[
      id(
        argument
      )
    ]
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    used_step_ids.update(
      id(
        proof_step
      )
      for block in local_body_blocks
      for proof_step in block.steps
    )

  used_step_ids.update(
    id(
      contribution.proof_step
    )
    for contributions in ordered_contributions
    for contribution in contributions
  )

  return frozenset(
    used_step_ids
  )


'''

  if (
    "def build_toda_group_proof_narrative_generic_used_step_ids("
    in text
  ):
    raise SystemExit(
      "R11 generic used-step helper is already present."
    )

  if marker not in text:
    raise SystemExit(
      "R11 contribution helper insertion marker not found."
    )

  text = text.replace(
    marker,
    helper + marker,
    1,
  )

  old = '''  (
    reference_entries,
    statement_lines_by_reference_number,
    rendered,
  ) = (
    filter_toda_group_proof_narrative_reference_entries_by_body_usage(
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    )
  )
  reference_section = (
'''

  new = '''  if "[R" in rendered:
    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_body_usage(
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
      )
    )
  else:
    generic_used_step_ids = (
      build_toda_group_proof_narrative_generic_used_step_ids(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        ordered_contributions,
      )
    )
    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        generic_used_step_ids,
        presentation.root_step,
      )
    )

  reference_section = (
'''

  text = replace_once(
    text,
    old,
    new,
    "R11 generic reference attribution",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )


def install_test(
  repo: Path,
) -> None:
  shutil.copy2(
    (
      PACKAGE_DIR
      / "tests"
      / "test_phase153_r11_generic_reference_attribution_filtering.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r11_generic_reference_attribution_filtering.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()
  backup_dir = (
    repo
    / "phase153_r11_generic_reference_attribution_filtering_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )

  for filename in (
    "toda_group_proof_narrative_references.py",
    "toda_group_proof_narrative_contribution_renderer.py",
  ):
    source = repo / filename
    backup = backup_dir / filename

    if not backup.exists():
      shutil.copy2(
        source,
        backup,
      )

  patch_references(
    repo
  )
  patch_contribution_renderer(
    repo
  )
  install_test(
    repo
  )

  print(
    "Phase 153-R11 generic-route Reference attribution/filtering applied."
  )
  print(
    "Changed:"
  )
  print(
    "  toda_group_proof_narrative_references.py"
  )
  print(
    "  toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Added:"
  )
  print(
    "  tests/test_phase153_r11_generic_reference_attribution_filtering.py"
  )


if __name__ == "__main__":
  main()
