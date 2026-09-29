from __future__ import annotations

import difflib
from pathlib import Path
import re
import sys

HISTORICAL_COMMIT = "908e24db89669750949fa9ad149f5e306ac05546"


def read_utf8_strict(path: str) -> str:
    data = Path(path).read_bytes()
    return data.decode("utf-8", errors="strict")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def present(text: str, *fragments: str) -> bool:
    c = compact(text)
    return all(compact(fragment) in c for fragment in fragments)


def ordered(text: str, first: str, second: str) -> bool:
    c = compact(text)
    a = compact(first)
    b = compact(second)
    return a in c and b in c and c.index(a) < c.index(b)


def nonempty_lines(text: str) -> tuple[str, ...]:
    return tuple(x.strip() for x in text.splitlines() if x.strip())


def replacement_character_count(text: str) -> int:
    return text.count("\ufffd")


def mojibake_markers(text: str) -> tuple[str, ...]:
    markers = ("縺", "繧", "蜿", "荳", "譁", "螟", "髫")
    return tuple(marker for marker in markers if marker in text)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: audit_phase146_6_r1.py HISTORICAL CURRENT")

    historical = read_utf8_strict(sys.argv[1])
    current = read_utf8_strict(sys.argv[2])

    old_lines = nonempty_lines(historical)
    new_lines = nonempty_lines(current)
    matcher = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)

    contracts = (
        (
            "2eta3 present",
            lambda t: present(t, r"2\eta_{3}", "=0"),
        ),
        (
            "Toda bracket definition present",
            lambda t: present(
                t,
                r"\nu'",
                r"\{\eta_{3}",
                r"2\iota_{4}",
                r"\eta_{4}\}_{1}",
            ),
        ),
        (
            "2eta3 before Toda bracket",
            lambda t: ordered(t, r"2\eta_{3}=0", r"\nu'\in\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"),
        ),
        (
            "nu' membership",
            lambda t: present(t, r"\nu'", r"\in\pi_{6}^{3}"),
        ),
        (
            "Hopf image",
            lambda t: present(t, r"H", r"\nu'", "=", r"\eta_{5}"),
        ),
        (
            "double relation",
            lambda t: present(t, r"2\nu'", "=", r"\eta_{3}^{3}"),
        ),
        (
            "EHP purpose prose",
            lambda t: (
                "位数を決定するために" in t
                and "EHP 完全列" in t
            ),
        ),
        (
            "five-term EHP sequence",
            lambda t: present(
                t,
                r"\pi_{7}^{3}",
                r"\pi_{7}^{5}",
                r"\pi_{5}^{2}",
                r"\pi_{6}^{3}",
                r"\pi_{6}^{5}",
            ),
        ),
        (
            "short exact sequence",
            lambda t: present(
                t,
                r"0\longrightarrow",
                r"\pi_{5}^{2}",
                r"\xrightarrow{E}\pi_{6}^{3}",
                r"\xrightarrow{H}\pi_{6}^{5}",
                r"\longrightarrow0",
            ),
        ),
        (
            "final group",
            lambda t: present(t, r"\pi_{6}^{3}", r"\mathbb{Z}/4", r"\nu'"),
        ),
    )

    print("=" * 78)
    print("Phase 146-6-R1 Encoding-Safe Historical Narrative Audit")
    print(f"Historical baseline commit: {HISTORICAL_COMMIT}")
    print("Production changes: none")
    print("Existing test changes: none")
    print("=" * 78)
    print()
    print("Encoding integrity")
    print("-" * 78)
    print(f"historical UTF-8 strict decode: PASS")
    print(f"current UTF-8 strict decode: PASS")
    print(f"historical replacement characters: {replacement_character_count(historical)}")
    print(f"current replacement characters: {replacement_character_count(current)}")
    print(f"historical mojibake markers: {mojibake_markers(historical) or 'none'}")
    print(f"current mojibake markers: {mojibake_markers(current) or 'none'}")
    print()
    print("Text shape")
    print("-" * 78)
    print(f"exact text parity: {historical == current}")
    print(f"historical chars: {len(historical)}")
    print(f"current chars: {len(current)}")
    print(f"historical nonempty lines: {len(old_lines)}")
    print(f"current nonempty lines: {len(new_lines)}")
    print(f"line similarity ratio: {matcher.ratio():.4f}")
    print()
    print("Semantic contract matrix")
    print("-" * 78)
    lost = []
    gained = []
    preserved = []
    absent = []
    for label, predicate in contracts:
        old = bool(predicate(historical))
        new = bool(predicate(current))
        if old and new:
            status = "PRESERVED"
            preserved.append(label)
        elif old and not new:
            status = "LOST"
            lost.append(label)
        elif not old and new:
            status = "GAINED"
            gained.append(label)
        else:
            status = "ABSENT"
            absent.append(label)
        print(f"{label}: historical={old} current={new} -> {status}")

    print()
    print("Summary")
    print("-" * 78)
    print(f"preserved: {len(preserved)}")
    for x in preserved:
        print(f"  + {x}")
    print(f"lost: {len(lost)}")
    for x in lost:
        print(f"  - {x}")
    print(f"gained: {len(gained)}")
    for x in gained:
        print(f"  + {x}")
    print(f"absent in both: {len(absent)}")
    for x in absent:
        print(f"  = {x}")

    diff_path = Path("phase146_6_r1_historical_vs_current.diff")
    diff_path.write_text(
        "\n".join(
            difflib.unified_diff(
                historical.splitlines(),
                current.splitlines(),
                fromfile="historical_phase136_2_pi6_3.txt",
                tofile="current_pi6_3.txt",
                lineterm="",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    print()
    print(f"Full UTF-8 unified diff written to: {diff_path}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
