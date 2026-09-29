# Phase 144-6-R2 audit package

監査のみ。production code は変更しません。

監査対象:
- legacy pi_6^3 Narrative の R1-R5
- generic/public Narrative の reference 保存状況
- depth 2 / depth 3 の式番号・式参照差
- eta composite supporting facts の Block / Argument 所属
- Semantic sidecar に reference identity / numbering が存在するか
- public renderer と generic multi-argument renderer の一致

全体 pytest は実行しません。
