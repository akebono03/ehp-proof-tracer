"""R3-40C limited proof-tree order and common renderer regressions."""

from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_27_typed_statement_projection import project_stable_eta_notation_transition
from phase168_r3_38_frozen_fulltext_audit.audit import capture, sections
from phase168_r3_39f_frozen_comparison.audit import assess
from proof import ProofRule
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition


def result_for(n, k):
    markdown, model, _ = capture(n, k)
    _, proof = sections(markdown)
    return proof, model


def flattened_order(model):
    result = project_narrative_order(model)
    return [index for entry in result
            for index in (entry.step_index, *entry.after_indices)]


def test_all_four_groups_preserve_complete_model_premise_order():
    for n in (2, 3, 4, 5):
        _, model = result_for(n, 1)
        indices = flattened_order(model)
        assert sorted(indices) == list(range(len(model.steps)))
        position = {index: position for position, index in enumerate(indices)}
        for index, step in enumerate(model.steps):
            for premise in step.premises:
                ancestor_indices = [p for p, candidate in enumerate(model.steps)
                                    if candidate is premise]
                if not ancestor_indices:
                    ancestor_indices = [p for p, candidate in enumerate(model.steps)
                                        if candidate == premise]
                assert ancestor_indices
                assert position[ancestor_indices[0]] < position[index]


def test_pi43_quotient_after_source_and_exactness_unchanged():
    proof, model = result_for(3, 1)
    assert proof.index(r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}") < proof.index("準同型定理")
    assert proof.count("次の完全列を考える") == 1
    assert r"\ker E=\mathbb{Z}\{2\eta_{2}\}" in proof


def test_pi54_source_iso_generator_transport_and_conclusion_order():
    proof, model = result_for(4, 1)
    source = proof.index(r"\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}")
    iso = proof.index("(n,m,k)=(3,4,1)")
    generator = proof.index(r"E(\eta_{3})=\eta_{4}")
    transport = proof.index(r"\pi_{5}^{4} = \mathbb{Z}/2\{E")
    conclusion = proof.index(r"\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}")
    assert source < iso < generator < transport < conclusion
    assert project_stable_eta_notation_transition(model, 9) is None


def test_pi65_transport_before_eta_image_and_explicit_iterated_identity():
    proof, model = result_for(5, 1)
    source = proof.index(r"\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}")
    iso = proof.index("(n,m,k)=(3,5,1)")
    transport = proof.index(r"\pi_{6}^{5} = \mathbb{Z}/2\{E^{2}")
    image = proof.index(r"E(\eta_{4})=\eta_{5}")
    transition = proof.index(r"E^{2}\eta_{3}=\eta_{5}")
    conclusion = proof.index(r"\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}")
    assert source < iso < transport < image < transition < conclusion
    assert proof.count(r"E^{2}\eta_{3}=\eta_{5}") == 1
    assert proof.rstrip().endswith("□")


def test_pi65_iterated_eta_identity_has_real_general_definition_citation():
    proof, model = result_for(5, 1)
    rows = [line for line in proof.splitlines() if r"E^{2}\eta_{3}=\eta_{5}" in line]
    assert len(rows) == 1
    allowed = {
        num
        for index, step in enumerate(model.steps)
        if step.rule is ProofRule.GIVEN
        and isinstance(step.conclusion, TodaEtaFamilyGeneralDefinition)
        for num in model.step_citation_numbers[index]
    }
    assert allowed
    assert any(f"[R{num}]" in rows[0] for num in allowed)
    assert "定義より" in rows[0]
    assert len([index for index in range(len(model.steps))
                if project_stable_eta_notation_transition(model, index) is not None]) == 1


def test_frozen_explanation_checklists_stay_twelve_of_twelve():
    for name, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1)):
        body, model = result_for(n, k)
        missing = [item["key"] for item in assess(name, body)
                   if not item["present"]]
        assert not missing, (name, missing)


def test_rendered_references_all_resolve_in_four_groups():
    for n in (2, 3, 4, 5):
        proof, model = result_for(n, 1)
        existing = {citation.number for citation in model.citations}
        assert existing
        for index, numbers in enumerate(model.step_citation_numbers):
            assert all(number in existing for number in numbers), index
        assert proof.rstrip().endswith("□")
