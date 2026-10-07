from pathlib import Path
import inspect
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


import toda_group_proof_narrative_reason_renderer as reason_renderer
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)


OLD_FRAGMENT = (
  "この完全性と $Δ=0$ より"
)
NEW_FRAGMENT = (
  "完全性より, $E:"
)


def git_diff(
  path: str,
) -> str:
  result = subprocess.run(
    [
      "git",
      "diff",
      "--",
      path,
    ],
    cwd=REPO_ROOT,
    text=True,
    capture_output=True,
    encoding="utf-8",
    errors="replace",
  )

  return result.stdout


def matching_test_files(
  fragment: str,
) -> tuple[
  tuple[
    str,
    int,
    str,
  ],
  ...,
]:
  rows = []

  for path in sorted(
    (
      REPO_ROOT
      / "tests"
    ).glob(
      "test_*.py"
    )
  ):
    text = path.read_text(
      encoding="utf-8",
      errors="replace",
    )

    for line_number, line in enumerate(
      text.splitlines(),
      start=1,
    ):
      if fragment in line:
        rows.append(
          (
            str(
              path.relative_to(
                REPO_ROOT
              )
            ),
            line_number,
            line.strip(),
          )
        )

  return tuple(
    rows
  )


def main() -> int:
  (
    presentation,
    _,
    semantic_sidecar,
    _,
  ) = _method_evidence_data(
    3,
    3,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  exactness_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  proof_body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  lines = [
    "# Phase 159 pi6_3 exactness reason contract audit",
    "",
    "## Current local renderer source",
    "",
    inspect.getsource(
      reason_renderer
      .render_toda_group_proof_narrative_reason_sentence
    ),
    "",
    "## Current local exactness reason",
    "",
    "count="
    + str(
      len(
        exactness_reasons
      )
    ),
  ]

  for index, reason in enumerate(
    exactness_reasons
  ):
    lines.append(
      "reason_"
      + str(
        index
      )
      + "="
      + repr(
        reason_renderer
        .render_toda_group_proof_narrative_reason_sentence(
          reason
        )
      )
    )

  lines.extend(
    (
      "",
      "## Public pi6_3 body lines around injectivity",
      "",
    )
  )

  body_lines = proof_body.splitlines()

  for index, line in enumerate(
    body_lines
  ):
    if (
      r"\pi_{5}^{2} \to \pi_{6}^{3}"
      in line
      or r"\ker E"
      in line
      or "$Δ=0$"
      in line
    ):
      start = max(
        0,
        index - 2,
      )
      end = min(
        len(
          body_lines
        ),
        index + 3,
      )

      for position in range(
        start,
        end,
      ):
        lines.append(
          str(
            position + 1
          )
          + ": "
          + body_lines[
            position
          ]
        )

      lines.append(
        ""
      )

  lines.extend(
    (
      "## Tests containing old contract fragment",
      "",
    )
  )

  old_matches = matching_test_files(
    OLD_FRAGMENT
  )

  if not old_matches:
    lines.append(
      "(none)"
    )

  for path, line_number, line in old_matches:
    lines.append(
      path
      + ":"
      + str(
        line_number
      )
      + ": "
      + line
    )

  lines.extend(
    (
      "",
      "## Tests containing concise contract fragment",
      "",
    )
  )

  new_matches = matching_test_files(
    NEW_FRAGMENT
  )

  if not new_matches:
    lines.append(
      "(none)"
    )

  for path, line_number, line in new_matches:
    lines.append(
      path
      + ":"
      + str(
        line_number
      )
      + ": "
      + line
    )

  lines.extend(
    (
      "",
      "## git diff: reason renderer",
      "",
      git_diff(
        "toda_group_proof_narrative_reason_renderer.py"
      ),
      "",
      "## git diff: Phase 150 exactness test",
      "",
      git_diff(
        "tests/test_phase150_rc4_5c_2_exactness_to_map_property.py"
      ),
      "",
      "## git diff: Phase 157 dangling connector test",
      "",
      git_diff(
        "tests/test_phase157_r20_repair43_dangling_connector_cleanup.py"
      ),
      "",
    )
  )

  output = "\n".join(
    lines
  )

  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi6_3_exactness_reason_contract_audit.txt"
  )
  output_path.write_text(
    output,
    encoding="utf-8",
  )

  print(
    output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
