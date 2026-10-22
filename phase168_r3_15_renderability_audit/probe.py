from collections import Counter
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_15_renderability_audit import audit_reasoned_renderability

bridge = build_shared_typed_bridge()
for n, k in ((2, 1), (3, 1), (2, 2), (4, 1)):
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    findings = audit_reasoned_renderability(result, model)
    print(f'PI_{n+k}^{n}: status={result.status.value} unrenderable={len(findings)} types={dict(Counter(f.statement_type for f in findings))}')
    for f in findings:
        availability = {name: bool(value) for name, value, error in f.candidates}
        errors = {name: error for name, value, error in f.candidates if error}
        print(f'  STEP {f.step_index}: {f.statement_type} rule={f.rule} inference={f.inference_name!r} available={availability} errors={errors}')
print('R3-15 RENDERABILITY AUDIT ONLY; no production files changed')
