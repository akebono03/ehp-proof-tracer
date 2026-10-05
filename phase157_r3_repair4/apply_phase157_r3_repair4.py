from pathlib import Path

FILES = (
    Path("tests/test_phase157_r3_pi6_3_reference_boundary.py"),
    Path("tests/test_phase157_r3_repair3_recursive_internal_recovery.py"),
)

OLD = r"E: \pi_{4}^{2} \xrightarrow{\cong} \pi_{5}^{3}"
NEW = r"E: \pi_{4}^{2} \to \pi_{5}^{3}"


def main():
    for path in FILES:
        if not path.exists():
            raise SystemExit(f"test file not found: {path}")

        text = path.read_text(encoding="utf-8")

        if OLD not in text:
            raise SystemExit(
                f"expected old renderer form not found in {path}"
            )

        text = text.replace(
            OLD,
            NEW,
        )

        path.write_text(
            text,
            encoding="utf-8",
            newline="\n",
        )
        print(f"updated: {path.resolve()}")

    print("Production code changes: none")


if __name__ == "__main__":
    main()
