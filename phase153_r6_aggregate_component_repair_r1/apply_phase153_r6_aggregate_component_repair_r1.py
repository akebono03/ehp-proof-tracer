from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  candidates = (
    PACKAGE_DIR.parent,
    Path.cwd(),
  )

  for candidate in candidates:
    if (
      (
        candidate
        / "toda_group_proof_narrative_contribution_renderer.py"
      ).is_file()
      and (
        candidate
        / "toda_group_proof_narrative_references.py"
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


def patch_imports(
  text: str,
) -> str:
  old = '''from collections import deque

from toda_group_proof_generic_narrative_renderer import (
'''

  new = '''from collections import deque
from dataclasses import (
  fields,
  is_dataclass,
)

from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_group_proof_generic_narrative_renderer import (
'''

  text = replace_once(
    text,
    old,
    new,
    "contribution renderer imports",
  )

  old = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  new = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  return replace_once(
    text,
    old,
    new,
    "contribution renderer reference imports",
  )


def patch_helpers(
  text: str,
) -> str:
  marker = '''def _toda_group_proof_narrative_reference_statement_lines_by_number(
'''

  helper = r'''def _phase153_r6_nested_value_contains(
  container,
  needle,
) -> bool:
  if container is needle:
    return True

  if isinstance(
    container,
    (
      str,
      bytes,
      int,
      float,
      bool,
      type(None),
    ),
  ):
    return False

  if isinstance(
    container,
    tuple,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container
    )

  if isinstance(
    container,
    list,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container
    )

  if isinstance(
    container,
    dict,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container.values()
    )

  if not is_dataclass(
    container
  ):
    return False

  return any(
    _phase153_r6_nested_value_contains(
      getattr(
        container,
        field.name,
      ),
      needle,
    )
    for field in fields(
      container
    )
  )


def _phase153_r6_group_relation_generators(
  statement,
) -> tuple:
  if not isinstance(
    statement,
    Relation,
  ):
    return ()

  if (
    statement.relation_type
    is not RelationType.EQUALITY
  ):
    return ()

  rhs = statement.rhs
  generator = getattr(
    rhs,
    "generator",
    None,
  )

  if generator is not None:
    return (
      generator,
    )

  summands = getattr(
    rhs,
    "summands",
    None,
  )

  if not isinstance(
    summands,
    tuple,
  ):
    return ()

  return tuple(
    generator
    for summand in summands
    for generator in (
      getattr(
        summand,
        "generator",
        None,
      ),
    )
    if generator is not None
  )


def _phase153_r6_reference_aggregate_component(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
):
  statement = proof_step.conclusion

  if not is_dataclass(
    statement
  ):
    return None

  relation_components = tuple(
    value
    for field in fields(
      statement
    )
    for value in (
      getattr(
        statement,
        field.name,
      ),
    )
    if (
      isinstance(
        value,
        Relation,
      )
      and _phase153_r6_group_relation_generators(
        value
      )
    )
  )

  if len(
    relation_components
  ) <= 1:
    return None

  external_consumers = tuple(
    edge.parent_step
    for edge in presentation.edges
    if (
      edge.premise_step
      is proof_step
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  )

  if not external_consumers:
    return None

  matching_components = []

  for component in relation_components:
    generators = (
      _phase153_r6_group_relation_generators(
        component
      )
    )

    if any(
      _phase153_r6_nested_value_contains(
        consumer.conclusion,
        generator,
      )
      for consumer in external_consumers
      for generator in generators
    ):
      matching_components.append(
        component
      )

  if len(
    matching_components
  ) != 1:
    return None

  return matching_components[
    0
  ]


def _phase153_r6_render_reference_statement(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  component = (
    _phase153_r6_reference_aggregate_component(
      presentation,
      entry,
      proof_step,
    )
  )

  if component is None:
    return rendered_statement

  component_step = ProofStep(
    conclusion=component,
    premises=(),
    rule=proof_step.rule,
    note=proof_step.note,
    inference_rule=proof_step.inference_rule,
  )

  return _render_generic_narrative_step(
    component_step
  )


'''

  if marker not in text:
    raise SystemExit(
      "contribution renderer helper insertion marker not found."
    )

  return text.replace(
    marker,
    helper + marker,
    1,
  )


def patch_statement_lines(
  text: str,
) -> str:
  old = '''    statement_lines = tuple(
      rendered_by_step_id[
        id(
          proof_step
        )
      ]
      for proof_step in selected_steps
    )
'''

  new = '''    statement_lines = tuple(
      _phase153_r6_render_reference_statement(
        presentation,
        entry,
        proof_step,
        rendered_by_step_id[
          id(
            proof_step
          )
        ],
      )
      for proof_step in selected_steps
    )
'''

  return replace_once(
    text,
    old,
    new,
    "reference statement line rendering",
  )


def install_test(
  repo: Path,
) -> None:
  shutil.copy2(
    (
      PACKAGE_DIR
      / "tests"
      / "test_phase153_r6_aggregate_component_granularity.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r6_aggregate_component_granularity.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()
  path = (
    repo
    / "toda_group_proof_narrative_contribution_renderer.py"
  )

  backup_dir = (
    repo
    / "phase153_r6_aggregate_component_repair_r1_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )
  backup_path = (
    backup_dir
    / path.name
  )

  if not backup_path.exists():
    shutil.copy2(
      path,
      backup_path,
    )

  text = path.read_text(
    encoding="utf-8"
  )
  text = patch_imports(
    text
  )
  text = patch_helpers(
    text
  )
  text = patch_statement_lines(
    text
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  install_test(
    repo
  )

  print(
    "Phase 153-R6 aggregate component repair R1 applied."
  )
  print(
    "Changed:"
  )
  print(
    "  toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Added:"
  )
  print(
    "  tests/test_phase153_r6_aggregate_component_granularity.py"
  )


if __name__ == "__main__":
  main()
