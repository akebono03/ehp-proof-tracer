"""Connect existing premise-validated exactness reasons to the R3-F graph trace.

No historical/public Markdown is read. This is still a trace, not a proof certificate.
"""

from dataclasses import dataclass
from dataclasses import replace

from proof import ProofRule
from phase162_r3f_recursive_renderer import (
    Phase162R3FRecord,
    build_phase162_r3f_recursive_records,
)
from toda_group_proof_narrative_reason_renderer import (
    render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
    _exactness_to_kernel_reason,
    _exactness_to_map_property_reason,
)
from toda_group_proof_presentation import TodaGroupProofPresentation


@dataclass(frozen=True)
class Phase162R3GResult:
    records: tuple[Phase162R3FRecord, ...]
    markdown: str
    checked_edge_count: int
    reason_kind_by_index: tuple[tuple[int, str], ...]


def _existing_exactness_reason(step):
    """Use existing builders, accepting only exact direct-premise matches."""
    candidates = tuple(
        reason
        for reason in (
            _exactness_to_map_property_reason(step),
            _exactness_to_kernel_reason(step),
        )
        if reason is not None
    )
    if len(candidates) > 1:
        raise ValueError('Conflicting existing exactness reasons')
    if not candidates:
        return None
    reason = candidates[0]
    if reason.conclusion_step is not step:
        raise ValueError('Reason conclusion identity mismatch')
    actual = {id(premise) for premise in step.premises}
    if len(reason.premise_steps) != 2 or any(
        id(premise) not in actual for premise in reason.premise_steps
    ):
        raise ValueError('Reason does not use actual direct premises')
    return reason


def build_phase162_r3g_existing_reason_trace(
    presentation: TodaGroupProofPresentation,
) -> Phase162R3GResult:
    """Preserve R3-F ordering; attach only justified existing exactness prose."""
    base_records, checked_edges = build_phase162_r3f_recursive_records(presentation)
    updated = []
    reason_kinds = []
    for record in base_records:
        if record.step.rule is ProofRule.GIVEN or record.reason is not None:
            updated.append(record)
            if record.reason is not None:
                reason_kinds.append((record.index, 'ROOT_GROUP_STRUCTURE_TRANSPORT'))
            continue
        reason = _existing_exactness_reason(record.step)
        if reason is None:
            updated.append(record)
            continue
        sentence = render_toda_group_proof_narrative_reason_sentence(reason)
        if not isinstance(sentence, str) or not sentence.strip():
            updated.append(record)
            continue
        updated.append(replace(record, reason=sentence, reason_status='EXPLAINED'))
        reason_kinds.append((record.index, reason.kind.value))

    lines = [
        '# Recursive ProofStep trace with existing exactness reasons',
        '',
        '注意: 理由が未対応の推論は証明文章として認証しない。',
        '',
    ]
    for record in updated:
        lines.extend((
            '### [S' + str(record.index).zfill(3) + '] ' + record.reason_status,
            '',
            '前提: ' + (
                ', '.join('[S' + str(index).zfill(3) + ']' for index in record.premise_indices)
                if record.premise_indices else 'なし'
            ),
            '',
            '事実: ' + record.mathematical_fact,
            '',
        ))
        if record.reason is not None:
            lines.append('推論理由: ' + record.reason)
        elif record.reason_status == 'UNEXPLAINED':
            lines.append('推論理由: 未対応')
        else:
            lines.append('根拠区分: GIVEN (既知の前提)')
        lines.append('')

    return Phase162R3GResult(
        records=tuple(updated),
        markdown='\n'.join(lines).rstrip() + '\n',
        checked_edge_count=checked_edges,
        reason_kind_by_index=tuple(reason_kinds),
    )
