from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_PATH = (
  ROOT
  / "toda_upstream_bootstrap.py"
)


OLD_IMPORT_LINE = (
  "  toda_pi4_3_delta_image_free_cyclic_inference_rule,\n"
)

OLD_RULE_LINE = (
  "    toda_pi4_3_delta_image_free_cyclic_inference_rule(),\n"
)


def remove_once(
  text: str,
  target: str,
  label: str,
) -> str:
  count = text.count(
    target
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, "
      f"found {count}"
    )

  return text.replace(
    target,
    "",
    1,
  )


def main() -> int:
  source = BOOTSTRAP_PATH.read_text(
    encoding="utf-8"
  )

  source = remove_once(
    source,
    OLD_IMPORT_LINE,
    "legacy pi4_3 Delta-image import",
  )

  source = remove_once(
    source,
    OLD_RULE_LINE,
    "legacy pi4_3 Delta-image rule call",
  )

  BOOTSTRAP_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 pi_4^3 repair1a applied."
  )
  print(
    "Changed: toda_upstream_bootstrap.py"
  )
  print(
    "Removed from _build_phase50_result(): "
    "legacy Whitehead-specific Im(Delta) rule"
  )
  print(
    "The legacy rule implementation itself "
    "remains available for compatibility."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
