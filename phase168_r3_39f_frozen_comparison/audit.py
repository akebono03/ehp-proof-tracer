"""Read-only Phase 168 frozen narrative comparison, using the existing R3-38 capture."""
from __future__ import annotations

import json
import re
from pathlib import Path

from phase168_r3_38_frozen_fulltext_audit import audit as frozen

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1))


def compact(text: str) -> str:
    """Ignore layout whitespace only; retain mathematical symbols and source facts."""
    text = re.sub(r"\s+", "", text)
    return text.replace("$", "").replace(r"\left", "").replace(r"\right", "")


def assess(name: str, proof: str) -> list[dict[str, object]]:
    """Explicit benchmark wording checks, not a mathematical proof validator."""
    flat = compact(proof)
    if name == "pi3_2":
        requirements = (
            ("exactness_for_injectivity", "完全性より", r"H:\pi_{3}^{2}\to\pi_{3}^{3}", "は単射"),
            ("delta_image_kernel_zero", r"\operatorname{Im}", r"\kerE=0", ""),
            ("hopf_iso_from_bijectivity", "単射性と全射性より", "", ""),
            ("no_generic_circle_in_proof", "", "", ""),
        )
        # For the first check, compare the immediate logical statement, not an
        # unrelated reference to exactness elsewhere in the proof.
        indices = [line for line in proof.splitlines() if "は単射" in line and "H:" in line]
        injectivity = any("完全性より" in line for line in indices)
        delta = (r"\operatorname{Im}" in flat and r"\kerE=0" in flat)
        iso = "単射性と全射性より" in proof
        circle = not bool(re.search(r"\\pi_\{?i\}?\^\{?1\}?", flat))
        return [
            {"key": requirements[0][0], "present": injectivity, "why": "H の単射を完全性から導いたことを明記"},
            {"key": requirements[1][0], "present": delta, "why": r"Im Δ = ker E = 0 を明記"},
            {"key": requirements[2][0], "present": iso, "why": "H の同型性を単射性と全射性から説明"},
            {"key": requirements[3][0], "present": circle, "why": "基準にない一般円周公式の本文再掲がない"},
        ]
    if name == "pi4_3":
        lines = [line for line in proof.splitlines() if "は全射" in line and "E:" in line]
        return [
            {"key": "surjectivity_from_exactness", "present": any("完全性より" in line for line in lines), "why": "E の全射を完全性から導いたことを明記"},
            {"key": "kernel_presentation", "present": r"\kerE=" in flat and r"\mathbb{Z}" in flat, "why": "ker E の具体的な表示"},
            {"key": "quotient_theorem", "present": "準同型定理より" in proof, "why": "準同型定理を明記"},
            {"key": "diagonal_general_in_proof", "present": bool(re.search(r"\\pi_\{?n\}?\^\{?n\}?", flat)), "why": "基準にも存在する対角群の一般式"},
        ]
    if name == "pi5_4":
        match = re.search(r"\(n,m,k\)=\(3,4,1\)", flat)
        cited = re.search(r"\[R\d+\].{0,100}適用", proof)
        source = flat.find(r"\pi_{4}^{3}")
        image = flat.find(r"E(\eta_{3})=\eta_{4}")
        if image < 0:
            image = flat.find(r"E\eta_{3}=\eta_{4}")
        return [
            {"key": "toda45_explicit_substitution", "present": match is not None, "why": "(4.5) への (n,m,k)=(3,4,1) の代入"},
            {"key": "specialization_citation_in_proof", "present": cited is not None, "why": "(4.5) を引用して適用したことを明記"},
            {"key": "source_before_generator_image", "present": source >= 0 and image >= 0 and source < image, "why": "引用する群構造を生成元の像より先に示す"},
            {"key": "specific_map_isomorphism", "present": r"E:\pi_{4}^{3}\to\pi_{5}^{4}" in flat and "は同型" in proof, "why": "具体的な E 同型を表示"},
        ]
    raise ValueError("Unknown frozen comparison case: " + name)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    # Reuse the established capture/diff implementation without modifying it.
    frozen.OUT = OUTPUT
    rows = []
    for name, n, k in CASES:
        comparison = frozen.compare(name, n, k)
        current = (OUTPUT / f"{name}_current.md").read_text(encoding="utf-8")
        _, proof = frozen.sections(current)
        checks = assess(name, proof)
        rows.append({
            "name": name,
            "baseline_sha256": comparison["baseline_sha256"],
            "reference_diff_lines": comparison["comparison"]["reference"]["difference_line_count"],
            "proof_diff_lines": comparison["comparison"]["proof"]["difference_line_count"],
            "reference_bodies_complete": comparison["observations"]["all_reference_entries_have_body"],
            "benchmark_explanations": checks,
            "current_file": f"{name}_current.md",
            "reference_diff": f"{name}_reference.diff",
            "proof_diff": f"{name}_proof.diff",
            "references": comparison["reference_entries"],
        })
    summary = {
        "status": "AUDIT_ONLY",
        "comparison": "frozen original versus current common Web renderer",
        "cases": rows,
        "limitations": [
            "Reference numbering is not frozen by BASELINE_POLICY.md.",
            "Diff lines are textual differences, not a mathematical-error count.",
            "Explanatory checks assess benchmark wording, not mathematical validity.",
            "No source or frozen baseline files have been modified.",
            "Full pytest suite has not been run.",
        ],
    }
    (OUTPUT / "audit.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 168 R3-39F — 固定基準との全文監査", "", "監査専用。実装コード・固定基準は変更しない。", "", "| 群 | Reference 差分行 | 本文差分行 | 基準の説明項目 |", "|---|---:|---:|---|"]
    for row in rows:
        passed = sum(check["present"] for check in row["benchmark_explanations"])
        total = len(row["benchmark_explanations"])
        lines.append(f'| {row["name"]} | {row["reference_diff_lines"]} | {row["proof_diff_lines"]} | {passed}/{total} |')
    for row in rows:
        lines.extend(["", "## " + row["name"], ""])
        for check in row["benchmark_explanations"]:
            status = "一致" if check["present"] else "不足または順序差"
            lines.append(f'- **{status}** — {check["why"]} (`{check["key"]}`)')
        lines.append(f'- 全文差分: `{row["reference_diff"]}`, `{row["proof_diff"]}`')
    lines += ["", "## 監査上の注意", "", "- この項目数は固定基準の全文一致率を意味しない。", "- Reference 番号の違いだけでは不合格としない。", "- 不一致は数学的な誤りとは限らない。", "- 全体 pytest は実行しない。", ""]
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("REPORT:", OUTPUT / "audit.json")


if __name__ == "__main__":
    main()
