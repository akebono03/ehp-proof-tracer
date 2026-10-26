"""R3Q: one map-property prose route, justified by typed proof premises."""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaHopfInvariantMap,
    TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase169_r3j1_narrative_import_isolation.audit import capture_actual_narrative
from proof import ProofRule, ProofStep
from toda_rules import (
    TodaDeltaInjectiveStatement, TodaDeltaZeroStatement,
    TodaHopfInvariantSurjectiveStatement, TodaHopfInvariantZeroStatement,
    TodaProp42ExactnessStatement, TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


def _step(statement, *premises):
    return ProofStep(conclusion=statement, premises=tuple(premises), rule=ProofRule.INFERENCE)


def _groups():
    g63 = TodaPrimaryGroup(6, 3)
    g65 = TodaPrimaryGroup(6, 5)
    g42 = TodaPrimaryGroup(4, 2)
    g53 = TodaPrimaryGroup(5, 3)
    g55 = TodaPrimaryGroup(5, 5)
    g32 = TodaPrimaryGroup(3, 2)
    return g63, g65, g42, g53, g55, g32


def test_delta_zero_uses_h_surjectivity_then_exactness():
    g63, g65, g42, _, _, _ = _groups()
    window = TodaEHPExactnessWindow(
        source_term=g63, middle_term=g65, target_term=g42,
        first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP,
    )
    mapping = TodaDeltaMap(g65, g42)
    proof = _step(
        TodaDeltaZeroStatement(map=mapping),
        _step(TodaHopfInvariantSurjectiveStatement(map=TodaHopfInvariantMap(g63, g65))),
        _step(TodaProp42ExactnessStatement(window)),
    )
    sentence = typed_sentence(proof.conclusion, proof)
    assert sentence is not None
    assert r"\ker\Delta=\operatorname{Im}H=\pi_{6}^{5}" in sentence
    assert r"\operatorname{Im}\Delta=\ker E=0" not in sentence


def test_delta_zero_from_suspension_isomorphism_and_exactness():
    middle = TodaPrimaryGroup(1, 1)
    source = TodaPrimaryGroup(3, 3)
    final = TodaPrimaryGroup(2, 2)
    mapping = TodaDeltaMap(source, middle)
    window = TodaEHPExactnessWindow(
        source_term=source, middle_term=middle, target_term=final,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    )
    proof = _step(
        TodaDeltaZeroStatement(map=mapping),
        _step(TodaSuspensionIsomorphismStatement(map=TodaSuspensionMap(middle, final))),
        _step(TodaProp42ExactnessStatement(window)),
    )
    sentence = typed_sentence(proof.conclusion, proof)
    assert sentence is not None
    assert "完全性より" in sentence
    assert r"\operatorname{Im}\Delta=\ker E=0" in sentence
    assert r"\Delta: \pi_{3}^{3}\to \pi_{1}^{1}" in sentence


def test_delta_zero_does_not_claim_kernel_from_unrelated_suspension():
    middle = TodaPrimaryGroup(1, 1)
    source = TodaPrimaryGroup(3, 3)
    final = TodaPrimaryGroup(2, 2)
    mapping = TodaDeltaMap(source, middle)
    window = TodaEHPExactnessWindow(
        source_term=source, middle_term=middle, target_term=final,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    )
    unrelated = TodaSuspensionMap(TodaPrimaryGroup(4, 3), TodaPrimaryGroup(5, 4))
    proof = _step(
        TodaDeltaZeroStatement(map=mapping),
        _step(TodaSuspensionIsomorphismStatement(map=unrelated)),
        _step(TodaProp42ExactnessStatement(window)),
    )
    assert r"\operatorname{Im}\Delta=\ker E=0" not in typed_sentence(proof.conclusion, proof)


def test_delta_zero_does_not_claim_kernel_from_unrelated_window():
    middle = TodaPrimaryGroup(1, 1)
    source = TodaPrimaryGroup(3, 3)
    final = TodaPrimaryGroup(2, 2)
    mapping = TodaDeltaMap(source, middle)
    unrelated_window = TodaEHPExactnessWindow(
        source_term=middle, middle_term=final, target_term=TodaPrimaryGroup(3, 3),
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    )
    proof = _step(
        TodaDeltaZeroStatement(map=mapping),
        _step(TodaSuspensionIsomorphismStatement(map=TodaSuspensionMap(middle, final))),
        _step(TodaProp42ExactnessStatement(unrelated_window)),
    )
    assert r"\operatorname{Im}\Delta=\ker E=0" not in typed_sentence(proof.conclusion, proof)


def test_e_injective_from_delta_zero_and_exactness():
    _, g65, g42, g53, _, _ = _groups()
    mapping = TodaSuspensionMap(g42, g53)
    window = TodaEHPExactnessWindow(
        source_term=g65, middle_term=g42, target_term=g53,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    )
    proof = _step(
        TodaSuspensionInjectiveStatement(map=mapping),
        _step(TodaDeltaZeroStatement(map=TodaDeltaMap(g65, g42))),
        _step(TodaProp42ExactnessStatement(window)),
    )
    assert r"完全性より, $\ker E=\operatorname{Im}\Delta=0$" in typed_sentence(proof.conclusion, proof)


def test_h_zero_from_delta_injective_and_exactness():
    _, _, _, g53, g55, g32 = _groups()
    mapping = TodaHopfInvariantMap(g53, g55)
    window = TodaEHPExactnessWindow(
        source_term=g53, middle_term=g55, target_term=g32,
        first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP,
    )
    proof = _step(
        TodaHopfInvariantZeroStatement(map=mapping),
        _step(TodaDeltaInjectiveStatement(map=TodaDeltaMap(g55, g32))),
        _step(TodaProp42ExactnessStatement(window)),
    )
    assert r"完全性より, $\operatorname{Im}H=\ker\Delta=0$" in typed_sentence(proof.conclusion, proof)


def test_e_surjective_from_h_zero_and_exactness():
    _, _, g42, g53, g55, _ = _groups()
    mapping = TodaSuspensionMap(g42, g53)
    window = TodaEHPExactnessWindow(
        source_term=g42, middle_term=g53, target_term=g55,
        first_map=EHP_E_MAP, second_map=EHP_H_MAP,
    )
    proof = _step(
        TodaSuspensionSurjectiveStatement(map=mapping),
        _step(TodaHopfInvariantZeroStatement(map=TodaHopfInvariantMap(g53, g55))),
        _step(TodaProp42ExactnessStatement(window)),
    )
    assert r"完全性より, $\operatorname{Im}E=\ker H=\pi_{5}^{3}$" in typed_sentence(proof.conclusion, proof)


def test_toda_suspension_isomorphism_mentions_both_properties():
    _, _, g42, g53, _, _ = _groups()
    mapping = TodaSuspensionMap(g42, g53)
    proof = _step(
        TodaSuspensionIsomorphismStatement(map=mapping),
        _step(TodaSuspensionInjectiveStatement(map=mapping)),
        _step(TodaSuspensionSurjectiveStatement(map=mapping)),
    )
    sentence = typed_sentence(proof.conclusion, proof)
    assert sentence is not None
    assert "単射性と全射性より" in sentence
    assert r"E: \pi_{4}^{2}\to \pi_{5}^{3}" in sentence


def test_isomorphism_with_wrong_map_witness_does_not_claim_both():
    _, _, g42, g53, _, _ = _groups()
    mapping = TodaSuspensionMap(g42, g53)
    different = TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4))
    proof = _step(
        TodaSuspensionIsomorphismStatement(map=mapping),
        _step(TodaSuspensionInjectiveStatement(map=mapping)),
        _step(TodaSuspensionSurjectiveStatement(map=different)),
    )
    assert "単射性と全射性より" not in typed_sentence(proof.conclusion, proof)


def test_unrelated_exactness_window_does_not_justify_e_injectivity():
    _, g65, g42, g53, _, _ = _groups()
    mapping = TodaSuspensionMap(g42, g53)
    unrelated = TodaEHPExactnessWindow(
        source_term=g42, middle_term=g53, target_term=TodaPrimaryGroup(5, 5),
        first_map=EHP_E_MAP, second_map=EHP_H_MAP,
    )
    proof = _step(
        TodaSuspensionInjectiveStatement(map=mapping),
        _step(TodaDeltaZeroStatement(map=TodaDeltaMap(g65, g42))),
        _step(TodaProp42ExactnessStatement(unrelated)),
    )
    sentence = typed_sentence(proof.conclusion, proof)
    assert r"\ker E=\operatorname{Im}\Delta=0" not in sentence
    assert "完全性より" not in sentence


def test_public_pi5_3_single_reasoned_path():
    result, model, markdown, view = capture_actual_narrative()
    assert result.status.value == "complete"
    assert view.key == "generic-complete-proof"
    assert "単射性と全射性より" in markdown
    assert r"\ker E=\operatorname{Im}\Delta=0" in markdown
    assert r"\operatorname{Im}H=\ker\Delta=0" in markdown
    assert r"\operatorname{Im}E=\ker H=\pi_{5}^{3}" in markdown
    assert "is surjective" not in markdown
    assert "is injective" not in markdown
    assert "is an isomorphism" not in markdown


def test_common_renderer_has_no_extra_phase_specific_prose_fork():
    import inspect
    import phase168_r3_5_model_renderer as renderer
    source = inspect.getsource(renderer.render_model_backed_narrative_markdown)
    assert "project_ehp_reasoned_lines" not in source
    assert "source_bodies_for_terminal_proof" not in source
    assert "sentence = typed_sentence(step.conclusion, step)" in source
    assert "elif body_line is not None:" in source
