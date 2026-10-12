# R4-R63 入力パス修正

## 変更対象

- `phase163_r4_r63_source_boundaries/run.ps1`：全文置換。R4-R42 の `phase163_r4_r42_tex_extract/inputs` を優先し、3個の TeX がそろう場合のみプロジェクト直下にフォールバック。決定したディレクトリをテストおよび監査プログラムへ渡す。
- `phase163_r4_r63_source_boundaries/tests/test_phase163_r4_r63_source_boundaries.py`：`import os` を追加、`evidence()` fixture 全体を修正。環境変数 `EHP_R63_TEX_ROOT` があればテストの TeX 参照に利用。
- `README.md`：英語で入力配置を追記。

監査本体の Python は無変更。出典範囲、候補16件、登録境界は無変更。全体 pytest は行わない。

## 変更後の import 全文（テスト）

```python
import copy
import json
import os
from pathlib import Path

import pytest

from phase163_r4_r63_source_boundaries import (
    SPAN_PROPOSALS,
    audit_boundaries,
    load_inputs,
    write_reports,
)
```

## 変更後 fixture 全文

```python
@pytest.fixture
def evidence():
    root = Path(__file__).resolve().parents[2]
    inventory = root / "phase163_r4_r62_output" / "remaining_definitions.json"
    if not inventory.exists():
        inventory = root / "remaining_definitions.json"
    tex_root = Path(os.environ.get("EHP_R63_TEX_ROOT", str(root)))
    return load_inputs(inventory, tex_root)
```

`run.ps1` は ZIP に全文収録。
