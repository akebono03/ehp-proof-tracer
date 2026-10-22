from __future__ import annotations

import json
from pathlib import Path

from web_group_proof import build_standard_web_group_proof_view

TARGETS = ((2, 1), (3, 1), (4, 1), (5, 1), (6, 1))


def line_text(line) -> str:
    if line.segments:
        return "".join(segment.value for segment in line.segments)
    return line.prefix + (line.statement_latex or "") + line.suffix


def audit_one(n: int, k: int) -> dict:
    view = build_standard_web_group_proof_view(n, k, max_depth=2, mode="narrative")
    lines = [line_text(line) for line in view.rendered_lines]
    name = f"pi{n+k}_{n}"
    output_dir = Path("phase167_r4_4_order_audit_results")
    output_dir.mkdir(exist_ok=True)
    (output_dir / f"{name}.txt").write_text(
        "\n".join(f"{i:03d} {line}" for i, line in enumerate(lines, 1)) + "\n",
        encoding="utf-8",
    )
    result = {"group": name, "line_count": len(lines), "violations": [], "not_observed": []}
    if (n, k) == (3, 1):
        # Only check what the public display actually makes observable.
        # This is not a complete ProofStep DAG-order proof.
        checks = (
            (r"\operatorname{Im}\Delta", r"\ker E", "image before kernel"),
            (r"\ker E", "は全射", "kernel before surjectivity"),
            ("は全射", "準同型定理", "surjectivity before quotient theorem"),
            ("準同型定理", "以上より", "quotient theorem before final conclusion"),
        )
        for left, right, label in checks:
            a = [i for i, line in enumerate(lines) if left in line]
            b = [i for i, line in enumerate(lines) if right in line]
            if not a or not b:
                result["not_observed"].append({"check": label, "left": a, "right": b})
            elif min(a) >= max(b):
                result["violations"].append({"check": label, "left": a, "right": b})
    return result


def main() -> int:
    records = [audit_one(n, k) for n, k in TARGETS]
    output_dir = Path("phase167_r4_4_order_audit_results")
    (output_dir / "report.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for r in records:
        print(f'{r["group"]}: {r["line_count"]} lines, '
              f'{len(r["violations"])} order violations, '
              f'{len(r["not_observed"])} unobserved checks')
    if any(r["violations"] or r["not_observed"] for r in records):
        print("AUDIT_INCOMPLETE_OR_FAILED: inspect report.json")
        return 1
    print("DISPLAY_ORDER_AUDIT_PASSED: limited visible checks only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
