from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_argument_ordering import (
    order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_multi_renderer import (
    render_toda_group_proof_narrative_multi_argument_markdown,
)

CASES = (
    (
        3,
        3,
        r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$",
    ),
    (
        5,
        3,
        r"$2\nu_{5} = E^{2}\nu'$",
    ),
)

for n, k, needle in CASES:
    presentation, blocks, sidecar, arguments = _method_evidence_data(n, k)
    ordered = order_toda_group_proof_narrative_arguments(arguments)
    rendered = render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
    )

    print("=" * 78)
    print(f"pi target: n={n}, k={k}")
    print(f"ordered argument source indexes: {[arguments.index(a) for a in ordered]}")
    print(f"needle count in final multi: {rendered.count(needle)}")
    print("-" * 78)

    positions = []
    start = 0
    while True:
        pos = rendered.find(needle, start)
        if pos < 0:
            break
        positions.append(pos)
        start = pos + 1

    for i, pos in enumerate(positions, 1):
        lo=max(0,pos-240)
        hi=min(len(rendered),pos+len(needle)+240)
        print(f"OCCURRENCE {i} at {pos}")
        print(rendered[lo:hi])
        print("-" * 78)
