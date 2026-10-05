# Phase 158-R2 — Narrative Public Shell Normalization

## 目的

proof depth 2 以上の public Narrative を、renderer route に依存せず次の構造へ統一する。

```text
# Group proof narrative

## 証明対象

...

## 使用する結果

...

---

## 証明

...

□
```

## Production code の変更

`toda_group_proof_narrative_renderer.py`

- 新規関数:
  - `_phase158_normalize_public_narrative_contract()`
  - 追加位置: `_is_phase150_rc4_generic_route_target()` の後、
    `render_toda_group_proof_narrative_markdown()` の直前
- 変更関数:
  - `render_toda_group_proof_narrative_markdown()`

import の変更はない。

## Phase 境界

変更する:
- public section shell
- missing target section の root conclusion からの補完
- Reference/Proof 間の `---`
- 最終 `□`

変更しない:
- Reference attribution
- fixed/proof-internal classification
- proof-body mathematical derivation
- generic semantic renderer の内容
- depth 1 legacy fallback

## Test

focused test と 112-group contract audit のみを実行する。
全体 pytest は Phase 158 の最後まで実行しない。
