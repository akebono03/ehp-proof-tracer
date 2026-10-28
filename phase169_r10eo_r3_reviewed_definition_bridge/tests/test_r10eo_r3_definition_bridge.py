"""R10EO-R3: checked Definition leaves and unchanged generic inference guards."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    StableFamilyMemberDefinition,
    canonical_member,
    cited_family_reference_sentence,
    expand_cited_stable_family,
)
from phase169_r10eo_r3_reviewed_definition_bridge.reviewed_definitions import (
    MANIFEST,
    REVIEWED_ATTESTATIONS,
    ROOT,
    build_cited_reviewed_definitions,
    reviewed_definition_ids,
    verified_reviewed_definitions,
)
from proof import (
    ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule,
)
from unified_statement_registry import AssertionOrigin, ReferenceKind


def _source(family_id: int) -> CitedStableFamilyDefinition:
    row, = [entry for entry in read_registered_stable_families()
            if entry.family_id == family_id]
    return CitedStableFamilyDefinition(row.family_id, row.minimum_n, row.stem)


def test_r10eo_r3_one_attested_source_with_checked_position():
    checked = verified_reviewed_definitions()
    assert len(checked) == 1
    record, occurrence, position = checked[0]
    assert record.family_id == 16
    assert occurrence.family_id == record.family_id
    assert occurrence.classification == "TEXT_ONLY_NOT_CITED"
    assert occurrence.source_sha256 == record.source_sha256
    assert position == 10800 + occurrence.line
    assert record.family_id in reviewed_definition_ids()


def test_r10eo_r3_source_admission_requires_actual_cited_given():
    bridge = build_cited_reviewed_definitions()
    assert len(bridge.proof_links) == 1
    link, = bridge.proof_links
    assertion = bridge.registry.assertion(link.assertion_id)
    reference = bridge.registry.reference(assertion.reference_id)
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert assertion.content == _source(16)
    assert reference.kind is ReferenceKind.DEFINITION
    assert "original edition unverified" in reference.source_id
    assert link.step is not None
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()
    assert link.step.conclusion == assertion.content


def test_r10eo_r3_existing_generic_image_rule_proves_typed_zeta_image():
    source = _source(16)
    link, = build_cited_reviewed_definitions().proof_links
    leaf = link.step
    assert leaf is not None
    steps = []
    for n in (13, 14):
        member = canonical_member(source, n)
        assert isinstance(member, StableFamilyMemberDefinition)
        options = expand_cited_stable_family(member, (source,))
        assert len(options) == 1
        matches = find_inference_matches_for_rule(options[0].rule, (leaf,))
        assert len(matches) == 1
        step = apply_inference_match(matches[0])
        assert step.rule is ProofRule.INFERENCE
        assert step.premises == (leaf,)
        steps.append(step)
    first = steps[0].conclusion.element
    second = steps[1].conclusion.element
    goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(24, 13), TodaPrimaryGroup(25, 14)),
        first, second,
    )
    assert expand_cited_stable_family(goal, ()) == ()
    options = expand_cited_stable_family(goal, (source,))
    assert len(options) == 1
    matches = find_inference_matches_for_rule(options[0].rule, tuple(steps))
    assert len(matches) == 1
    result = apply_inference_match(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == tuple(steps)
    assert cited_family_reference_sentence(source) is not None


def test_r10eo_r3_reject_forged_member_or_image_given():
    source = _source(16)
    first = canonical_member(source, 13)
    second = canonical_member(source, 14)
    assert first is not None and second is not None
    goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(24, 13), TodaPrimaryGroup(25, 14)),
        first.element, second.element,
    )
    option, = expand_cited_stable_family(goal, (source,))
    forged = (ProofStep(first, (), ProofRule.GIVEN),
              ProofStep(second, (), ProofRule.GIVEN))
    assert find_inference_matches_for_rule(option.rule, forged) == ()
    assert canonical_member(replace(source, stem=12), 13) is None


def test_r10eo_r3_unknown_csv_id_not_promoted():
    row, = (entry for entry in read_registered_stable_families()
            if entry.family_id == 103)
    fake = CitedStableFamilyDefinition(row.family_id, row.minimum_n, row.stem)
    assert canonical_member(fake, row.minimum_n) is None
    assert cited_family_reference_sentence(fake) is None


def test_r10eo_r3_refuse_modified_transcription(tmp_path):
    source = tmp_path / "sources" / "toda" / "Toda_06_2.tex"
    source.parent.mkdir(parents=True)
    existing = (ROOT / "sources" / "toda" / "Toda_06_2.tex").read_text(
        encoding="utf-8-sig",
    )
    source.write_text(existing.replace(
        r"\zeta_{n}:=E^{\,n-5}\zeta_{5}",
        r"\zeta_{n}:=E^{\,n-6}\zeta_{5}",
    ), encoding="utf-8")
    folder = tmp_path / "data"
    folder.mkdir()
    (folder / "HyoujiGen.csv").write_bytes(
        (ROOT / "data" / "HyoujiGen.csv").read_bytes(),
    )
    with pytest.raises(ValueError, match="absent or ambiguous"):
        verified_reviewed_definitions(root=tmp_path, manifest_path=MANIFEST)


def test_r10eo_r3_refuse_unreviewed_attestation_metadata():
    record, = REVIEWED_ATTESTATIONS
    forged = replace(record, line=record.line + 1)
    with pytest.raises(ValueError, match="fingerprint, line or paragraph"):
        verified_reviewed_definitions(attestations=(forged,))
    forged_type = replace(record, stem=12)
    with pytest.raises(ValueError, match="metadata disagrees"):
        verified_reviewed_definitions(attestations=(forged_type,))


def test_r10eo_r3_preserves_old_definition_registrations():
    from phase169_r10d2_general_family_definition.family_citation import (
        build_cited_stable_family_definitions,
    )
    from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
        build_cited_chapter_vi_family_definitions,
    )
    assert len(build_cited_stable_family_definitions().proof_links) == 2
    assert len(build_cited_chapter_vi_family_definitions().proof_links) == 3


def test_r10eo_r3_guarded_patcher_has_complete_functions():
    from phase169_r10eo_r3_reviewed_definition_bridge.patch import (
        HERE, function_span,
    )
    functions = HERE / "full_functions"
    for name in ("canonical_member.py", "cited_family_reference_sentence.py",
                 "build_shared_typed_bridge.py"):
        source = (functions / name).read_text(encoding="utf-8")
        function_name = name.removesuffix(".py")
        assert function_span(source, function_name) == (0, len(source))
