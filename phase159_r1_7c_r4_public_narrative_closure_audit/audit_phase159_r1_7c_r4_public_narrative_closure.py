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
LEADING_REFERENCES = re.compile(
  r"^((?:\(\d+\)(?:,\s*|\s+と\s+)?)+)\s*より,"
)
PAREN_NUMBER = re.compile(
  r"\((\d+)\)"
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


def _section(
  rendered: str,
  marker: str,
  next_marker: str | None,
) -> str:
  start = rendered.find(
    marker
  )

  if start < 0:
    return ""

  start += len(
    marker
  )

  if next_marker is None:
    return rendered[
      start:
    ]

  end = rendered.find(
    next_marker,
    start,
  )

  if end < 0:
    return rendered[
      start:
    ]

  return rendered[
    start:end
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

  target_show_findings = []
  dearu_findings = []
  forward_reference_findings = []
  defective_numbered_trios = []
  fully_numbered_trios = 0
  pairs_without_isomorphism = 0

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

      target = _section(
        rendered,
        "## 証明対象\n\n",
        "## 使用する結果",
      )
      proof = _section(
        rendered,
        "## 証明\n\n",
        None,
      )

      if "を示す." in target:
        target_show_findings.append(
          label
        )

      for line_number, line in enumerate(
        proof.splitlines(),
        start=1,
      ):
        if (
          "は単射である."
          in line
          or "は全射である."
          in line
        ):
          dearu_findings.append(
            (
              label,
              line_number,
              line,
            )
          )

      lines = proof.splitlines()
      tag_line_by_number = {}

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        for match in TAG.finditer(
          line
        ):
          number = int(
            match.group(
              1
            )
          )
          tag_line_by_number.setdefault(
            number,
            line_number,
          )

      for line_number, line in enumerate(
        lines,
        start=1,
      ):
        match = LEADING_REFERENCES.match(
          line.strip()
        )

        if match is None:
          continue

        numbers = tuple(
          int(
            value
          )
          for value in PAREN_NUMBER.findall(
            match.group(
              1
            )
          )
        )

        for number in numbers:
          tag_line = tag_line_by_number.get(
            number
          )

          if (
            tag_line is None
            or tag_line >= line_number
          ):
            forward_reference_findings.append(
              (
                label,
                line_number,
                number,
                tag_line,
                line,
              )
            )

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

      for map_text in paired_maps:
        iso_rows = isomorphism.get(
          map_text,
          ()
        )

        if not iso_rows:
          pairs_without_isomorphism += 1
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

        if (
          inj_row[
            1
          ] is not None
          and surj_row[
            1
          ] is not None
          and iso_row[
            1
          ]
          == (
            inj_row[
              1
            ],
            surj_row[
              1
            ],
          )
          and iso_row[
            2
          ].endswith(
            " は同型."
          )
          and inj_row[
            0
          ] < iso_row[
            0
          ]
          and surj_row[
            0
          ] < iso_row[
            0
          ]
        ):
          fully_numbered_trios += 1
        else:
          defective_numbered_trios.append(
            (
              label,
              map_text,
              inj_row,
              surj_row,
              iso_row,
            )
          )

  print(
    "=" * 78
  )
  print(
    "Phase 159 R1-7c R4 public Narrative closure audit"
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
    'target "を示す." findings:',
    len(
      target_show_findings
    ),
  )
  print(
    "map-property dearu findings:",
    len(
      dearu_findings
    ),
  )
  print(
    "forward equation references:",
    len(
      forward_reference_findings
    ),
  )
  print(
    "fully numbered injective+surjective+isomorphism trios:",
    fully_numbered_trios,
  )
  print(
    "defective numbered trios:",
    len(
      defective_numbered_trios
    ),
  )
  print(
    "injective+surjective pairs without isomorphism:",
    pairs_without_isomorphism,
  )

  if target_show_findings:
    print()
    print(
      '[TARGET "を示す." FINDINGS]'
    )
    for label in target_show_findings:
      print(
        label
      )

  if dearu_findings:
    print()
    print(
      "[MAP-PROPERTY DEARU FINDINGS]"
    )
    for label, line_number, line in dearu_findings:
      print(
        label,
        line_number,
        line,
      )

  if forward_reference_findings:
    print()
    print(
      "[FORWARD EQUATION REFERENCES]"
    )
    for (
      label,
      line_number,
      number,
      tag_line,
      line,
    ) in forward_reference_findings:
      print(
        label,
        "line",
        line_number,
        "number",
        number,
        "tag_line",
        tag_line,
        line,
      )

  if defective_numbered_trios:
    print()
    print(
      "[DEFECTIVE NUMBERED TRIOS]"
    )
    for row in defective_numbered_trios:
      print(
        row
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
