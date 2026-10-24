def build_cited_eta_family_definition(source_path: Path) -> RegistryBridgeResult:
    path = Path(source_path)
    data = path.read_text(encoding="utf-8-sig")
    # Verify full content, not a guessed citation inferred from the target.
    required = (r"\(n\ge2\) に対し", r"\eta_n=E^{\,n-2}\eta_2")
    if not all(part in data for part in required):
        raise ValueError("Toda chapter V general eta-family clause not verified")
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID, kind=ReferenceKind.DEFINITION,
        locator="Chapter V, i)",
        source_id="sources/toda/Toda_05_2.tex (adopted transcription, original edition unverified)",
    ))
    general = TodaEtaFamilyGeneralDefinition()
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        kind=AssertionKind.DEFINITION, content=general,
        origin=AssertionOrigin.FIXED_STATEMENT, defined_symbol="eta_n", scope="n>=2",
    ))
    step = ProofStep(general, (), ProofRule.GIVEN, inference_rule=InferenceRule(
        name="Toda chapter V eta-family notation",
        literature_reference=LiteratureReference(label="Toda Chapter V eta notation", locator="Chapter V, i)"),
    ))
    return RegistryBridgeResult(registry, (), (ProofStepLink(ASSERTION_ID, step=step),))
