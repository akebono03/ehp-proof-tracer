from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_12_body_binding import build_narrative_body_lines
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

bridge = build_shared_typed_bridge()
for n, k in ((2, 1), (3, 1), (2, 2), (4, 1)):
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    lines = build_narrative_body_lines(result, model)
    markdown = render_model_backed_narrative_markdown(result, model)
    assert '使用する結果' in markdown and '証明' in markdown
    assert all(line.citation_numbers == model.step_citation_numbers[line.step_index] for line in lines)
    print(f'PI_{n+k}^{n}: status={result.status.value} proof_steps={len(model.steps)} '
          f'body_lines={len(lines)} references={len(model.citations)}')
print('R3-12 BODY CITATION BINDING: PASS')
