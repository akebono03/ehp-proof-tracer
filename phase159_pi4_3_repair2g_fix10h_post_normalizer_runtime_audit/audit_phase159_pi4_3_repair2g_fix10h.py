from __future__ import annotations

from pathlib import Path
import inspect
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      ROOT
    ),
  )

import toda_group_proof_narrative_renderer as renderer

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def main() -> int:
  print(
    "=== Phase159 fix10h post-normalizer runtime audit ==="
  )
  print(
    "Production code changes: NONE"
  )
  print(
    "Renderer module:",
    renderer.__file__,
  )

  contract = (
    renderer
    ._phase158_normalize_public_narrative_contract
  )

  print()
  print(
    "=== runtime public-contract source ==="
  )
  contract_source = inspect.getsource(
    contract
  )
  print(
    contract_source
  )

  print()
  print(
    "=== renderer functions containing relevant tokens ==="
  )

  relevant_tokens = (
    r"\tag{",
    "単射である.",
    "全射である.",
    "同型写像である.",
    "単射.",
    "全射.",
    "同型.",
  )

  for name, value in sorted(
    vars(
      renderer
    ).items()
  ):
    if (
      not inspect.isfunction(
        value
      )
      or value.__module__
      != renderer.__name__
    ):
      continue

    try:
      source = inspect.getsource(
        value
      )
    except OSError:
      continue

    matched = tuple(
      token
      for token in relevant_tokens
      if token in source
    )

    if not matched:
      continue

    print()
    print(
      "---",
      name,
      "---"
    )
    print(
      "matched:",
      matched,
    )
    print(
      source
    )

  original_equation_normalizer = (
    renderer
    ._phase158_normalize_public_equation_numbers
  )

  sentinel_injective = (
    "__FIX10H_INJECTIVE_SENTINEL__"
  )
  sentinel_surjective = (
    "__FIX10H_SURJECTIVE_SENTINEL__"
  )

  def traced_equation_normalizer(
    proof_body,
  ):
    result = original_equation_normalizer(
      proof_body
    )

    replaced = []

    for line in result:
      if (
        r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
        in line
        and "単射" in line
      ):
        replaced.append(
          sentinel_injective
        )
        continue

      if (
        r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
        in line
        and "全射" in line
      ):
        replaced.append(
          sentinel_surjective
        )
        continue

      replaced.append(
        line
      )

    print()
    print(
      "=== equation normalizer replaced output ==="
    )
    for line in replaced:
      if (
        "FIX10H" in line
        or "単射" in line
        or "全射" in line
        or r"\tag{" in line
      ):
        print(
          repr(
            line
          )
        )

    return replaced

  renderer._phase158_normalize_public_equation_numbers = (
    traced_equation_normalizer
  )

  report = build_standard_toda_report(
    n=2,
    k=1,
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  print()
  print(
    "=== final public Narrative with sentinels ==="
  )
  rendered = (
    renderer
    .render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  print(
    rendered
  )

  print()
  print(
    "injective sentinel survives:",
    sentinel_injective in rendered,
  )
  print(
    "surjective sentinel survives:",
    sentinel_surjective in rendered,
  )
  print(
    "tag1 present:",
    r"\tag{1}" in rendered,
  )
  print(
    "tag2 present:",
    r"\tag{2}" in rendered,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
