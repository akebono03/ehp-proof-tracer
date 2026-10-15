from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _strip_reference_prefix(
  paragraph: str,
) -> str:
  stripped = paragraph.strip()

  if not stripped.startswith(
    "[R"
  ):
    return stripped

  marker_end = stripped.find(
    "]"
  )

  if marker_end < 0:
    return stripped

  suffix = stripped[
    marker_end + 1:
  ]

  for prefix in (
    "より, ",
    "を用いて, ",
  ):
    if suffix.startswith(
      prefix
    ):
      return suffix[
        len(
          prefix
        ):
      ]

  return stripped


def _concise(
  line: str,
) -> str:
  stripped = _strip_reference_prefix(
    line
  )

  for prefix in (
    "完全性より, ",
    "以上より, ",
    "したがって, ",
    "これより, ",
    "これらより, ",
  ):
    if stripped.startswith(
      prefix
    ):
      stripped = stripped[
        len(
          prefix
        ):
      ]
      break

  for verbose, concise in (
    (
      " は単射である.",
      " は単射.",
    ),
    (
      " は全射である.",
      " は全射.",
    ),
    (
      " は零写像である.",
      " は零写像.",
    ),
    (
      " は同型写像である.",
      " は同型.",
    ),
  ):
    if stripped.endswith(
      verbose
    ):
      stripped = (
        stripped[
          :-len(
            verbose
          )
        ]
        + concise
      )
      break

  return stripped.strip().rstrip(
    ".,"
  )


def _math_spans(
  text: str,
) -> tuple[
  str,
  ...,
]:
  spans = []
  start = 0

  while True:
    left = text.find(
      "$",
      start,
    )

    if left < 0:
      break

    right = text.find(
      "$",
      left + 1,
    )

    if right < 0:
      break

    spans.append(
      text[
        left:
        right + 1
      ]
    )
    start = right + 1

  return tuple(
    spans
  )


def main() -> int:
  (
    presentation,
    _,
    _,
    _,
  ) = _method_evidence_data(
    2,
    1,
  )

  public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  _, marker, body = public.partition(
    "## 証明"
  )

  if marker != "## 証明":
    raise RuntimeError(
      "proof marker not found"
    )

  paragraphs = [
    paragraph.strip()
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  ]

  definition_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    for rendered in (
      _render_generic_narrative_step(
        node.proof_step
      ),
    )
    if (
      rendered
      and "を満たす"
      in rendered
      and "を定める."
      in rendered
    )
  )

  print(
    "=============================================================="
  )
  print(
    "Phase 159 pi3_2 definition locality condition audit15"
  )
  print(
    "=============================================================="
  )
  print(
    "definition_step_count="
    + str(
      len(
        definition_steps
      )
    )
  )

  for definition_index, proof_step in enumerate(
    definition_steps
  ):
    generic_definition = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    print()
    print(
      "=== definition["
      + str(
        definition_index
      )
      + "] ==="
    )
    print(
      "generic_definition="
      + repr(
        generic_definition
      )
    )

    spans = _math_spans(
      generic_definition
    )

    print(
      "math_spans="
      + repr(
        spans
      )
    )

    isomorphism_premises = tuple(
      premise_step
      for premise_step in proof_step.premises
      for line in (
        _render_generic_narrative_step(
          premise_step
        ),
      )
      if (
        line
        and "同型写像である."
        in line
      )
    )

    print(
      "isomorphism_premise_count="
      + str(
        len(
          isomorphism_premises
      )
    )
    )

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if (
        paragraph.startswith(
          "この同型写像により, "
        )
        and all(
          span in paragraph
          for span in spans
        )
      )
    )

    print(
      "definition_matches="
      + repr(
        definition_matches
      )
    )

    for premise_index, premise_step in enumerate(
      proof_step.premises
    ):
      line = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      key = (
        _concise(
          line
        )
        if line
        else None
      )
      matches = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if (
          line
          and _concise(
            paragraph
          )
          == key
        )
      )

      print(
        "premise["
        + str(
          premise_index
        )
        + "]="
        + repr(
          line
        )
      )
      print(
        "  key="
        + repr(
          key
        )
      )
      print(
        "  matches="
        + repr(
          matches
        )
      )

    if len(
      definition_matches
    ) == 1:
      definition_public = paragraphs[
        definition_matches[
          0
        ]
      ]
      print(
        "definition_public="
        + repr(
          definition_public
        )
      )

  print()
  print(
    "=== Relevant public paragraphs ==="
  )

  for index, paragraph in enumerate(
    paragraphs
  ):
    if (
      r"\pi_{3}^{3}"
      in paragraph
      or "同型"
      in paragraph
      or "この同型写像により"
      in paragraph
    ):
      print(
        "["
        + str(
          index
        )
        + "] "
        + repr(
          paragraph
        )
      )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
