# Phase 163 R4-R11 — 祖先由来の診断

**監査状態: BLOCKED_BY_PROVENANCE**

| 成分 | 引用接続 | 内容検査 | 祖先の構造的不備 |
|---|---|---|---|
| `pi6_3_group_relation` | VERIFICATION_FAILED | NOT_VERIFIED | `root/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]: INFERENCE_PREMISES_MISSING` |
| `pi7_4_group_relation` | VERIFICATION_FAILED | NOT_VERIFIED | `root/premise[1]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]: INFERENCE_PREMISES_MISSING` |
| `pi8_5_group_relation` | VERIFICATION_FAILED | NOT_VERIFIED | `root/premise[0]/premise[0]/premise[0]/premise[4]/premise[0]/premise[0]/premise[0]: INFERENCE_PREMISES_MISSING`, `root/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]: INFERENCE_PREMISES_MISSING` |
| `higher_nu_group_relation` | VERIFICATION_FAILED | NOT_VERIFIED | `root/premise[0]/premise[0]/premise[0]/premise[0]/premise[0]/premise[4]/premise[0]/premise[0]/premise[0]: INFERENCE_PREMISES_MISSING`, `root/premise[0]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[1]/premise[0]/premise[0]/premise[0]/premise[3]: INFERENCE_PREMISES_MISSING` |

## 重要

- 引用検証に失敗した Statement は metadata_only のまま維持します。
- 不備を検出しなかった場合も、既存の validator が不合格なら接続しません。
- 証明木に不足する推論規則や前提を捏造して補いません。
- 文献原本の独立照合、全体 pytest は未実施です。
