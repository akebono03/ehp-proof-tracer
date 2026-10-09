"""Phase 162 R9: read-only proof ancestry and narrative provenance audit.

No repository files or ProofStep objects are modified.
"""

from collections import Counter
from pathlib import Path
import json
import re

from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from proof import ProofRule
from toda_group_proof_narrative_transport_facts import extract_suspension_transport_facts
from toda_group_proof_narrative_transport_link import render_suspension_transport_link
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from web_group_proof import _group_proof_statement_latex


ISSUES = {
    "unrelated_H_pi3": (r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}", "H(π3²→π3³): unrelated map"),
    "unrelated_E_pi3": (r"E: \\pi_{3}^{2} \\to \\pi_{4}^{3}", "E(π3²→π4³): ancillary suspension"),
    "wrong_kernel_context": (r"\\ker E=\\operatorname{Im}Δ=\\mathbb{Z}", "ker E / Im Δ claim: inspect map context"),
    "symbolic_stable": (r"\\pi_{n + 1}^{n}", "symbolic stable family in pi5³ output"),
    "stable_tail": ("証明木に記録された群構造の移送について", "stable transport appended narrative"),
    "eta_tautology": (r"\\eta_{3} = \\eta_{3}", "eta3 tautology"),
    "eta_composition": (r"\\eta_{3}\\eta_{3} = \\eta_{3}^{2}", "eta3 eta3 expression"),
    "delta_iota5": (r"\\Delta\\left(\\iota_{5}\\right)", "delta(iota5) repetitions"),
}


def walk(root):
    seen = set()
    stack = [(root, 0, "root")]
    while stack:
        step, depth, path = stack.pop()
        if id(step) in seen:
            continue
        seen.add(id(step))
        yield step, depth, path
        for i in reversed(range(len(step.premises))):
            stack.append((step.premises[i], depth + 1, f"{path}/{i + 1}"))


def step_record(step, depth, path):
    latex, fallback = _group_proof_statement_latex(step.conclusion)
    return {
        "path": path,
        "depth": depth,
        "id": id(step),
        "rule": step.rule.name if isinstance(step.rule, ProofRule) else str(step.rule),
        "premises": len(step.premises),
        "type": type(step.conclusion).__name__,
        "latex": latex,
        "fallback": fallback,
    }


def analyze():
    replay = build_phase162_pi5_3_web_replay(max_depth=40)
    root = replay.root_step
    presentation = build_toda_group_proof_presentation(replay)
    if presentation.root_step is not root:
        raise AssertionError("The reconstructed root was replaced")
    markdown = render_toda_group_proof_narrative_markdown(presentation)
    records = [step_record(s, d, p) for s, d, p in walk(root)]
    facts = extract_suspension_transport_facts(root)
    tail = render_suspension_transport_link(root, lambda s: _group_proof_statement_latex(s.conclusion)[0])
    clauses = [x.strip() for x in markdown.split("## 証明\n", 1)[-1].split("\n\n") if x.strip()]
    occurrences = {}
    for key, (needle, meaning) in ISSUES.items():
        marked = [i + 1 for i, c in enumerate(clauses) if needle in c]
        matches = [r for r in records if needle in (r["latex"] or "")]
        occurrences[key] = {
            "description": meaning,
            "paragraph_numbers": marked,
            "tree_node_count_containing_exact_fragment": len(matches),
            "tree_paths_containing_exact_fragment": [r["path"] for r in matches[:15]],
        }
    return {
        "root": root,
        "presentation": presentation,
        "markdown": markdown,
        "records": records,
        "clauses": clauses,
        "issues": occurrences,
        "facts": facts,
        "rendered_tail": tail,
    }


def report(audit):
    records = audit["records"]
    out = [
        "# Phase 162 R9 — π₅³ 証明木と表示の出所監査",
        "",
        "**監査のみ。証明木・Renderer・Web のコードは変更しない。**",
        "",
        f"- Root preserved: {audit['presentation'].root_step is audit['root']}",
        f"- Unique ancestor ProofSteps: {len(records)}",
        f"- Presentation nodes: {len(audit['presentation'].nodes)}",
        f"- Narrative paragraphs: {len(audit['clauses'])}",
        "- Report meanings: 'tree matches' are exact rendered fragments, not proof validity judgments.",
        "",
        "## 1. 最終結論からの直接依存",
        "",
    ]
    for r in records:
        if r["depth"] <= 2:
            out.append(f"- `{r['path']}` depth={r['depth']}, `{r['rule']}`, `{r['type']}`, premises={r['premises']}: `{r['latex'] or r['fallback']}`")
    out.extend(["", "## 2. 問題のある文章の出所候補", ""])
    for name, item in audit["issues"].items():
        out.append(f"### {name}")
        out.append(f"- 概要: {item['description']}")
        out.append(f"- 本文段落番号: {item['paragraph_numbers']}")
        out.append(f"- 証明木の数式に同一断片を含むノード数: {item['tree_node_count_containing_exact_fragment']}")
        out.append(f"- 該当する最初の経路: {item['tree_paths_containing_exact_fragment']}")
        out.append("")
    out.extend(["## 3. Stable transport の抽出元", ""])
    facts = audit["facts"]
    out.append(f"- `extract_suspension_transport_facts(root)` 結果: {'FOUND' if facts else 'NONE'}")
    if facts:
        by_id = {r["id"]: r for r in records}
        for name in ("source_group_step", "isomorphism_step", "transported_group_step", "generator_bridge_step"):
            step = getattr(facts, name)
            r = by_id.get(id(step))
            out.append(f"- `{name}`: path={r['path'] if r else 'not in ancestry'}; `{_group_proof_statement_latex(step.conclusion)[0]}`")
    out.append(f"- `render_suspension_transport_link` returned text: {bool(audit['rendered_tail'])}")
    out.extend(["", "## 4. 証明木の全ノード（経路・型・式）", ""])
    for r in records:
        out.append(f"- `{r['path']}` [{r['rule']}] {r['type']}: `{r['latex'] or r['fallback']}`")
    out.extend(["", "## 5. 本文段落", ""])
    for i, paragraph in enumerate(audit["clauses"], 1):
        out.append(f"{i}. {paragraph.replace(chr(10), ' ')[:700]}")
    out.extend(["", "## 6. 今後の判断", "", "- 子孫にあるという理由だけで既知結果を Reference や本文に採用してよいわけではない。", "- 次の修正では根の直接依存・必要な EHP 導出・内部補助導出を区別する。", "- 意味の異なる完全列を文字列一致だけで統合しない。", ""])
    return "\n".join(out)


def main():
    audit = analyze()
    output = Path(__file__).resolve().parent / "audit_output"
    output.mkdir(exist_ok=True)
    (output / "provenance.md").write_text(report(audit), encoding="utf-8")
    (output / "narrative.md").write_text(audit["markdown"], encoding="utf-8")
    data = {
        "nodes": audit["records"],
        "issues": audit["issues"],
        "transport_facts_found": audit["facts"] is not None,
        "transport_tail_rendered": bool(audit["rendered_tail"]),
    }
    (output / "provenance.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Root preserved: {audit['presentation'].root_step is audit['root']}")
    print(f"Ancestor steps: {len(audit['records'])}; narrative paragraphs: {len(audit['clauses'])}")
    for key, item in audit["issues"].items():
        print(f"{key}: paragraphs={item['paragraph_numbers']}, tree_matches={item['tree_node_count_containing_exact_fragment']}")
    print("Audit output:", output / "provenance.md")
    print("Read-only R9 audit completed. Full suite not run.")


if __name__ == "__main__":
    main()
