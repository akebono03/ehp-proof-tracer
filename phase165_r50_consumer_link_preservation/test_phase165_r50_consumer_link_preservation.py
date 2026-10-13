
from web_group_proof import build_standard_web_group_proof_view

def _text():
    view = build_standard_web_group_proof_view(
        n=2, k=1, max_depth=2, mode="narrative"
    )
    return "\n".join(
        line.prefix + (line.statement_latex or "") + line.suffix
        for line in view.rendered_lines
    )

def test_r50_reference_and_delta_reason_survive_final_web_rendering():
    text = _text()
    reference = text.split("使用する結果",1)[1].split("証明",1)[0]
    assert "(5.1)" in reference
    assert "Proposition 5.1" in reference
    assert "Proposition 4.2" in reference
    assert r"\operatorname{Im}" in text
    assert r"\ker E=0" in text
    assert text.index("は単射") < text.index("は全射") < text.index("単射性と全射性より")
    assert text.count("は零写像") == 1
    assert text.count("単射性と全射性より") == 1
