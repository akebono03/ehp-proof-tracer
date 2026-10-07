from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
BACKUP_DIR = (
  PACKAGE_DIR
  / "backup_before_apply"
)

FUNCTION_NAME = (
  "def "
  "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown("
)

R9_A_BLOCK = """  rendered = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      rendered,
    )
  )

"""

R9_C_BLOCK = """  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

"""


def _function_slice(
    source: str,
) -> tuple[int, int, str]:
    start = source.find(
        FUNCTION_NAME
    )

    if start < 0:
        raise RuntimeError(
            "Target renderer function was not found."
        )

    next_function = source.find(
        "\ndef ",
        start + len(
            FUNCTION_NAME
        ),
    )

    if next_function < 0:
        end = len(
            source
        )
    else:
        end = (
            next_function
            + 1
        )

    return (
        start,
        end,
        source[
            start:end
        ],
    )


def _insert_r9_a(
    function_source: str,
) -> str:
    anchor = (
        "  generic_used_step_ids = (\n"
    )
    anchor_index = (
        function_source.find(
            anchor
        )
    )

    if anchor_index < 0:
        raise RuntimeError(
            "R9-A structural anchor "
            "`generic_used_step_ids` "
            "was not found."
        )

    prefix = function_source[
        :anchor_index
    ]

    if prefix.rstrip().endswith(
        R9_A_BLOCK.rstrip()
    ):
        print(
            "R9-A: already applied"
        )
        return function_source

    print(
        "R9-A: inserting final "
        "reflexive suppression"
    )

    return (
        function_source[
            :anchor_index
        ]
        + R9_A_BLOCK
        + function_source[
            anchor_index:
        ]
    )


def _insert_r9_c(
    function_source: str,
) -> str:
    reference_anchor = (
        "  reference_section = (\n"
    )
    reference_index = (
        function_source.rfind(
            reference_anchor
        )
    )

    if reference_index < 0:
        raise RuntimeError(
            "R9-C structural anchor "
            "`reference_section` "
            "was not found."
        )

    final_usage_anchor = (
        '  if "[R" in rendered:\n'
    )
    usage_index = (
        function_source.rfind(
            final_usage_anchor,
            0,
            reference_index,
        )
    )

    if usage_index < 0:
        raise RuntimeError(
            "R9-C final body-usage "
            "anchor was not found."
        )

    prefix = function_source[
        :usage_index
    ]

    if prefix.rstrip().endswith(
        R9_C_BLOCK.rstrip()
    ):
        print(
            "R9-C: already applied"
        )
        return function_source

    print(
        "R9-C: inserting "
        "post-selection Reference relink"
    )

    return (
        function_source[
            :usage_index
        ]
        + R9_C_BLOCK
        + function_source[
            usage_index:
        ]
    )


def main() -> int:
    if not TARGET.is_file():
        raise RuntimeError(
            f"Target file not found: {TARGET}"
        )

    source = TARGET.read_text(
        encoding="utf-8"
    )

    (
        function_start,
        function_end,
        function_source,
    ) = _function_slice(
        source
    )

    updated_function = (
        _insert_r9_a(
            function_source
        )
    )
    updated_function = (
        _insert_r9_c(
            updated_function
        )
    )

    if (
        updated_function
        == function_source
    ):
        print(
            "No production changes "
            "were necessary."
        )
        return 0

    updated_source = (
        source[
            :function_start
        ]
        + updated_function
        + source[
            function_end:
        ]
    )

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    backup = (
        BACKUP_DIR
        / TARGET.name
    )

    if not backup.exists():
        shutil.copy2(
            TARGET,
            backup,
        )

    TARGET.write_text(
        updated_source,
        encoding="utf-8",
    )

    print(
        f"Updated: {TARGET.name}"
    )
    print(
        "Changed function: "
        "render_toda_group_proof_narrative_"
        "multi_argument_with_contributions_markdown"
    )
    print(
        "No import changes."
    )
    print(
        "No group-specific n/k branch added."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
