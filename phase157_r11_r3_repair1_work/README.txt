Phase157 R11-R3 repair1

前回の R11-R3 audit は reason prose renderer の import module 名を誤っていた。

誤:
toda_group_proof_narrative_reason_prose

正:
toda_group_proof_narrative_reason_renderer

この repair1 は import だけを修正し、
以下4段階で statement origin を確認する。

1. base markdown
2. contribution insertion 後
3. reason prose insertion 後
4. final public narrative

対象:
- E: pi_4^2 -> pi_5^3
- pi_6^5 = Z/2{eta_5}

Production code changes: none
Test code changes: none
pytest: not run
