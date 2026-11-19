# Phase 175 R4R12R13R5 — Δ 単射候補の型付き監査

## 調査対象

- `phase175_r4r12r13r2_delta_injective_e_surjective.rule.delta_injective_inputs`
- `phase175_r4r12r13r3_public_delta_e_bridge.provider.delta_free_coordinate_proposals`
- `phase175_r4r10_cited_58_prop25_public.source.canonical_toda58`
- `phase169_r10e4_ordered_db_prior.db_prior.exact_prior_database_result`
- `phase165_r52_r9_shared_math.shared_expansion_provider`

## 目的

Δ 単射候補が0件となる位置を、出典・群の直和型・自由生成元・有限生成元・座標計算・公開接続に分けて記録する。監査結果をもって未解決証明を完成と見なさない。

## 変更範囲

追加するのはこの監査用パッケージのみ。既存ファイル、API、数学規則、GIVEN、証明データは変更しない。

## Gate

DryRun と本実行で読み取り専用監査が正常終了し、限定 pytest 3件が通過したら監査 PASS。`DELTA_CANDIDATES=0` 自体は未完成であり監査失敗を意味しない。

## 次の境界

R13R5 の結果で具体的な不一致が確定した後に、必要性が数学的に検証された一般的な表現同値性または照合規則のみを別 Phase/round で検討する。全体 pytest は Phase 175 の最後にのみ実施する。
