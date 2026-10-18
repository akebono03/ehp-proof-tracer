# 変更対象とコード全文

変更対象：`phase165_r52_partial_proof.py` の `render_partial_proof_markdown()`。import の変更なし。新規関数の追加なし。

```python
def render_partial_proof_markdown(result: PartialProofResult) -> str:
    \"\"\"Route complete results to the restored Narrative; incomplete results to partial.\"\"\"
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(result)
    from toda_group_proof_narrative_renderer import render_toda_partial_proof_narrative_markdown
    return render_toda_partial_proof_narrative_markdown(result)

```

テスト全体は `test_route.py`、実行コード全体は `install.py` と `run.ps1` に収録。
