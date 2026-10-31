# 置換する既存コードの全文

- ファイル：`phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py`
- 変更対象：`test_r3z_general_higher_eta_is_reference_only`
- 変更後の import：従前と同一。下に全文を示す。
- 変更後の関数：下に全文を示す。
- ファイル全体：`output/test_r3z_reference_only_generic_eta_FULL.py` に格納。

```python
from __future__ import annotations

import re

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
from phase165_r57_r20_general_specialization import specialize_typed_statement
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, Relation
from web_group_proof_common import _group_proof_statement_latex
```

```python
def test_r3z_general_higher_eta_is_reference_only(rendered_pi53):
    proof, model, reference, body = rendered_pi53
    assert proof.status is ProofSearchStatus.COMPLETE
    assert model.steps is proof.proven_steps
    assert model.root_index is not None
    assert model.steps[model.root_index].rule is ProofRule.INFERENCE
    assert model.steps[model.root_index].conclusion == proof.conclusion
    assert model.status is ProofSearchStatus.COMPLETE
    assert model.open_goals == proof.open_goals == ()
    assert r"\pi_{n+1}^{n}" in reference
    assert r"\pi_{n+1}^{n}" not in body
    assert r"\eta_{n}" not in body
    assert r"\pi_{6}^{5}" in body
    assert body.rstrip().endswith("□")
```

追加監査パッケージの関数全文は `install.py` および `tests/test_install.py` に省略なしで格納した。これらは本番実装に import しない。
