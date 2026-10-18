from pathlib import Path
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

out = Path('phase165_r2_order_fix_results')
out.mkdir(exist_ok=True)

def generate(n, k):
    result = search_group_from_registered_goal(n=n, k=k)
    assert result.status.value == 'complete', (n, k, result.status)
    markdown = render_partial_proof_markdown(result)
    web = build_partial_web_group_proof_view(result, mode='narrative')
    assert web.rendered_lines
    return markdown

pi32 = generate(2, 1)
pi43 = generate(3, 1)
(out / 'pi3_2_after.md').write_text(pi32, encoding='utf-8')
(out / 'pi4_3_after.md').write_text(pi43, encoding='utf-8')
assert pi32 == (out / 'pi3_2_before.md').read_text(encoding='utf-8'), 'pi3_2 changed'
assert pi43.count(r'\ker E') == 1, 'missing or duplicated kernel'
assert pi43.count('第一同型定理') == 1, 'missing or duplicated first isomorphism theorem'
assert pi43.index(r'\operatorname{Im}\Delta') < pi43.index(r'\ker E'), 'kernel before Delta image'
assert pi43.index(r'\ker E') < pi43.index('は全射'), 'kernel after surjectivity'
assert pi43.index('は全射') < pi43.index('第一同型定理'), 'quotient before surjectivity'
assert pi43.index('第一同型定理') < pi43.rfind('以上より,'), 'quotient after conclusion'
assert r'\pi_{4}^{3}' in pi43
print('PASS: pi3_2 unchanged; pi4_3 kernel and quotient in mathematical order')
print('Remaining wording issues are not modified by this patch.')
