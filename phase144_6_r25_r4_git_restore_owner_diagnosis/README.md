# Phase 144-6 R25-R4

R25-R4 は R24 rollback を文字列置換で行いません。

最初に確認済みの R24 production 対象である次の2ファイルだけを
Git `HEAD` からそのまま復元します。

- `main.py`
- `toda_group_proof_narrative_argument_multi_renderer.py`

使用する操作は次のものです。

```powershell
git restore --source=HEAD -- `
  "main.py" `
  "toda_group_proof_narrative_argument_multi_renderer.py"
```

直後に `git diff --exit-code` を実行し、両ファイルが HEAD と完全一致
している場合だけ focused tests と owner diagnosis に進みます。

## Diagnosis boundary

診断では `pi_6^3` の depth=2 と full/default presentation を比較し、
`ProofStep` identity を使って以下を追跡します。

- `establish_definition` Argument の有無
- definition block / step の owner
- contribution owner
- final Narrative への生存
- `pi_5^3` supporting step の owner
- contribution role / placement / provider
- premise / parent edge
- final Narrative への生存

新しい production repair は行いません。
全体 pytest は実行しません。
診断結果を確認した時点で停止します。
