from __future__ import annotations

import ast
import shutil
from pathlib import Path


TARGET = Path("toda_group_proof_narrative_renderer.py")
BACKUP_DIR = Path(
    "phase159_pi3_2_reference_general_form_repair19_backup"
)


NEW_CANONICALIZER = r'''def _phase159_r1_6c_canonicalize_toda_51_reference(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "\n---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  reference_body = rendered[
    content_start:
    boundary_index
  ]
  lines = reference_body.splitlines()
  output = []
  index = 0

  while index < len(
    lines
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\] "
      r"\(5\.1\)\.\*\*$",
      lines[
        index
      ].strip(),
    )

    if match is None:
      output.append(
        lines[
          index
        ]
      )
      index += 1
      continue

    output.append(
      lines[
        index
      ]
    )
    output.append(
      (
        r"$\pi_{i}^{1} = 0\ (i > 1),"
        r"\qquad "
        r"\pi_{i}^{n} = 0\ (i < n)$."
      )
    )
    output.append(
      (
        r"$\pi_{n}^{n} = "
        r"\mathbb{Z}\{\iota_{n}\}$."
      )
    )

    index += 1

    while (
      index < len(
        lines
      )
      and not lines[
        index
      ].strip().startswith(
        "**[R"
      )
    ):
      index += 1

  normalized_reference = "\n".join(
    output
  ).rstrip()

  return (
    rendered[
      :content_start
    ]
    + normalized_reference
    + rendered[
      boundary_index:
    ]
  )
'''


def _replace_top_level_function(
    source: str,
    function_name: str,
    replacement: str,
) -> str:
    tree = ast.parse(source)
    target = next(
        (
            node
            for node in tree.body
            if (
                isinstance(
                    node,
                    ast.FunctionDef,
                )
                and node.name == function_name
            )
        ),
        None,
    )

    if target is None:
        raise RuntimeError(
            "function not found: "
            + function_name
        )

    lines = source.splitlines(
        keepends=True
    )
    start = target.lineno - 1
    end = target.end_lineno

    newline = (
        "\r\n"
        if "\r\n" in source
        else "\n"
    )
    replacement_text = (
        replacement.strip("\n")
        .replace(
            "\n",
            newline,
        )
        + newline
    )

    return (
        "".join(
            lines[
                :start
            ]
        )
        + replacement_text
        + "".join(
            lines[
                end:
            ]
        )
    )


def _wrap_public_renderer_final_return(
    source: str,
) -> str:
    tree = ast.parse(source)
    target = next(
        (
            node
            for node in tree.body
            if (
                isinstance(
                    node,
                    ast.FunctionDef,
                )
                and node.name
                == "render_toda_group_proof_narrative_markdown"
            )
        ),
        None,
    )

    if target is None:
        raise RuntimeError(
            "render_toda_group_proof_narrative_markdown "
            "not found"
        )

    final_return = next(
        (
            node
            for node in reversed(
                target.body
            )
            if isinstance(
                node,
                ast.Return,
            )
        ),
        None,
    )

    if final_return is None:
        raise RuntimeError(
            "public renderer final return not found"
        )

    segment = ast.get_source_segment(
        source,
        final_return,
    )

    if segment is None:
        raise RuntimeError(
            "could not read public renderer return"
        )

    if (
        "_phase159_r1_6c_canonicalize_toda_51_reference"
        in segment
    ):
        return source

    value_segment = ast.get_source_segment(
        source,
        final_return.value,
    )

    if value_segment is None:
        raise RuntimeError(
            "could not read public renderer return value"
        )

    newline = (
        "\r\n"
        if "\r\n" in source
        else "\n"
    )

    value_lines = value_segment.splitlines()
    indented_value = newline.join(
        "      " + line
        for line in value_lines
    )

    replacement = (
        "  return ("
        + newline
        + "    _phase159_r1_6c_canonicalize_toda_51_reference("
        + newline
        + indented_value
        + newline
        + "    )"
        + newline
        + "  )"
    )

    lines = source.splitlines(
        keepends=True
    )
    start = final_return.lineno - 1
    end = final_return.end_lineno

    return (
        "".join(
            lines[
                :start
            ]
        )
        + replacement
        + newline
        + "".join(
            lines[
                end:
            ]
        )
    )


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(
            "Run this script from the "
            "ehp-proof-tracer repository root: "
            + str(
                TARGET
            )
        )

    source = TARGET.read_text(
        encoding="utf-8"
    )

    if (
        "def _phase159_r1_6c_canonicalize_toda_51_reference("
        not in source
    ):
        raise RuntimeError(
            "Expected Toda (5.1) canonicalizer "
            "is not present in the current renderer."
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

    updated = _replace_top_level_function(
        source,
        "_phase159_r1_6c_canonicalize_toda_51_reference",
        NEW_CANONICALIZER,
    )
    updated = _wrap_public_renderer_final_return(
        updated
    )

    ast.parse(
        updated
    )

    TARGET.write_text(
        updated,
        encoding="utf-8",
    )

    print(
        "Applied Phase 159 pi3_2 "
        "Reference general-form repair19."
    )
    print(
        "Changed: "
        + str(
            TARGET.resolve()
        )
    )
    print(
        "Backup:  "
        + str(
            backup.resolve()
        )
    )


if __name__ == "__main__":
    main()
