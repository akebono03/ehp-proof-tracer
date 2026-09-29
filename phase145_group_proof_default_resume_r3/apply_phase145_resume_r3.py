from pathlib import Path


def main():
    path = Path("tests/test_phase131_5_web_group_proof.py")
    text = path.read_text(encoding="utf-8")

    marker = "def test_phase131_5_group_proof_post_keeps_result_and_shows_proof():"
    next_marker = "\ndef "
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"{path}: target test function not found")

    end = text.find(next_marker, start + len(marker))
    if end < 0:
        end = len(text)

    function_text = text[start:end]

    explicit = (
        '      "group_proof_depth": "2",\n'
        '      "group_proof_mode": "trace",\n'
    )
    legacy = '      "group_proof_depth": "2",\n'

    if explicit in function_text:
        print("already applied: explicit group_proof_mode=trace")
        return

    if function_text.count(legacy) != 1:
        raise RuntimeError(
            f"{path}: expected exactly one legacy depth entry in target test"
        )

    new_function = function_text.replace(legacy, explicit, 1)
    path.write_text(
        text[:start] + new_function + text[end:],
        encoding="utf-8",
    )

    print("Phase 145 Resume R3 apply: PASS")
    print("Changed only:")
    print(
        "  tests/test_phase131_5_web_group_proof.py::"
        "test_phase131_5_group_proof_post_keeps_result_and_shows_proof"
    )
    print("Added explicit group_proof_mode=trace.")
    print("Production changes in R3: none")


if __name__ == "__main__":
    main()
