from toda_group_proof_narrative_reason_renderer import finalize_phase165_r49_typed_reason_order


def test_phase165_r49_display_order_on_real_pi32_reasons():
    from toda_group_query import TodaGroupQuery
    from toda_calculation_facade import build_standard_toda_report
    from phase164_r5_r2_common_replay import build_phase164_r5_r2_common_replay
    from toda_group_proof_presentation import build_toda_group_proof_presentation
    from toda_group_proof_narrative_semantics import (
        build_toda_group_proof_narrative_semantic_closure_presentation,
        build_toda_group_proof_narrative_semantic_sidecar,
    )
    from toda_group_proof_narrative_reasons import build_toda_group_proof_narrative_reason_sidecar
    from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
    from toda_group_query_semantics import classify_toda_group_query_domain

    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(n=2, k=1, max_depth=2, mode='narrative')
    text = '\n'.join(line.prefix + (line.statement_latex or '') + line.suffix for line in view.rendered_lines)
    assert '単射性と全射性より' in text
    assert 'Im' in text and 'ker' in text
    assert text.index('は単射') < text.index('は全射') < text.index('単射性と全射性より')
    assert text.count('は零写像') == 1
    assert text.count('は同型') >= 1
