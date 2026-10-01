from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = PACKAGE_ROOT / "backup_before_repair3"


def backup(path: Path) -> None:
  relative = path.relative_to(
    REPO_ROOT
  )
  target = BACKUP_ROOT / relative
  target.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    path,
    target,
  )


def replace_if_present(
  text: str,
  old: str,
  new: str,
) -> tuple[str, bool]:
  if old not in text:
    return (
      text,
      False,
    )

  return (
    text.replace(
      old,
      new,
    ),
    True,
  )


def update_file(
  relative_path: str,
  replacements,
) -> None:
  path = REPO_ROOT / relative_path

  if not path.exists():
    raise RuntimeError(
      "missing file: "
      + str(
        path
      )
    )

  backup(
    path
  )
  text = path.read_text(
    encoding="utf-8",
  )
  changed = False

  for old, new, label in replacements:
    text, did_change = replace_if_present(
      text,
      old,
      new,
    )

    if did_change:
      print(
        "  updated:",
        label,
      )
      changed = True
    else:
      print(
        "  already-current or absent:",
        label,
      )

  path.write_text(
    text,
    encoding="utf-8",
  )

  print(
    "checked:",
    relative_path,
  )

  if not changed:
    print(
      "  no content change required"
    )


def main() -> int:
  update_file(
    "toda_group_proof_generic_narrative_renderer.py",
    (
      (
        'and stripped.endswith(\n        "."\n      )\n    ):\n      stripped = (\n        stripped[\n          :-1\n        ]\n        + "。"\n      )',
        'and stripped.endswith(\n        "。"\n      )\n    ):\n      stripped = (\n        stripped[\n          :-1\n        ]\n        + "."\n      )',
        "generic sentence-ending normalizer direction",
      ),
      (
        '"次の短完全列を得る。"',
        '"次の短完全列を得る."',
        "short exact sequence sentence ending",
      ),
      (
        'return "次の完全列を考える。"',
        'return "次の完全列を考える."',
        "exactness lead sentence ending",
      ),
      (
        '" の条件のもとで, 次の定義を用いる。"',
        '" の条件のもとで, 次の定義を用いる."',
        "definition lead sentence ending",
      ),
      (
        '" を用いて, 次の完全列を考える。"',
        '" を用いて, 次の完全列を考える."',
        "exactness dependency sentence ending",
      ),
    ),
  )

  update_file(
    "toda_group_proof_narrative_reason_renderer.py",
    (
      (
        "次の定義を用いる。",
        "次の定義を用いる.",
        "definition applicability ending",
      ),
      (
        "を適用できる。\\n",
        "を適用できる.\\n",
        "reference applicability ending",
      ),
      (
        "である。\\n",
        "である.\\n",
        "reason factual ending",
      ),
      (
        "を生成する。\\n",
        "を生成する.\\n",
        "generator reason ending",
      ),
      (
        "が決まる。\\nしたがって、",
        "が決まる.\\nしたがって、",
        "reason derivation ending",
      ),
    ),
  )

  update_file(
    "toda_group_proof_narrative_references.py",
    (
      (
        'lines = ["使用する結果を先にまとめる。", ""]',
        'lines = ["使用する結果を先にまとめる.", ""]',
        "reference introduction ending",
      ),
    ),
  )

  update_file(
    "toda_group_proof_narrative_argument_renderer.py",
    (
      (
        'f"${subject_latex}$ を定める。" ',
        'f"${subject_latex}$ を定める." ',
        "argument definition ending spaced form",
      ),
      (
        'f"${subject_latex}$ を定める。"',
        'f"${subject_latex}$ を定める."',
        "argument definition ending",
      ),
      (
        'f"${subject_latex}$ の位数を決定する。" ',
        'f"${subject_latex}$ の位数を決定する." ',
        "argument order ending spaced form",
      ),
      (
        'f"${subject_latex}$ の位数を決定する。"',
        'f"${subject_latex}$ の位数を決定する."',
        "argument order ending",
      ),
      (
        'f"${subject_latex}$ の群構造を決定する。" ',
        'f"${subject_latex}$ の群構造を決定する." ',
        "argument group ending spaced form",
      ),
      (
        'f"${subject_latex}$ の群構造を決定する。"',
        'f"${subject_latex}$ の群構造を決定する."',
        "argument group ending",
      ),
      (
        '"する。" ',
        '"する." ',
        "argument suffix contract spaced form",
      ),
      (
        '"する。"',
        '"する."',
        "argument suffix contract",
      ),
    ),
  )

  update_file(
    "toda_group_proof_narrative_exactness_method_renderer.py",
    (
      (
        'return "そのために、次の完全列を考える。"',
        'return "そのために、次の完全列を考える."',
        "exactness transition ending",
      ),
    ),
  )

  update_file(
    "toda_group_proof_narrative_argument_body_renderer.py",
    (
      (
        '+ "$ は完全である。"',
        '+ "$ は完全である."',
        "argument exactness ending",
      ),
    ),
  )

  update_file(
    "toda_group_proof_narrative_contribution_renderer.py",
    (
      (
        '"を用いる。"',
        '"を用いる."',
        "reference marker neutral sentence ending",
      ),
      (
        '"を得る。"',
        '"を得る."',
        "reference replacement ending",
      ),
    ),
  )

  update_file(
    "toda_group_proof_narrative_renderer.py",
    (
      (
        '"を用いる。" ',
        '"を用いる." ',
        "legacy reference use spaced ending",
      ),
      (
        '"を用いる。"',
        '"を用いる."',
        "legacy reference use ending",
      ),
      (
        '"を得る。" ',
        '"を得る." ',
        "legacy derivation spaced ending",
      ),
      (
        '"を得る。"',
        '"を得る."',
        "legacy derivation ending",
      ),
      (
        '"である。" ',
        '"である." ',
        "legacy assertion spaced ending",
      ),
      (
        '"である。"',
        '"である."',
        "legacy assertion ending",
      ),
      (
        '"ことを示す。" ',
        '"ことを示す." ',
        "legacy purpose spaced ending",
      ),
      (
        '"ことを示す。"',
        '"ことを示す."',
        "legacy purpose ending",
      ),
    ),
  )

  test_paths = (
    "tests/test_phase154_r2_internal_prose_fallback_leakage.py",
    "tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py",
    "tests/test_phase154_r2_fix2_semantic_sentence_composition.py",
    "tests/test_phase154_r2_fix3_reference_marker_completion.py",
    "tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py",
    "tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py",
    "tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py",
  )

  test_replacements = (
    (
      "は単射である。",
      "は単射である.",
      "injective expectation ending",
    ),
    (
      "は完全である。",
      "は完全である.",
      "exactness expectation ending",
    ),
    (
      "分解を用いる。",
      "分解を用いる.",
      "decomposition expectation ending",
    ),
    (
      "分解写像は同型写像である。",
      "分解写像は同型写像である.",
      "isomorphism expectation ending",
    ),
    (
      "使用する結果を先にまとめる。",
      "使用する結果を先にまとめる.",
      "reference introduction expectation ending",
    ),
    (
      "[R1]を用いる。",
      "[R1]を用いる.",
      "neutral reference expectation ending",
    ),
    (
      "[R2]を用いる。",
      "[R2]を用いる.",
      "reference expectation ending",
    ),
  )

  for relative_path in test_paths:
    update_file(
      relative_path,
      test_replacements,
    )

  obsolete_tests = (
    "tests/test_phase154_r6_1_shared_punctuation_normalization.py",
    "tests/test_phase154_r6_1_repair1_remaining_periods.py",
    "tests/test_phase154_r6_1_repair2_idempotent_resume.py",
  )

  for relative_path in obsolete_tests:
    path = REPO_ROOT / relative_path

    if not path.exists():
      continue

    backup(
      path
    )
    path.unlink()
    print(
      "removed obsolete wrong-policy test:",
      relative_path,
    )

  new_test_source = (
    PACKAGE_ROOT
    / "tests"
    / "test_phase154_r6_1_repair3_ascii_period_policy.py"
  )
  new_test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r6_1_repair3_ascii_period_policy.py"
  )

  if new_test_target.exists():
    backup(
      new_test_target
    )

  shutil.copy2(
    new_test_source,
    new_test_target,
  )

  print(
    "added:",
    new_test_target.relative_to(
      REPO_ROOT
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
