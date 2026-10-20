# Phase 166 R3-C 第2段階：限定テストの修正

変更対象は `phase166_r3c_stage2/test_stage2.py` の `test_non_earlier_reference_is_rejected` のデコレータのみ。テスト関数そのもの、その他のテスト関数、import、既存の本番コードは変更しない。

修正後のテストファイル全文は同梱の `test_stage2.py` に収録。既存ファイルと新ファイルの相違は次の1行のみ。

```python
@pytest.mark.parametrize("position", [78, 79, None])
```

証明対象の掲載位置78に対して、76、77は厳密に先行するため利用可能。78、79、未設定は利用不可。

対象限定 pytest：`phase166_r3c_stage2/test_stage2.py`、`tests/test_phase165_r3_recursive_search.py`、`phase166_r3_ordered_lookup/tests/test_phase166_r3_ordered_lookup.py`。

完了条件：対象限定テストが PASS し、Web の $\pi_3^2$ が `generic-complete-proof` を維持する。R3-D/R3-E および全体 pytest は実施しない。
