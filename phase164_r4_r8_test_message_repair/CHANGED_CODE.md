# Phase 164 R4-R8 テスト期待値の修正

## 変更対象

- `tests/test_phase164_r4_r8_registry_reconstruction.py` の `test_fake_source_statement_id_rejected()` のみ。
- 既存 Production コードは変更しない。
- import は変更しない。以下が変更後の import を含む先頭部分の全文。

```python
"""Phase 164 R4-R8: fixed literature references flow into actual reconstruction."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement
```

## 置換するテスト関数の全文

```python
def test_fake_source_statement_id_rejected(inputs):
    crosswalk, leaves, roots = inputs
    changed = dict(crosswalk)
    changed["leaves"] = [dict(row) for row in crosswalk["leaves"]]
    changed["leaves"][1]["source_statement_id"] = "toda:tex:ch5:fake"
    with pytest.raises(ValueError, match="source IDs or source identity changed"):
        reconstruct_phase164_r4_r8_pi5_3(
            changed, leaves, roots, user_confirmed_original=True,
        )

```

## 理由

偽の出典 ID は `register_phase164_r4_r6_typed_bindings()` で `ValueError("source IDs or source identity changed")` として拒否される。拒否の挙動は正しいためテストの `match` だけをこのメッセージに合わせる。

## 実行

`run.ps1` は修正したテストファイル全体を配置し、R4-R8・R4-R6・R4-R3・Phase 161 R7 の局所 pytest を実行後、既存 R4-R8 のレポートと証明文章を生成する。

## 完了条件

- 33件の対象テストが成功する。
- `phase164_r4_r8_output` に Registry 経由の証明再構築結果が出力される。
- 全体 pytest は Phase 164 の最終段階まで行わない。

## 次の Phase 境界

今回はテストメッセージ修正のみ。機能追加・一般化・Phase 164 終了判定は含めない。
