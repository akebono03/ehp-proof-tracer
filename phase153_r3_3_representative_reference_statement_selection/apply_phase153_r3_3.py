from pathlib import Path
import shutil


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
PAYLOAD_ROOT = PACKAGE_ROOT / "payload"

TARGETS = (
    (
        PAYLOAD_ROOT / "toda_group_proof_narrative_references.py",
        REPO_ROOT / "toda_group_proof_narrative_references.py",
    ),
    (
        PAYLOAD_ROOT
        / "tests"
        / "test_phase153_r3_3_reference_statement_selection.py",
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_3_reference_statement_selection.py",
    ),
)


def main() -> int:
    for source, target in TARGETS:
        if not source.is_file():
            raise FileNotFoundError(
                "payload file not found: "
                + str(source)
            )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.copyfile(
            source,
            target,
        )
        print(
            "updated: "
            + str(
                target.relative_to(
                    REPO_ROOT
                )
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
