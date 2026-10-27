# Phase 169 R8 — 3-stem 安定輸送の依存関係監査

- モード: AUDIT_ONLY
- Git HEAD: `c6ec2cd7579d16472e2381b9dfe5ff6e5b592546`
- 既存 tracked files 不変: `True`
- 全体 pytest: 未実行

| 群 | 証明状態 | ProofStep | 未解決 Goal | 共通輸送候補 |
|---|---|---:|---:|---:|
| π_8^5 | search_failed | 0 | 3 | 0 |
| π_9^6 | search_failed | 0 | 3 | 1 |

π_9^6 の先行候補 π_8^5: 文献順利用=True, 理由=prior_fixed_source, 型付き画像数=1
| π_10^7 | search_failed | 0 | 3 | 1 |

π_10^7 の先行候補 π_8^5: 文献順利用=True, 理由=prior_fixed_source, 型付き画像数=2

π_10^7 の先行候補 π_9^6: 文献順利用=False, 理由=source_not_prior, 型付き画像数=1

## 解釈の注意

- 先行 group Relation は DB の候補であり GIVEN ではない。
- `eligible` は文献順の可否であり、群構造の証明完成ではない。
- `direct_general_transport_candidates` は証明候補であり complete ではない。
- 画像の型付き構築と、画像の実際の証明は別段階。
- 3-stem 公開 Provider の変更・R6B の実行は一切行わない。
- 数値的な安定範囲は k=3 の n>=5。
