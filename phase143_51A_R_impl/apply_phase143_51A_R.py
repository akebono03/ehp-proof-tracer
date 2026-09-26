from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent
GENERIC = ROOT / "toda_group_proof_generic_narrative_renderer.py"


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def install_catalog() -> None:
  source = SOURCE / "toda_group_proof_narrative_provenance_catalog.py"
  destination = ROOT / "toda_group_proof_narrative_provenance_catalog.py"
  shutil.copyfile(source, destination)
  print(f"updated {destination}")


def patch_generic_renderer() -> None:
  text = GENERIC.read_text(encoding="utf-8")

  old_homotopy_import = '''from homotopy_groups import (
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
'''
  new_homotopy_import = '''from homotopy_groups import (
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaSuspensionMap,
)
'''
  text = replace_once(
    text,
    old_homotopy_import,
    new_homotopy_import,
    "homotopy_groups import",
  )

  old_catalog_import = '''from toda_group_proof_narrative_catalog import (
  REFERENCE_STATEMENT_TYPES,
)
'''
  new_catalog_import = '''from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
'''
  text = replace_once(
    text,
    old_catalog_import,
    new_catalog_import,
    "provenance catalog import",
  )

  old_classification = '''_GENERIC_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES = (
  *REFERENCE_STATEMENT_TYPES,
  TodaProp44DecompositionMap,
)


def _is_generic_narrative_provenance_only_statement(
  statement,
) -> bool:
  return isinstance(
    statement,
    _GENERIC_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES,
  )


'''
  new_classification = '''def _is_generic_narrative_provenance_only_statement(
  statement,
) -> bool:
  return (
    is_toda_group_proof_narrative_provenance_only_statement(
      statement
    )
  )


'''
  text = replace_once(
    text,
    old_classification,
    new_classification,
    "provenance-only classification",
  )

  GENERIC.write_text(text, encoding="utf-8")
  print(f"updated {GENERIC}")


def install_test() -> None:
  source = SOURCE / "tests" / "test_phase143_51a_r_provenance_semantic_catalog.py"
  destination = ROOT / "tests" / "test_phase143_51a_r_provenance_semantic_catalog.py"
  shutil.copyfile(source, destination)
  print(f"updated {destination}")


def main() -> None:
  install_catalog()
  patch_generic_renderer()
  install_test()


if __name__ == "__main__":
  main()
