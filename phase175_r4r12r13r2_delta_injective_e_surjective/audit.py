"""Isolated Phase 175 R13R2 arithmetic and source-boundary audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import e_surjective_inputs


def run(root: Path, dry_run: bool) -> int:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                            text=True, capture_output=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R13R2 requires develop")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          text=True, capture_output=True, check=True).stdout.strip()
    signed = canonical_toda58()
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    required = e_surjective_inputs(goal)
    if required is None or required[0].map != signed.map:
        raise RuntimeError("Toda (5.8) Delta is not the EHP Delta target")
    report = {
        "phase": "175-R4R12R13R2", "dry_run": dry_run, "head": head,
        "gate": "PASS_R13R2_ISOLATED_RULES_NOT_PUBLIC_NOT_COMPLETE",
        "new_given": 0, "new_mathematical_rules": 2,
        "production_changes": [], "full_pytest_executed": False,
        "public_provider_connected": False, "target_proof_complete": False,
        "delta": repr(signed.map),
        "exactness": [repr(x) for x in required[1:]],
    }
    output = root / "phase175_r4r12r13r2_delta_injective_e_surjective" / "output"
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("gate", "head", "new_given", "public_provider_connected", "target_proof_complete"):
        print("PHASE175_R13R2_" + key.upper() + "=" + str(report[key]))
    print("PHASE175_R13R2_REPORT=" + str(output / "report.json"))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
