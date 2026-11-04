# R15R15R2 — 変更クラス・関数・import 全文

変更対象: `web_group_proof_common.py` の `WebGroupProofView` クラス全体、`phase165_r52_r3_web_adapter.py` の `build_partial_web_group_proof_view` 関数全体、`templates/index.html` の群問い合わせ `not_found` 分岐。新たな関数は `patches.py`、`install.py`、`tests` に追加（下記 `SOURCE_CODE.md`）。クラス以外の既存関数は変更しない。import の変更はないが、再現用に import 部分を全文掲載する。

## web_group_proof_common.py — 変更前と同じ import 全文

```python
from dataclasses import dataclass
from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from toda_human_readable_renderer import render_toda_public_group_relation_latex
from toda_proof_narrative_renderer import render_toda_proof_statement_latex
```

## web_group_proof_common.py — WebGroupProofView クラス全体

```python
@dataclass(frozen=True)
class WebGroupProofView:
  n: int
  k: int
  conclusion_latex: str
  theorem: str | None
  phase: str | None
  key: str
  steps: tuple[
    WebGroupProofStepView,
    ...,
  ]
  max_depth: int
  mode: str = "trace"
  rendered_lines: tuple[
    WebGroupProofRenderedLineView,
    ...,
  ] = ()
  partial_result: bool = False
  abstract_structure_certified: bool = False

  def __post_init__(
    self,
  ) -> None:
    for name, value in (
      ("n", self.n),
      ("k", self.k),
    ):
      if (
        isinstance(
          value,
          bool,
        )
        or not isinstance(
          value,
          int,
        )
      ):
        raise TypeError(
          f"{name} must be an int"
        )

    if not isinstance(
      self.conclusion_latex,
      str,
    ):
      raise TypeError(
        "conclusion_latex must be a str"
      )

    if not self.conclusion_latex:
      raise ValueError(
        "conclusion_latex must not be empty"
      )

    if (
      self.theorem is not None
      and not isinstance(
        self.theorem,
        str,
      )
    ):
      raise TypeError(
        "theorem must be a str or None"
      )

    if (
      self.phase is not None
      and not isinstance(
        self.phase,
        str,
      )
    ):
      raise TypeError(
        "phase must be a str or None"
      )

    if not isinstance(
      self.key,
      str,
    ):
      raise TypeError(
        "key must be a str"
      )

    if not self.key:
      raise ValueError(
        "key must not be empty"
      )

    if not isinstance(
      self.steps,
      tuple,
    ):
      raise TypeError(
        "steps must be a tuple"
      )

    if not isinstance(self.partial_result, bool):
      raise TypeError("partial_result must be a bool")

    if not isinstance(self.abstract_structure_certified, bool):
      raise TypeError("abstract_structure_certified must be a bool")

    if self.abstract_structure_certified and not self.partial_result:
      raise ValueError("abstract certificate cannot mark a complete named proof")

    if not self.steps and not self.partial_result:
      raise ValueError(
        "steps must not be empty"
      )

    for step in self.steps:
      if not isinstance(
        step,
        WebGroupProofStepView,
      ):
        raise TypeError(
          "steps must contain only "
          "WebGroupProofStepView values"
        )

    if (
      isinstance(
        self.max_depth,
        bool,
      )
      or not isinstance(
        self.max_depth,
        int,
      )
    ):
      raise TypeError(
        "max_depth must be an int"
      )

    if self.max_depth < 0:
      raise ValueError(
        "max_depth must be nonnegative"
      )

    if self.mode not in (
      "trace",
      "outline",
      "narrative",
    ):
      raise ValueError(
        "mode must be trace, outline, or narrative"
      )

    if not isinstance(
      self.rendered_lines,
      tuple,
    ):
      raise TypeError(
        "rendered_lines must be a tuple"
      )

    for line in self.rendered_lines:
      if not isinstance(
        line,
        WebGroupProofRenderedLineView,
      ):
        raise TypeError(
          "rendered_lines must contain only "
          "WebGroupProofRenderedLineView values"
        )

    if (
      self.mode == "trace"
      and self.rendered_lines
    ):
      raise ValueError(
        "trace mode must not have rendered_lines"
      )

    if (
      self.mode != "trace"
      and not self.rendered_lines
    ):
      raise ValueError(
        "outline and narrative modes require "
        "rendered_lines"
      )
```

## phase165_r52_r3_web_adapter.py — import 全文

```python
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus, render_partial_proof_markdown
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from web_group_proof_common import (
    WebGroupProofStepView,
    WebGroupProofView,
    _build_group_proof_rendered_lines,
    _group_proof_rule_name,
    _group_proof_statement_latex,
)
```

## phase165_r52_r3_web_adapter.py — 関数全体

```python
def build_partial_web_group_proof_view(
    result: PartialProofResult,
    *,
    max_depth: int = 2,
    mode: str = "narrative",
    narrative_model: ProofNarrativeModel | None = None,
) -> WebGroupProofView:
    """Adapt searched steps; render a supplied proof model without rewriting it."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")
    if narrative_model is not None and not isinstance(narrative_model, ProofNarrativeModel):
        raise TypeError("narrative_model must be ProofNarrativeModel or None")

    n = result.target.sphere_dimension
    dimension = result.target.group_dimension
    k = dimension - n
    target_latex = rf"\pi_{{{dimension}}}^{{{n}}}"
    if result.status is ProofSearchStatus.COMPLETE:
        target_statement = result.conclusion
    else:
        target_statement = next(
            (
                item for item in reversed(result.open_goals)
                if getattr(item, "lhs", None) == result.target
                or getattr(item, "group", None) == result.target
            ),
            None,
        )
    if target_statement is not None:
        statement_latex, fallback_type = _group_proof_statement_latex(target_statement)
        if statement_latex is not None and fallback_type is None:
            target_latex = statement_latex

    steps = []
    for step in result.proven_steps:
        statement_latex, fallback_type_name = _group_proof_statement_latex(step.conclusion)
        steps.append(WebGroupProofStepView(
            depth=0,
            statement_latex=statement_latex,
            fallback_type_name=fallback_type_name,
            rule_name=_group_proof_rule_name(step),
            role_name="derived",
        ))

    if mode == "trace":
        rendered_lines = ()
    else:
        if narrative_model is None:
            # Preserve the existing legacy/compatibility narrative route.
            markdown = render_partial_proof_markdown(result)
            from phase173_r4_r15r9_shared_abstract_renderer.projection import (
                render_certified_abstract_section,
            )
            abstract_markdown = render_certified_abstract_section(result)
            if abstract_markdown:
                markdown = markdown.rstrip() + "\n\n" + abstract_markdown + "\n"
        else:
            from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
            markdown = render_model_backed_narrative_markdown(result, narrative_model)
        rendered_lines = _build_group_proof_rendered_lines(markdown)

    return WebGroupProofView(
        n=n,
        k=k,
        conclusion_latex=target_latex,
        theorem=None,
        phase="165 R52-R3",
        key=("generic-complete-proof" if result.status is ProofSearchStatus.COMPLETE else "generic-partial-proof"),
        steps=tuple(steps),
        max_depth=max_depth,
        mode=mode,
        rendered_lines=rendered_lines,
        partial_result=(result.status is not ProofSearchStatus.COMPLETE),
        abstract_structure_certified=(result.abstract_structure is not None),
    )
```

## templates/index.html — 置換する条件分岐全体

```html
      {% elif view.status.value == "not_found" %}
        {% if group_proof_view and not group_proof_view.partial_result %}
          <p>Typed proof search completed. See Group proof below.</p>
        {% elif group_proof_view and group_proof_view.abstract_structure_certified %}
          <p>
            A verified abstract group structure is available, but the
            named-generator proof is incomplete. See Group proof below.
          </p>
        {% else %}
          <p>No proof-backed result found for this query.</p>
        {% endif %}
```

今回 `WebGroupQueryView` と `build_standard_web_group_query_view` は変更しない。`abstract_structure_certified` は証明書の有無のみを伝え、記名生成元の完成状態や結果を昇格しない。

## R15R15R2 での Installer 修正

旧 Installer の `REVIEWED_HEAD` と未コミット R15R14 再適用ロジックを廃止し、R15R14 コミット済みの baseline と Git blob 一致を使用。新規の `install.py`、`patches.py`、`run.ps1` は `SOURCE_CODE.md` に全文収録。
