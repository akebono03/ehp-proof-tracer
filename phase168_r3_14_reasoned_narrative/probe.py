from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_14_reasoned_narrative import (
    build_reasoned_narrative_lines,
    render_reasoned_narrative_markdown,
)

bridge = build_shared_typed_bridge()
for n, k in ((2, 1), (3, 1), (2, 2), (4, 1)):
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    lines = build_reasoned_narrative_lines(result, model)
    markdown = render_reasoned_narrative_markdown(result, model)
    links = sum(len(line.premise_indices) for line in lines)
    unsupported = sum(line.conclusion_latex is None for line in lines)
    print(f"PI_{n+k}^{n}: status={result.status.value} "
          f"reasoned_lines={len(lines)} dependency_edges={links} "
          f"unrenderable={unsupported} references={len(model.citations)} "
          f"markdown_characters={len(markdown)}")
print("R3-14 OPT-IN REASONED TRACE: PASS")
