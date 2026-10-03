from pathlib import Path
import re
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
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


TARGETS = (
  (3, 3),
  (4, 6),
  (5, 7),
  (9, 7),
)

HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)


for n, k in TARGETS:
  report = build_standard_toda_report(
    n=n,
    k=k,
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
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  reference, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  print(
    "=" * 78
  )
  print(
    f"pi_{n + k}^{n}"
  )

  for match in HEADER_RE.finditer(
    reference
  ):
    number = int(
      match.group(
        1
      )
    )
    title = match.group(
      2
    )
    marker = (
      "[R"
      + str(
        number
      )
      + "]"
    )
    print(
      marker
      + " "
      + title
      + " body_count="
      + str(
        body.count(
          marker
        )
      )
    )
