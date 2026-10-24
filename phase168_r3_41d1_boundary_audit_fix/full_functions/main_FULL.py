def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = [one_case(name, n, k) for name, n, k in CASES]
    successful = [case for case in cases if case["capture_error"] is None]
    if not successful:
        raise RuntimeError("All real public searches failed; no audit evidence obtained")
    live_partial = [case for case in successful
                    if case["status_is_incomplete"] and case["name"] != "pi4_3_control"]
    cited_partial = [case for case in live_partial if case["citation_count"]]
    stepped_partial = [case for case in live_partial if case["search_step_count"]]
    registered_partial = [case for case in live_partial if case["registered_citation_count"]]
    body_partial = [case for case in live_partial if case["reference_with_body_count"]]
    unresolved_issues = sorted({issue for case in successful
                                for issue in case["state_issues"]
                                + case["citation_projection"]["issues"]})
    source_hashes = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in SOURCES
    }
    report = {
        "phase": "168 R3-41D1",
        "mode": "READ_ONLY_REAL_SEARCH_REFERENCE_AUDIT",
        "capture_errors": sum(case["capture_error"] is not None for case in cases),
        "coverage_status": (
            "CAPTURE_FAILURES" if any(case["capture_error"] for case in cases)
            else "CITED_PARTIAL_OBSERVED" if cited_partial
            else "NO_CITED_PARTIAL_OBSERVED"
        ),
        "source_sha256": source_hashes,
        "cases": cases,
        "coverage": {
            "real_search_attempts": len(CASES) - 1,
            "real_search_successful": len([case for case in successful
                                           if case["name"] != "pi4_3_control"]),
            "actual_incomplete_cases": len(live_partial),
            "actual_incomplete_with_steps": len(stepped_partial),
            "actual_incomplete_with_any_citation": len(cited_partial),
            "actual_incomplete_with_registered_citation": len(registered_partial),
            "actual_incomplete_with_reference_body": len(body_partial),
            "live_cited_partial_proven": bool(cited_partial),
        },
        "observed_issues": unresolved_issues,
        "scope_limits": [
            "No mathematical conclusion or reference is inferred from a goal.",
            "Samples are real Web searches, not a complete census of 112 targets.",
            "A zero-citation incomplete result does not validate partial citation rendering.",
            "A reference heading with no body is counted as a content gap.",
            "A standalone rule reference and a registered assertion are distinguished.",
            "This audit neither changes implementation nor runs full pytest.",
        ],
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    table = [
        "# Phase 168 R3-41D1 — 実探索の Reference・Narrative 監査", "",
        "読み取り専用。使用された ProofStep と screened bridge、Model、Web 表示を同時に確認する。", "",
        "| 対象 | 状態 | 証明 Step | Reference | 本文あり | Goal | 表示・引用の問題 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for case in cases:
        if case["capture_error"] is not None:
            table.append(f'| {case["name"]} | 実行エラー | - | - | - | - | {case["capture_error"]} |')
            continue
        issues = len(case["state_issues"] + case["citation_projection"]["issues"])
        table.append(f'| {case["name"]} | {case["status"]} | '
                     f'{case["search_step_count"]} | {case["citation_count"]} | '
                     f'{case["reference_with_body_count"]} | {case["open_goal_count"]} | {issues}件 |')
    c = report["coverage"]
    table.extend(("", "## 実探索の観測範囲", "",
                  f'- 未完成の検索結果: {c["actual_incomplete_cases"]}件',
                  f'- うち ProofStep あり: {c["actual_incomplete_with_steps"]}件',
                  f'- うち Reference あり: {c["actual_incomplete_with_any_citation"]}件',
                  f'- うち登録出典あり: {c["actual_incomplete_with_registered_citation"]}件',
                  f'- うち Reference 本文あり: {c["actual_incomplete_with_reference_body"]}件',
                  "", "## 判定上の注意", "",
                  "- Reference 番号や見出しがあっても、本文がなければ本文完成とは判定しない。",
                  "- 非完成の探索結果に引用が存在しなければ、実際の部分証明の引用表示は未検証と記録する。",
                  "- GIVEN で出典がない場合は未接続として報告し、引用は補わない。",
                  "- 各群の `*_reference.md` と `*_narrative.md` に実表示の内容を保存する。",
                  "- 実行エラーや表示不足があっても調査結果として報告し、実装ファイルは変更しない。",
                  "- 全体 pytest は実行しない。", "",
                  "## 見つかった問題", ""))
    if unresolved_issues:
        table.extend("- " + issue for issue in unresolved_issues)
    else:
        table.append("- 観測できた範囲では整合性違反なし（未観測範囲は未検証）。")
    table.append("")
    (OUTPUT / "audit.md").write_text("\n".join(table), encoding="utf-8")
    bundle = OUTPUT / "review_bundle.zip"
    with ZipFile(bundle, "w", compression=ZIP_DEFLATED) as archive:
        for file in sorted(OUTPUT.glob("*.md")) + sorted(OUTPUT.glob("*.json")) + sorted(OUTPUT.glob("*.txt")):
            archive.write(file, file.name)
    print("R3-41D READ_ONLY audit captured", len(successful), "real cases")
    print("ACTUAL_INCOMPLETE", len(live_partial),
          "CITED_PARTIAL", len(cited_partial), "REGISTERED_PARTIAL", len(registered_partial))
    print("ISSUES", unresolved_issues)
    print("REPORT", OUTPUT / "audit.md")
    print("UPLOAD_BUNDLE", bundle)
    print("COVERAGE_STATUS", report["coverage_status"],
          "CAPTURE_ERRORS", report["capture_errors"])
    print("Implementation unchanged. Full pytest NOT run.")
    if report["capture_errors"]:
        raise RuntimeError(
            "Some real searches were not captured; inspect the saved report. "
            "Audit coverage remains incomplete.")
