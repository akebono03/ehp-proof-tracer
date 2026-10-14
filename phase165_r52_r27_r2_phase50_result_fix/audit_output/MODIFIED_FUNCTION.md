# 変更後の関数全文

```python
def build_toda_52_composition_isomorphism_step():
  phase50 = _build_phase50_result()
  eta2_definition_steps = tuple(
    step for step in phase50["result"].steps
    if isinstance(step.conclusion, TodaPi32Eta2DefinitionStatement)
  )
  return eta2_definition_steps

```
