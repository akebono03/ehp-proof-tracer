# Phase 173 R15R17-R3R4: Full Changed Test Functions

Only historical test contracts change. All production modules are byte-for-byte unchanged.

The named-generator proof remains incomplete where its typed open goals are unresolved.
Verified abstract ProofSteps remain cited once in the canonical public Narrative.
Explicit legacy APIs and their own tests keep their independent historical output.

## `phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py`

### Import block (unchanged)

```python
"""Repository-dependent real source-first certificates and common Web projection."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    abstract_invariants_latex,
    render_certified_abstract_section,
)
from proof import ProofRule


```

### Complete test function: `test_shared_model_backed_web_displays_abstract_and_keeps_named_pending`

```python
def test_shared_model_backed_web_displays_abstract_and_keeps_named_pending(proved_abstract_result) -> None:
    model = build_proof_narrative_model(proved_abstract_result)
    view = build_partial_web_group_proof_view(
        proved_abstract_result, mode="narrative", narrative_model=model,
    )
    assert view.key == "generic-partial-proof"
    assert view.partial_result
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("検証済みの途中経過") == 0
    assert view.abstract_structure_certified
    assert any(step is proved_abstract_result.abstract_structure.proof_step
               for step in model.steps)
    assert any(r"\pi_{35}^{4}" in (line.statement_latex or "")
               and r"\cong" in (line.statement_latex or "")
               for line in view.rendered_lines)
    assert any(line.kind == "heading" and line.prefix == "未解決 Goal"
               for line in view.rendered_lines)
```

## `phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py`

### Import block (unchanged)

```python
"""Real source-first abstract evidence through the one canonical Narrative Model."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import (
    render_model_backed_narrative_markdown,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_section,
    render_certified_abstract_model_section,
)
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _build_group_proof_rendered_lines


```

### Complete test function: `test_source_first_certificate_is_owned_by_model_and_rendered_once`

```python
@pytest.mark.parametrize("k", (8, 31))
def test_source_first_certificate_is_owned_by_model_and_rendered_once(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    model = build_proof_narrative_model(result)
    assert result.abstract_structure is not None
    assert model.abstract_structure is result.abstract_structure
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    abstract = render_certified_abstract_model_section(model)
    assert abstract == ""
    assert "## 証明済みの抽象群構造" in render_certified_abstract_section(result)
    assert any(step is result.abstract_structure.proof_step for step in model.steps)
    after = render_model_backed_narrative_markdown(result, model)
    assert after.count("## 使用する結果") == 1
    assert "## 証明済みの抽象群構造" not in after
    assert "### 検証済み証明木の Reference" not in after
    assert "Proposition 4.4" in after
    assert "Lemma 5.4" in after
    assert r"\cong" in after
    assert "## 未解決 Goal" in after
    direct_view = build_partial_web_group_proof_view(
        result, mode="narrative", narrative_model=model,
    )
    assert direct_view.rendered_lines == _build_group_proof_rendered_lines(after)
    assert direct_view.key == "generic-partial-proof" and direct_view.partial_result
    assert result.abstract_structure.proof_step not in result.proven_steps
    assert model.open_goals == result.open_goals
    assert model.diagnostics == result.diagnostics
```

### Complete test function: `test_public_default_path_and_legacy_path_keep_one_abstract_section`

```python
@pytest.mark.parametrize("k", (8, 31))
def test_public_default_path_and_legacy_path_keep_one_abstract_section(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    for citation_source in ("model", "legacy"):
        view = build_standard_web_group_proof_view(
            n=4, k=k, goal=goal, mode="narrative", citation_source=citation_source,
        )
        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        if citation_source == "model":
            assert headings.count("使用する結果") == 1
            assert headings.count("証明済みの抽象群構造") == 0
            assert headings.count("検証済みの途中経過") == 0
            assert headings.count("未解決 Goal") == 1
            shown = "\n".join(
                segment.value for line in view.rendered_lines
                for segment in line.segments
            )
            assert r"\cong" in shown
        else:
            # The separately requested legacy API retains its old projection.
            assert headings.count("証明済みの抽象群構造") == 1
        assert view.key == "generic-partial-proof"
        assert view.partial_result
```

## `phase173_r4_r15r12_reference_correction/tests/test_integration.py`

### Import block (unchanged)

```python
"""Actual source-first Proof Tree to canonical Narrative Model to Web regressions."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


```

### Complete test function: `test_abstract_only_groups_remain_partial`

```python
@pytest.mark.parametrize('k', (8, 31))
def test_abstract_only_groups_remain_partial(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode='narrative', citation_source='model',
    )
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    assert view.key == 'generic-partial-proof' and view.partial_result
    headings = [line.prefix for line in view.rendered_lines if line.kind == 'heading']
    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("未解決 Goal") == 1
    assert view.abstract_structure_certified
    assert any(r"\cong" in segment.value
               for line in view.rendered_lines for segment in line.segments)
```

## `phase173_r4_r15r13_unified_presentation/tests/test_integration.py`

### Import block (unchanged)

```python
"""Real Web group view checks on the same Narrative Model pipeline."""
from __future__ import annotations

import pytest

from web_group_proof import build_standard_web_group_proof_view
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result


```

### Complete test function: `test_one_presentation_contract_for_both_proof_states`

```python
@pytest.mark.parametrize("n,k,complete", ((4, 3, True), (4, 7, True),
                                        (4, 8, False), (4, 31, False)))
def test_one_presentation_contract_for_both_proof_states(
    n: int, k: int, complete: bool,
) -> None:
    goal = None if complete else exact_prior_database_result(n, k)
    view = build_standard_web_group_proof_view(
        n=n, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result is not complete
    assert view.key == ("generic-complete-proof" if complete
                        else "generic-partial-proof")
    headings = [line.prefix for line in view.rendered_lines
                if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert "証明" not in headings
    assert "証明対象" not in headings
    assert sum(line.kind == "separator" for line in view.rendered_lines) == 1
    if complete:
        assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                       for line in view.rendered_lines)
        assert any("[R" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
    else:
        assert headings.count("未解決 Goal") == 1
        assert headings.count("証明済みの抽象群構造") == 0
        assert headings.count("検証済みの途中経過") == 0
        assert headings.count("確認済み ProofStep（与件を含む）") == 1
        assert any("探索状態" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
        assert any(r"\cong" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
```

## `phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py`

### Import block (unchanged)

```python
"""Focused real typed partial and complete view regression tests."""
from __future__ import annotations

import pytest

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _group_proof_statement_latex


```

### Complete test function: `test_real_partial_web_does_not_leak_internal_diagnostics`

```python
@pytest.mark.parametrize("k", (8, 15))
def test_real_partial_web_does_not_leak_internal_diagnostics(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None and len(result.open_goals) == 3
    assert result.abstract_structure is not None
    assert any("Relation(" in item for item in result.diagnostics)
    model = build_proof_narrative_model(result)
    # Preserve the internal model for audits; only the public view is projected.
    raw = render_model_backed_narrative_markdown(result, model)
    assert "expected a verified registered derivation" in raw
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-partial-proof" and view.partial_result
    assert sum(line.kind == "heading" and line.prefix == "未解決 Goal"
               for line in view.rendered_lines) == 1
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert view.abstract_structure_certified
    rendered = "\n".join(
        segment.value for line in view.rendered_lines for segment in line.segments
    )
    assert "CyclicStructureStatement（数式表示未対応）" not in rendered
    assert "Relation(lhs=" not in rendered
    assert "導出候補 0 件" in rendered
    assert r"\mathbb{Z}/2\{" in rendered
    assert r"\pi_{" in rendered
```

## `phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py`

### Import block (unchanged)

```python
"""Real Web proof state, typed certificate, and Flask result banner regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

import web_app
from toda_calculation_result import TodaCalculationStatus
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import WebGroupProofView
from web_group_query import WebGroupQueryView


```

### Complete test function: `test_certificate_flag_comes_from_actual_verified_partial_result`

```python
@pytest.mark.parametrize("n,k,certified", (
    (4, 3, False),
    (4, 8, True),
    (4, 31, True),
))
def test_certificate_flag_comes_from_actual_verified_partial_result(
    n: int, k: int, certified: bool,
) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    assert view.abstract_structure_certified is certified
    if certified:
        assert view.partial_result
        assert view.key == "generic-partial-proof"
        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        assert headings.count("使用する結果") == 1
        assert headings.count("証明済みの抽象群構造") == 0
        assert headings.count("未解決 Goal") == 1
        assert any(r"\cong" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
    else:
        assert not view.partial_result
        assert view.key == "generic-complete-proof"
```

### Complete test function: `test_real_flask_result_explains_abstract_only_status`

```python
def test_real_flask_result_explains_abstract_only_status(monkeypatch) -> None:
    # Avoid repeating the distinct old group-query search. The *real* typed
    # proof search and certificate-bound Web adapter remain in this test.
    def query_not_found(n: int, k: int) -> WebGroupQueryView:
        assert (n, k) == (4, 8)
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None, proof_available=False,
        )

    monkeypatch.setattr(web_app, "build_standard_web_group_query_view", query_not_found)
    app = web_app.create_app()
    app.config.update(TESTING=True)
    response = app.test_client().post("/", data={"n": "4", "k": "8"})
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "A verified abstract group structure is available" in text
    assert "named-generator proof is incomplete" in text
    assert "No proof-backed result found for this query" not in text
    assert "generic-partial-proof" in text
    assert "使用する結果" in text
    assert r"\cong" in text
```

## `phase173_r4_r15r15r2_head_guard_fix/tests/test_integration.py`

### Import block (unchanged)

```python
"""Real Web proof state, typed certificate, and Flask result banner regressions."""
from __future__ import annotations

from dataclasses import replace

import pytest

import web_app
from toda_calculation_result import TodaCalculationStatus
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import WebGroupProofView
from web_group_query import WebGroupQueryView


```

### Complete test function: `test_certificate_flag_comes_from_actual_verified_partial_result`

```python
@pytest.mark.parametrize("n,k,certified", (
    (4, 3, False),
    (4, 8, True),
    (4, 31, True),
))
def test_certificate_flag_comes_from_actual_verified_partial_result(
    n: int, k: int, certified: bool,
) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    assert view.abstract_structure_certified is certified
    if certified:
        assert view.partial_result
        assert view.key == "generic-partial-proof"
        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        assert headings.count("使用する結果") == 1
        assert headings.count("証明済みの抽象群構造") == 0
        assert headings.count("未解決 Goal") == 1
        assert any(r"\cong" in segment.value for line in view.rendered_lines
                   for segment in line.segments)
    else:
        assert not view.partial_result
        assert view.key == "generic-complete-proof"
```

### Complete test function: `test_real_flask_result_explains_abstract_only_status`

```python
def test_real_flask_result_explains_abstract_only_status(monkeypatch) -> None:
    # Avoid repeating the distinct old group-query search. The *real* typed
    # proof search and certificate-bound Web adapter remain in this test.
    def query_not_found(n: int, k: int) -> WebGroupQueryView:
        assert (n, k) == (4, 8)
        return WebGroupQueryView(
            n=n, k=k, status=TodaCalculationStatus.NOT_FOUND,
            result_latex=None, proof_available=False,
        )

    monkeypatch.setattr(web_app, "build_standard_web_group_query_view", query_not_found)
    app = web_app.create_app()
    app.config.update(TESTING=True)
    response = app.test_client().post("/", data={"n": "4", "k": "8"})
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "A verified abstract group structure is available" in text
    assert "named-generator proof is incomplete" in text
    assert "No proof-backed result found for this query" not in text
    assert "generic-partial-proof" in text
    assert "使用する結果" in text
    assert r"\cong" in text
```

## `phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py`

### Import block (unchanged)

```python
"""Real certified partial proofs display their checked intermediate premises."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_model_section,
    render_certified_abstract_section,
)
from web_group_proof import build_standard_web_group_proof_view


```

### Complete test function: `test_abstract_certificate_displays_actual_verified_milestones`

```python
@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_abstract_certificate_displays_actual_verified_milestones(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    assert result.abstract_structure.proof_step not in result.proven_steps

    model = build_proof_narrative_model(result)
    progress = render_certified_abstract_model_section(model)
    assert progress == ""
    # The explicit legacy helper remains available without a public sidecar.
    legacy_section = render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in legacy_section
    assert "### 検証済み証明木の Reference" in legacy_section
    assert "## 証明済みの抽象群構造" in legacy_section
    assert any(step is result.abstract_structure.proof_step for step in model.steps)
    assert len(model.citations) >= 4
    markdown = render_model_backed_narrative_markdown(result, model)
    assert markdown.count("## 使用する結果") == 1
    assert "### 検証済み証明木の Reference" not in markdown
    assert "## 検証済みの途中経過" not in markdown
    assert "## 証明済みの抽象群構造" not in markdown
    assert "Proposition 4.4" in markdown
    assert "Lemma 5.4" in markdown
    assert markdown.count("DB prior: sphere.csv") >= 2
    assert r"\cong" in markdown
    assert "先行データベースの " not in markdown

    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    assert view.key == "generic-partial-proof"
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert headings.count("未解決 Goal") == 1
    shown = "\n".join(
        seg.value for line in view.rendered_lines for seg in line.segments
    )
    assert "sphere.csv" in shown and "Lemma 5.4" in shown
    assert "Relation(lhs=" not in shown
    assert "、" not in shown and "。" not in shown
    assert result.conclusion is None and result.open_goals
```

### Complete test function: `test_legacy_and_model_paths_share_abstract_progress`

```python
def test_legacy_and_model_paths_share_abstract_progress() -> None:
    goal = exact_prior_database_result(4, 8)
    assert goal is not None
    views = (
        build_standard_web_group_proof_view(
            n=4, k=8, goal=goal, mode="narrative", citation_source=source,
        )
        for source in ("model", "legacy")
    )
    for source, view in zip(("model", "legacy"), views):
        assert view.key == "generic-partial-proof"
        headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        if source == "model":
            assert headings.count("使用する結果") == 1
            assert headings.count("検証済みの途中経過") == 0
            assert headings.count("証明済みの抽象群構造") == 0
        else:
            assert headings.count("検証済みの途中経過") == 1
            assert headings.count("証明済みの抽象群構造") == 1
```

## `phase173_r4_r15r16r2_shared_tree_narrative/tests/test_integration.py`

### Import block (unchanged)

```python
"""Public projection of a separately verified tree through the common renderer."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_section,
)
from phase173_r4_r15r16r2_shared_tree_narrative.tree_adapter import (
    render_verified_tree_progress,
    verified_tree_postorder,
)
from web_group_proof import build_standard_web_group_proof_view


```

### Complete test function: `test_real_abstract_tree_reuses_common_renderer`

```python
@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_real_abstract_tree_reuses_common_renderer(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    structure = result.abstract_structure
    assert structure is not None
    ordered = verified_tree_postorder(structure.proof_step)
    assert ordered[-1] is structure.proof_step
    assert len(ordered) >= 4
    assert structure.proof_step not in result.proven_steps
    lines = render_verified_tree_progress(result.target, structure.proof_step)
    joined = "\n".join(lines)
    assert "### 検証済み証明木の Reference" in joined
    assert "### 検証済み ProofStep" in joined
    assert "Proposition 4.4" in joined
    assert "Lemma 5.4" in joined
    assert "DB prior: sphere.csv" in joined
    assert "- 与件:" in joined or "- 推論:" in joined
    assert "Relation(lhs=" not in joined
    assert "数式表示未対応" not in joined
    assert "先行データベースの " not in joined
    assert "4つの前提" not in joined
    rendered = render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in rendered
    assert "### 検証済み ProofStep" in rendered

    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert headings.count("未解決 Goal") == 1
    shown = "\n".join(segment.value for line in view.rendered_lines
                       for segment in line.segments)
    assert "Proposition 4.4" in shown
    assert "sphere.csv" in shown
    assert "Lemma 5.4" in shown
    assert "、" not in shown and "。" not in shown
    assert result.conclusion is None and result.open_goals
```

## `phase173_r4_r15r16r3_staged_guard_fix/tests/test_integration.py`

### Import block (unchanged)

```python
"""Public projection of a separately verified tree through the common renderer."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_section,
)
from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import (
    render_verified_tree_progress,
    verified_tree_postorder,
)
from web_group_proof import build_standard_web_group_proof_view


```

### Complete test function: `test_real_abstract_tree_reuses_common_renderer`

```python
@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_real_abstract_tree_reuses_common_renderer(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    structure = result.abstract_structure
    assert structure is not None
    ordered = verified_tree_postorder(structure.proof_step)
    assert ordered[-1] is structure.proof_step
    assert len(ordered) >= 4
    assert structure.proof_step not in result.proven_steps
    lines = render_verified_tree_progress(result.target, structure.proof_step)
    joined = "\n".join(lines)
    assert "### 検証済み証明木の Reference" in joined
    assert "### 検証済み ProofStep" in joined
    assert "Proposition 4.4" in joined
    assert "Lemma 5.4" in joined
    assert "DB prior: sphere.csv" in joined
    assert "- 与件:" in joined or "- 推論:" in joined
    assert "Relation(lhs=" not in joined
    assert "数式表示未対応" not in joined
    assert "先行データベースの " not in joined
    assert "4つの前提" not in joined
    rendered = render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in rendered
    assert "### 検証済み ProofStep" in rendered

    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("検証済みの途中経過") == 0
    assert headings.count("証明済みの抽象群構造") == 0
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert headings.count("未解決 Goal") == 1
    shown = "\n".join(segment.value for line in view.rendered_lines
                       for segment in line.segments)
    assert "Proposition 4.4" in shown
    assert "sphere.csv" in shown
    assert "Lemma 5.4" in shown
    assert "、" not in shown and "。" not in shown
    assert result.conclusion is None and result.open_goals
```

## New test files (complete)

### `test_patch_contract.py`

```python
"""Independent fail-closed contracts for the historical test-only corrections."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r17r3r4_historical_test_contract.patches import (
    CHANGES,
    FILES,
    transform,
)

ROOT = Path(__file__).resolve().parents[2]


def test_all_modified_tests_were_reviewed_and_are_syntactically_valid() -> None:
    assert set(FILES) == set(CHANGES)
    assert len(FILES) == 10
    for path in FILES:
        original = (ROOT / path).read_text(encoding="utf-8")
        updated = transform(path, original)
        assert updated != original.replace("\r\n", "\n")
        ast.parse(updated, filename=path)
        assert "pytest.skip" not in updated
        assert "pytest.xfail" not in updated


def test_every_replacement_is_fail_closed_and_not_repeatable() -> None:
    for path in FILES:
        updated = transform(path, (ROOT / path).read_text(encoding="utf-8"))
        with pytest.raises(RuntimeError, match="unreviewed or already patched"):
            transform(path, updated)


def test_unreviewed_test_path_is_rejected() -> None:
    with pytest.raises(ValueError, match="unreviewed test path"):
        transform("web_group_proof.py", "def test_dummy(): pass\n")


def test_helper_and_legacy_tests_are_preserved() -> None:
    p = ROOT / "phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py"
    updated = transform(p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8"))
    assert "def test_source_verified_abstract_markdown_is_explicitly_partial" in updated
    assert "def test_shared_fallback_web_uses_same_abstract_projection" in updated
    assert "def test_trace_route_remains_without_added_narrative" in updated
    assert 'assert "証明済みの抽象群構造" in section' in updated

```

### `test_unified_public_contract.py`

```python
"""Real Web regression after historical test expectations follow the unified model."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_model_web_keeps_one_source_list_and_unproved_named_goals(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    model = build_proof_narrative_model(result)
    assert model.open_goals == result.open_goals
    assert any(step is result.abstract_structure.proof_step for step in model.steps)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, citation_source="model", mode="narrative",
    )
    assert view.partial_result and view.abstract_structure_certified
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("使用する結果") == 1
    assert headings.count("未解決 Goal") == 1
    assert headings.count("確認済み ProofStep（与件を含む）") == 1
    assert "検証済み証明木の Reference" not in headings
    assert "検証済みの途中経過" not in headings
    assert "証明済みの抽象群構造" not in headings
    shown = "\n".join(segment.value for line in view.rendered_lines
                       for segment in line.segments)
    assert "Proposition 4.4" in shown
    assert "Lemma 5.4" in shown
    assert r"\cong" in shown
    assert "数式表示未対応" not in shown
    assert "Relation(lhs=" not in shown
    assert "、" not in shown and "。" not in shown


def test_uncertified_group_keeps_no_fabricated_references() -> None:
    result = search_group_from_registered_goal(n=5, k=3)
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert not model.citations
    assert result.open_goals and result.conclusion is None
    view = build_standard_web_group_proof_view(n=5, k=3, mode="narrative")
    assert view.key == "generic-partial-proof"
    assert not view.abstract_structure_certified
    assert not view.steps


def test_named_complete_proof_stays_complete() -> None:
    result = search_group_from_registered_goal(n=4, k=4)
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    view = build_standard_web_group_proof_view(n=4, k=4, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert not view.partial_result and not view.abstract_structure_certified

```
