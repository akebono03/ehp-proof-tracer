def execute(root: Path) -> int:
    from phase169_r10et_closeout_r2_documentation.update_docs import (
        DOCUMENT_BLOBS, REVIEWED_SOURCE_BLOBS,
    )

    baseline = snapshot(root)
    if not (root / ".git").exists() or git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop Git repository")
    if baseline[0] != REVIEWED_HEAD:
        raise RuntimeError("Local HEAD differs from reviewed GitHub commit")
    if git(root, "rev-parse", "refs/remotes/origin/develop") != REVIEWED_HEAD:
        raise RuntimeError("origin/develop tracking ref differs")
    remote = git(root, "ls-remote", "origin", "refs/heads/develop")
    if remote != REVIEWED_HEAD + "\trefs/heads/develop":
        raise RuntimeError("Remote develop moved; review the new commit first")
    if baseline[2]:
        raise RuntimeError("Staged changes must be reviewed separately")
    if baseline[1]:
        raise RuntimeError("Tracked unstaged changes are not allowed after document commit")
    for path, expected_blob in REVIEWED_SOURCE_BLOBS.items():
        if git(root, "hash-object", f"--path={path}", path) != expected_blob:
            raise RuntimeError("Production source/test differs: " + path)
    backup = Path(os.environ["LOCALAPPDATA"]).resolve() / "EHPProofTracerRecovery" / BACKUP_NAME
    documents = certify_documents(root, backup)
    r6 = json.loads((root / R6_REPORT).read_text(encoding="utf-8"))
    required, probes = review_r6_report(r6)
    if snapshot(root) != baseline:
        raise RuntimeError("Git HEAD, tracked changes or index changed during audit")
    root_resolved = root.resolve()
    report_dir = backup.parent / ("r10et_closeout_r3_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    report_dir_resolved = report_dir.resolve()
    if report_dir_resolved == root_resolved or root_resolved in report_dir_resolved.parents:
        raise RuntimeError("Audit output must be outside the repository")
    report_dir.mkdir(parents=True, exist_ok=False)
    report = {
        "mode": "AUDIT_ONLY", "head": REVIEWED_HEAD,
        "documents": documents, "r6_required_pass": required,
        "r6_probes_pass": probes, "source_count": len(REVIEWED_SOURCE_BLOBS),
        "tracked_unchanged": True, "full_pytest_run": False,
        "r10et_complete": True, "phase169_complete": False,
        "decision": "R10ET_DOCUMENT_CLOSED_PHASE169_STILL_OPEN",
    }
    (report_dir / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (report_dir / "audit.md").write_text(
        "# R10ET Closeout R3 — 完了文書・監査根拠の照合\n\n"
        + "- R10ET 文書5件: 全文一致。\n"
        + "- 監査対象の本番実装・テスト8件: GitHub commit と一致。\n"
        + f"- R6 必須: {required}/16 PASS、追加: {probes}/3 PASS。\n"
        + "- Git index と既存差分: 保持。\n"
        + "- Phase 169 全体 pytest・終了判定: 未実施。\n",
        encoding="utf-8",
    )
    print("R10ET_CLOSEOUT_R3_REVIEWED_HEAD=" + REVIEWED_HEAD)
    print("R10ET_CLOSEOUT_R3_DOCUMENTS=5/5_PASS")
    print("R10ET_CLOSEOUT_R3_SOURCES=8/8_PASS")
    print(f"R10ET_CLOSEOUT_R3_R6_CASES={required + probes}/19_PASS")
    print("R10ET_CLOSEOUT_R3_INDEX_PRESERVED=True")
    print("R10ET_CLOSEOUT_R3_FULL_PYTEST_NOT_RUN=True")
    print("R10ET_CLOSEOUT_R3_DECISION=R10ET_DOCUMENT_CLOSED_PHASE169_STILL_OPEN")
    print("R10ET_CLOSEOUT_R3_REPORT=" + str(report_dir / "audit.md"))
    print("R10ET_CLOSEOUT_R3_EXIT=0")
    return 0
