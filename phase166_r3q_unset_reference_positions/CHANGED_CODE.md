# Phase 166 R3-Q：掲載位置未設定 Reference の既存文献IDへの接続

## 変更対象

- `phase166_r3l_reference_order.py`：定数 `REVIEWED_REFERENCE_ALIASES` に4件を追加。関数・クラス・import は変更しない。
- 新規 `phase166_r3q_unset_reference_positions/apply.py`、`restore.py`、`run.ps1`：導入・自動復元・限定テスト。
- 新規 `tests/test_phase166_r3q_unset_reference_positions.py`：テスト4件。import と関数全文はファイルに記載。

## 追加する対応（既存の辞書内）

```python
    "adopted:ref:7": "toda:Proposition 4.2",
    "adopted:ref:8": "toda:Proposition 4.2",
    "adopted:ref:9": "toda:Proposition 4.2",
    "adopted:reference:prop42:general": "toda:Proposition 4.2",
```

GitHub 上の `phase166_r3m_source_order_audit_results.json` では、7・8・9は `phase163:archive:toda:tex:ch4:0005` を出典として保持している。一般形は `phase165_r12_r11_prop42_unified.py` が同一 SOURCE_ID の文献命題を使用している。manifest は `toda:Proposition 4.2` を位置68として保持する。名称だけによる推測的な位置付与はしない。

変更対象の辞書・import を含む完全な `phase166_r3l_reference_order.py` は、変更後に本番ファイルそのものとして存在する。現行ファイル全文をバックアップしたうえで辞書の4件だけを追加するため、その他の API と既存内容は維持する。

## テスト・完了条件

```powershell
python -m pytest -q phase166_r3q_unset_reference_positions/tests/test_phase166_r3q_unset_reference_positions.py phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py
```

10 PASS、4つの Reference が同じ既存位置に接続され、R3-P の位置と π₃² の完全証明が維持されること。全体 pytest は Phase 166 終了時のみ。

## 次 Phase との境界

R3-Q の文献位置接続の一部である。通常 Web 証明探索への掲載順ゲート全面移行、π₄³・π₅⁴ の完成保証、Proof 再利用や専用分岐は実装しない。
