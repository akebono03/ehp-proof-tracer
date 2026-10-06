from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "toda_literature_statement_boundary.py"

RULE_NAME = "Toda Equation 5.7 nu-prime eta_6 Hopf value"

COMPONENT_ENTRY = (
  '  "Toda Equation 5.7 nu-prime eta_6 Hopf value": '
  '"nu_prime_eta6_hopf_relation",\n'
)

LOCATOR_ENTRY = (
  '  "Toda Equation 5.7 nu-prime eta_6 Hopf value": '
  '"Equation 5.7",\n'
)


def insert_after_dictionary_open(
  source: str,
  dictionary_name: str,
  entry: str,
  unique_marker: str,
) -> str:
  if unique_marker in source:
    return source

  anchor = (
    dictionary_name
    + " = {\n"
  )
  index = source.find(
    anchor
  )

  if index < 0:
    raise RuntimeError(
      "dictionary not found: "
      + dictionary_name
    )

  insert_at = (
    index
    + len(
      anchor
    )
  )

  return (
    source[
      :insert_at
    ]
    + entry
    + source[
      insert_at:
    ]
  )


def main() -> None:
  if not BOUNDARY.exists():
    raise FileNotFoundError(
      BOUNDARY
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6b_repair3_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    BOUNDARY,
    backup_dir / BOUNDARY.name,
  )

  source = BOUNDARY.read_text(
    encoding="utf-8-sig"
  )

  source = insert_after_dictionary_open(
    source,
    "_FIXED_RULE_COMPONENT_KEYS",
    COMPONENT_ENTRY,
    (
      '"Toda Equation 5.7 nu-prime eta_6 Hopf value": '
      '"nu_prime_eta6_hopf_relation"'
    ),
  )

  locator_dictionary_index = source.find(
    "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {\n"
  )

  if locator_dictionary_index < 0:
    raise RuntimeError(
      "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME not found"
    )

  locator_tail = source[
    locator_dictionary_index:
  ]

  if (
    '"Toda Equation 5.7 nu-prime eta_6 Hopf value": '
    '"Equation 5.7"'
    not in locator_tail
  ):
    anchor = (
      "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {\n"
    )
    insert_at = (
      locator_dictionary_index
      + len(
        anchor
      )
    )
    source = (
      source[
        :insert_at
      ]
      + LOCATOR_ENTRY
      + source[
        insert_at:
      ]
    )

  BOUNDARY.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6b repair3 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Mapped Equation 5.7 Hopf-value rule "
    "to its existing fixed component."
  )
  print(
    "Test changes: none."
  )


if __name__ == "__main__":
  main()
