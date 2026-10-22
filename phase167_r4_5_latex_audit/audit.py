from __future__ import annotations

import json
from pathlib import Path

from web_group_proof import build_standard_web_group_proof_view


GROUPS = ((2, 1), (3, 1), (4, 1), (5, 1), (6, 1))
OUTPUT = Path("phase167_r4_5_latex_audit_results")


def validate_latex(latex: str) -> list[str]:
    issues = []
    braces = []
    escaped = False
    for offset, char in enumerate(latex):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "{":
            braces.append(offset)
        elif char == "}":
            if braces:
                braces.pop()
            else:
                issues.append(f"unmatched closing brace at {offset}")
    if braces:
        issues.append(f"{len(braces)} unmatched opening brace(s)")
    if escaped:
        issues.append("trailing backslash")
    for token in (r"\begin{", r"\end{"):
        if latex.count(token) != latex.count(r"\end{" if token == r"\begin{" else r"\begin{"):
            issues.append("unbalanced begin/end environment count")
            break
    if latex.count(r"\left") != latex.count(r"\right"):
        issues.append("unbalanced left/right")
    if "\x00" in latex:
        issues.append("NUL character in LaTeX")
    return list(dict.fromkeys(issues))


def collect() -> list[dict]:
    OUTPUT.mkdir(exist_ok=True)
    reports = []
    for n, k in GROUPS:
        name = f"pi{n+k}_{n}"
        view = build_standard_web_group_proof_view(
            n, k, max_depth=2, mode="narrative"
        )
        lines = []
        problems = []
        for number, line in enumerate(view.rendered_lines, 1):
            record = {
                "line": number,
                "kind": line.kind,
                "prefix": line.prefix,
                "statement_latex": line.statement_latex,
                "suffix": line.suffix,
                "segments": [
                    {"kind": segment.kind, "value": segment.value}
                    for segment in line.segments
                ],
            }
            lines.append(record)
            candidates = (
                [("statement_latex", line.statement_latex)]
                if line.statement_latex is not None else []
            )
            candidates += [
                (f"segment[{i}]", segment.value)
                for i, segment in enumerate(line.segments)
                if segment.kind in ("inline_math", "display_math")
            ]
            for field, latex in candidates:
                for message in validate_latex(latex):
                    problems.append({
                        "line": number, "field": field,
                        "issue": message, "latex": latex,
                    })
        (OUTPUT / f"{name}.json").write_text(
            json.dumps(lines, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        report = {"group": name, "line_count": len(lines),
                  "latex_fields_checked": sum(
                      (line["statement_latex"] is not None)
                      + sum(s["kind"] in ("inline_math", "display_math")
                            for s in line["segments"]) for line in lines),
                  "issues": problems}
        reports.append(report)
        print(f"{name}: {len(lines)} lines, {len(problems)} syntactic warnings")
    (OUTPUT / "report.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Audit files:", OUTPUT.resolve())
    print("NOTE: static syntactic audit only; visual/math semantics need inspection.")
    return reports


if __name__ == "__main__":
    collect()
