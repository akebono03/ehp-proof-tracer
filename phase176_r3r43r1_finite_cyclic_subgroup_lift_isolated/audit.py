"""Check the reviewed API baseline; never run public proof search."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
REVIEWED_HEAD = "a9225ddbbed20fd350d4cdf2f3dd68fdcb598f93"
PINS = {
    'phase175_r3_pi73_hopf_lift/rule.py': '9457cece2b7f3ff7eb1b756296225c0ee0516897',
    'phase175_r3_pi73_hopf_lift/tests/test_rule.py': 'cf61613fedf68060271307d060067d9a55e3718c',
    'phase165_r12_r2_quotient_rules.py': '2b3e8e0449382e9245ee22f08501e9cede0a5b59',
    'phase165_r12_r12_ehp_consequences.py': '895dc98ad4d25f14fb7aac8fa52460a77fd049bc',
    'phase165_r12_r11_prop42_unified.py': '79752ec035244677ff6a54debff312e87a76fbf2',
    'phase165_r14_r6_generic_iso.py': '8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7',
    'phase171_r2j_r2_cyclic_hopf_surjective/source.py': 'ebe53bc49872bd12b8c6eb0649e853726d7d45fe',
    'phase165_r52_r9_shared_math.py': '165f2d0ad78e0dcb05d01ec0784b974a92c5ee02',
    'phase176_r3r42_root_backward_frontier_audit/audit.py': '7e8d68768214d678b87cbf4541c4f5e7bbe3e69e',
    'phase176_r3r42_root_backward_frontier_audit/tests/test_audit.py': 'd7f5d82db290d4f669775983166e3a577e40090c',
    'proof.py': '2eb683053eaf7146bd89afbc581a386af08b8060',
    'homotopy_groups.py': '883faf1b4a067485c9127f14dbb575aaa195960e',
    'expression.py': '7f7cd97468cd753643369f54774ee9892968c345',
    'phase165_r3_recursive_search.py': '06009bfcf57f99cac58c229d99c53f16324692d0',
    'map_facts.py': '86fbf404783e15d344595bf54df5a9a8bafc35fc',
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True,
                                   encoding="utf-8", errors="replace").strip()


def source_guard() -> str:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("TRACKED_WORKTREE_NOT_CLEAN")
    for path, expected in PINS.items():
        actual = git("rev-parse", f"HEAD:{path}")
        if actual != expected:
            raise RuntimeError(f"REVIEWED_SOURCE_CHANGED: {path}: {actual} != {expected}")
        ast.parse((ROOT / path).read_text(encoding="utf-8-sig"), filename=path)
    for path in Path(__file__).resolve().parent.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    return git("rev-parse", "HEAD")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head = source_guard()
    from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME
    if not RULE_NAME:
        raise RuntimeError("RULE_IMPORT_FAILED")
    if source_guard() != head:
        raise RuntimeError("HEAD_CHANGED_DURING_AUDIT")
    print("PHASE176_R3R43R1_HEAD=" + head)
    print("PHASE176_R3R43R1_REVIEWED_HEAD=" + REVIEWED_HEAD)
    print("PHASE176_R3R43R1_PINNED_FILES=" + str(len(PINS)))
    print("PHASE176_R3R43R1_GATE=" + ("PASS_R3R43R1_DRYRUN" if args.dry_run else "PASS_R3R43R1_SOURCE_GUARD"))
    print("PHASE176_R3R43R1_PUBLIC_CONNECTION=NOT_DONE")
    print("PHASE176_R3R43R1_ROOT_PROVED=NOT_CLAIMED")
    print("PHASE176_R3R43R1_NEW_GIVEN=0")
    print("PHASE176_R3R43R1_FULL_PYTEST=NOT_RUN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
