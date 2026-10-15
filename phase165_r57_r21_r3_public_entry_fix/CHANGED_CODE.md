# R57-R21-R3 変更コード

変更対象: `phase165_r52_partial_proof.py` の `render_partial_proof_markdown()`。import の変更なし。ほかのクラス・関数を変更しない。公開関数の有効な最終定義を置換する。関連する追加テストの全文は ZIP 内 `test_phase165_r57_r21_r3_public_entry_fix.py`。

```python
def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Render all partial and complete searches through the effective shared renderer."""
    from toda_group_proof_generic_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    return render_toda_partial_proof_narrative_markdown(result)
```

installer は `install.py`、実行スクリプトは `run.ps1` に全文収録。
