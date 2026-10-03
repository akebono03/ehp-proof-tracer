# Phase157 R11-R6 changed code

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更関数:

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`

削除する処理:

```python
  rendered = (
    _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(
      presentation,
      rendered,
    )
  )
```

この処理が proof body に実際には消費されない

```text
E: pi_4^2 -> pi_5^3 isomorphism
```

を後から復元していたことを R11-R5 で確認済み。

helper function 自体は今回削除しない。
Phase157 R11 の必要最小限変更に留める。

## 新規テスト

`tests/test_phase157_r11_proof_body_relevance.py`

テスト関数:

- `test_phase157_r11_pi6_3_body_excludes_unconsumed_suspension_isomorphism`
- `test_phase157_r11_pi6_3_body_keeps_consumed_pi6_5_group`
- `test_phase157_r11_pi6_5_group_precedes_its_order_consumer`

## 実行 pytest

```powershell
python -m pytest `
  tests/test_phase157_r11_proof_body_relevance.py `
  tests/test_phase157_r5_r9_fixed_definition_body_suppression.py `
  -q
```

## 完了条件

1. 不要な suspension isomorphism が proof body から消える。
2. `pi_6^5 = Z/2{eta_5}` は残る。
3. `pi_6^5` は order consumer より前にある。
4. Phase157-R5/R9 の Reference/body suppression を壊さない。

## 次との境界

次は R11 の代表群・軽量横断確認。
112-group audit と full pytest は Phase157 closure でのみ実行する。
