"""Export a graph-built root segment and record its deliberately limited scope."""

import json
from pathlib import Path

from audit_phase162_r3b_existing_renderer import build_r3b_presentation
from phase162_r3e_structured_root_renderer import (
    render_phase162_r3e_structured_root_markdown,
)
from proof import ProofRule


def main() -> None:
    _, presentation = build_r3b_presentation()
    root_text = render_phase162_r3e_structured_root_markdown(presentation)
    if not root_text:
        raise RuntimeError('Root transport renderer did not apply')
    output = Path('phase162_r3e_output')
    output.mkdir(exist_ok=True)
    (output / 'structured_root_only.md').write_text(root_text, encoding='utf-8')
    report = {
        'status': 'ROOT_COMPOSED_FROM_PROOFSTEP',
        'public_renderer_changed': False,
        'legacy_markdown_used_as_input': False,
        'root_premise_count': len(presentation.root_step.premises),
        'presentation_node_count': len(presentation.nodes),
        'presentation_edge_count': len(presentation.edges),
        'inference_count': sum(
            n.proof_step.rule is ProofRule.INFERENCE for n in presentation.nodes
        ),
        'root_reason_placement': 'GRAPH_COMPOSITION_NOT_TEXT_MARKER',
        'recursive_premise_proofs_rendered': False,
        'full_proof_semantic_certification': False,
        'next_boundary': 'Integrate recursive evidence narration before replacing the public Renderer',
    }
    (output / 'r3e_audit.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('Root Markdown:', (output / 'structured_root_only.md').resolve())


if __name__ == '__main__':
    main()
