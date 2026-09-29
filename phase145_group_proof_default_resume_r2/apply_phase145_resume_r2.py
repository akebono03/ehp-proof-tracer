from pathlib import Path
import re


def main():
    path = Path("tests/test_phase131_5_web_group_proof.py")
    text = path.read_text(encoding="utf-8")

    function_name = "test_phase131_5_group_proof_post_keeps_result_and_shows_proof"
    pattern = re.compile(
        rf"^def {re.escape(function_name)}\\([\\s\\S]*?(?=^def |\\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if match is None:
        raise RuntimeError(f"{path}: target function not found")

    function_text = match.group(0)
    explicit_line = '          "group_proof_mode": "trace",\\n'

    if explicit_line in function_text:
        print("already applied: explicit Web trace mode")
        return

    old = '          "group_proof_depth": "2",\\n'
    new = (
        '          "group_proof_depth": "2",\\n'
        '          "group_proof_mode": "trace",\\n'
    )
    if function_text.count(old) != 1:
        raise RuntimeError(
            f"{path}: expected one group_proof_depth entry in {function_name}"
        )

    new_function = function_text.replace(old, new, 1)
    path.write_text(
        text[:match.start()] + new_function + text[match.end():],
        encoding="utf-8",
    )

    print("Phase 145 Resume R2 apply: PASS")
    print("Changed only the failing legacy Web test.")
    print("Added explicit group_proof_mode=trace.")
    print("Production changes in R2: none")


if __name__ == "__main__":
    main()
