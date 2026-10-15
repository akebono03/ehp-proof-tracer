# R5-R15 変更コード

## 変更対象

- `phase162_web_narrative_integration.py` の関数 `_build_phase162_legacy_validated_isomorphism_markdown()` のみ。
- import は変更しない。クラスの変更はない。
- 新規テストファイル `test_r5_r15.py` は既存 tests を変更しない。
- インストール補助: `install.py`, `restore.py`, `run.ps1`。

## 置換後の関数全文

```python
def _build_phase162_legacy_validated_isomorphism_markdown() -> str:
    """Render only after the exact provenance roots pass R7 validation.

    EHP leaves are sourced from the R5-R11 shared module through the existing
    compatibility import, rather than reconstructed in this legacy renderer.
    """
    prop51, hopf_eta5, exactness = _phase162_ehp_leaves()
    leaves = (prop51, hopf_eta5) + exactness
    trusted = {}
    visited = set()

    def collect(step: ProofStep) -> None:
        key = id(step)
        if key in visited:
            return
        visited.add(key)
        if step.rule is ProofRule.GIVEN:
            trusted[key] = step
        for premise in step.premises:
            collect(premise)

    for leaf in leaves:
        collect(leaf)

    validated = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, tuple(trusted.values())
    )
    presentation = build_validated_backward_proof_presentation(validated)
    markdown = render_validated_backward_proof_markdown(presentation)
    return _format_phase162_proof_sentences(
        _compose_phase162_group_conclusion(markdown)
    )
```

## 新規テスト全文

```python
from __future__ import annotations
import ast
from pathlib import Path
from unittest.mock import Mock

from phase162_web_narrative_integration import _build_phase162_legacy_validated_isomorphism_markdown
import phase162_web_narrative_integration as legacy
from proof import ProofRule


def test_r5_r15_legacy_uses_shared_ehp_leaves(monkeypatch):
    given = Mock()
    given.rule = ProofRule.GIVEN
    given.premises = ()
    given2 = Mock()
    given2.rule = ProofRule.GIVEN
    given2.premises = ()
    given3 = Mock()
    given3.rule = ProofRule.GIVEN
    given3.premises = ()
    calls = []
    monkeypatch.setattr(legacy, '_phase162_ehp_leaves', lambda: (given, given2, (given3,)))
    monkeypatch.setattr(legacy, 'phase161_r5_target_goal', lambda: 'GOAL')
    def reconstruction(goal, leaves, roots):
        calls.append((goal, leaves, roots))
        return 'VALIDATED'
    monkeypatch.setattr(legacy, 'reconstruct_phase161_r7_validated_goal', reconstruction)
    monkeypatch.setattr(legacy, 'build_validated_backward_proof_presentation', lambda result: result)
    monkeypatch.setattr(legacy, 'render_validated_backward_proof_markdown', lambda presentation: 'RAW')
    monkeypatch.setattr(legacy, '_compose_phase162_group_conclusion', lambda markdown: markdown+' GROUP')
    monkeypatch.setattr(legacy, '_format_phase162_proof_sentences', lambda markdown: markdown+' FORMAT')
    assert _build_phase162_legacy_validated_isomorphism_markdown() == 'RAW GROUP FORMAT'
    assert len(calls) == 1
    goal, leaves, roots = calls[0]
    assert goal == 'GOAL'
    assert leaves == (given, given2, given3)
    assert set(map(id, roots)) == {id(given), id(given2), id(given3)}


def test_r5_r15_legacy_builder_has_no_duplicated_ehp_windows():
    target = Path(legacy.__file__)
    tree = ast.parse(target.read_text(encoding='utf-8-sig'))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_build_phase162_legacy_validated_isomorphism_markdown')
    called = {n.func.id for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert '_phase162_ehp_leaves' in called
    assert 'TodaEHPExactnessWindow' not in called
    assert 'build_phase55_representative_result' not in called
    assert 'build_phase58_representative_result' not in called


def test_r5_r15_existing_public_api_remains():
    assert callable(legacy.build_phase162_web_validated_isomorphism_markdown)
    assert callable(legacy._build_phase162_existing_group_connection)
    assert callable(legacy._phase162_ehp_leaves)

```
