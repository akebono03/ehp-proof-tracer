from pathlib import Path
import hashlib
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

def narrative(n,k):
    result=search_group_from_registered_goal(n=n,k=k)
    if result.status.value != 'complete':
        raise AssertionError(f'pi_{n+k}^{n}: search status {result.status.value}')
    markdown=render_partial_proof_markdown(result)
    web=build_partial_web_group_proof_view(result,mode='narrative')
    assert web.rendered_lines
    return markdown

folder=Path('phase165_r2_display_results');folder.mkdir(exist_ok=True)
pi32=narrative(2,1)
pi43=narrative(3,1)
(folder/'pi3_2_after.md').write_text(pi32,encoding='utf-8')
(folder/'pi4_3_after.md').write_text(pi43,encoding='utf-8')
reference=folder/'pi3_2_before.md'
assert reference.exists(), 'missing pi3_2_before.md baseline'
assert pi32==reference.read_text(encoding='utf-8'), 'pi3_2 narrative regression'
assert r'\ker E' in pi43, 'missing kernel in pi43'
assert '第一同型定理' in pi43, 'missing first isomorphism theorem in pi43'
assert r'\pi_{4}^{3}' in pi43, 'missing pi43 conclusion'
print('R2 PASS: pi3_2 unchanged, pi4_3 kernel and quotient visible')
