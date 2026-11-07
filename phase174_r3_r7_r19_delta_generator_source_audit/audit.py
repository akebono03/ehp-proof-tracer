"""R19: source-first, read-only audit of the Delta generator/image proof gap.

This module never inserts a proof leaf, mathematical rule, or production provider.
A group-generator name is not itself a typed proof that an element is in im(Delta).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R19"
PRIOR_HEAD = "7ecd12f28b5943b105ac6a953be69b44eae4a26e"
REVIEWED_HEAD = "3ba55c65566bdf391d425bae04038b8b521240a4"
R18_AUDIT_PATH = "phase174_r3_r7_r18_delta_image_surjectivity/audit.py"
ALLOWED_MERGE_PREFIXES = (
    "phase174_r3_r7_r18r1_git_mixed_eol_guard/",
    "phase174_r3_r7_r18r2_local_evidence_recovery/",
)
PINS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "phase166_r3aj_structured_generator.py": "c6ecbc4bb95631a58de38b412879d22c1e1c2c61",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "map_facts.py": "86fbf404783e15d344595bf54df5a9a8bafc35fc",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r57_r19_delta_image_backward.py": "c5b3447258f41e15219ead8daeeb17cbb5605b6d",
    "toda_delta_image_rules.py": "f0ccdc2d3b8545986caaaba51a213c86cc08b781",
    "phase165_r52_r9_shared_math.py": "d42bb7420cf58f4dd466511d6498c66d9917b29c",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py": "f8da1f6fb7d5fb66feae33b4a4847fbad6891342",
    "phase174_r3_r7_r18_delta_image_surjectivity/audit.py": "0849f4039101941c10e0c1679d3ec2741092719c",
    "phase174_r3_r7_r18_delta_image_surjectivity/tests/test_public_frontier.py": "a1af1761e7b291263d02b8048bfc9ea909e7aa51",
}

PROP_START = r"\begin{proposition}\label{prop:5.9}"
PROP_GROUP = r"\pi^{6}_{11}=\mathbb Z\gen{\Delta(\iota_{13})}"
PROOF_SUSPENSION_ZERO = r"E\pi_{10}^5=0"
PROOF_HOPF_IMAGE = r"H(\Delta(\iota_{13}))=\pm2\iota_{11}"
PROOF_ROOT_ZERO = r"\pi_{12}^7=0"


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
    ).stdout


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_reviewed_checkout(data: bytes, stored: bytes, pinned: str) -> bool:
    """Trust only a pinned Git object and its exact whole-file EOL variants."""
    if len(pinned) != 40 or git_blob_sha(stored) != pinned:
        return False
    normalized = stored.replace(b"\r\n", b"\n")
    return data in (stored, normalized, normalized.replace(b"\n", b"\r\n"))


def classify_lineage(local: str, remote: str, tracked: tuple[str, ...],
                     changed_by_merge: tuple[str, ...], merge_count: int) -> str:
    """Allow only an exact R18R2 clean merge or its reviewed local handoff."""
    if remote != REVIEWED_HEAD or local not in (PRIOR_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed GitHub/local develop HEAD")
    if merge_count != 1:
        raise RuntimeError("R18R2 merge count differs from reviewed lineage")
    if not changed_by_merge or R18_AUDIT_PATH not in changed_by_merge:
        raise RuntimeError("Missing R18R2 audited source change")
    if any(path != R18_AUDIT_PATH and not path.startswith(ALLOWED_MERGE_PREFIXES)
           for path in changed_by_merge):
        raise RuntimeError("Unexpected R18R2 merged file")
    if local == REVIEWED_HEAD and tracked == ():
        return "R18R2_MERGED_CLEAN"
    if local == PRIOR_HEAD and tracked == (R18_AUDIT_PATH,):
        return "R18R2_PATCH_UNCOMMITTED_MATCH_REMOTE"
    raise RuntimeError("Unreviewed tracked changes: " + repr(tracked))


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    """Pin actual files, Git lineage, and the exact R18R2 handoff."""
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R19 immediately under repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R19 requires develop")
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    local = git("rev-parse", "HEAD", root=root)
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged modifications require a separate review")
    tracked = tuple(sorted(git("diff", "--name-only", root=root).splitlines()))
    git_bytes("merge-base", "--is-ancestor", PRIOR_HEAD, REVIEWED_HEAD, root=root)
    changed = tuple(git("diff", "--name-only", PRIOR_HEAD, REVIEWED_HEAD, root=root).splitlines())
    commits = git("rev-list", PRIOR_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines()
    lineage = classify_lineage(local, remote, tracked, changed, len(commits))
    for relative, pinned in PINS.items():
        path = root / relative
        stored = git_bytes("show", REVIEWED_HEAD + ":" + relative, root=root)
        if not path.is_file() or not matches_reviewed_checkout(path.read_bytes(), stored, pinned):
            raise RuntimeError("R19 source mismatch: " + relative)
    return {
        "local_head": local, "remote_head": remote, "lineage": lineage,
        "source_guard": "PASS", "pinned_files": len(PINS),
        "tracked_changes": list(tracked),
    }


def inspect_toda_proposition(source: str) -> dict[str, Any]:
    """Distinguish the cited proposition, its proof, and missing separate image identity."""
    if source.count(PROP_START) != 1:
        raise RuntimeError("Toda Proposition 5.9 not uniquely located")
    start = source.index(PROP_START)
    end = source.find(r"\qed", start)
    if end < start:
        raise RuntimeError("Toda Proposition 5.9 proof end missing")
    segment = source[start:end]
    markers = (PROP_GROUP, PROOF_SUSPENSION_ZERO, PROOF_HOPF_IMAGE, PROOF_ROOT_ZERO)
    if any(segment.count(marker) != 1 for marker in markers):
        raise RuntimeError("Toda Proposition 5.9 source chain changed")
    locations = [segment.index(marker) for marker in markers]
    if locations != sorted(locations):
        raise RuntimeError("Toda Proposition 5.9 derivation order changed")
    return {
        "source_locator": "Toda Proposition 5.9 (adopted TeX)",
        "proposition_lists_free_cyclic_generator": True,
        "proof_has_suspension_zero": True,
        "proof_has_hopf_delta_image": True,
        "proof_concludes_target_zero": True,
        "proposition_group_result_is_not_independent_given": True,
        "original_print_edition_verified": False,
    }


def inspect_generator_row(csv_source: str) -> dict[str, Any]:
    """An encoded generator *label* does not certify typed Delta application."""
    rows = list(csv.DictReader(csv_source.lstrip("\ufeff").splitlines()))
    records = [row for row in rows if row.get("id") == "5"]
    if len(records) != 1:
        raise RuntimeError("Delta generator identity row missing or ambiguous")
    row = records[0]
    expected = {"display": "Δ(ι13)", "kinds": "1", "k": "5", "n": "6",
                "latex": r"\Delta(\iota_{13})"}
    if any(row.get(field) != value for field, value in expected.items()):
        raise RuntimeError("Delta generator DB notation changed")
    return {
        "row_id": 5,
        "display": row["display"],
        "dimension": (int(row["n"]), int(row["k"])),
        "typed_delta_application_in_csv": False,
        "database_row_is_proof": False,
    }


def inspect_live_frontier() -> dict[str, Any]:
    """Read public Proof Search; neither create a step nor change its provider."""
    from expression import HomotopyElement, MapApplication
    from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from phase174_r3_r7_r18_delta_image_surjectivity.audit import (
        inspect_live_frontier as r18_frontier,
    )
    from phase174_r3_r7_r18_delta_image_surjectivity.rule import (
        delta_surjectivity_image_inputs,
    )
    from proof import Relation, RelationType
    from toda_rules import TodaDeltaImageFreeCyclicStatement

    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    children = ehp_zero_inputs(target)
    if children is None or len(children) != 4 or not isinstance(children[0], MapSurjective):
        raise RuntimeError("EHP root and Delta goal changed")
    delta_goal = children[0]
    prior = exact_prior_database_result(6, 5)
    if (not isinstance(prior, Relation) or prior.lhs != delta_goal.map.target_group
            or prior.relation_type is not RelationType.EQUALITY
            or not isinstance(prior.rhs, FreeCyclicGroup)):
        raise RuntimeError("Concrete Delta codomain DB goal unavailable")
    generator = prior.rhs.generator
    # A name printed as 'Delta(iota13)' is not a typed MapApplication;
    # the missing provenance must be proved, never inferred from spelling.
    if not isinstance(generator, HomotopyElement) or isinstance(generator, MapApplication):
        raise RuntimeError("Generator's reviewed symbolic representation changed")
    needed = delta_surjectivity_image_inputs(delta_goal, prior)
    if (needed is None or len(needed) != 2
            or not isinstance(needed[1], TodaDeltaImageFreeCyclicStatement)
            or needed[1].image_group.generator != generator):
        raise RuntimeError("R18 general image/codomain inference changed")
    live = r18_frontier()
    expected = {
        "public_root_proposals": 1,
        "public_delta_surjectivity_proposals": 0,
        "isolated_delta_surjectivity_proposals": 1,
        "public_codomain_presentation_proposals": 1,
        "public_delta_free_cyclic_image_proposals": 0,
        "matching_cited_signed_delta_witness_count": 0,
        "codomain_prior_db_admissible": True,
        "search_verified_steps": 0,
        "search_status": "search_failed",
    }
    for key, value in expected.items():
        if live.get(key) != value:
            raise RuntimeError("R18 public proof boundary changed: " + key)
    if live.get("completion_claimed") is not False:
        raise RuntimeError("Unverified root-completion claim")
    return {
        "root_candidates": live["public_root_proposals"],
        "delta_public_candidates": live["public_delta_surjectivity_proposals"],
        "delta_isolated_candidates": live["isolated_delta_surjectivity_proposals"],
        "codomain_presentation_candidates": live["public_codomain_presentation_proposals"],
        "delta_image_public_candidates": live["public_delta_free_cyclic_image_proposals"],
        "signed_delta_witnesses": live["matching_cited_signed_delta_witness_count"],
        "db_prior_admissible": live["codomain_prior_db_admissible"],
        "generator_expression_type": type(generator).__name__,
        "generator_is_typed_map_application": isinstance(generator, MapApplication),
        "typed_identity_proof_found": False,
        "search_status": live["search_status"],
        "verified_steps": live["search_verified_steps"],
        "new_given": 0, "new_rules": 0,
        "completion_claimed": False,
    }


def report_path(*, dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = base / "EHPProofTracerAudit" / "phase174_r3_r7_r19"
    return folder / ("generator_source_preflight.json" if dry_run else "generator_source_audit.json")


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(root)
    toda = inspect_toda_proposition((root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig"))
    row = inspect_generator_row((root / "data/HyoujiGen.csv").read_text(encoding="utf-8-sig"))
    live = None if dry_run else inspect_live_frontier()
    return {
        "phase": PHASE,
        "git_state": state,
        "source": toda,
        "database_notation": row,
        "live": live,
        "mode": "SOURCE_PREFLIGHT" if dry_run else "READ_ONLY_TYPED_GENERATOR_GAP",
        "new_group_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": False,
        "full_pytest_run": False,
        "target_completed": False,
        "gate": ("PASS_R19_SOURCE_PREFLIGHT" if dry_run
                 else "PASS_R19_DELTA_GENERATOR_TYPED_IMAGE_GAP_REMAINS"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    destination = report_path(dry_run=args.dry_run)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R19_"
    state = report["git_state"]
    print(prefix + "LOCAL_HEAD=" + state["local_head"])
    print(prefix + "REMOTE_HEAD=" + state["remote_head"])
    print(prefix + "LINEAGE=" + state["lineage"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "TODA_PROP59_GROUP_CLAUSE=True")
    print(prefix + "GENERATOR_ROW_IS_PROOF=False")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "PUBLIC_DELTA_IMAGE_PROPOSALS=" + str(live["delta_image_public_candidates"]))
        print(prefix + "SIGNED_DELTA_WITNESSES=" + str(live["signed_delta_witnesses"]))
        print(prefix + "DB_GENERATOR_TYPE=" + live["generator_expression_type"])
        print(prefix + "DB_GENERATOR_IS_MAP_APPLICATION=" + str(live["generator_is_typed_map_application"]))
        print(prefix + "SEARCH_STATUS=" + live["search_status"])
        print(prefix + "VERIFIED_STEPS=" + str(live["verified_steps"]))
    print(prefix + "NEW_GIVEN=0")
    print(prefix + "NEW_MATH_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
