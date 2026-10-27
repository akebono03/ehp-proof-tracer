def build_typed_literature_bridge(source_bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Produce two fixed, source-bound general claims; never promote other archive rows."""
    verify_prop44_hopf_fibration_source()
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for locator, source_id, digest, tokens, claim, kind in _SOURCES:
        candidates = [
            a for a in source_bridge.registry._assertions.values()
            if a.origin is AssertionOrigin.SOURCE_ARCHIVE
            and isinstance(a.content, dict)
            and a.content.get("source_statement_id") == source_id
        ]
        if len(candidates) != 1:
            raise ValueError(f"unique source archive entry required: {locator}")
        archive = candidates[0].content
        text = archive.get("source_text")
        if (not isinstance(text, str) or archive.get("source_sha256") != digest
                or any(token not in text for token in tokens)):
            raise ValueError(f"source content does not match reviewed scope: {locator}")
        ref_id = f"typed_literature:{source_id}"
        assertion_id = f"typed_literature:assertion:{source_id}"
        registry.add_reference(LiteratureEntry(ref_id, kind, locator, source_id=source_id))
        registry.add_assertion(AssertionEntry(
            assertion_id, ref_id, AssertionKind.STATEMENT, claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=claim, premises=(), rule=ProofRule.GIVEN,
        )))
        records.append(MigrationRecord(
            "phase165_r52_r27_r5", locator, assertion_id,
            MigrationStatus.STRUCTURED, "typed universal literature claim; specialization not certified",
        ))
    _register_toda45(registry, links, records, source_bridge)
    return RegistryBridgeResult(registry, tuple(records), tuple(links))

