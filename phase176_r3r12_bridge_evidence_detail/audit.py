"""Read-only detailed evidence audit of the R3R10/R3R11 hand-off."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Any

GUARD_TERMS = (
    ("screened_general_law", "screened_general_law(bridge)"),
    ("exactly_one_source_law", "len(laws) != 1"),
    ("typed_suspension", "valid_suspension(goal.map)"),
    ("zero_target", "isinstance(goal.target_generator, Zero)"),
    ("lifted_stable_composition", "lifted_stable_composition(goal.source_generator)"),
    ("typed_composition_factors", "typed_composition_factors(lifted)"),
    ("canonical_annihilator_instance", "canonical_annihilator_instance(laws[0], factors[0].dimension)"),
    ("exact_relation_match", "cited_relation != Relation(lifted, Zero(), RelationType.EQUALITY)"),
    ("two_premise_rule", "expand_proved_composite_zero_image(goal, image)"),
)


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"report root is not a dict: {path}")
    return data


def flatten(value: Any, prefix: str = "", depth: int = 0) -> list[dict[str, Any]]:
    """Retain exact paths to primitive fields, without guessing schemas."""
    if depth > 24:
        return []
    if isinstance(value, dict):
        return [record for k, v in value.items()
                for record in flatten(v, f"{prefix}.{k}" if prefix else str(k), depth + 1)]
    if isinstance(value, list):
        return [record for index, v in enumerate(value)
                for record in flatten(v, f"{prefix}[{index}]", depth + 1)]
    if value is None or isinstance(value, (str, bool, int, float)):
        return [{"path": prefix, "value": value}]
    return []


def selected(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tokens = ("observed", "step", "conclusion", "premise", "candidate", "goal",
              "generator", "relation", "reference", "source", "law", "rule",
              "zero", "shared", "isolated", "status", "inferred", "provider")
    return [r for r in records if any(t in r["path"].lower() for t in tokens)]


def evaluate_static_guards(provider_text: str) -> dict[str, bool]:
    return {name: marker in provider_text for name, marker in GUARD_TERMS}


def audit(root: Path, previous10: Path, previous11: Path) -> dict[str, Any]:
    r10 = read_json(previous10)
    r11 = read_json(previous11)
    provider = root / "phase175_r4r14r5_public_zero_transport" / "provider.py"
    source = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    guards = evaluate_static_guards(provider.read_text(encoding="utf-8-sig"))
    registration = "build_public_composite_zero_transport_provider(bridge)" in source
    subprocess_result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if subprocess_result.returncode:
        raise RuntimeError(subprocess_result.stderr)
    records10 = flatten(r10)
    records11 = flatten(r11)
    relevant10 = selected(records10)
    relevant11 = selected(records11)
    # A truthful boundary: saved console counts and static scans cannot establish
    # why runtime provider guards rejected an exact object without typed evaluation.
    return {
        "phase": 176, "stage": "R3R12", "kind": "READ_ONLY_EVIDENCE_DETAIL",
        "git_head": subprocess_result.stdout.strip(),
        "r3r10_path": str(previous10), "r3r11_path": str(previous11),
        "r3r10_top_level_keys": list(r10), "r3r11_top_level_keys": list(r11),
        "r3r10_observed_payload": r10.get("observed"),
        "r3r10_selected_scalar_records": relevant10,
        "r3r11_selected_scalar_records": relevant11,
        "r3r10_scalar_record_count": len(records10),
        "r3r11_scalar_record_count": len(records11),
        "static_provider_guard_inventory": guards,
        "shared_registration_present": registration,
        "bridge_cause_confirmed": False,
        "reason": "Typed runtime goals, screened source law and individual guard outcomes have not been compared in this stage.",
        "new_given": 0, "new_math_rules": 0, "production_changes": 0,
        "full_pytest": "NOT_RUN",
        "gate": "PASS_R3R12_EVIDENCE_EXTRACTED_CAUSE_OPEN" if all(guards.values()) and registration else "FAIL_R3R12_SOURCE_GUARD",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, type=Path)
    p.add_argument("--previous10", required=True, type=Path)
    p.add_argument("--previous11", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    report = audit(args.root.resolve(), args.previous10.resolve(), args.previous11.resolve())
    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(f"PHASE176_R3R12_GATE={'PASS_R3R12_READ_ONLY_DRYRUN' if args.dry_run and report['gate'].startswith('PASS') else report['gate']}")
    print(f"PHASE176_R3R12_HEAD={report['git_head']}")
    print(f"PHASE176_R3R12_STATIC_GUARDS={sum(report['static_provider_guard_inventory'].values())}/{len(report['static_provider_guard_inventory'])}")
    print(f"PHASE176_R3R12_R10_OBSERVED={json.dumps(report['r3r10_observed_payload'], ensure_ascii=False, default=str)}")
    print(f"PHASE176_R3R12_R10_RELEVANT={len(report['r3r10_selected_scalar_records'])}")
    for record in report['r3r10_selected_scalar_records']:
        value = str(record['value']).replace('\n', ' ')
        print(f"EVIDENCE_R10 {record['path']} = {value[:300]}")
    print(f"PHASE176_R3R12_BRIDGE_CAUSE_CONFIRMED=False")
    print(f"PHASE176_R3R12_REPORT={args.output}")
    print("PHASE176_R3R12_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report['gate'].startswith('PASS') else 1


if __name__ == "__main__":
    raise SystemExit(main())
