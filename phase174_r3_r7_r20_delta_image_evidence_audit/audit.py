"""Read-only audit of the cited Delta image argument in adopted Toda Prop. 5.9."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "654d46f6f225fc6b641a1760ce0e3f08598419c3"
PARENT_HEAD = "3ba55c65566bdf391d425bae04038b8b521240a4"
SOURCE = "sources/toda/Toda_05_2.tex"
START = r"\begin{proposition}\label{prop:5.9}"
END = r"\begin{lemma}\label{lemma:5.10}"
MARKERS = {
    "group_presentation": r"\pi^{6}_{11}=\mathbb Z\gen{\Delta(\iota_{13})}",
    "suspension_zero": r"E\pi_{10}^5=0",
    "hopf_delta": r"H(\Delta(\iota_{13}))=\pm2\iota_{11}",
    "delta_isomorphism": r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
    "root_zero": r"\pi_{12}^7=0",
}


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(("git",) + args, cwd=root, capture_output=True, check=True,
                          encoding="utf-8", errors="replace", text=True).stdout.strip()


def verify_checkout(root: Path = ROOT) -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("R20 must be extracted at the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R20 requires develop")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if (local, remote) != (REVIEWED_HEAD, REVIEWED_HEAD):
        raise RuntimeError("R20 reviewed HEAD mismatch; re-audit changes before running")
    if git("diff", "--name-only", root=root) or git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("R20 requires no tracked changes")
    if git("rev-parse", "HEAD^", root=root) != PARENT_HEAD:
        raise RuntimeError("R19 merge parent differs from reviewed lineage")
    for path in (SOURCE,
                 "phase174_r3_r7_r19_delta_generator_source_audit/audit.py",
                 "phase174_r3_r7_r18_delta_image_surjectivity/rule.py"):
        if not (root / path).is_file():
            raise RuntimeError("Missing reviewed source: " + path)
        stored = subprocess.run(("git", "show", REVIEWED_HEAD + ":" + path), cwd=root,
                                capture_output=True, check=True).stdout
        actual = (root / path).read_bytes()
        normalized = stored.replace(b"\r\n", b"\n")
        if actual not in (stored, normalized, normalized.replace(b"\n", b"\r\n")):
            raise RuntimeError("Reviewed source mismatch: " + path)
    return {"local_head": local, "remote_head": remote, "source_guard": "PASS"}


def inspect_source(source: str) -> dict[str, object]:
    if source.count(START) != 1 or source.count(END) != 1:
        raise RuntimeError("Prop 5.9 / Lemma 5.10 boundary not unique")
    segment = source[source.index(START):source.index(END)]
    for key, marker in MARKERS.items():
        if segment.count(marker) < 1:
            raise RuntimeError("Missing Prop 5.9 evidence: " + key)
    if not (segment.index(MARKERS["group_presentation"])
            < segment.index(MARKERS["suspension_zero"])
            < segment.index(MARKERS["hopf_delta"])
            < segment.index(MARKERS["delta_isomorphism"])
            < segment.index(MARKERS["root_zero"])):
        raise RuntimeError("Proposition proof dependency order changed")
    # Proposition statement and its proof may share a section. This audit does not
    # promote a displayed result, an isomorphism arrow, or a database name to GIVEN.
    return {
        "source_locator": "adopted Toda_05_2.tex, Proposition 5.9 proof",
        "evidence_clauses": list(MARKERS),
        "delta_iso_is_present_in_proof_text": True,
        "delta_iso_is_independently_proven_in_public_search": False,
        "signed_generator_identity_is_typed_proof": False,
        "original_print_edition_checked": False,
    }


def report(*, dry_run: bool) -> dict[str, object]:
    checkout = verify_checkout()
    source = inspect_source((ROOT / SOURCE).read_text(encoding="utf-8-sig"))
    live = None
    if not dry_run:
        from phase174_r3_r7_r19_delta_generator_source_audit.audit import inspect_live_frontier
        live = inspect_live_frontier()
        if (live["delta_image_public_candidates"] != 0
                or live["signed_delta_witnesses"] != 0
                or live["verified_steps"] != 0
                or live["search_status"] != "search_failed"
                or live["completion_claimed"] is not False):
            raise RuntimeError("R20 public boundary changed; reassess before proceeding")
    return {
        "phase": "174-R3-R7-R20", "checkout": checkout, "source": source,
        "live_r19_frontier": live, "new_given": 0, "new_rules": 0,
        "production_changes": False, "full_pytest": False,
        "root_complete": False,
        "gate": ("PASS_R20_SOURCE_PREFLIGHT_ONLY" if dry_run
                 else "PASS_R20_SOURCE_EVIDENCE_FOUND_TYPED_IMAGE_PENDING"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r20"
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / ("source_preflight.json" if args.dry_run else "source_audit.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R3R7R20_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R20_TODA_PROP59_DELTA_ISOMORPHISM_TEXT=True")
    print("PHASE174_R3R7R20_NEW_GIVEN=0")
    print("PHASE174_R3R7R20_NEW_RULES=0")
    print("PHASE174_R3R7R20_ROOT_COMPLETE=False")
    print("PHASE174_R3R7R20_FULL_PYTEST=False")
    print("PHASE174_R3R7R20_REPORT=" + str(output))
    print("PHASE174_R3R7R20_GATE=" + str(result["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
