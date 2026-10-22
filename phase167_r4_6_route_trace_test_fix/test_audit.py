from phase167_r4_6_route_trace.audit import matching_lines


def test_trace_matching_lines():
    content = "$\\pi_{n}^{n}$.\n$\\pi_{5}^{5}$."
    lines = matching_lines(content)
    assert len(lines) == 2


def test_trace_ignores_other_content():
    assert matching_lines("ordinary text") == []
