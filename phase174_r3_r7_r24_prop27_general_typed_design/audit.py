"""Source-first typed design audit for Toda Proposition 2.7.

No production inference rule, GIVEN, or certified ProofStep is created.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess

PHASE = "174-R3-R7-R24"
REVIEWED_HEAD = "5349f850428085a162f5b286deebfaa0bdcfb9d0"
ROOT = Path(__file__).resolve().parents[1]
SOURCE = "sources/toda/Toda_02_2.tex"
SECONDARY = "sources/toda/Toda_05_2.tex"
LEGACY_TEST = "tests/test_phase50_prop27_theorem_semantics.py"
GENERAL_EQUATION = r"H\!\bigl(\Delta(\iota_{2n+1})\bigr)\ =\ \pm\,2\,\iota_{2n-1}"
SPECIAL_EQUATION = r"H(\Delta(\iota_{13}))=\pm2\iota_{11}"


@dataclass(frozen=True)
class Prop27TypedDesign:
    """Mathematical signature only; not an executable proof statement."""
    n: int
    source_group: tuple[int, int]
    delta_target_group: tuple[int, int]
    hopf_target_group: tuple[int, int]
    source_iota_dimension: int
    target_iota_dimension: int
    absolute_coefficient: int
    sign_is_undetermined: bool


def specialize_prop27_design(n: int) -> Prop27TypedDesign:
    """Specialize a sourced theorem schema, never infer a ProofStep."""
    if type(n) is not int or n < 2 or n % 2 != 0:
        raise ValueError("Toda Proposition 2.7 requires an even integer n >= 2")
    return Prop27TypedDesign(
        n=n,
        source_group=(2 * n + 1, 2 * n + 1),
        delta_target_group=(2 * n - 1, n),
        hopf_target_group=(2 * n - 1, 2 * n - 1),
        source_iota_dimension=2 * n + 1,
        target_iota_dimension=2 * n - 1,
        absolute_coefficient=2,
        sign_is_undetermined=True,
    )


def source_contract(source: str, secondary: str, legacy: str) -> dict[str, object]:
    """Confirm the exact primary TeX proposition and legacy rule separation."""
    matches = re.findall(
        r"\\begin\{proposition\}\\label\{prop:2\.7\}(.*?)\\end\{proposition\}",
        source, flags=re.DOTALL,
    )
    if len(matches) != 1:
        raise ValueError("Chapter II Proposition 2.7 not unique")
    proposition = matches[0]
    if "$n$ が偶数のとき" not in proposition or GENERAL_EQUATION not in proposition:
        raise ValueError("Chapter II even-n typed formula changed")
    if r"H[\,\iota_n,\ \iota_n\,]" not in source:
        raise ValueError("Whitehead-square source context missing")
    if SPECIAL_EQUATION not in secondary:
        raise ValueError("Chapter V n=6 specialization citation missing")
    if "WhiteheadProduct" not in legacy or "TodaProp27HopfInvariantUpToSignStatement" not in legacy:
        raise ValueError("Legacy Whitehead product semantics changed")
    return {
        "chapter_ii_source": SOURCE,
        "even_n_condition": True,
        "chapter_v_n6_specialization": True,
        "legacy_whitehead_rule_distinct": True,
        "chapter_v_sidebar_mismatch": (r"\iota_{2m-1}" in secondary),
    }


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
        encoding="utf-8", errors="replace", text=True,
    ).stdout.strip()


def guard_checkout(root: Path = ROOT) -> dict[str, str]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R24 inside the repository root")
    branch = git("branch", "--show-current", root=root)
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if branch != "develop" or local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed branch or HEAD; no checkout or reset performed")
    modified = sorted(set(git("diff", "--name-only", root=root).splitlines()) |
                      set(git("diff", "--cached", "--name-only", root=root).splitlines()))
    if modified:
        raise RuntimeError("Tracked changes require independent review: " + ", ".join(modified))
    for path in (SOURCE, SECONDARY, LEGACY_TEST):
        checked = subprocess.run(("git", "show", "HEAD:" + path), cwd=root,
                                 check=True, capture_output=True).stdout
        present = (root / path).read_bytes()
        normalized = checked.replace(b"\r\n", b"\n")
        if present not in (checked, normalized, normalized.replace(b"\n", b"\r\n")):
            raise RuntimeError("Reviewed source mismatch: " + path)
    return {"branch": branch, "local_head": local, "remote_head": remote, "source_guard": "PASS"}


def audit(root: Path = ROOT) -> dict[str, object]:
    state = guard_checkout(root)
    sources = source_contract(
        (root / SOURCE).read_text(encoding="utf-8-sig"),
        (root / SECONDARY).read_text(encoding="utf-8-sig"),
        (root / LEGACY_TEST).read_text(encoding="utf-8-sig"),
    )
    target = specialize_prop27_design(6)
    if (target.source_group, target.delta_target_group, target.hopf_target_group) != (
        (13, 13), (11, 6), (11, 11)
    ):
        raise RuntimeError("Incorrect n=6 Delta/Hopf typing")
    return {
        "phase": PHASE, "git": state, "source": sources,
        "n6_signature": vars(target), "new_given": 0,
        "new_production_rules": 0, "verified_proof_steps": 0,
        "full_pytest": False, "root_complete": False,
        "gate": "PASS_R24_PROP27_TYPED_DESIGN_SOURCE_VERIFIED_IMPLEMENTATION_PENDING",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = audit()
    prefix = "PHASE174_R3R7R24_"
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD=" + result["git"]["local_head"])
    print(prefix + "GENERAL_EVEN_N_CONDITION=True")
    print(prefix + "N6_DELTA=pi_13^13_to_pi_11^6")
    print(prefix + "N6_HOPF=pi_11^6_to_pi_11^11")
    print(prefix + "SIGN_UNDETERMINED=True")
    print(prefix + "CHAPTER_V_SIDEBAR_MISMATCH=" + str(result["source"]["chapter_v_sidebar_mismatch"]))
    print(prefix + "NEW_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "MODE=" + ("DRYRUN" if args.dry_run else "AUDIT"))
    print(prefix + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
