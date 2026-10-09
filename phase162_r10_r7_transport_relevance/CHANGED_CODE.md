# R10-R7 変更単位

対象ファイル: `toda_group_proof_narrative_transport_link.py`

変更: `render_suspension_transport_link()` 全体と import 全体。`add_transport_link_to_common_markdown()` は変更しない。

## 変更後 import（全文）

```python
from collections.abc import Callable

from proof import ProofStep
from toda_stable_group_transport import (
    _concrete_toda_group_matches_structural_group,
)
from toda_group_proof_narrative_transport_facts import (
    extract_suspension_transport_facts,
)
```

## 置換後関数（全文）

```python
def render_suspension_transport_link(
    root: ProofStep,
    render_step_latex: Callable[[ProofStep], str | None],
) -> str | None:
    """Describe a transport only when its destination is the current goal.

    A transport found solely in a subsidiary proof cannot be appended to
    the narrative of an unrelated target group.
    """
    facts = extract_suspension_transport_facts(root)
    if facts is None:
        return None
    if root.conclusion.lhs == facts.source_group_step.conclusion.lhs:
        return None
    if not _concrete_toda_group_matches_structural_group(
        root.conclusion.lhs,
        facts.transported_group_step.conclusion.lhs,
    ):
        return None
    source = render_step_latex(facts.source_group_step)
    isomorphism = render_step_latex(facts.isomorphism_step)
    transported = render_step_latex(facts.transported_group_step)
    bridge = render_step_latex(facts.generator_bridge_step)
    if not all((source, isomorphism, transported, bridge)):
        return None
    return (
        "証明木に記録された群構造の移送について、"
        f"${source}$ と ${isomorphism}$ から ${transported}$ を得る。"
        f"生成元の対応は ${bridge}$ である。"
    )
```

新規テスト: `phase162_r10_r7_transport_relevance/test_r10_r7.py`（ZIP内に関数全体・import全文を収録）。

完了条件: pi_5^3 の無関係な祖先移送は追加されない。既存 stable target pi_5^4 の移送は維持。既存 stable base は追加しない。全体テストは Phase 最後だけ。

境界: 不適切な H 写像と Whitehead 積の繰り返しについては本変更では扱わない。
