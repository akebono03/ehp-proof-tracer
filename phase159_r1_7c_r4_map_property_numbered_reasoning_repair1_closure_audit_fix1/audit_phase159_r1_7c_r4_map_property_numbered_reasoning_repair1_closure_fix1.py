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
  r"^\[R\d+\]より,\s*"
)
PROSE_PREFIX = re.compile(
  r"^(?:これより,\s*)"
)
CONNECTOR_PREFIX = re.compile(
  r"^\((\d+)\),\s*\((\d+)\)\s+より,\s*"
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


def _strip_property_prefixes(
  line: str,
) -> str:
  stripped = line.strip()
  stripped = REFERENCE_PREFIX.sub(
    "",
    stripped,
  )
  stripped = PROSE_PREFIX.sub(
    "",
    stripped,
  )

  return stripped


def _map_property(
  line: str,
  suffix: str,
):
  stripped = _strip_property_prefixes(
    line
  )

  if not stripped.endswith(
    suffix
  ):
    return None

  map_text = stripped[
    :-len(
      suffix
    )
  ].strip()

  match = TAG.search(
    map_text
  )
  number = (
    int(
      match.group(
        1
      )
    )
    if match is not None
    else None
  )
  map_text = TAG.sub(
    "",
    map_text,
  ).strip()

  return (
    map_text,
    number,
  )


def _isomorphism(
  line: str,
):
  stripped = line.strip()
  match = CONNECTOR_PREFIX.match(
    stripped
  )
  connector_numbers = (
    (
      int(
        match.group(
          1
        )
      ),
      int(
        match.group(
          2
        )
      ),
    )
    if match is not None
    else None
  )

  stripped = CONNECTOR_PREFIX.sub(
    "",
    stripped,
  )

  for suffix in (
    " は同型.",
    " は同型写像.",
    " は同型である.",
    " は同型写像である.",
  ):
    if stripped.endswith(
      suffix
    ):
      return (
        stripped[
          :-len(
            suffix
          )
        ].strip(),
        connector_numbers,
      )

  return None


def main() -> None:
  rendered_count = 0
  failed = []

  trios = []
  fully_numbered_trios = []
  defective_trios = []
  pair_without_iso = []

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

      injective = {}
      surjective = {}
      isomorphism = {}

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        inj = _map_property(
          line,
          " は単射.",
        )

        if inj is not None:
          injective.setdefault(
            inj[0],
            []
          ).append(
            (
              line_number,
              inj[1],
              line,
            )
          )

        surj = _map_property(
          line,
          " は全射.",
        )

        if surj is not None:
          surjective.setdefault(
            surj[0],
            []
          ).append(
            (
              line_number,
              surj[1],
              line,
            )
          )

        iso = _isomorphism(
          line
        )

        if iso is not None:
          isomorphism.setdefault(
            iso[0],
            []
          ).append(
            (
              line_number,
              iso[1],
              line,
            )
          )

      paired_maps = (
        set(
          injective
        )
        & set(
          surjective
        )
      )

      for map_text in sorted(
        paired_maps
      ):
        iso_rows = isomorphism.get(
          map_text,
          ()
        )

        if not iso_rows:
          pair_without_iso.append(
            (
              label,
              map_text,
              injective[
                map_text
              ],
              surjective[
                map_text
              ],
            )
          )
          continue

        inj_row = injective[
          map_text
        ][
          0
        ]
        surj_row = surjective[
          map_text
        ][
          0
        ]
        iso_row = iso_rows[
          0
        ]

        row = (
          label,
          map_text,
          inj_row,
          surj_row,
          iso_row,
        )
        trios.append(
          row
        )

        inj_number = inj_row[
          1
        ]
        surj_number = surj_row[
          1
        ]
        iso_numbers = iso_row[
          1
        ]

        if (
          inj_number is not None
          and surj_number is not None
          and iso_numbers
          == (
            inj_number,
            surj_number,
          )
          and iso_row[
            2
          ].endswith(
            " は同型."
          )
        ):
          fully_numbered_trios.append(
            row
          )
        else:
          defective_trios.append(
            row
          )

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 numbered reasoning repair1 closure audit fix1"
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

  print(
    "[FULLY NUMBERED TRIOS]"
  )
  for (
    label,
    map_text,
    inj_row,
    surj_row,
    iso_row,
  ) in fully_numbered_trios:
    print(
      label,
      map_text,
    )
    print(
      "  injective:",
      inj_row[
        2
      ],
    )
    print(
      "  surjective:",
      surj_row[
        2
      ],
    )
    print(
      "  isomorphism:",
      iso_row[
        2
      ],
    )

  if defective_trios:
    print()
    print(
      "[DEFECTIVE TRIOS]"
    )
    for (
      label,
      map_text,
      inj_row,
      surj_row,
      iso_row,
    ) in defective_trios:
      print(
        label,
        map_text,
      )
      print(
        "  injective:",
        inj_row[
          2
        ],
      )
      print(
        "  surjective:",
        surj_row[
          2
        ],
      )
      print(
        "  isomorphism:",
        iso_row[
          2
        ],
      )

  print()
  print(
    "[PAIRS WITHOUT ISOMORPHISM]"
  )
  for (
    label,
    map_text,
    inj_rows,
    surj_rows,
  ) in pair_without_iso:
    print(
      label,
      map_text,
    )
    for row in inj_rows:
      print(
        "  injective:",
        row[
          2
        ],
      )
    for row in surj_rows:
      print(
        "  surjective:",
        row[
          2
        ],
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
    "injective+surjective+isomorphism trios:",
    len(
      trios
    ),
  )
  print(
    "fully numbered trios:",
    len(
      fully_numbered_trios
    ),
  )
  print(
    "defective trios:",
    len(
      defective_trios
    ),
  )
  print(
    "injective+surjective pairs without isomorphism:",
    len(
      pair_without_iso
    ),
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
