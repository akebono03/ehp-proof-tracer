"""Lightweight isolated audit tests. No project source imports required."""
from audit import analyze, normalize, parent_path, risk_tags


def sample():
    return {
        "summary": {"nodes": 3, "presentation_edges": 2},
        "steps": [
            {"id": 0, "parent_node_ids": [], "premise_node_ids": [1], "statement_latex": "C"},
            {"id": 1, "parent_node_ids": [0], "premise_node_ids": [2], "statement_latex": "H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"},
            {"id": 2, "parent_node_ids": [1], "premise_node_ids": [], "statement_latex": "H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"},
        ],
        "body_lines": [
            {"line": 7, "text": "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は全射.", "math": ["H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"], "candidate_step_ids": [1, 2], "origin": "STEP_EXACT_MATH"},
            {"line": 8, "text": "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は全射.", "math": ["H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"], "candidate_step_ids": [1, 2], "origin": "STEP_EXACT_MATH"},
        ],
        "transport_paragraph": None,
    }


def test_phase162_r10_r6_dependency_chain():
    steps = {i["id"]: i for i in sample()["steps"]}
    assert parent_path(2, steps, [0]) == [2, 1, 0]


def test_phase162_r10_r6_duplicate_line_and_statement_distinct():
    result = analyze(sample())
    assert result["summary"]["duplicate_text_groups"] == 1
    assert result["summary"]["duplicate_math_node_groups"] == 1
    assert result["rows"][0]["same_statement_node_ids"] == [1, 2]
    assert result["rows"][0]["duplicate_text_lines"] == [7, 8]


def test_phase162_r10_r6_map_tag():
    result = analyze(sample())
    assert result["summary"]["tags"]["OFF_TARGET_H_MAP"] == 2
    assert normalize(r"\left H \right") == "H"


def test_phase162_r10_r6_no_fabricated_origin():
    data = sample()
    data["body_lines"] = [{"line": 1, "text": "unrelated", "math": [], "candidate_step_ids": [], "origin": "CONNECTOR_OR_PROSE"}]
    result = analyze(data)
    assert result["rows"][0]["diagnosis"] == "NO_STEP_TEXT_MATCH"
    assert result["rows"][0]["exact_paths_node_to_root"] == {}
