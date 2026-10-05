from __future__ import annotations

from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP_DIR = REPO_ROOT / "phase158_r2_repair1_backup_before_apply"


HELPER = r'''def _phase158_preserve_dedicated_reference_detail(
  original_rendered: str,
  connected_rendered: str,
) -> str:
  if not isinstance(
    original_rendered,
    str,
  ):
    raise TypeError(
      "original_rendered must be a str"
    )

  if not isinstance(
    connected_rendered,
    str,
  ):
    raise TypeError(
      "connected_rendered must be a str"
    )

  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  original_lines = original_rendered.splitlines()
  connected_lines = connected_rendered.splitlines()

  try:
    original_reference_index = original_lines.index(
      reference_header
    )
    original_proof_index = original_lines.index(
      proof_header
    )
    connected_reference_index = connected_lines.index(
      reference_header
    )
    connected_proof_index = connected_lines.index(
      proof_header
    )
  except ValueError:
    return connected_rendered

  if not (
    original_reference_index < original_proof_index
    and connected_reference_index < connected_proof_index
  ):
    return connected_rendered

  original_reference_body = original_lines[
    original_reference_index + 1:
    original_proof_index
  ]

  while (
    original_reference_body
    and not original_reference_body[0].strip()
  ):
    original_reference_body.pop(0)

  while (
    original_reference_body
    and not original_reference_body[-1].strip()
  ):
    original_reference_body.pop()

  if not original_reference_body:
    return connected_rendered

  original_statement_lines = original_reference_body[1:]

  while (
    original_statement_lines
    and not original_statement_lines[0].strip()
  ):
    original_statement_lines.pop(0)

  while (
    original_statement_lines
    and not original_statement_lines[-1].strip()
  ):
    original_statement_lines.pop()

  if not original_statement_lines:
    return connected_rendered

  connected_reference_body = connected_lines[
    connected_reference_index + 1:
    connected_proof_index
  ]

  original_statement_text = "\n".join(
    original_statement_lines
  ).strip()
  connected_reference_text = "\n".join(
    connected_reference_body
  )

  if (
    original_statement_text
    and original_statement_text in connected_reference_text
  ):
    return connected_rendered

  merged_reference_body = connected_reference_body[:]

  while (
    merged_reference_body
    and not merged_reference_body[-1].strip()
  ):
    merged_reference_body.pop()

  merged_reference_body.extend(
    (
      "",
      *original_statement_lines,
    )
  )

  return (
    "\n".join(
      (
        *connected_lines[:connected_reference_index + 1],
        *merged_reference_body,
        "",
        *connected_lines[connected_proof_index:],
      )
    ).rstrip()
    + "\n"
  )


'''


OLD_BRANCH = r'''  if phase134_24_pi15_8 is not None:
    rendered = (
      _phase153_r3_10_connect_public_reference_section(
        presentation,
        phase134_24_pi15_8,
      )
    )

    return (
      _phase158_normalize_public_narrative_contract(
        presentation,
        rendered,
      )
    )
'''


NEW_BRANCH = r'''  if phase134_24_pi15_8 is not None:
    rendered = (
      _phase153_r3_10_connect_public_reference_section(
        presentation,
        phase134_24_pi15_8,
      )
    )
    rendered = (
      _phase158_preserve_dedicated_reference_detail(
        phase134_24_pi15_8,
        rendered,
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
    source = TARGET.read_text(
        encoding="utf-8",
    )

    if (
        "def _phase158_normalize_public_narrative_contract("
        not in source
    ):
        raise RuntimeError(
            "Phase 158-R2 must be applied before repair1."
        )

    if (
        "def _phase158_preserve_dedicated_reference_detail("
        in source
    ):
        print(
            "Phase 158-R2 repair1 already appears to be applied."
        )
        return 0

    helper_marker = (
        "def _phase158_normalize_public_narrative_contract(\n"
    )
    helper_index = source.find(
        helper_marker
    )

    if helper_index < 0:
        raise RuntimeError(
            "Phase 158 normalization helper was not found."
        )

    if OLD_BRANCH not in source:
        raise RuntimeError(
            "Expected Phase 158-R2 pi15_8 branch was not found."
        )

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    backup = BACKUP_DIR / TARGET.name

    if not backup.exists():
        shutil.copy2(
            TARGET,
            backup,
        )

    source = (
        source[:helper_index]
        + HELPER
        + source[helper_index:]
    )
    source = source.replace(
        OLD_BRANCH,
        NEW_BRANCH,
        1,
    )

    TARGET.write_text(
        source,
        encoding="utf-8",
    )

    print(
        "Phase 158-R2 repair1 applied."
    )
    print(
        f"Backup: {backup}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
