from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

TEST = ROOT / "tests" / "test_phase157_r20_generic_dependency_rendering.py"


NEW_TEST = r'''def test_phase157_r20_reference_dependencies_are_recovered_from_graph():
  rendered = _render_pi6_3_r20()

  for reference in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "(5.7)",
  ):
    assert reference in rendered
'''


def replace_function(
    path: Path,
    function_name: str,
    new_source: str,
) -> None:
    text = path.read_text(
        encoding="utf-8"
    )
    marker = (
        "def "
        + function_name
        + "("
    )
    start = text.find(
        marker
    )
    if start < 0:
        raise SystemExit(
            f"function not found: {function_name}"
        )

    next_start = text.find(
        "\ndef ",
        start + len(marker),
    )
    if next_start < 0:
        end = len(
            text
        )
    else:
        end = (
            next_start
            + 1
        )

    path.write_text(
        (
            text[
                :start
            ]
            + new_source.rstrip()
            + "\n\n"
            + text[
                end:
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    BACKUP.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        TEST,
        BACKUP / TEST.name,
    )

    replace_function(
        TEST,
        "test_phase157_r20_reference_dependencies_are_recovered_from_graph",
        NEW_TEST,
    )

    print(
        "Phase 159 R1-7c R4 generator canonicalization repair1 fix2 applied."
    )
    print(
        "Production code changes: none"
    )
    print(
        "Updated stale explicit-marker expectation in "
        "tests/test_phase157_r20_generic_dependency_rendering.py"
    )


if __name__ == "__main__":
    main()
