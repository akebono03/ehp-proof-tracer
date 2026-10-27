"""R10E8 focused source and proof tests; no per-element rule implemented."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, StableFamilyMemberDefinition,
    build_cited_stable_family_definitions, canonical_member,
    cited_family_reference_sentence, expand_cited_stable_family,
    verified_source_positions,
)
from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
    CHAPTER_VI_SOURCE, build_cited_chapter_vi_family_definitions,
    verified_chapter_vi_source_positions,
)
from phase169_r10e8_hyoujigen_generic_suspension.patch import (
    transformed_sources,
)
from phase169_r10e8_hyoujigen_generic_suspension.source_records import (
    CHAPTER_VI_SOURCE_RECORDS,
)
from proof import (
    ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule,
)
from unified_statement_registry import AssertionOrigin


def _family_source(family_id: int) -> CitedStableFamilyDefinition:
    family, = (row for row in read_registered_stable_families()
               if row.family_id == family_id)
    return CitedStableFamilyDefinition(
        family.family_id, family.minimum_n, family.stem,
    )


def _image(family_id: int, n: int) -> GeneratorImage:
    source = _family_source(family_id)
    first = canonical_member(source, n)
    second = canonical_member(source, n + 1)
    assert first is not None and second is not None
    return GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(n + source.stem, n),
            TodaPrimaryGroup(n + source.stem + 1, n + 1),
        ), first.element, second.element,
    )


def test_r10e8_chapter_v_historical_api_unchanged():
    assert dict(verified_source_positions()) == {4: 8550, 9: 10450}
    assert len(build_cited_stable_family_definitions().proof_links) == 2


def test_r10e8_three_source_clauses_are_distinct_and_source_ordered():
    rows = verified_chapter_vi_source_positions()
    assert tuple(id for id, _ in rows) == (10, 11, 12)
    assert tuple(pos for _, pos in rows) == tuple(sorted(pos for _, pos in rows))
    bridge = build_cited_chapter_vi_family_definitions()
    assert len(bridge.proof_links) == 3
    assert len(bridge.registry._assertions) == 3
    for link in bridge.proof_links:
        assert link.step is not None
        assert link.step.rule is ProofRule.GIVEN
        assert link.step.premises == ()
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
        assert assertion.content == link.step.conclusion
        assert reference.publication_position is not None
        assert "original edition unverified" in reference.source_id


@pytest.mark.parametrize("family_id,n", [(10, 10), (11, 10), (12, 11)])
def test_r10e8_every_image_has_two_real_inferred_definitions(family_id, n):
    source = _family_source(family_id)
    bridge = build_cited_chapter_vi_family_definitions()
    leaf, = (link.step for link in bridge.proof_links
             if link.step is not None and link.step.conclusion == source)
    inferred_definitions = []
    for index in (n, n + 1):
        member = canonical_member(source, index)
        assert isinstance(member, StableFamilyMemberDefinition)
        options = expand_cited_stable_family(member, (source,))
        assert len(options) == 1
        matches = find_inference_matches_for_rule(options[0].rule, (leaf,))
        assert len(matches) == 1
        step = apply_inference_match(matches[0])
        assert step.rule is ProofRule.INFERENCE
        assert step.premises == (leaf,)
        inferred_definitions.append(step)
    image = _image(family_id, n)
    options = expand_cited_stable_family(image, (source,))
    assert len(options) == 1
    matches = find_inference_matches_for_rule(
        options[0].rule, tuple(inferred_definitions),
    )
    assert len(matches) == 1
    final = apply_inference_match(matches[0])
    assert final.rule is ProofRule.INFERENCE
    assert final.conclusion == image
    assert final.premises == tuple(inferred_definitions)
    assert cited_family_reference_sentence(source) is not None


@pytest.mark.parametrize("family_id,n", [(10, 10), (11, 10), (12, 11)])
def test_r10e8_csv_metadata_without_citation_never_proves_image(family_id, n):
    image = _image(family_id, n)
    assert expand_cited_stable_family(image, ()) == ()
    source = _family_source(family_id)
    options = expand_cited_stable_family(image, (source,))
    assert len(options) == 1
    first, second = options[0].subgoals
    forged = (ProofStep(first, (), ProofRule.GIVEN),
              ProofStep(second, (), ProofRule.GIVEN))
    assert find_inference_matches_for_rule(options[0].rule, forged) == ()
    assert expand_cited_stable_family(replace(image,
        target_generator=replace(image.target_generator,
                                 source=image.target_generator.source + 1)),
        (source,)) == ()


def test_r10e8_tampered_chapter_vi_definition_rejected(tmp_path):
    original = CHAPTER_VI_SOURCE.read_text(encoding="utf-8-sig")
    altered = original.replace(CHAPTER_VI_SOURCE_RECORDS[0].defining_clause,
                               r"\varepsilon_n:=E^{\,n-4}\varepsilon_3\quad (n\ge3)")
    path = tmp_path / "Toda_06_2.tex"
    path.write_text(altered, encoding="utf-8")
    with pytest.raises(ValueError, match="Chapter VI source clause"):
        verified_chapter_vi_source_positions(source_path=path)


def test_r10e8_tampered_source_anchor_rejected(tmp_path):
    original = CHAPTER_VI_SOURCE.read_text(encoding="utf-8-sig")
    marker = CHAPTER_VI_SOURCE_RECORDS[1].paragraph_start
    altered = original.replace(marker, marker + marker)
    path = tmp_path / "Toda_06_2.tex"
    path.write_text(altered, encoding="utf-8")
    with pytest.raises(ValueError, match="Chapter VI source clause"):
        verified_chapter_vi_source_positions(source_path=path)


def test_r10e8_new_sourced_families_still_distinct():
    all_types = {_family_source(i).family_id: _family_source(i)
                 for i in (10, 11, 12)}
    assert len(all_types) == 3
    first = _image(10, 10)
    assert expand_cited_stable_family(first, (all_types[11],)) == ()
    assert expand_cited_stable_family(first, (all_types[10],))


def test_r10e8_patcher_has_source_guard():
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    original_a = (root / "phase169_r10d2_general_family_definition" /
                  "family_citation.py").read_text(encoding="utf-8")
    original_b = (root / "phase165_r52_r9_shared_math.py").read_text(
        encoding="utf-8",
    )
    assert "CHAPTER_VI_SOURCE_RECORDS" in original_a
    assert "build_cited_chapter_vi_family_definitions" in original_b
    with pytest.raises(RuntimeError, match="R10D2 family guard changed"):
        transformed_sources(original_a, original_b)
