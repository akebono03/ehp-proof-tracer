# Phase 166 R3-C import 修正

## 変更対象

- 新規 `phase166_r3b_publication_order_binding/__init__.py`：既存ディレクトリを package として認識させ、3個の公開 API を再エクスポートする。
- 新規 `phase166_r3c_import_fix/run.ps1`：import の確認と R3-C 限定テストを実行する。
- 新規 `phase166_r3c_import_fix/README.md`、`CHANGED_CODE.md`。

## 変更しないもの

- `phase165_r3_recursive_search.py`：R3-C 適用済みのまま変更しない。
- `phase166_r3b_publication_order_binding/phase166_r3b_publication_order_binding.py`：変更なし。
- 既存テスト：変更なし。
- 掲載順、命題内順、依存関係、ProofStep、Renderer、SQLite：変更なし。

## 新規ファイルの全文

`phase166_r3b_publication_order_binding/__init__.py`:

```python
"""Phase 166 R3-B public exports from the existing publication-order module.

Package marker resolves the directory/module name collision for R3-C.
"""

from .phase166_r3b_publication_order_binding import (
    PublicationOrderBinding,
    PublicationOrderBindingSummary,
    connect_phase163_publication_order,
)

__all__ = [
    "PublicationOrderBinding",
    "PublicationOrderBindingSummary",
    "connect_phase163_publication_order",
]
```

## 対象テスト

`python -m pytest -q phase166_r3c_ordered_search/tests/test_phase166_r3c_ordered_search.py`

## 完了条件・境界

import の成功と R3-C 9件 PASS。全体 pytest は Phase 166 終了時にのみ実施。R3-D の $\\pi_3^2$ 証明検証は実施しない。
