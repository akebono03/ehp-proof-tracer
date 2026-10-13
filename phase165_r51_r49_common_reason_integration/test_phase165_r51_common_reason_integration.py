from pathlib import Path

from toda_group_proof_narrative_reason_renderer import (
    finalize_phase165_r49_typed_reason_order,
)
from web_group_proof import build_standard_web_group_proof_view


def test_r51_shared_renderer_owns_r49_ordering():
    assert finalize_phase165_r49_typed_reason_order.__module__ == (
        'toda_group_proof_narrative_reason_renderer'
    )
    view = build_standard_web_group_proof_view(n=2, k=1, max_depth=2, mode='narrative')
    text = '\n'.join(line.prefix + (line.statement_latex or '') + line.suffix for line in view.rendered_lines)
    assert text.index('は単射') < text.index('は全射') < text.index('単射性と全射性より')
    assert r'\operatorname{Im}' in text
    assert r'\ker E=0' in text
    assert text.count('は零写像') == 1
    assert '(5.1)' in text and 'Proposition 4.2' in text and 'Proposition 5.1' in text
