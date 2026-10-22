from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_13_dependency_model import build_narrative_inferences

bridge = build_shared_typed_bridge()
for n, k in ((2, 1), (3, 1), (2, 2), (4, 1)):
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    nodes = build_narrative_inferences(result, model)
    edges = sum(len(node.premise_indices) for node in nodes)
    missing = sum(len(node.unresolved_premises) for node in nodes)
    print(f"PI_{n+k}^{n}: status={result.status.value} steps={len(nodes)} "
          f"dependency_edges={edges} unresolved_premises={missing} "
          f"citations={len(model.citations)}")
print("R3-13 DEPENDENCY MODEL: AUDIT COMPLETE")
