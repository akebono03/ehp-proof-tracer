# Phase157 R5-R10 repair5

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

変更する関数:

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`

変更内容:

Reference section を proof body に連結する最終箇所で、public section structure を直接生成する。

```text
# Group proof narrative

## 使用する結果

...

---

## 証明

...
```

これにより `pi_6^3` でも legacy intro に依存せず、Reference/Proof 境界が明示される。

### `tests/test_phase157_r5_r10_reference_proof_boundary_qed.py`

`## 証明対象` と `## 証明` を混同しないよう、exact proof heading を検索する。

## Phase 境界

proof body relevance、Reference selection、argument ordering は変更しない。
