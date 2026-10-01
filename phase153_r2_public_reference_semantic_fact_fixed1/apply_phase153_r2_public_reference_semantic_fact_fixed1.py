from pathlib import Path


TEST = Path(
    "tests/test_phase153_r2_public_reference_semantic_fact.py"
)


def main() -> int:
    text = TEST.read_text(
        encoding="utf-8"
    )

    old = '  assert "まず、[R1]を用いる。" in rendered\n'
    new = '  assert "[R1]を用いる。" in rendered\n'

    if new in text and old not in text:
        print(
            "Focused test repair: already applied"
        )
        return 0

    if old not in text:
        raise RuntimeError(
            "expected Phase153-R2 focused test assertion "
            "was not found"
        )

    if text.count(old) != 1:
        raise RuntimeError(
            "expected focused test assertion is not unique"
        )

    TEST.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )

    print(
        "Focused test repair applied:"
    )
    print(
        "  removed dependency on premise lead 'まず'"
    )
    print(
        "  kept semantic contract '[R1]を用いる。'"
    )
    print(
        "Production changes: none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
