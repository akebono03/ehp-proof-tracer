def audit_citation_projection(model: object, bridge: object,
                              markdown: str, view: object) -> dict:
    """Check explicit source link provenance and both raw/Web Reference bodies.

    A reference lacking a body is reported as a gap, not silently called verified.
    Inference-only references are distinguished from registered assertion bodies.
    """
    raw_reference = markdown_reference_text(markdown)
    web_reference = web_reference_text(view)
    raw_compact = normalize_visible(raw_reference)
    web_compact = normalize_visible(web_reference)
    steps = model.steps
    citations = model.citations
    index = {citation.number: citation for citation in citations}
    issues = []
    if len(index) != len(citations) or set(index) != set(range(1, len(citations) + 1)):
        issues.append("NONCONTIGUOUS_OR_DUPLICATE_CITATION_NUMBERS")
    if len(model.step_citation_numbers) != len(steps):
        issues.append("STEP_CITATION_MAPPING_LENGTH")

    used_given = [step for step in steps
                  if getattr(getattr(step, "rule", None), "value", None) == "given"]
    used_links = [link for link in bridge.proof_links
                  if link.step is not None and any(
                      link.step is step or link.step == step for step in used_given)]
    linked_ids = {link.assertion_id for link in used_links}
    mapped_ids = set()
    citation_rows = []
    for citation in citations:
        locator = citation.reference.locator or citation.reference.label
        expected_heading = f"[R{citation.number}] {locator}."
        heading_raw = f"**{expected_heading}**"
        raw_heading_count = raw_reference.count(heading_raw)
        web_heading = normalize_visible(expected_heading) in web_compact
        if raw_heading_count != 1:
            issues.append(f"REFERENCE_HEADING_MISMATCH:R{citation.number}")
        if not web_heading:
            issues.append(f"REFERENCE_HEADING_NOT_IN_WEB:R{citation.number}")
        unexpected_ids = set(citation.assertion_ids) - linked_ids
        if unexpected_ids:
            issues.append(f"UNMATCHED_ASSERTION_LINK:R{citation.number}")
        mapped_ids.update(citation.assertion_ids)
        bodies = []
        for body in citation.statement_bodies:
            compact = normalize_visible(body)
            visible_in_raw = compact in raw_compact
            visible_in_web = compact in web_compact
            if not visible_in_raw:
                issues.append(f"REFERENCE_BODY_NOT_RENDERED:R{citation.number}")
            if not visible_in_web:
                issues.append(f"REFERENCE_BODY_NOT_IN_WEB:R{citation.number}")
            bodies.append({"body": body, "raw_reference_present": visible_in_raw,
                           "web_reference_present": visible_in_web})
        if not bodies:
            issue = ("REGISTERED_ASSERTION_BODY_MISSING" if citation.assertion_ids
                     else "INFERENCE_OR_RULE_ONLY_BODY_MISSING")
            issues.append(f"{issue}:R{citation.number}")
        for step_index in citation.step_indices:
            if step_index not in range(len(steps)):
                issues.append(f"CITATION_NONEXISTENT_STEP:R{citation.number}")
            elif (step_index >= len(model.step_citation_numbers)
                  or citation.number not in model.step_citation_numbers[step_index]):
                issues.append(f"CITATION_STEP_MAP_DISAGREES:R{citation.number}")
        citation_rows.append({
            "number": citation.number,
            "locator": locator,
            "step_indices": list(citation.step_indices),
            "assertion_ids": list(citation.assertion_ids),
            "reference_ids": list(citation.reference_ids),
            "body_count": len(bodies),
            "bodies": bodies,
            "raw_heading_count": raw_heading_count,
            "web_heading": web_heading,
        })
    for step_index, numbers in enumerate(model.step_citation_numbers):
        for number in numbers:
            if number not in index or step_index not in index[number].step_indices:
                issues.append(f"STEP_MAP_UNMATCHED_REFERENCE:step={step_index}:R{number}")
    lost_links = linked_ids - mapped_ids
    if lost_links:
        issues.append("USED_PROOF_LINK_OMITTED_FROM_MODEL")
    unlinked_givens = []
    for step_index, step in enumerate(steps):
        if step not in used_given:
            continue
        if step_index >= len(model.step_citation_numbers) or not model.step_citation_numbers[step_index]:
            unlinked_givens.append(step_index)
    # An unlinked GIVEN may be a mathematical base fact. Report it, do not invent a source.
    if unlinked_givens:
        issues.append("GIVEN_WITHOUT_CITATION")
    allowed = set(index)
    _, proof_text = split_narrative_sections(markdown)
    used_proof_tags = {int(number) for number in re.findall(
        r"\[R(\d+)\]", proof_text)}
    dangling_tags = sorted(used_proof_tags - allowed)
    if dangling_tags:
        issues.append("PROOF_REFERENCES_NONEXISTENT_CITATION")
    return {
        "citations": citation_rows,
        "used_registered_link_count": len(used_links),
        "used_registered_assertion_ids": sorted(linked_ids),
        "unmapped_used_assertion_ids": sorted(lost_links),
        "unlinked_given_step_indices": unlinked_givens,
        "proof_reference_numbers": sorted(used_proof_tags),
        "dangling_reference_numbers": dangling_tags,
        "issues": sorted(set(issues)),
    }
