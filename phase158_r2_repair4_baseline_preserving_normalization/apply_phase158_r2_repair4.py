from __future__ import annotations

from pathlib import Path
import py_compile
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_renderer.py"
R2_BASELINE = (
  REPO_ROOT
  / "phase158_r2_backup_before_apply"
  / "toda_group_proof_narrative_renderer.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase158_r2_repair4_backup_before_restore"
)

PUBLIC_DEF = (
  "def render_toda_group_proof_narrative_markdown(\n"
)
BASELINE_DEF = (
  "def _phase158_baseline_render_toda_group_proof_narrative_markdown(\n"
)

APPENDIX = r'''

def _phase158_public_narrative_target_lines(
  presentation: TodaGroupProofPresentation,
) -> list[str]:
  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  if root_latex is not None:
    return [
      r"\[",
      root_latex,
      r"\]",
      "",
      "を示す.",
    ]

  return [
    (
      _render_group_proof_narrative_fact(
        presentation.root_step
      )
      + "を示す."
    ),
  ]


def _phase158_strip_terminal_qed_lines(
  lines: list[str],
) -> list[str]:
  result = lines[:]

  while (
    result
    and not result[-1].strip()
  ):
    result.pop()

  qed_markers = {
    "□",
    r"$\square$",
    r"\(\square\)",
    r"\square",
  }

  if (
    result
    and result[-1].strip()
    in qed_markers
  ):
    result.pop()

  while (
    result
    and not result[-1].strip()
  ):
    result.pop()

  return result


def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  title = "# Group proof narrative"
  target_header = "## 証明対象"
  reference_header = "## 使用する結果"
  separator = "---"
  proof_header = "## 証明"
  qed = "□"

  source_lines = (
    rendered.rstrip().splitlines()
  )

  if (
    source_lines
    and source_lines[0] == title
  ):
    content_lines = source_lines[1:]
  else:
    content_lines = source_lines[:]

  while (
    content_lines
    and not content_lines[0].strip()
  ):
    content_lines.pop(0)

  def exact_index(
    marker: str,
  ) -> int | None:
    try:
      return content_lines.index(
        marker
      )
    except ValueError:
      return None

  target_index = exact_index(
    target_header
  )
  reference_index = exact_index(
    reference_header
  )
  proof_index = exact_index(
    proof_header
  )

  if target_index is not None:
    target_end_candidates = [
      index
      for index in (
        reference_index,
        proof_index,
        len(
          content_lines
        ),
      )
      if (
        index is not None
        and index > target_index
      )
    ]
    target_end = min(
      target_end_candidates
    )
    target_body = content_lines[
      target_index + 1:
      target_end
    ]
  else:
    target_body = (
      _phase158_public_narrative_target_lines(
        presentation
      )
    )

  while (
    target_body
    and not target_body[0].strip()
  ):
    target_body.pop(0)

  while (
    target_body
    and not target_body[-1].strip()
  ):
    target_body.pop()

  reference_body: list[str] = []

  if (
    reference_index is not None
    and proof_index is not None
    and reference_index < proof_index
  ):
    reference_body = content_lines[
      reference_index + 1:
      proof_index
    ]

  while (
    reference_body
    and not reference_body[0].strip()
  ):
    reference_body.pop(0)

  while (
    reference_body
    and not reference_body[-1].strip()
  ):
    reference_body.pop()

  if (
    reference_body
    and reference_body[-1].strip()
    == separator
  ):
    reference_body.pop()

    while (
      reference_body
      and not reference_body[-1].strip()
    ):
      reference_body.pop()

  if proof_index is not None:
    proof_body = content_lines[
      proof_index + 1:
    ]
  elif (
    target_index is None
    and reference_index is None
  ):
    proof_body = content_lines[:]
  else:
    proof_body = []

  while (
    proof_body
    and not proof_body[0].strip()
  ):
    proof_body.pop(0)

  proof_body = (
    _phase158_strip_terminal_qed_lines(
      proof_body
    )
  )

  lines = [
    title,
    "",
    target_header,
    "",
    *target_body,
    "",
    reference_header,
    "",
  ]

  if reference_body:
    lines.extend(
      (
        *reference_body,
        "",
      )
    )

  lines.extend(
    (
      separator,
      "",
      proof_header,
      "",
      *proof_body,
      "",
      qed,
    )
  )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )


def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  return (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
'''


def main() -> int:
  if not R2_BASELINE.exists():
    raise RuntimeError(
      "Phase 158-R2 pre-apply backup was not found: "
      + str(
        R2_BASELINE
      )
    )

  baseline_source = (
    R2_BASELINE.read_text(
      encoding="utf-8",
    )
  )

  if PUBLIC_DEF not in baseline_source:
    raise RuntimeError(
      "Public renderer definition was not found "
      "in the R2 pre-apply backup."
    )

  if (
    "_phase158_normalize_public_narrative_contract"
    in baseline_source
  ):
    raise RuntimeError(
      "The R2 pre-apply backup already contains "
      "Phase 158 code."
    )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  current_backup = (
    BACKUP_DIR
    / TARGET.name
  )

  if not current_backup.exists():
    shutil.copy2(
      TARGET,
      current_backup,
    )

  restored_source = (
    baseline_source.replace(
      PUBLIC_DEF,
      BASELINE_DEF,
      1,
    )
  )

  if PUBLIC_DEF in restored_source:
    raise RuntimeError(
      "More than one public renderer definition "
      "exists in the baseline."
    )

  restored_source = (
    restored_source.rstrip()
    + APPENDIX
    + "\n"
  )

  TARGET.write_text(
    restored_source,
    encoding="utf-8",
  )

  py_compile.compile(
    str(
      TARGET
    ),
    doraise=True,
  )

  print(
    "Phase 158-R2 repair4 applied."
  )
  print(
    "Baseline restored from:"
  )
  print(
    "  "
    + str(
      R2_BASELINE
    )
  )
  print(
    "Syntax check: PASS"
  )
  print(
    "Policy: baseline mathematical content is preserved; "
    "only the public shell and terminal QED marker are normalized."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
