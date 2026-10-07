from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"


R9_A_OLD = """  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )

  generic_used_step_ids = (
"""

R9_A_NEW = """  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      rendered,
    )
  )

  generic_used_step_ids = (
"""


R9_C_OLD = """    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        boundary_visible_used_step_ids,
        presentation.root_step,
      )
    )

  if "[R" in rendered:
"""

R9_C_NEW = """    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        boundary_visible_used_step_ids,
        presentation.root_step,
      )
    )

  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

  if "[R" in rendered:
"""


def replace_once(
    source: str,
    old: str,
    new: str,
    label: str,
) -> str:
    count = source.count(old)

    if count == 0:
        if new in source:
            print(f"{label}: already applied")
            return source
        raise RuntimeError(
            f"{label}: expected anchor was not found"
        )

    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one anchor, found {count}"
        )

    print(f"{label}: applying")
    return source.replace(
        old,
        new,
        1,
    )


def main() -> int:
    if not TARGET.is_file():
        raise RuntimeError(
            f"Target file not found: {TARGET}"
        )

    source = TARGET.read_text(
        encoding="utf-8"
    )

    updated = replace_once(
        source,
        R9_A_OLD,
        R9_A_NEW,
        "R9-A final reflexive suppression",
    )
    updated = replace_once(
        updated,
        R9_C_OLD,
        R9_C_NEW,
        "R9-C post-selection reference relink",
    )

    if updated == source:
        print("No production changes were necessary.")
        return 0

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        TARGET,
        BACKUP_DIR / TARGET.name,
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
    )

    print(f"Updated: {TARGET.name}")
    print(
        "No group-specific n/k branch was added."
    )
    print(
        "No import change was required."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
