from dataclasses import replace
import hashlib

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_tex_citation_policy import (
    TexCitationStatus,
    assess_adopted_tex_citation,
)
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin,
    LiteratureEntry, ReferenceKind, UnifiedStatementRegistry,
)


def make_bridge():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "tex:r", ReferenceKind.PROPOSITION, "Proposition T",
        source_id="Toda translated TeX; not original edition verified",
        publication_position=1,
    ))
    for key, index in (("first", 1), ("second", 2)):
        text = f"source assertion {key}"
        registry.add_assertion(AssertionEntry(
            key, "tex:r", AssertionKind.STATEMENT,
            {"source_text": text,
             "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
             "source_position": index},
            origin=AssertionOrigin.SOURCE_ARCHIVE,
        ))
    return RegistryBridgeResult(registry, (), ())


def test_adopted_tex_source_is_citable_without_paper_comparison():
    result = assess_adopted_tex_citation(make_bridge(), "first")
    assert result.status is TexCitationStatus.ALLOWED
    assert result.usable_as_reference
    assert result.proof_step_eligible is False


def test_adopted_tex_citation_enforces_prior_position():
    bridge = make_bridge()
    assert assess_adopted_tex_citation(
        bridge, "first", citing_assertion_id="second"
    ).status is TexCitationStatus.ALLOWED
    assert assess_adopted_tex_citation(
        bridge, "second", citing_assertion_id="first"
    ).status is TexCitationStatus.DENIED


def test_source_integrity_failure_rejected():
    bridge = make_bridge()
    old = bridge.registry.assertion("first")
    bridge.registry._assertions["first"] = replace(
        old, content={**old.content, "source_text": "tampered"}
    )
    assert assess_adopted_tex_citation(
        bridge, "first"
    ).status is TexCitationStatus.DENIED


def test_untyped_archive_never_becomes_proof_step():
    result = assess_adopted_tex_citation(make_bridge(), "second")
    assert result.proof_step_eligible is False
