"""Phase 162 R3-F: lossless dependency-ordered ProofStep narration audit.

The only supported inference explanation is the already-validated root cyclic
transport. Other inferences are explicitly marked UNEXPLAINED. This renderer
must never be presented as a fully narrated or mathematically certified proof.
"""

from dataclasses import dataclass

from proof import ProofRule, ProofStep
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_presentation import TodaGroupProofPresentation
from toda_group_structure_transport_reason import render_group_structure_transport_reason


@dataclass(frozen=True)
class Phase162R3FRecord:
    index: int
    step: ProofStep
    premise_indices: tuple[int, ...]
    mathematical_fact: str
    reason: str | None
    reason_status: str


@dataclass(frozen=True)
class Phase162R3FResult:
    markdown: str
    records: tuple[Phase162R3FRecord, ...]
    checked_edge_count: int


def build_phase162_r3f_recursive_records(
    presentation: TodaGroupProofPresentation,
) -> tuple[tuple[Phase162R3FRecord, ...], int]:
    """Visit every reachable ProofStep once, premises before their consumer."""
    if not isinstance(presentation, TodaGroupProofPresentation):
        raise TypeError('presentation must be TodaGroupProofPresentation')

    root = presentation.root_step
    if not isinstance(root, ProofStep):
        raise TypeError('presentation root must be ProofStep')

    step_by_id = {id(node.proof_step): node.proof_step for node in presentation.nodes}
    if id(root) not in step_by_id or step_by_id[id(root)] is not root:
        raise ValueError('Presentation root identity is missing')
    if len(step_by_id) != len(presentation.nodes):
        raise ValueError('Presentation has duplicate ProofStep nodes')

    edge_keys = [
        (id(edge.parent_step), edge.premise_index, id(edge.premise_step))
        for edge in presentation.edges
    ]
    if len(edge_keys) != len(set(edge_keys)):
        raise ValueError('Presentation has duplicated dependency edges')
    expected_edges = {
        (id(step), index, id(premise))
        for step in step_by_id.values()
        for index, premise in enumerate(step.premises)
    }
    if set(edge_keys) != expected_edges:
        raise ValueError('Presentation dependency edges differ from ProofStep premises')
    if any(id(premise) not in step_by_id for step in step_by_id.values() for premise in step.premises):
        raise ValueError('Premise is missing from Presentation nodes')

    state = {}
    ordered_steps = []

    def visit(step: ProofStep) -> None:
        step_id = id(step)
        if state.get(step_id) == 1:
            raise ValueError('ProofStep dependency cycle detected')
        if state.get(step_id) == 2:
            return
        state[step_id] = 1
        for premise in step.premises:
            visit(premise)
        state[step_id] = 2
        ordered_steps.append(step)

    visit(root)
    if len(ordered_steps) != len(step_by_id):
        raise ValueError('Presentation contains unreachable ProofStep nodes')

    index_by_identity = {id(step): i + 1 for i, step in enumerate(ordered_steps)}
    records = []
    for index, step in enumerate(ordered_steps, 1):
        premise_indices = tuple(index_by_identity[id(p)] for p in step.premises)
        if any(premise_index >= index for premise_index in premise_indices):
            raise ValueError('Proof order is not dependency-first')
        fact = _render_generic_narrative_step(step)
        if not isinstance(fact, str) or not fact.strip():
            raise ValueError('A ProofStep fact cannot be represented')
        reason = None
        if step is root:
            reason = render_group_structure_transport_reason(step)
        if step.rule is ProofRule.GIVEN:
            status = 'GIVEN'
        elif reason is not None:
            status = 'EXPLAINED'
        else:
            status = 'UNEXPLAINED'
        records.append(Phase162R3FRecord(index, step, premise_indices, fact, reason, status))
    return tuple(records), len(edge_keys)


def render_phase162_r3f_recursive_markdown(
    presentation: TodaGroupProofPresentation,
) -> Phase162R3FResult:
    """Render a trace, not a falsely polished proof; never read legacy Markdown."""
    records, checked_edges = build_phase162_r3f_recursive_records(presentation)
    lines = [
        '# Recursive ProofStep trace (not a complete mathematical proof)',
        '',
        '## 監査対象',
        '',
        '全依存ノードを前提優先で一度ずつ列挙する。',
        '未対応の推論理由は明示し、証明された文章として扱わない。',
        '',
        '## 依存順の記録',
        '',
    ]
    for record in records:
        step = record.step
        lines.append('### [S' + str(record.index).zfill(3) + '] ' + record.reason_status)
        lines.append('')
        if record.premise_indices:
            lines.append('前提: ' + ', '.join('[S' + str(i).zfill(3) + ']' for i in record.premise_indices))
        else:
            lines.append('前提: なし')
        lines.append('')
        lines.append('事実: ' + record.mathematical_fact)
        lines.append('')
        if record.reason_status == 'EXPLAINED':
            lines.append('推論理由: ' + record.reason)
        elif record.reason_status == 'UNEXPLAINED':
            rule = step.inference_rule
            lines.append('推論理由: 未対応 (rule=' + (rule.name if rule is not None else 'unspecified') + ')')
        else:
            lines.append('根拠区分: GIVEN (既知の前提。本文内では導出しない)')
        lines.append('')
    text = '\n'.join(lines).rstrip() + '\n'
    return Phase162R3FResult(text, records, checked_edges)
