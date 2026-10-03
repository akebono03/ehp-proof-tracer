from pathlib import Path

TARGET = Path(
    "tests/test_phase157_r2_literature_statement_boundary.py"
)

OLD = 'def test_phase157_r2_untracked_reference_is_not_classified():\n  boundary = classify_toda_literature_statement_step(\n    _step(\n      "Toda Proposition 5.15 test",\n      "Proposition 5.15",\n    )\n  )\n\n  assert boundary is None\n'
NEW = 'def test_phase157_r2_untracked_rule_in_tracked_reference_is_proof_internal():\n  boundary = classify_toda_literature_statement_step(\n    _step(\n      "Toda Proposition 5.15 test",\n      "Proposition 5.15",\n    )\n  )\n\n  assert boundary is not None\n  assert boundary.classification == (\n    TodaLiteratureStatementClassification.PROOF_INTERNAL\n  )\n  assert boundary.reference_locator == "Proposition 5.15"\n  assert boundary.component_key is None\n'


def main():
    if not TARGET.exists():
        raise SystemExit(f"target not found: {TARGET}")

    text = TARGET.read_text(
        encoding="utf-8"
    )

    if OLD not in text:
        raise SystemExit(
            "expected Phase157-R2 test block not found"
        )

    text = text.replace(
        OLD,
        NEW,
        1,
    )

    TARGET.write_text(
        text,
        encoding="utf-8",
        newline="\n",
    )

    print(
        "Phase157-R4-R2 repair1 applied."
    )
    print(
        f"updated: {TARGET.resolve()}"
    )
    print(
        "Production code changes: none"
    )


if __name__ == "__main__":
    main()
