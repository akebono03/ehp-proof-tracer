from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_r6_1"

PROD_REPLACEMENTS = {'toda_group_proof_generic_narrative_renderer.py': [('    return prose\n', '    return (\n      _normalize_toda_group_proof_narrative_sentence_endings(\n        prose\n      )\n    )\n', 'generic prose return'), ('def _render_generic_narrative_step(\n', 'def _normalize_toda_group_proof_narrative_sentence_endings(\n  prose: str,\n) -> str:\n  if not isinstance(\n    prose,\n    str,\n  ):\n    raise TypeError(\n      "prose must be a str"\n    )\n\n  normalized_lines = []\n\n  for line in prose.splitlines():\n    stripped = line.rstrip()\n    trailing = line[\n      len(\n        stripped\n      ):\n    ]\n    has_japanese = any(\n      (\n        "\\u3040" <= character <= "\\u30ff"\n        or "\\u3400" <= character <= "\\u9fff"\n      )\n      for character in stripped\n    )\n\n    if (\n      has_japanese\n      and stripped.endswith(\n        "."\n      )\n    ):\n      stripped = (\n        stripped[\n          :-1\n        ]\n        + "。"\n      )\n\n    normalized_lines.append(\n      stripped\n      + trailing\n    )\n\n  return "\\n".join(\n    normalized_lines\n  )\n\n\ndef _render_generic_narrative_step(\n', 'insert sentence ending normalizer'), ('"次の短完全列を得る."', '"次の短完全列を得る。"', 'short exact period'), ('return "次の完全列を考える."', 'return "次の完全列を考える。"', 'exactness lead period'), ('" の条件のもとで, 次の定義を用いる."', '" の条件のもとで, 次の定義を用いる。"', 'definition lead period'), ('" を用いて, 次の完全列を考える."', '" を用いて, 次の完全列を考える。"', 'dependency lead period')], 'toda_group_proof_narrative_reason_renderer.py': [('"次の定義を用いる."', '"次の定義を用いる。"', 'reason definition'), (' を適用できる.\\n"', ' を適用できる。\\n"', 'reason applicability'), ('"である.\\n"', '"である。\\n"', 'reason derivation'), ('を生成する.\\n"', 'を生成する。\\n"', 'reason generator'), ('が決まる.\\nしたがって、"', 'が決まる。\\nしたがって、"', 'reason result')], 'toda_group_proof_narrative_references.py': [('lines = ["使用する結果を先にまとめる.", ""]', 'lines = ["使用する結果を先にまとめる。", ""]', 'reference intro')], 'toda_group_proof_narrative_argument_renderer.py': [('f"${subject_latex}$ を定める."', 'f"${subject_latex}$ を定める。"', 'argument definition'), ('f"${subject_latex}$ の位数を決定する."', 'f"${subject_latex}$ の位数を決定する。"', 'argument order'), ('f"${subject_latex}$ の群構造を決定する."', 'f"${subject_latex}$ の群構造を決定する。"', 'argument group'), ('"する."', '"する。"', 'argument suffix')], 'toda_group_proof_narrative_exactness_method_renderer.py': [('return "そのために、次の完全列を考える."', 'return "そのために、次の完全列を考える。"', 'exactness transition')], 'toda_group_proof_narrative_argument_body_renderer.py': [('+ "$ は完全である."', '+ "$ は完全である。"', 'argument exactness')]}
TEST_FILES = ['tests/test_phase154_r2_internal_prose_fallback_leakage.py', 'tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py', 'tests/test_phase154_r2_fix2_semantic_sentence_composition.py', 'tests/test_phase154_r2_fix3_reference_marker_completion.py', 'tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py', 'tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py', 'tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py']
TEST_REPLACEMENTS = [('$\\nu_{4}$ の分解写像は同型写像である.', '$\\nu_{4}$ の分解写像は同型写像である。'), ('$\\nu_{4}$ の分解を用いる.', '$\\nu_{4}$ の分解を用いる。'), ('使用する結果を先にまとめる.', '使用する結果を先にまとめる。')]


def backup(path: Path) -> None:
  relative = path.relative_to(REPO_ROOT)
  target = BACKUP_ROOT / relative
  target.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(path, target)


def update_required(path: Path, replacements) -> None:
  backup(path)
  text = path.read_text(encoding="utf-8")

  for old, new, label in replacements:
    if old not in text:
      raise RuntimeError(
        "required pattern not found in "
        + str(path)
        + ": "
        + label
      )
    text = text.replace(old, new)

  path.write_text(text, encoding="utf-8")
  print("updated:", path.relative_to(REPO_ROOT))


def main() -> int:
  for relative_path, replacements in PROD_REPLACEMENTS.items():
    path = REPO_ROOT / relative_path
    if not path.exists():
      raise RuntimeError("missing file: " + str(path))
    update_required(path, replacements)

  test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_1_shared_punctuation_normalization.py"
  )
  test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_1_shared_punctuation_normalization.py"
  )
  backup(test_target) if test_target.exists() else None
  shutil.copy2(test_source, test_target)
  print("added:", test_target.relative_to(REPO_ROOT))

  for relative_path in TEST_FILES:
    path = REPO_ROOT / relative_path
    if not path.exists():
      continue

    backup(path)
    text = path.read_text(encoding="utf-8")
    updated = text

    for old, new in TEST_REPLACEMENTS:
      updated = updated.replace(old, new)

    if updated != text:
      path.write_text(updated, encoding="utf-8")
      print("updated test expectation:", relative_path)

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
