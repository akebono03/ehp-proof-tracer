def audit_four_cases(root: Path) -> list[dict]:
    from phase168_r3_38_frozen_fulltext_audit.audit import capture
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_26_exactness_projection import project_exactness_chains

    # This function is also invoked directly by pytest, before main().
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = []
    for label, n, k in CASES:
        narrative, model, view = capture(n, k)
        suppressed = {i for chain in project_exactness_chains(model)
                      for i in chain.step_indices}
        entries = project_narrative_order(model)
        indices = [entry.step_index for entry in entries]
        positions = {index: position for position, index in enumerate(indices)}
        inversions = []
        for child_index, step in enumerate(model.steps):
            for premise in step.premises:
                matches = [i for i, candidate in enumerate(model.steps) if candidate is premise]
                if not matches:
                    matches = [i for i, candidate in enumerate(model.steps) if candidate == premise]
                if not matches or positions[matches[0]] >= positions[child_index]:
                    inversions.append([matches[0] if matches else None, child_index])
        current_path = OUTPUT / (label + "_current.md")
        current_path.write_text(narrative, encoding="utf-8")
        previous_path = (root / "phase168_r3_40e_remove_deferred_render" / "output"
                         / (label + "_after.md"))
        previous_identical = (
            current_path.read_bytes() == previous_path.read_bytes()
            if previous_path.is_file() else None
        )
        result = {
            "case": label,
            "step_count": len(model.steps),
            "citation_count": len(model.citations),
            "narrative_sha256": hashlib.sha256(narrative.encode("utf-8")).hexdigest(),
            "complete_coverage": sorted(indices) == list(range(len(model.steps))),
            "all_after_indices_empty": all(entry.after_indices == () for entry in entries),
            "no_dependency_inversions": len(inversions) == 0,
            "dependency_inversions": inversions,
            "all_suppressed_still_in_dependency_order": suppressed.issubset(set(indices)),
            "matches_r3_40e_snapshot": previous_identical,
            "web_narrative_route": view.key,
        }
        results.append(result)
    return results
