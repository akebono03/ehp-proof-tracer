# Phase 165 R6-2 R4-3 候補生成根拠監査

- 状態: `PROVENANCE_AUDITED`
- 検査 Goal: 201
- 証明検証数: 0

## 経路別の候補

| Provider ID | 候補数 |
|---|---:|
| R26_GENERIC | 7 |
| SEEDED_R4 | 14 |
| SHARED | 22 |

## エラー

```json
[]
```

## 制約

- An object rule ID is accepted only if exposed by the registry entry.
- Matching cited premise IDs do not prove which witness bound a variable.
- Witness/Seeded returns do not expose the witness-selection trace.
- Fingerprint overlap compares proposals, not proofs.
- SHARED may deduplicate and gate candidates, so totals need not add.
- This audit does not execute recursive proof reconstruction.

候補ごとの Rule ID、前提、重複、出典候補は JSON を参照。
