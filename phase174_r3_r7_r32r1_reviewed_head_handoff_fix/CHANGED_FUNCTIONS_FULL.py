# This is the complete replacement of R32 audit.verify_checkout().
# Add REVIEWED_R31_MERGE_HEAD immediately after REVIEWED_HEAD in audit.py.
REVIEWED_R31_MERGE_HEAD = "02f694b27a4239052bfa9d27a116fca6bbbff6b5"

def verify_checkout() -> dict[str, object]:
    """Fail closed on new GitHub code, preserving the untracked R31 package."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R32 ZIP must be extracted at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R32 requires develop")
    head = git("rev-parse", "HEAD")
    remote_result = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_result.split()[0] if remote_result else ""
    # GitHub reviewed R31 as one successor commit containing only the R31 audit
    # package. The checkout may still be at R30 while R31 is locally untracked.
    # The R31 file is checked below against its original exact SHA256 in both
    # handoff modes; never fetch, pull, reset, or overwrite it here.
    if (remote != REVIEWED_R31_MERGE_HEAD
            or head not in (REVIEWED_HEAD, REVIEWED_R31_MERGE_HEAD)):
        raise RuntimeError("Unreviewed local/remote develop handoff; review before R32")
    staged = git("diff", "--cached", "--name-only").splitlines()
    changed = git("diff", "--name-only").splitlines()
    if staged or changed:
        raise RuntimeError("Tracked edits require review; no reset performed")
    for relative, sha in PINS.items():
        file = ROOT / relative
        if not file.is_file() or not matches_pin(file.read_bytes(), sha):
            raise RuntimeError("R32 reviewed file differs: " + relative)
    prior = ROOT / R31_AUDIT
    if not prior.is_file():
        raise RuntimeError("R31 audited package is not present; do not overwrite it")
    text = prior.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != R31_SHA256:
        raise RuntimeError("R31 audit file changed; previous work needs review")
    return {
        "local_head": head,
        "remote_head": remote,
        "handoff_mode": (
            "R31_LOCAL_UNMERGED_REVIEWED" if head == REVIEWED_HEAD
            else "R31_MERGED_REVIEWED"
        ),
        "source_guard": "PASS",
        "r30_preserved": True,
        "r31_preserved": True,
        "git_pins_checked": len(PINS),
        "tracked_changes": 0,
    }

