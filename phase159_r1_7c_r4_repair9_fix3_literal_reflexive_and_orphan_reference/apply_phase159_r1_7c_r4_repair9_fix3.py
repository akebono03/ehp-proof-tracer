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

OLD_R9_A_BLOCK = '''  rendered = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      rendered,
    )
  )

'''

OLD_R9_C_BLOCK = '''  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

'''

NEW_HELPER = r'''def suppress_toda_group_proof_narrative_literal_reflexive_equalities(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  retained = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    comparable = paragraph.strip()

    if comparable.startswith(
      "[R"
    ):
      marker_end = comparable.find(
        "]"
      )

      if marker_end >= 0:
        suffix = comparable[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            comparable = suffix[
              len(
                prefix
              ):
            ]
            break

    comparable = comparable.rstrip(
      "."
    ).strip()

    if (
      comparable.startswith(
        "$"
      )
      and comparable.endswith(
        "$"
      )
    ):
      equation = comparable[
        1:-1
      ]

      if equation.count(
        "="
      ) == 1:
        lhs, rhs = equation.split(
          "=",
          1,
        )

        if (
          lhs.strip()
          == rhs.strip()
        ):
          continue

    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )


'''

NEW_R9_A_BLOCK = '''  rendered = (
    suppress_toda_group_proof_narrative_literal_reflexive_equalities(
      rendered
    )
  )

'''

R9_C_ELSE = '''  else:
    reference_entries = ()
    statement_lines_by_reference_number = {}

'''


def _remove_fix2_blocks(
    source: str,
) -> str:
    source = source.replace(
        OLD_R9_A_BLOCK,
        "",
        1,
    )
    source = source.replace(
        OLD_R9_C_BLOCK,
        "",
        1,
    )
    return source


def _insert_helper(
    source: str,
) -> str:
    if (
        "def suppress_toda_group_proof_narrative_literal_reflexive_equalities("
        in source
    ):
        print(
            "literal reflexive helper: already present"
        )
        return source

    anchor = (
        "def suppress_toda_group_proof_narrative_reflexive_equalities(\n"
    )
    index = source.find(
        anchor
    )

    if index < 0:
        raise RuntimeError(
            "Existing reflexive suppression helper "
            "anchor was not found."
        )

    print(
        "Adding literal reflexive equality helper."
    )

    return (
        source[
            :index
        ]
        + NEW_HELPER
        + source[
            index:
        ]
    )


def _function_slice(
    source: str,
) -> tuple[
    int,
    int,
    str,
]:
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
        end = next_function + 1

    return (
        start,
        end,
        source[
            start:end
        ],
    )


def _insert_final_literal_suppression(
    function_source: str,
) -> str:
    anchor = (
        "  generic_used_step_ids = (\n"
    )
    index = function_source.find(
        anchor
    )

    if index < 0:
        raise RuntimeError(
            "R9-A anchor "
            "`generic_used_step_ids` "
            "was not found."
        )

    prefix = function_source[
        :index
    ]

    if prefix.rstrip().endswith(
        NEW_R9_A_BLOCK.rstrip()
    ):
        print(
            "R9-A literal suppression: already applied"
        )
        return function_source

    print(
        "R9-A: inserting final literal "
        "reflexive suppression."
    )

    return (
        function_source[
            :index
        ]
        + NEW_R9_A_BLOCK
        + function_source[
            index:
        ]
    )


def _insert_final_orphan_reference_suppression(
    function_source: str,
) -> str:
    reference_anchor = (
        "  reference_section = (\n"
    )
    reference_index = function_source.rfind(
        reference_anchor
    )

    if reference_index < 0:
        raise RuntimeError(
            "Final reference section anchor "
            "was not found."
        )

    final_usage_anchor = (
        '  if "[R" in rendered:\n'
    )
    usage_index = function_source.rfind(
        final_usage_anchor,
        0,
        reference_index,
    )

    if usage_index < 0:
        raise RuntimeError(
            "Final body-usage filter anchor "
            "was not found."
        )

    block_end_anchor = (
        "\n\n  reference_section = (\n"
    )
    block_end = function_source.find(
        block_end_anchor,
        usage_index,
    )

    if block_end < 0:
        raise RuntimeError(
            "Could not locate the end of the "
            "final body-usage filter block."
        )

    current_block = function_source[
        usage_index:block_end
    ]

    if (
        "reference_entries = ()"
        in current_block
        and "statement_lines_by_reference_number = {}"
        in current_block
    ):
        print(
            "R9-C orphan suppression: already applied"
        )
        return function_source

    print(
        "R9-C: adding final orphan "
        "Reference suppression."
    )

    return (
        function_source[
            :block_end
        ]
        + "\n"
        + R9_C_ELSE.rstrip(
            "\n"
        )
        + function_source[
            block_end:
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

    updated = _remove_fix2_blocks(
        source
    )
    updated = _insert_helper(
        updated
    )

    (
        function_start,
        function_end,
        function_source,
    ) = _function_slice(
        updated
    )

    updated_function = (
        _insert_final_literal_suppression(
            function_source
        )
    )
    updated_function = (
        _insert_final_orphan_reference_suppression(
            updated_function
        )
    )

    updated = (
        updated[
            :function_start
        ]
        + updated_function
        + updated[
            function_end:
        ]
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
    )

    print(
        f"Updated: {TARGET.name}"
    )
    print(
        "No import changes."
    )
    print(
        "No group-specific n/k branch added."
    )
    print(
        "Removed repair9 fix2 relink/suppression calls."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
