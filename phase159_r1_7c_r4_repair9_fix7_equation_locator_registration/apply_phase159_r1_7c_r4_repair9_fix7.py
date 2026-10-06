from __future__ import annotations

from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

BOUNDARY = REPO_ROOT / "toda_literature_statement_boundary.py"
REFERENCES = REPO_ROOT / "toda_group_proof_narrative_references.py"

TEST_BOUNDARY_R5 = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r5_r3_boundary_catalog_expansion.py"
)
TEST_BOUNDARY_R4 = (
  REPO_ROOT
  / "tests"
  / "test_phase157_r4_r2_boundary_catalog.py"
)
TEST_REFERENCE_INFERENCE = (
  REPO_ROOT
  / "tests"
  / "test_phase156_r5_repair4_bridge_reference_inference.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"


def _backup(path: Path) -> None:
    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    target = BACKUP_DIR / path.name
    if not target.exists():
        shutil.copy2(
            path,
            target,
        )


def _replace_exact_count(
    source: str,
    old: str,
    new: str,
    expected_count: int,
    label: str,
) -> str:
    count = source.count(old)

    if count == 0 and new in source:
        print(
            f"{label}: already applied"
        )
        return source

    if count != expected_count:
        raise RuntimeError(
            f"{label}: expected {expected_count} occurrence(s), "
            f"found {count}"
        )

    print(
        f"{label}: replacing {count} occurrence(s)"
    )
    return source.replace(
        old,
        new,
    )


def _update_boundary() -> None:
    source = BOUNDARY.read_text(
        encoding="utf-8"
    )

    updated = source

    updated = _replace_exact_count(
        updated,
        'reference_locator="Equation 5.13"',
        'reference_locator="(5.13)"',
        3,
        "Equation 5.13 component locators",
    )
    updated = _replace_exact_count(
        updated,
        '"Equation 5.13": _EQUATION_513_COMPONENTS',
        '"(5.13)": _EQUATION_513_COMPONENTS',
        1,
        "Equation 5.13 catalog key",
    )
    updated = _replace_exact_count(
        updated,
        '"Toda Equation 5.13 Delta nu_9": "Equation 5.13"',
        '"Toda Equation 5.13 Delta nu_9": "(5.13)"',
        1,
        "Equation 5.13 nu9 fixed-rule locator",
    )
    updated = _replace_exact_count(
        updated,
        '"Toda Equation 5.13 Delta eta_11 squared zero": "Equation 5.13"',
        '"Toda Equation 5.13 Delta eta_11 squared zero": "(5.13)"',
        1,
        "Equation 5.13 eta11 fixed-rule locator",
    )
    updated = _replace_exact_count(
        updated,
        '"Toda Equation 5.13 Delta eta_13 zero": "Equation 5.13"',
        '"Toda Equation 5.13 Delta eta_13 zero": "(5.13)"',
        1,
        "Equation 5.13 eta13 fixed-rule locator",
    )

    updated = _replace_exact_count(
        updated,
        '"Equation 5.7": (',
        '"(5.7)": (',
        1,
        "Equation 5.7 catalog key",
    )
    updated = _replace_exact_count(
        updated,
        'reference_locator="Equation 5.7"',
        'reference_locator="(5.7)"',
        1,
        "Equation 5.7 component locator",
    )

    updated = _replace_exact_count(
        updated,
        '"Equation 5.8": (',
        '"(5.8)": (',
        1,
        "Equation 5.8 catalog key",
    )
    updated = _replace_exact_count(
        updated,
        'reference_locator="Equation 5.8"',
        'reference_locator="(5.8)"',
        1,
        "Equation 5.8 component locator",
    )
    updated = _replace_exact_count(
        updated,
        "'Toda Equation 5.8 integration': 'Equation 5.8'",
        "'Toda Equation 5.8 integration': '(5.8)'",
        1,
        "Equation 5.8 fixed-rule locator",
    )

    internal_anchor = (
        "_PHASE157_R5_R3_INTERNAL_RULE_LOCATORS = {\n"
    )
    equation57_line = (
        "    'Toda Equation 5.7 nu-prime eta_6 Hopf value': '(5.7)',\n"
    )

    if equation57_line not in updated:
        anchor_index = updated.find(
            internal_anchor
        )
        if anchor_index < 0:
            raise RuntimeError(
                "Internal rule-locator mapping anchor was not found."
            )

        insert_at = (
            anchor_index
            + len(
                internal_anchor
            )
        )
        updated = (
            updated[:insert_at]
            + equation57_line
            + updated[insert_at:]
        )
        print(
            "Equation 5.7 internal rule locator: added"
        )
    else:
        print(
            "Equation 5.7 internal rule locator: already present"
        )

    compile(
        updated,
        str(
            BOUNDARY
        ),
        "exec",
    )

    if updated != source:
        _backup(
            BOUNDARY
        )
        BOUNDARY.write_text(
            updated,
            encoding="utf-8",
        )


def _update_reference_inference() -> None:
    source = REFERENCES.read_text(
        encoding="utf-8"
    )

    old = """  if named_match is not None:
    kind, number = named_match.groups()
    locator = f"{kind} {number}"
    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )
"""

    new = """  if named_match is not None:
    kind, number = named_match.groups()

    if kind == "Equation":
      locator = f"({number})"
    else:
      locator = f"{kind} {number}"

    return LiteratureReference(
      label=f"Toda {locator}",
      locator=locator,
    )
"""

    if new in source:
        print(
            "Named Equation inference: already applied"
        )
        return

    if source.count(
        old
    ) != 1:
        raise RuntimeError(
            "Named reference inference block was not found exactly once."
        )

    updated = source.replace(
        old,
        new,
        1,
    )

    compile(
        updated,
        str(
            REFERENCES
        ),
        "exec",
    )

    _backup(
        REFERENCES
    )
    REFERENCES.write_text(
        updated,
        encoding="utf-8",
    )
    print(
        "Named Equation inference: Equation N.M -> (N.M)"
    )


def _replace_test_values(
    path: Path,
    replacements: tuple[
      tuple[str, str, int],
      ...,
    ],
) -> None:
    source = path.read_text(
        encoding="utf-8"
    )
    updated = source

    for old, new, expected_count in replacements:
        count = updated.count(
            old
        )

        if count == 0 and new in updated:
            continue

        if count != expected_count:
            raise RuntimeError(
                f"{path.name}: expected {expected_count} "
                f"occurrence(s) of {old!r}, found {count}"
            )

        updated = updated.replace(
            old,
            new,
        )

    compile(
        updated,
        str(
            path
        ),
        "exec",
    )

    if updated != source:
        _backup(
            path
        )
        path.write_text(
            updated,
            encoding="utf-8",
        )
        print(
            f"Updated test expectations: {path.name}"
        )


def _append_reference_inference_test() -> None:
    source = TEST_REFERENCE_INFERENCE.read_text(
        encoding="utf-8"
    )

    test_source = r'''

def test_phase159_r1_7c_r4_repair9_fix7_named_equation_infers_parenthesized_locator():
  reference = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      "Toda Equation 5.7 nu-prime eta_6 Hopf value"
    )
  )

  assert reference is not None
  assert reference.label == "Toda (5.7)"
  assert reference.locator == "(5.7)"
'''

    if (
        "test_phase159_r1_7c_r4_repair9_fix7_named_equation_infers_parenthesized_locator"
        in source
    ):
        print(
            "Named Equation inference test: already present"
        )
        return

    updated = (
        source.rstrip()
        + test_source
        + "\n"
    )

    compile(
        updated,
        str(
            TEST_REFERENCE_INFERENCE
        ),
        "exec",
    )

    _backup(
        TEST_REFERENCE_INFERENCE
    )
    TEST_REFERENCE_INFERENCE.write_text(
        updated,
        encoding="utf-8",
    )
    print(
        "Named Equation inference test: added"
    )


def main() -> int:
    for path in (
        BOUNDARY,
        REFERENCES,
        TEST_BOUNDARY_R5,
        TEST_BOUNDARY_R4,
        TEST_REFERENCE_INFERENCE,
    ):
        if not path.is_file():
            raise RuntimeError(
                f"Required file not found: {path}"
            )

    _update_boundary()
    _update_reference_inference()

    _replace_test_values(
        TEST_BOUNDARY_R5,
        (
            (
                "'Equation 5.7'",
                "'(5.7)'",
                1,
            ),
            (
                "'Equation 5.8'",
                "'(5.8)'",
                1,
            ),
        ),
    )

    _replace_test_values(
        TEST_BOUNDARY_R4,
        (
            (
                '"Equation 5.13"',
                '"(5.13)"',
                1,
            ),
        ),
    )

    _append_reference_inference_test()

    print(
        "Production files changed:"
    )
    print(
        "  toda_literature_statement_boundary.py"
    )
    print(
        "  toda_group_proof_narrative_references.py"
    )
    print(
        "No renderer title-normalization rule was added."
    )
    print(
        "No group-specific n/k branch was added."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
