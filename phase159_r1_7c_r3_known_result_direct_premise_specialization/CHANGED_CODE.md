# Phase 159 R1-7c R3 — replacement units

## 変更対象

- `toda_group_proof_narrative_contribution_renderer.py`
  - import 全文は下記。
  - 新規 functions 全文は `apply_phase159_r1_7c_r3.py` の `HELPERS` に省略なしで収録。
  - 既存 `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()` は
    最終 ordering 後に R3 postprocessor を1回呼ぶだけの最小変更。
- `tests/test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py`
  - 新規 test file。必要 import と全 test functions を全文収録。

## 変更後 import 全文

```python
from collections import deque
from dataclasses import (
  fields,
  is_dataclass,
  replace,
)

from expression import (
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)

from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_latex,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_step,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeOperationKind,
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
  order_toda_group_proof_narrative_injective_image_order_reason,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
  restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)
```

## 既存 function の変更単位

実行 patch は既存 function 全体を再生成しない。
R2 までの local changes を保持するため、次の一意 anchor のみ置換する。

```python
  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )
  rendered = (
    specialize_toda_group_proof_narrative_root_zero_direct_premises(
      presentation,
      rendered,
    )
  )

  generic_used_step_ids = (
```

新規 functions と新規 tests は package 内で全文確認できる。
