def inspect_report(recovery: Path, root: Path) -> tuple[Path, dict]:
    """Accept a successful R1 Gate from any reviewed ancestor commit.

    R1 may have run before audit-only packages were committed. Its HEAD must be
    between BASELINE_HEAD and REVIEWED_REMOTE_HEAD on the same ancestry path.
    All previous success, scope, command and log-presence checks remain in force.
    """
    paths = sorted(recovery.glob(REPORT_DIR_PREFIX + "*/report.json"), reverse=True)
    if not paths:
        raise RuntimeError(
            "No R1 Gate report.json found under "
            + str(recovery / (REPORT_DIR_PREFIX + "*"))
            + "; do not rerun full pytest just to create a report"
        )
    rejected: list[str] = []
    for path in paths:
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            rejected.append(path.name + ": invalid or unreadable JSON: " + str(exc))
            continue
        if not isinstance(report, dict):
            rejected.append(str(path) + ": JSON root is not an object")
            continue
        focused, active = report.get("focused"), report.get("active_full")
        if not isinstance(focused, dict) or not isinstance(active, dict):
            rejected.append(str(path) + ": missing focused / active_full results")
            continue
        valid = (
            report.get("mode") == "PHASE169_END_OF_PHASE_TEST"
            and report.get("phase169_test_gate_pass") is True
            and report.get("git_index_preserved") is True
            and report.get("phase169_certified") is False
            and report.get("decision") == "TEST_GATE_PASS_PENDING_PHASE169_CLOSEOUT_DOCUMENTATION"
            and report.get("reviewed_files") == 13
            and report.get("r6_cases") == 19
            and focused.get("passed_count") == 67 and focused.get("exit_code") == 0
            and active.get("passed_count") == 3546 and active.get("exit_code") == 0
            and isinstance(focused.get("command"), list)
            and len(focused["command"]) >= 10
            and isinstance(active.get("command"), list)
            and active["command"][-1:] == ["tests"]
            and active["command"][1:8] == [
                "-B", "-m", "pytest", "-q", "--tb=short", "--disable-warnings", "-p"
            ]
            and "no:cacheprovider" in active["command"]
        )
        if not valid:
            rejected.append(str(path) + ": R1 Gate results or command differ from reviewed contract")
            continue
        if not all(isinstance(x.get("log"), str) and Path(x["log"]).is_file()
                   for x in (focused, active)):
            rejected.append(str(path) + ": focused or active pytest log missing")
            continue
        head = report.get("head")
        if not (isinstance(head, str) and len(head) == 40
                and all(character in "0123456789abcdef" for character in head)):
            rejected.append(str(path) + ": malformed Gate Git HEAD")
            continue
        try:
            in_reviewed_history = (
                git(root, "merge-base", BASELINE_HEAD, head) == BASELINE_HEAD
                and git(root, "merge-base", head, REVIEWED_REMOTE_HEAD) == head
            )
        except RuntimeError:
            in_reviewed_history = False
        if not in_reviewed_history:
            rejected.append(str(path) + ": Gate HEAD is outside reviewed commit ancestry: " + head)
            continue
        print("PHASE169_CLOSEOUT_R3B_R1_REPORT_HEAD=" + head, flush=True)
        print("PHASE169_CLOSEOUT_R3B_R1_REPORT_PATH=" + str(path), flush=True)
        return path, report
    details = "\n".join(rejected[:10])
    raise RuntimeError(
        "No verified successful Phase 169 R1 Gate report found among "
        + str(len(paths)) + " candidate(s). Rejections:\n" + details
    )
