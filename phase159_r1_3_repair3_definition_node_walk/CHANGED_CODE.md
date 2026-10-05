# Phase 159-R1-3 repair3

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase159_project_generic_semantics_to_public_proof()`

import の変更はありません。
テストの変更もありません。

## 変更内容

definition projection の走査対象を

```python
semantic_sidecar.dependency_semantics
```

から

```python
semantic_presentation.nodes
```

へ変更する。

判定そのものは `_phase159_unique_preimage_definition_line()` に委譲する。
その helper は `proof_step.premises` に同一 map の isomorphism premise が
存在する場合だけ文字列を返すため、一般的な semantic condition のままである。

## 変更後の definition traversal 全体

```python
  for node in semantic_presentation.nodes:
    proof_step = node.proof_step
    original = _render_generic_narrative_step(
      proof_step
    )
    replacement = (
      _phase159_unique_preimage_definition_line(
        proof_step,
      )
    )

    if replacement is None:
      continue

    for index, line in enumerate(
      lines
    ):
      if original not in line:
        continue

      prefix = line[
        :line.find(
          original
        )
      ]

      if prefix in (
        "これらから, ",
        "これらより, ",
        "このことから, ",
        "したがって, ",
      ):
        prefix = ""

      lines[
        index
      ] = (
        prefix
        + replacement
      )
      break
```

## 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase49_generator_transport.py" `
  ".\tests\test_phase143_71a_eta_definition_visibility.py"
```

## 完了条件

- Phase 159 focused tests が全 PASS。
- definition/inference regression が全 PASS。
- `git diff --check` が PASS。
- pi_3^2 public Narrative で eta_2 が isomorphism による unique preimage として表示される。

## 次 Phase との境界

今回変更しない:
- exactness component
- map-property numbering
- target rendering
- Reference attribution
- theorem / inference rule
- stable range / Freudenthal
