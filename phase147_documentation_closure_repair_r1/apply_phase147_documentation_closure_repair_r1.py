from pathlib import Path


TARGETS = (
    Path("docs/development_log.md"),
    Path("docs/proof_records.md"),
)


def normalize_eof(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")

    text = path.read_text(encoding="utf-8")

    if not text.strip():
        raise SystemExit(f"refusing to normalize empty file: {path}")

    normalized = text.rstrip("\r\n") + "\n"
    path.write_text(normalized, encoding="utf-8")


def main() -> int:
    for path in TARGETS:
        normalize_eof(path)

    print("Phase 147 Documentation Closure Repair R1 applied.")
    print("Normalized EOF only:")
    print("  docs/development_log.md")
    print("  docs/proof_records.md")
    print("Unchanged:")
    print("  docs/roadmap.md")
    print("  README.md")
    print("  docs/design.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
