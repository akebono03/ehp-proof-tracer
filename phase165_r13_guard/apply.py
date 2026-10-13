from pathlib import Path
import ast

root = Path(__file__).resolve().parent.parent
selector = root / 'phase164_r5_r2_common_replay.py'
text = selector.read_text(encoding='utf-8-sig')
old = '    return build_toda_group_result_proof_replay(group_result, max_depth=max_depth)'
new = '''    if n == 2 and k == 1:
        raise ValueError(
            "Phase 165: pi_3^2 has no certified typed-statement proof; "
            "legacy repository replay is prohibited for this goal"
        )

    return build_toda_group_result_proof_replay(group_result, max_depth=max_depth)'''
if new in text:
    print('Selector already guarded.')
elif text.count(old) == 1:
    selector.write_text(text.replace(old, new), encoding='utf-8')
    print('Selector guarded for (n,k)=(2,1).')
else:
    raise RuntimeError('Unexpected selector source; no files changed')
ast.parse(selector.read_text(encoding='utf-8'))

test = root / 'tests' / 'test_phase164_r5_r2_unified_web_display.py'
s = test.read_text(encoding='utf-8-sig')
old_count = '    assert len(calls) == 109'
new_count = '    assert len(calls) == 108'
old_except = '            if (n, k) in ((3, 2), (4, 1), (5, 1)):'
new_except = '            if (n, k) in ((2, 1), (3, 2), (4, 1), (5, 1)):'
if new_count in s and new_except in s:
    print('Existing selector test already updated.')
elif s.count(old_count) == 1 and s.count(old_except) == 1:
    s = s.replace(old_count, new_count).replace(old_except, new_except)
    test.write_text(s, encoding='utf-8')
    print('Adjusted legacy selector test scope.')
else:
    raise RuntimeError('Unexpected existing test; inspect manually')
ast.parse(test.read_text(encoding='utf-8'))
