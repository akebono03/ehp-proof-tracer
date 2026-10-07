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
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


N_RANGE = range(
  2,
  16,
)
K_RANGE = range(
  0,
  8,
)
MAX_DEPTH = 2

TAG = re.compile(
  r"\\tag\{(\d+)\}"
)
REFERENCE_PREFIX = re.compile(
  r"^\[R\d+\]\s*より,\s*"
)
GENERIC_PREFIX = re.compile(
  r"^(これより,\s*)"
)

INJECTIVE_SUFFIX = " は単射."
SURJECTIVE_SUFFIX = " は全射."

ISOMORPHISM_SUFFIXES = (
  " は同型.",
  " は同型写像.",
  " は同型である.",
  " は同型写像である.",
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


def _render(
  n: int,
  k: int,
) -> str:
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
    max_depth=MAX_DEPTH,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _proof_body(
  rendered: str,
) -> str:
  marker = "## 証明\n\n"
  parts = rendered.split(
    marker,
    1,
  )

  if len(
    parts
  ) != 2:
    return rendered

  return parts[
    1
  ]


def _normalize_map_statement(
  line: str,
  property_suffix: str,
) -> tuple[
  str,
  int | None,
] | None:
  stripped = line.strip()
  stripped = REFERENCE_PREFIX.sub(
    "",
    stripped,
  )
  stripped = GENERIC_PREFIX.sub(
    "",
    stripped,
  )

  if not stripped.endswith(
    property_suffix
  ):
    return None

  map_text = stripped[
    :-len(
      property_suffix
    )
  ].strip()

  tag_match = TAG.search(
    map_text
  )
  tag_number = (
    int(
      tag_match.group(
        1
      )
    )
    if tag_match is not None
    else None
  )

  map_text = TAG.sub(
    "",
    map_text,
  ).strip()

  return (
    map_text,
    tag_number,
  )


def _isomorphism_map(
  line: str,
) -> str | None:
  stripped = line.strip()

  for suffix in ISOMORPHISM_SUFFIXES:
    if suffix not in stripped:
      continue

    prefix, _, _ = stripped.partition(
      suffix
    )

    if "より, " in prefix:
      prefix = prefix.split(
        "より, ",
        1,
      )[
        1
      ]

    prefix = REFERENCE_PREFIX.sub(
      "",
      prefix,
    )
    prefix = GENERIC_PREFIX.sub(
      "",
      prefix,
    )

    return TAG.sub(
      "",
      prefix,
    ).strip()

  return None


def main() -> None:
  rendered_count = 0
  failed = []

  paired_outputs = []
  paired_map_count = 0
  fully_numbered_pair_count = 0
  unnumbered_pair_count = 0
  mixed_pair_count = 0
  paired_with_isomorphism = 0
  paired_without_isomorphism = 0

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 map-property numbered-reasoning audit2"
  )
  print(
    "=" * 78
  )
  print(
    "audit range: n=2..15, k=0..7"
  )
  print(
    "This range is an audit sample, not a permanent group-count contract."
  )
  print()

  for n in N_RANGE:
    for k in K_RANGE:
      label = _label(
        n,
        k,
      )

      try:
        rendered = _render(
          n,
          k,
        )
      except Exception as exc:
        failed.append(
          (
            label,
            type(
              exc
            ).__name__,
            str(
              exc
            ),
          )
        )
        continue

      rendered_count += 1
      body = _proof_body(
        rendered
      )
      lines = body.splitlines()

      injective_by_map = {}
      surjective_by_map = {}
      isomorphism_maps = set()

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        injective = _normalize_map_statement(
          line,
          INJECTIVE_SUFFIX,
        )

        if injective is not None:
          map_text, tag_number = injective
          injective_by_map.setdefault(
            map_text,
            []
          ).append(
            (
              line_number,
              tag_number,
              line,
            )
          )

        surjective = _normalize_map_statement(
          line,
          SURJECTIVE_SUFFIX,
        )

        if surjective is not None:
          map_text, tag_number = surjective
          surjective_by_map.setdefault(
            map_text,
            []
          ).append(
            (
              line_number,
              tag_number,
              line,
            )
          )

        isomorphism = _isomorphism_map(
          line
        )

        if isomorphism is not None:
          isomorphism_maps.add(
            isomorphism
          )

      paired_maps = tuple(
        sorted(
          set(
            injective_by_map
          )
          & set(
            surjective_by_map
          )
        )
      )

      if not paired_maps:
        continue

      output_rows = []

      for map_text in paired_maps:
        paired_map_count += 1

        injective_rows = injective_by_map[
          map_text
        ]
        surjective_rows = surjective_by_map[
          map_text
        ]

        injective_tagged = any(
          tag_number is not None
          for _, tag_number, _ in injective_rows
        )
        surjective_tagged = any(
          tag_number is not None
          for _, tag_number, _ in surjective_rows
        )

        if (
          injective_tagged
          and surjective_tagged
        ):
          status = "FULLY_NUMBERED_PAIR"
          fully_numbered_pair_count += 1
        elif (
          not injective_tagged
          and not surjective_tagged
        ):
          status = "UNNUMBERED_PAIR"
          unnumbered_pair_count += 1
        else:
          status = "MIXED_PAIR"
          mixed_pair_count += 1

        has_isomorphism = (
          map_text
          in isomorphism_maps
        )

        if has_isomorphism:
          paired_with_isomorphism += 1
        else:
          paired_without_isomorphism += 1

        output_rows.append(
          (
            map_text,
            status,
            has_isomorphism,
            injective_rows,
            surjective_rows,
          )
        )

      paired_outputs.append(
        (
          label,
          output_rows,
        )
      )

      print(
        "-" * 78
      )
      print(
        label
      )

      for (
        map_text,
        status,
        has_isomorphism,
        injective_rows,
        surjective_rows,
      ) in output_rows:
        print(
          "[PAIR]"
        )
        print(
          "map:",
          map_text,
        )
        print(
          "status:",
          status,
        )
        print(
          "isomorphism conclusion:",
          (
            "YES"
            if has_isomorphism
            else "NO"
          ),
        )

        print(
          "injective:"
        )
        for (
          line_number,
          tag_number,
          line,
        ) in injective_rows:
          print(
            " ",
            f"line {line_number}",
            f"tag={tag_number}",
            line,
          )

        print(
          "surjective:"
        )
        for (
          line_number,
          tag_number,
          line,
        ) in surjective_rows:
          print(
            " ",
            f"line {line_number}",
            f"tag={tag_number}",
            line,
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
    "rendered:",
    rendered_count,
  )
  print(
    "failed:",
    len(
      failed
    ),
  )
  print(
    "outputs with injective+surjective same-map pairs:",
    len(
      paired_outputs
    ),
  )
  print(
    "paired maps:",
    paired_map_count,
  )
  print(
    "fully numbered pairs:",
    fully_numbered_pair_count,
  )
  print(
    "unnumbered pairs:",
    unnumbered_pair_count,
  )
  print(
    "mixed pairs:",
    mixed_pair_count,
  )
  print(
    "pairs with isomorphism conclusion:",
    paired_with_isomorphism,
  )
  print(
    "pairs without isomorphism conclusion:",
    paired_without_isomorphism,
  )

  if failed:
    print()
    print(
      "[FAILURES]"
    )
    for label, error_type, message in failed:
      print(
        label,
        error_type,
        message,
      )

  print()
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
