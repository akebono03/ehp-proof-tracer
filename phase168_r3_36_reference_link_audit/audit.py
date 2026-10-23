"""R3-36: read-only inspection of proof-to-reference linkage."""
from __future__ import annotations

import ast
import json
from pathlib import Path

TARGETS = {
    "phase168_r3_3_proof_narrative_model.py": ("build_proof_narrative_model",),
    "phase168_r3_4_link_bridge.py": ("build_linked_proof_narrative_model",),
    "phase163_r4_r12_stable_bases.py": ("register_stable_minimal_dimensions",),
    "unified_statement_registry.py": ("AssertionEntry", "ProofStepLink"),
}
SEARCH_WORDS = (
    "Toda45IsomorphismStatement",
    "toda_45_generic_finite_cyclic_transport_inference_rule",
    "stable-base:1-stem:pi4_3_group_relation",
    "boundary:Proposition 5.1:higher_eta_group_relation",
)


def inspect_file(path: Path, names: tuple[str, ...]) -> dict:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    definitions = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in names:
            definitions.append({"name": node.name, "first_line": node.lineno, "last_line": node.end_lineno})
    return {"path": path.name, "definitions": definitions,
            "missing_definitions": sorted(set(names) - {d["name"] for d in definitions})}


def audit_repository(root: Path) -> dict:
    missing = [name for name in TARGETS if not (root / name).is_file()]
    if missing:
        raise FileNotFoundError("Required source files absent: " + ", ".join(missing))
    inspected = [inspect_file(root / name, names) for name, names in TARGETS.items()]
    occurrences = []
    for path in sorted(root.glob("*.py")):
        if path.name.startswith("test_"):
            continue
        source = path.read_text(encoding="utf-8-sig", errors="replace")
        for line_no, line in enumerate(source.splitlines(), 1):
            for word in SEARCH_WORDS:
                if word in line:
                    occurrences.append({"path": path.name, "line": line_no,
                                        "token": word, "source": line.strip()[:240]})
    model = (root / "phase168_r3_3_proof_narrative_model.py").read_text(encoding="utf-8-sig")
    adapter = (root / "phase168_r3_4_link_bridge.py").read_text(encoding="utf-8-sig")
    base = (root / "phase163_r4_r12_stable_bases.py").read_text(encoding="utf-8-sig")
    checks = {
        "model_uses_exact_step_equality": "link.step != step" in model,
        "model_allows_inference_only_citation": "located.append((rule_reference, None, None))" in model,
        "adapter_filters_used_given_steps": "used_given_steps" in adapter,
        "pi43_base_is_proof_internal": "origin=AssertionOrigin.PROOF_INTERNAL" in base,
        "pi43_base_depends_on_prop51_general": "dependencies=(GENERAL_ID_1,)" in base,
    }
    return {"mode": "AUDIT_ONLY", "targets": inspected, "checks": checks,
            "occurrences": occurrences,
            "next_checks": [
                "Compare the actual pi5^4 ProofStep values to bridge.proof_links, without matching by display name.",
                "Distinguish general Toda(4.5) assertion from its n=3,m=4,k=1 instantiation.",
                "Inspect registry AssertionOrigin and dependencies before constructing Reference body.",
                "Compare actual rendered Reference contents with the fixed baseline after a separate patch.",
            ]}


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "output" / "audit.json")
    args = parser.parse_args()
    report = audit_repository(args.root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("AUDIT_ONLY: no repository files modified")
    print("CHECKS:", report["checks"])
    print("OCCURRENCES:", len(report["occurrences"]))
    print("REPORT:", args.output.resolve())


if __name__ == "__main__":
    main()
