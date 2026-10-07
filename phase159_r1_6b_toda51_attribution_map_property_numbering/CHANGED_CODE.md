# Phase 159-R1-6b

## 変更対象

- `toda_literature_statement_boundary.py`
  - `_EQUATION_51_COMPONENTS` を追加
  - `_FIXED_COMPONENTS_BY_REFERENCE`
  - `_FIXED_RULE_COMPONENT_KEYS`
  - `_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME`
- `toda_upstream_bootstrap.py`
  - `_build_phase49_result()` の最初の3 premise
- `toda_group_proof_narrative_renderer.py`
  - `import re`
  - 新規 `_phase159_number_public_map_property_statement()`
  - `render_toda_group_proof_narrative_markdown()`
- `tests/test_phase159_r1_6a_foundational_reference_identity.py`
  - R1-6b により superseded（置換）
- 新規 `tests/test_phase159_r1_6b_toda51_attribution.py`

## `(5.1)` fixed components

```python
_EQUATION_51_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="circle_higher_homotopy_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text="i > 1",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="sphere_connectivity_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text="i < n",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="stable_negative_zero",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text="k < 0",
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="diagonal_identity_group",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="stable_zero_stem",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="diagonal_suspension_isomorphism",
    statement_role=TodaLiteratureStatementRole.OTHER,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=False,
  ),
)
```

## `_build_phase49_result()` の変更部分

最初の3つの `ProofStep` を以下へ置換する。

```python
    ProofStep(
      conclusion=pi_2_1_zero_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=InferenceRule(
        name=(
          "Toda (5.1) circle higher homotopy zero"
        ),
        literature_reference=LiteratureReference(
          label="Toda (5.1)",
          locator="(5.1)",
        ),
      ),
    ),
    ProofStep(
      conclusion=pi_3_3_free_cyclic_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=InferenceRule(
        name=(
          "Toda (5.1) diagonal identity group"
        ),
        literature_reference=LiteratureReference(
          label="Toda (5.1)",
          locator="(5.1)",
        ),
      ),
    ),
    ProofStep(
      conclusion=e_pi_1_1_to_pi_2_2_isomorphism_fact(),
      premises=(),
      rule=ProofRule.GIVEN,
      inference_rule=InferenceRule(
        name=(
          "Toda (5.1) low-dimensional "
          "suspension isomorphism"
        ),
        literature_reference=LiteratureReference(
          label="Toda (5.1)",
          locator="(5.1)",
        ),
      ),
    ),
```

## renderer import

変更後、既存 import 群に加えて以下が必要。

```python
import re
```

## 新規番号正規化関数

`render_toda_group_proof_narrative_markdown()` の直前に追加。

```python
def _phase159_number_public_map_property_statement(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  pattern = re.compile(
    r"^\$(?P<map>.+?)"
    r"\\tag\{(?P<number>[0-9]+)\}"
    r"\$ は"
    r"(?P<property>単射|全射|同型|零写像)"
    r"\.$"
  )

  lines = []

  for line in rendered.splitlines():
    match = pattern.match(
      line.strip()
    )

    if match is None:
      lines.append(
        line
      )
      continue

    leading = line[
      :len(
        line
      )
      - len(
        line.lstrip()
      )
    ]

    lines.append(
      leading
      + "$"
      + match.group(
        "map"
      )
      + r" \text{ は"
      + match.group(
        "property"
      )
      + r"}. \tag{"
      + match.group(
        "number"
      )
      + "}$"
    )

  return "\n".join(
    lines
  )
```

## `render_toda_group_proof_narrative_markdown()` 全体

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_normalize_public_map_property_wording(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_number_public_map_property_statement(
      rendered
    )
  )

  return (
    _phase159_inject_foundational_reference_section(
      presentation,
      rendered,
    )
  )
```

## テスト

新規:
`tests/test_phase159_r1_6b_toda51_attribution.py`

検証:
- 3 low-dimensional facts が `(5.1)` fixed statement として分類される。
- Reference は単一 `[R1] (5.1)`。
- `[F1]`〜`[F3]` は消える。
- target `pi_3^2=Z{eta_2}` は Reference に入らない。
- Proposition 5.1 に誤帰属しない。
- `(1)`, `(2)` は `単射`, `全射` まで含む statement 全体に付く。

## pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py" `
  ".\tests\test_phase49_low_dimensional_facts.py" `
  ".\tests\test_phase49_generator_transport.py"
```

## 完了条件

- `[R1] (5.1)` に統合。
- `[F...]` を public Narrative から撤去。
- map-property tag が property を含む。
- focused / related tests PASS。
- `git diff --check` PASS。
- full pytest は未実行。

## 次 Phase との境界

R1-6b は attribution と numbering まで。
必要なら次段で `(5.1)` Reference と proof body の prose linkage
（`[R1] より` / `完全性より`）をさらに整える。
