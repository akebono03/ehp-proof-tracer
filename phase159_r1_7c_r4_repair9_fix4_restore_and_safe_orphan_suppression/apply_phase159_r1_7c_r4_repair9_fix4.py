from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)

FIX3_DIR = (
  REPO_ROOT
  / "phase159_r1_7c_r4_repair9_fix3_literal_reflexive_and_orphan_reference"
)
FIX3_BACKUP = (
  FIX3_DIR
  / "backup_before_apply"
  / TARGET.name
)

BACKUP_DIR = (
  PACKAGE_DIR
  / "backup_before_fix4"
)

FUNCTION_NAME = (
  "def "
  "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown("
)

FIX2_R9_A_BLOCK = '''  rendered = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      rendered,
    )
  )

'''

FIX2_R9_C_BLOCK = '''  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

'''

LITERAL_HELPER = r'''def suppress_toda_group_proof_narrative_literal_reflexive_equalities(
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

FINAL_LITERAL_BLOCK = '''  rendered = (
    suppress_toda_group_proof_narrative_literal_reflexive_equalities(
      rendered
    )
  )

'''

ORPHAN_SUPPRESSION_BLOCK = '''  if "[R" not in rendered:
    reference_entries = ()
    statement_lines_by_reference_number = {}

'''


def _restore_from_fix3_backup() -> str:
    if not FIX3_BACKUP.is_file():
        raise RuntimeError(
            "fix3 backup was not found: "
            + str(FIX3_BACKUP)
        )

    if TARGET.is_file():
        BACKUP_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.copy2(
            TARGET,
            BACKUP_DIR / TARGET.name,
        )

    restored = FIX3_BACKUP.read_text(
        encoding="utf-8"
    )
    print(
        "Restored production source from fix3 backup."
    )
    return restored


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
        end = next_function + 1

    return (
        start,
        end,
        source[
            start:end
        ],
    )


def _remove_fix2_calls(
    function_source: str,
) -> str:
    removed_a = (
        FIX2_R9_A_BLOCK
        in function_source
    )
    removed_c = (
        FIX2_R9_C_BLOCK
        in function_source
    )

    function_source = (
        function_source.replace(
            FIX2_R9_A_BLOCK,
            "",
            1,
        )
    )
    function_source = (
        function_source.replace(
            FIX2_R9_C_BLOCK,
            "",
            1,
        )
    )

    print(
        "Removed fix2 final graph suppression:",
        removed_a,
    )
    print(
        "Removed fix2 post-selection relink:",
        removed_c,
    )

    return function_source


def _insert_helper(
    source: str,
) -> str:
    if (
        "def suppress_toda_group_proof_narrative_literal_reflexive_equalities("
        in source
    ):
        return source

    anchor = (
        "def suppress_toda_group_proof_narrative_reflexive_equalities(\n"
    )
    index = source.find(
        anchor
    )

    if index < 0:
        raise RuntimeError(
            "Existing reflexive helper anchor "
            "was not found."
        )

    return (
        source[
            :index
        ]
        + LITERAL_HELPER
        + source[
            index:
        ]
    )


def _insert_final_literal(
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
            "generic_used_step_ids anchor "
            "was not found."
        )

    prefix = function_source[
        :index
    ]

    if prefix.rstrip().endswith(
        FINAL_LITERAL_BLOCK.rstrip()
    ):
        return function_source

    return (
        function_source[
            :index
        ]
        + FINAL_LITERAL_BLOCK
        + function_source[
            index:
        ]
    )


def _insert_orphan_suppression(
    function_source: str,
) -> str:
    anchor = (
        "  reference_section = (\n"
    )
    index = function_source.rfind(
        anchor
    )

    if index < 0:
        raise RuntimeError(
            "Final reference_section anchor "
            "was not found."
        )

    prefix = function_source[
        :index
    ]

    if prefix.rstrip().endswith(
        ORPHAN_SUPPRESSION_BLOCK.rstrip()
    ):
        return function_source

    return (
        function_source[
            :index
        ]
        + ORPHAN_SUPPRESSION_BLOCK
        + function_source[
            index:
        ]
    )


def main() -> int:
    source = _restore_from_fix3_backup()

    (
        function_start,
        function_end,
        function_source,
    ) = _function_slice(
        source
    )

    function_source = (
        _remove_fix2_calls(
            function_source
        )
    )

    source = (
        source[
            :function_start
        ]
        + function_source
        + source[
            function_end:
        ]
    )

    source = _insert_helper(
        source
    )

    (
        function_start,
        function_end,
        function_source,
    ) = _function_slice(
        source
    )

    function_source = (
        _insert_final_literal(
            function_source
        )
    )
    function_source = (
        _insert_orphan_suppression(
            function_source
        )
    )

    source = (
        source[
            :function_start
        ]
        + function_source
        + source[
            function_end:
        ]
    )

    compile(
        source,
        str(
            TARGET
        ),
        "exec",
    )

    TARGET.write_text(
        source,
        encoding="utf-8",
    )

    print(
        "Syntax validation: PASS"
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
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
