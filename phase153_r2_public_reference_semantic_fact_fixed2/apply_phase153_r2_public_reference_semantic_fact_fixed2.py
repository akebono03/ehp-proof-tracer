from pathlib import Path


TEST = Path(
    "tests/test_phase153_r2_public_reference_semantic_fact.py"
)


def main() -> int:
    text = TEST.read_text(
        encoding="utf-8"
    )

    old = '''def test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "[R1]を用いる。" in rendered
  assert (
    "Toda Proposition 5.8 finite-dimensional integration"
    not in rendered
  )
'''

    new = '''def test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "Toda Proposition 5.8を用いる。" in rendered
  assert (
    "Toda Proposition 5.8 finite-dimensional integration"
    not in rendered
  )
'''

    if new in text and old not in text:
        print(
            "Focused test repair Fixed2: already applied"
        )
        return 0

    if old not in text:
        raise RuntimeError(
            "expected Fixed1 test function was not found"
        )

    if text.count(old) != 1:
        raise RuntimeError(
            "expected Fixed1 test function is not unique"
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
        "Focused test repair Fixed2 applied:"
    )
    print(
        "  root theorem declaration is the public body contract"
    )
    print(
        "  [R1] remains in the reference section"
    )
    print(
        "  provenance-only internal label remains hidden"
    )
    print(
        "Production changes: none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
