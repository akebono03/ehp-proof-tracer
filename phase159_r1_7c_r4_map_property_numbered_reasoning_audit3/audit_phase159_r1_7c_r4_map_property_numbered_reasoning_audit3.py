from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
ROOT_TEXT = str(
  ROOT
)

if ROOT_TEXT not in sys.path:
  sys.path.insert(
    0,
    ROOT_TEXT,
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGETS = (
  (
    3,
    6,
    r"$\Delta: \pi_{9}^{5} \to \pi_{7}^{2}$",
  ),
  (
    3,
    7,
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$",
  ),
  (
    6,
    5,
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$",
  ),
)

TAG = re.compile(
  r"\\tag\{\d+\}"
)
REFERENCE_PREFIX = re.compile(
  r"^\[R\d+\]\s*より,\s*"
)
GENERIC_PREFIX = re.compile(
  r"^(これより,\s*)"
)


def _label(
  n: int,
  k: int,
) -> str:
  return (
    "pi_"
    + str(
      n + k
    )
    + "^"
    + str(
      n
    )
  )


def _normalize_rendered_map_prefix(
  text: str,
) -> str:
  stripped = text.strip()
  stripped = REFERENCE_PREFIX.sub(
    "",
    stripped,
  )
  stripped = GENERIC_PREFIX.sub(
    "",
    stripped,
  )
  stripped = TAG.sub(
    "",
    stripped,
  )

  for suffix in (
    " は単射.",
    " は単射である.",
    " は全射.",
    " は全射である.",
    " は同型.",
    " は同型である.",
    " は同型写像.",
    " は同型写像である.",
  ):
    if stripped.endswith(
      suffix
    ):
      return stripped[
        :-len(
          suffix
        )
      ].strip()

  return stripped


def _rule_name(
  step,
) -> str:
  inference_rule = getattr(
    step,
    "inference_rule",
    None,
  )

  if inference_rule is None:
    return "<none>"

  return str(
    getattr(
      inference_rule,
      "name",
      "<unnamed>",
    )
  )


def _build(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )

  if not report.candidates:
    raise RuntimeError(
      "no report candidate"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  return (
    raw,
    closure,
    rendered,
  )


def _matching_steps(
  presentation,
  target_map: str,
):
  matches = []

  for node_index, node in enumerate(
    presentation.nodes,
    start=1,
  ):
    step = node.proof_step

    try:
      rendered = _render_generic_narrative_step(
        step
      )
    except Exception as exc:
      rendered = (
        "<render error: "
        + type(
          exc
        ).__name__
        + ": "
        + str(
          exc
        )
        + ">"
      )

    normalized = _normalize_rendered_map_prefix(
      rendered
    )

    rule_name = _rule_name(
      step
    )
    conclusion_type = type(
      step.conclusion
    ).__name__

    is_target_map = (
      normalized == target_map
    )
    is_isomorphism_candidate = (
      target_map in rendered
      and (
        "同型"
        in rendered
        or "isomorphism"
        in rule_name.lower()
        or "Isomorphism"
        in conclusion_type
      )
    )

    if (
      is_target_map
      or is_isomorphism_candidate
    ):
      matches.append(
        (
          node_index,
          conclusion_type,
          rule_name,
          rendered,
          is_target_map,
          is_isomorphism_candidate,
        )
      )

  return tuple(
    matches
  )


def _public_lines(
  rendered: str,
  target_map: str,
):
  marker = "## 証明\n\n"
  parts = rendered.split(
    marker,
    1,
  )
  proof = (
    parts[1]
    if len(
      parts
    ) == 2
    else rendered
  )

  return tuple(
    (
      line_number,
      line,
    )
    for line_number, line in enumerate(
      proof.splitlines(),
      start=1,
    )
    if target_map in TAG.sub(
      "",
      line,
    )
  )


def main() -> None:
  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property numbered-reasoning audit3"
  )
  print(
    "=" * 78
  )

  semantic_isomorphism_targets = 0
  no_semantic_isomorphism_targets = 0

  for n, k, target_map in TARGETS:
    label = _label(
      n,
      k,
    )
    raw, closure, rendered = _build(
      n,
      k,
    )

    raw_matches = _matching_steps(
      raw,
      target_map,
    )
    closure_matches = _matching_steps(
      closure,
      target_map,
    )
    public_lines = _public_lines(
      rendered,
      target_map,
    )

    has_semantic_isomorphism = any(
      is_iso
      for (
        _node_index,
        _conclusion_type,
        _rule_name_text,
        _rendered_text,
        _is_target_map,
        is_iso,
      ) in (
        *raw_matches,
        *closure_matches,
      )
    )

    if has_semantic_isomorphism:
      semantic_isomorphism_targets += 1
    else:
      no_semantic_isomorphism_targets += 1

    print()
    print(
      "-" * 78
    )
    print(
      label
    )
    print(
      "target map:",
      target_map,
    )
    print(
      "semantic isomorphism step:",
      (
        "YES"
        if has_semantic_isomorphism
        else "NO"
      ),
    )

    print()
    print(
      "[PUBLIC LINES]"
    )
    for line_number, line in public_lines:
      print(
        f"line {line_number}: {line}"
      )

    print()
    print(
      "[RAW MATCHES]"
    )
    if not raw_matches:
      print(
        "<none>"
      )

    for (
      node_index,
      conclusion_type,
      rule_name,
      step_rendered,
      is_target_map,
      is_iso,
    ) in raw_matches:
      print(
        "node_index:",
        node_index,
      )
      print(
        "conclusion_type:",
        conclusion_type,
      )
      print(
        "rule_name:",
        rule_name,
      )
      print(
        "rendered:",
        step_rendered,
      )
      print(
        "target-map property:",
        is_target_map,
      )
      print(
        "isomorphism candidate:",
        is_iso,
      )
      print()

    print(
      "[SEMANTIC-CLOSURE MATCHES]"
    )
    if not closure_matches:
      print(
        "<none>"
      )

    for (
      node_index,
      conclusion_type,
      rule_name,
      step_rendered,
      is_target_map,
      is_iso,
    ) in closure_matches:
      print(
        "node_index:",
        node_index,
      )
      print(
        "conclusion_type:",
        conclusion_type,
      )
      print(
        "rule_name:",
        rule_name,
      )
      print(
        "rendered:",
        step_rendered,
      )
      print(
        "target-map property:",
        is_target_map,
      )
      print(
        "isomorphism candidate:",
        is_iso,
      )
      print()

  print(
    "=" * 78
  )
  print(
    "SUMMARY"
  )
  print(
    "=" * 78
  )
  print(
    "targets:",
    len(
      TARGETS
    ),
  )
  print(
    "targets with semantic isomorphism step:",
    semantic_isomorphism_targets,
  )
  print(
    "targets without semantic isomorphism step:",
    no_semantic_isomorphism_targets,
  )
  print(
    "Production code changes: none"
  )
  print(
    "Test code changes: none"
  )
  print(
    "Full pytest: not run"
  )


if __name__ == "__main__":
  main()
