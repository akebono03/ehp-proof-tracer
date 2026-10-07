from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_PATH = (
  ROOT
  / "toda_upstream_bootstrap.py"
)


OLD_IMPORT_LINE = (
  "  toda_delta_iota5_whitehead_square_inference_rule,\n"
)

OLD_RULE_LINE = (
  "    toda_delta_iota5_whitehead_square_inference_rule(),\n"
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
    "legacy Whitehead Delta import",
  )

  source = remove_once(
    source,
    OLD_RULE_LINE,
    "legacy Whitehead Delta rule call",
  )

  BOOTSTRAP_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159 pi_4^3 repair1b applied."
  )
  print(
    "Changed: toda_upstream_bootstrap.py"
  )
  print(
    "Removed from _build_phase50_result(): "
    "legacy Delta(iota_5)=+/-[iota_2,iota_2] route"
  )
  print(
    "The legacy rule implementation remains "
    "available in toda_rules.py."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
