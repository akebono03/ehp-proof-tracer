from toda_calculation_facade import build_standard_toda_report
from toda_group_query import TodaGroupQuery
from toda_group_query_semantics import classify_toda_group_query_domain
from phase164_r5_r2_common_replay import build_phase164_r5_r2_common_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
)
from web_group_proof import build_standard_web_group_proof_view


def test_r50_pi32_keeps_adopted_typed_literature_leaves():
    view = build_standard_web_group_proof_view(n=2, k=1, max_depth=2, mode='narrative')
    replay = view.presentation.source_replay if hasattr(view, 'presentation') else None
    if replay is None:
        report = build_standard_toda_report(n=2, k=1)
        result = report.candidates[0].source_candidate.group_result
        replay = build_phase164_r5_r2_common_replay(2, 1, result, 2, 'narrative')
    presentation = build_toda_group_proof_presentation(replay)
    entries = build_toda_group_proof_narrative_reference_entries(presentation)
    assert {'(5.1)', 'Proposition 5.1', 'Proposition 4.2'} <= {entry.reference.locator for entry in entries}
    kept = filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(entries, presentation.root_step)
    assert {'(5.1)', 'Proposition 5.1', 'Proposition 4.2'} <= {entry.reference.locator for entry in kept}


def test_r50_pi32_web_reference_section_not_empty_and_reason_order_preserved():
    view = build_standard_web_group_proof_view(n=2, k=1, max_depth=2, mode='narrative')
    text = '\n'.join(line.prefix + (line.statement_latex or '') + line.suffix for line in view.rendered_lines)
    reference = text.split('使用する結果', 1)[1].split('証明', 1)[0]
    assert '[R1]' in reference
    assert '(5.1)' in reference
    assert 'Proposition 5.1' in reference
    assert 'Proposition 4.2' in reference
    assert text.index('は単射') < text.index('は全射') < text.index('単射性と全射性より')
    assert 'Im' in text and 'ker' in text
