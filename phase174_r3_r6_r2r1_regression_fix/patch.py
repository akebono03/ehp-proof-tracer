"""Fail-closed two-file follow-up to the reviewed R3-R6-R2 implementation.

Only the old R3-R4 audit and its cumulative test are updated. Both are
checked against the R3-R6-R2 revision and the exact reviewed Git blobs.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
from pathlib import Path

from phase174_r3_r6_r2_prop44_lemma54.patch import (
    BLOBS as PREVIOUS_BLOBS,
    HEAD,
    TRANSFORM as PREVIOUS_TRANSFORM,
    normalize,
    replace_one,
    full_unit,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TEST = "phase174_r3_r4_public_delta_connection/tests/test_connection.py"
AUDIT = "phase174_r3_r4_public_delta_connection/audit.py"
AUDIT_BLOB = "d78cb903a236f210f05be05a198fd9b17055924e"


def git_bytes(*args: str) -> bytes:
    return subprocess.run(("git", *args), cwd=ROOT, check=True,
                          capture_output=True).stdout


def blob_hash(content: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(content)).encode("ascii") + b"\0" + content
    ).hexdigest()


def patch_cumulative_test(text: str) -> str:
    """Preserve byte-exact lineage checks; normalize only checkout line endings."""
    text = replace_one(
        text,
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n",
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import normalize, patch_shared\n",
        label="R3-R4 cumulative test's reviewed import",
    )
    before = (
        "    new_source = patch_shared(r3r6.decode('utf-8')).encode('utf-8')\n"
        "    assert current in (r3r4, r3r5, r3r6, new_source)\n"
    )
    after = (
        "    new_source = patch_shared(normalize(r3r6.decode('utf-8'))).encode('utf-8')\n"
        "    assert normalize(current.decode('utf-8')) in tuple(\n"
        "        normalize(candidate.decode('utf-8'))\n"
        "        for candidate in (r3r4, r3r5, r3r6, new_source)\n"
        "    )\n"
    )
    text = replace_one(text, before, after, label="R3-R4 reviewed LF/CRLF replay")
    ast.parse(text, filename=TEST)
    return text


def patch_delta_audit(text: str) -> str:
    """Use the same earlier verified Lemma 5.4 source as the completed root."""
    text = replace_one(
        text,
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n",
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n"
        "    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource\n"
        "    from phase174_r3_r6_r2_prop44_lemma54.source import (\n"
        "        attach_earlier_verified_lemma54,\n"
        "    )\n",
        label="R3-R4 delta audit independently cited lemma imports",
    )
    before = (
        "    if citation is None:\n"
        "        raise ValueError(\"No actual pi_8^5 publication position\")\n"
        "    screened = screen_shared_proof_context(\n"
    )
    after = (
        "    if citation is None:\n"
        "        raise ValueError(\"No actual pi_8^5 publication position\")\n"
        "    amended = attach_earlier_verified_lemma54(bridge, citation)\n"
        "    if amended is bridge:\n"
        "        raise ValueError(\"Verified Lemma 5.4 must precede this proof target\")\n"
        "    bridge = amended\n"
        "    screened = screen_shared_proof_context(\n"
    )
    text = replace_one(text, before, after, label="R3-R4 source-first public context")
    text = replace_one(
        text,
        "        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())\n"
        "        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())\n",
        "        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())\n"
        "        or not proof_has_cited_leaf(step.premises[0], TodaLemma54TypedSource())\n"
        "        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())\n",
        label="R3-R4 independently inferred lemma ancestry",
    )
    ast.parse(text, filename=AUDIT)
    return text


def reviewed_changes() -> dict[str, tuple[bytes, bytes]]:
    """Check the previous 9-file patch was installed and no tracked changes are staged.

    This supports re-running this follow-up but refuses arbitrary edits to
    other R3-R6-R2 outputs and refuses unexpected edits in its own two files.
    """
    branch = git_bytes("branch", "--show-current").decode("utf-8").strip()
    local = git_bytes("rev-parse", "HEAD").decode("ascii").strip()
    remote = git_bytes("ls-remote", "origin", "refs/heads/develop").decode("ascii").split()
    if branch != "develop" or local != HEAD or remote != [HEAD, "refs/heads/develop"]:
        raise ValueError("Unreviewed R3-R6-R2 HEAD or remote develop")
    if git_bytes("diff", "--cached", "--name-only").strip():
        raise ValueError("Staged changes must be reviewed")

    for path, transform in PREVIOUS_TRANSFORM.items():
        committed = git_bytes("show", "HEAD:" + path)
        if blob_hash(committed) != PREVIOUS_BLOBS[path]:
            raise ValueError("Reviewed R3-R6-R2 Git blob changed: " + path)
        expected = transform(normalize(committed.decode("utf-8-sig")))
        actual = normalize((ROOT / path).read_text(encoding="utf-8-sig"))
        if path == TEST:
            authorized = (expected, patch_cumulative_test(expected))
        else:
            authorized = (expected,)
        if actual not in authorized:
            raise ValueError("Unreviewed R3-R6-R2 working file: " + path)

    committed = git_bytes("show", "HEAD:" + AUDIT)
    if blob_hash(committed) != AUDIT_BLOB:
        raise ValueError("Reviewed historical Delta audit Git blob changed")
    old_audit = normalize(committed.decode("utf-8-sig"))
    new_audit = patch_delta_audit(old_audit)

    original_test = git_bytes("show", "HEAD:" + TEST)
    old_test = PREVIOUS_TRANSFORM[TEST](normalize(original_test.decode("utf-8-sig")))
    new_test = patch_cumulative_test(old_test)
    current_audit = normalize((ROOT / AUDIT).read_text(encoding="utf-8-sig"))
    current_test = normalize((ROOT / TEST).read_text(encoding="utf-8-sig"))
    if current_audit not in (old_audit, new_audit):
        raise ValueError("Unreviewed R3-R4 audit changes")
    if current_test not in (old_test, new_test):
        raise ValueError("Unreviewed R3-R4 cumulative test changes")
    return {
        AUDIT: ((ROOT / AUDIT).read_bytes(), new_audit.encode("utf-8")),
        TEST: ((ROOT / TEST).read_bytes(), new_test.encode("utf-8")),
    }


def apply(*, dry_run: bool) -> None:
    changes = reviewed_changes()
    print("PHASE174_R3R6R2R1_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R2R1_REVIEWED_HEAD=" + HEAD)
    print("PHASE174_R3R6R2R1_REVIEWED_PRIOR_FILES=" + str(len(PREVIOUS_BLOBS)))
    print("PHASE174_R3R6R2R1_TARGET_FILES=" + str(len(changes)))
    if dry_run:
        print("PHASE174_R3R6R2R1_DRY_RUN_GATE=PASS")
        return
    snapshots = {path: prior for path, (prior, _) in changes.items()}
    try:
        for path, (_, new) in changes.items():
            (ROOT / path).write_bytes(new)
        output = PACKAGE / "output"
        output.mkdir(parents=True, exist_ok=True)
        for path, (_, new) in changes.items():
            text = new.decode("utf-8")
            (output / (path.replace("/", "__") + ".FULL.py")).write_text(
                text, encoding="utf-8",
            )
            fn = "inspect_public_provider" if path == AUDIT else "test_r3r4_real_production_file_has_only_reviewed_wiring"
            (output / (fn + "_FULL.py")).write_text(full_unit(text, fn), encoding="utf-8")
        print("PHASE174_R3R6R2R1_PATCH=PASS")
        print("PHASE174_R3R6R2R1_FULL_REPLACEMENTS=" + str(output))
    except BaseException:
        for path, old in snapshots.items():
            (ROOT / path).write_bytes(old)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    apply(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
