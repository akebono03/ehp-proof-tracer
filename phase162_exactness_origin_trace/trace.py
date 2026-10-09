"""Read-only trace of the first renderer stage emitting malformed exactness markup."""

from __future__ import annotations

from collections import Counter
from functools import wraps

import toda_group_proof_narrative_renderer as renderer


PATTERNS = (
    '$$\\pi_',
    '$ は完全である.$ は完全である.',
)


def _lines(value):
    if isinstance(value, str):
        return value.splitlines()
    if isinstance(value, list):
        return value
    return []


def _inspect(stage, part, value):
    lines = _lines(value)
    counts = Counter({pattern: sum(line.count(pattern) for line in lines) for pattern in PATTERNS})
    print(f'[{stage}] {part} counts={dict(counts)}')
    samples = [line.strip() for line in lines if any(p in line for p in PATTERNS)]
    for sample in samples[:2]:
        print('   ', repr(sample[:260]))
    return tuple(counts[p] for p in PATTERNS)


def _wrap(name):
    original = getattr(renderer, name)

    @wraps(original)
    def traced(*args, **kwargs):
        # First argument is presentation on most stages; the last positional
        # argument is the actual text/list for all selected functions.
        incoming = args[-1] if args else None
        before = _inspect(name, 'IN ', incoming)
        output = original(*args, **kwargs)
        after = _inspect(name, 'OUT', output)
        if before != after:
            print(f'  FIRST/CHANGED DEFECT COUNTS AT {name}: {before} -> {after}')
        return output

    setattr(renderer, name, traced)


def main():
    stages = (
        '_phase159_consolidate_public_exactness_lines',
        '_phase159_project_generic_semantics_to_public_proof',
        '_phase159_r1_7b_normalize_public_exact_sequences',
        '_phase158_baseline_render_toda_group_proof_narrative_markdown',
        '_phase158_normalize_public_narrative_contract',
    )
    for name in stages:
        if hasattr(renderer, name):
            _wrap(name)
        else:
            print('Stage not found:', name)

    from phase162_pi5_3_renderer_audit import render_phase162_pi5_3_reconstructed_proof
    from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data
    from tests.test_phase59_n3_ehp_chain import build_phase59_3_data

    data = build_phase59_4_data()
    leaves = build_phase59_3_data()['premise_steps']
    result = render_phase162_pi5_3_reconstructed_proof(
        data['pi4_2_step'],
        (data['eta3_definition_step'], data['eta4_definition_step']),
        leaves,
    )
    _inspect('PUBLIC NARRATIVE', 'FINAL', result.markdown)
    print('Read-only tracing completed; no production source or tests changed.')


if __name__ == '__main__':
    main()
