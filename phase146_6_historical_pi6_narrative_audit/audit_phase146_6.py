from __future__ import annotations

import difflib
from pathlib import Path
import re
import sys


HISTORICAL_COMMIT = "908e24db89669750949fa9ad149f5e306ac05546"
MATH_RE = re.compile(r"\$|\\\[|\\\]|\\pi_|\\eta_|\\nu|\\Delta|\\xrightarrow|\\longrightarrow")


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def _nonempty_lines(text: str) -> tuple[str, ...]:
    return tuple(line.strip() for line in text.splitlines() if line.strip())


def _math_lines(text: str) -> tuple[str, ...]:
    return tuple(line for line in _nonempty_lines(text) if MATH_RE.search(line))


def _ordered_unique(lines: tuple[str, ...]) -> tuple[str, ...]:
    seen = set()
    result = []
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        result.append(line)
    return tuple(result)


def _sample(label: str, rows: tuple[str, ...], limit: int = 12) -> None:
    print(f"{label}: {len(rows)}")
    for row in rows[:limit]:
        print(f"  {row}")
    if len(rows) > limit:
        print(f"  ... ({len(rows) - limit} more)")


def _contains(text: str, needle: str) -> bool:
    return needle in text


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: audit_phase146_6.py HISTORICAL_OUTPUT CURRENT_OUTPUT"
        )

    historical = _read(sys.argv[1])
    current = _read(sys.argv[2])

    old_lines = _nonempty_lines(historical)
    new_lines = _nonempty_lines(current)
    matcher = difflib.SequenceMatcher(
        a=old_lines,
        b=new_lines,
        autojunk=False,
    )

    old_math = _ordered_unique(_math_lines(historical))
    new_math = _ordered_unique(_math_lines(current))
    old_math_set = set(old_math)
    new_math_set = set(new_math)

    old_only_math = tuple(x for x in old_math if x not in new_math_set)
    new_only_math = tuple(x for x in new_math if x not in old_math_set)

    historical_contracts = (
        (
            "2eta3 before bracket",
            r"2\eta_{3}=0.",
            r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}.",
        ),
        (
            "membership",
            r"\nu'\in\pi_{6}^{3}.",
            None,
        ),
        (
            "Hopf image",
            r"H(\nu')=\eta_{5}.",
            None,
        ),
        (
            "double relation",
            r"2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5}=\eta_{3}^{3}.",
            None,
        ),
        (
            "EHP purpose",
            "$\\nu'$ の位数を決定するために, 次の EHP 完全列を考える.",
            None,
        ),
        (
            "short exact sequence",
            r"0\longrightarrow\pi_{5}^{2}\xrightarrow{E}\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}\longrightarrow 0.",
            None,
        ),
        (
            "final group",
            r"\pi_{6}^{3}=\mathbb{Z}/4\{\nu'\}",
            None,
        ),
    )

    print("=" * 78)
    print("Phase 146-6 Historical pi_6^3 Narrative vs Current Generic Audit")
    print(f"Historical baseline commit: {HISTORICAL_COMMIT}")
    print("Production changes: none")
    print("Existing test changes: none")
    print("=" * 78)
    print()
    print(f"exact text parity: {historical == current}")
    print(f"historical chars: {len(historical)}")
    print(f"current chars: {len(current)}")
    print(f"historical nonempty lines: {len(old_lines)}")
    print(f"current nonempty lines: {len(new_lines)}")
    print(f"line similarity ratio: {matcher.ratio():.4f}")
    print(
        "changed hunks: "
        + str(sum(tag != "equal" for tag, *_ in matcher.get_opcodes()))
    )
    print()
    _sample("historical-only math/formula lines", old_only_math)
    print()
    _sample("current-only math/formula lines", new_only_math)
    print()
    print("Historical semantic contract probes")
    print("-" * 78)
    for label, first, second in historical_contracts:
        old_first = _contains(historical, first)
        new_first = _contains(current, first)
        if second is None:
            print(
                f"{label}: historical={old_first} current={new_first}"
            )
            continue
        old_second = _contains(historical, second)
        new_second = _contains(current, second)
        old_order = (
            old_first
            and old_second
            and historical.index(first) < historical.index(second)
        )
        new_order = (
            new_first
            and new_second
            and current.index(first) < current.index(second)
        )
        print(
            f"{label}: historical={old_first and old_second}/{old_order} "
            f"current={new_first and new_second}/{new_order}"
        )

    diff_path = Path("phase146_6_historical_vs_current.diff")
    diff = difflib.unified_diff(
        historical.splitlines(),
        current.splitlines(),
        fromfile="historical_phase136_2_pi6_3.txt",
        tofile="current_generic_pi6_3.txt",
        lineterm="",
    )
    diff_path.write_text("\n".join(diff) + "\n", encoding="utf-8")
    print()
    print(f"Full unified diff written to: {diff_path}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
