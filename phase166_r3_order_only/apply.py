"""Install the Phase 166 R3 order-only common search gate, with backup."""
from pathlib import Path
import ast
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'phase165_r3_recursive_search.py'
START = 'def _typed_reference_steps('
END = '\n\ndef reconstruct_registered_goal('
NEW_HELPER = '''def _typed_reference_steps(
    bridge: RegistryBridgeResult,
    goal: object,
    citing_assertion_id: str,
) -> tuple[ProofStep, ...]:
    """Return exact, linked GIVEN references that precede the citing assertion.

    Eligibility depends on source order, not on independent review or
    source-transcription status. Unknown order does not count as prior.
    """
    citing = bridge.registry.assertion(citing_assertion_id)
    citing_ref = bridge.registry.reference(citing.reference_id)
    result = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is not type(goal) or assertion.content != goal:
            continue
        if assertion.assertion_id == citing_assertion_id:
            continue
        cited_ref = bridge.registry.reference(assertion.reference_id)
        if (not cited_ref.source_id or not citing_ref.source_id
                or cited_ref.source_id != citing_ref.source_id):
            continue
        if assertion.reference_id == citing.reference_id:
            preceding = (
                assertion.component_position is not None
                and citing.component_position is not None
                and assertion.component_position < citing.component_position
            )
        else:
            preceding = (
                assertion.available_after_position is not None
                and citing_ref.publication_position is not None
                and assertion.available_after_position < citing_ref.publication_position
            )
        if not preceding:
            continue
        links = tuple(x for x in bridge.proof_links if x.assertion_id == assertion.assertion_id)
        if len(links) != 1 or links[0].step is None:
            continue
        step = links[0].step
        if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                or type(step.conclusion) is not type(goal) or step.conclusion != goal):
            raise ValueError("typed Reference proof link is inconsistent")
        result.append(step)
    return tuple(result)
'''

def apply():
    if not TARGET.exists():
        raise FileNotFoundError(f'Project root must contain {TARGET.name}: {ROOT}')
    source = TARGET.read_text(encoding='utf-8-sig')
    if 'def _typed_reference_steps(' not in source or 'def reconstruct_registered_goal(' not in source:
        raise RuntimeError('Expected existing common search functions not found')
    if 'Eligibility depends on source order' in source:
        print('Already applied')
        return
    start = source.index(START)
    end = source.index(END, start)
    revised = source[:start] + NEW_HELPER.rstrip() + source[end:]
    # Preserve the complete existing public function and its API; replace only
    # the three leaf-lookup branches with the same order-only reference gate.
    a = revised.index('            if lookup_mode == "typed_reference_ordered":', revised.index('def reconstruct_registered_goal('))
    b = revised.index('            # A uniquely registered fixed Reference', a)
    existing = revised[a:b]
    for token in ('ordered_typed_reference_steps', 'find_eligible_goal_candidates', '_typed_reference_steps'):
        if token not in existing:
            raise RuntimeError(f'Unexpected search code: {token} missing')
    revised = revised[:a] + '''            # All lookup modes use one order-only reference eligibility gate.
            # Retain lookup_mode and verified_assertion_ids for API compatibility.
            options = list(_typed_reference_steps(bridge, target, citing_assertion_id))
''' + revised[b:]
    ast.parse(revised)
    backup_dir = ROOT / 'phase166_r3_order_only_backups'
    backup_dir.mkdir(exist_ok=True)
    backup = backup_dir / (TARGET.name + '.' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.bak')
    shutil.copy2(TARGET, backup)
    TARGET.write_text(revised, encoding='utf-8')
    # Update one existing integration expectation that depended on the
    # withdrawn independent-review requirement in the common search.
    test_path = ROOT / 'phase165_r52_r15_ordered_citation' / 'test_phase165_r52_r15_ordered_citation.py'
    if test_path.exists():
        test_src = test_path.read_text(encoding='utf-8-sig')
        old = '''    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal('fact', bridge, 'citing', lambda goal: (), lookup_mode='typed_reference_ordered')'''
        new = '''    assert reconstruct_registered_goal(
        'fact', bridge, 'citing', lambda goal: (), lookup_mode='typed_reference_ordered'
    ) is step'''
        old_unordered = '''def test_existing_unordered_mode_preserved():
    bridge, step = _fixture(available=None)
    found = reconstruct_registered_goal('fact', bridge, 'citing', lambda goal: (), lookup_mode='typed_reference')
    assert found is step'''
        new_unordered = '''def test_unordered_mode_now_respects_order():
    bridge, step = _fixture(available=None)
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal('fact', bridge, 'citing', lambda goal: (), lookup_mode='typed_reference')'''
        if old in test_src and old_unordered in test_src:
            shutil.copy2(test_path, backup_dir / (test_path.name + '.' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.bak'))
            updated_tests = test_src.replace(old, new).replace(old_unordered, new_unordered)
            test_path.write_text(updated_tests, encoding='utf-8')
            print('UPDATED LEGACY INTEGRATION TEST:', test_path)
        else:
            raise RuntimeError('Expected Phase 165 integration test content not found')
    print('PATCHED:', TARGET)
    print('BACKUP:', backup)

if __name__ == '__main__':
    apply()
