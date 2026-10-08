from test_phase161_reference_range_render import _entry
from toda_group_proof_narrative_references import (
    render_toda_group_proof_narrative_reference_entries_markdown,
)


def test_phase161_reference_range_whitespace_exact_and_no_duplicates():
    entries = (
        _entry(1, '(5.2)', 'Toda 5.2 eta_2 composition isomorphism'),
        _entry(2, 'Proposition 5.1', 'Toda Proposition 5.1 finite-dimensional integration'),
    )
    statements = {
        1: (r'$\eta_2\circ-:\pi_i^3\to\pi_i^2$ は同型.',),
        2: (r'$\pi_{n+1}^n=\mathbb{Z}/2\{\eta_n\}$.',),
    }
    rendered = render_toda_group_proof_narrative_reference_entries_markdown(
        entries, statements
    )
    assert r'(i \ge 3)' in rendered
    assert r'(n \ge 3)' in rendered
    assert r'\ge  3' not in rendered
    assert rendered.count(r'(i \ge 3)') == 1
    assert rendered.count(r'(n \ge 3)') == 1
