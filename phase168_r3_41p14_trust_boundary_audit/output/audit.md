# Phase 168 R3-41P14 — Trust Boundary 経路監査

本監査は読み取り専用。アプリ本体、既存テスト、固定基準は変更しない。

## 3群の監査

| 群 | 推論 | GIVEN | 本文・Reference全文一致 | Citation |
|---|---:|---:|---|---|
| pi3_2 | 13 | 5 | True | True |
| pi4_3 | 19 | 6 | True | True |
| pi5_4 | 7 | 3 | True | True |

## 標準Web経路の人工入力による境界監査

※内部関数をモックした構造テストであり、外部ユーザーからの攻撃可能性を立証するものではない。

| ケース | 検証呼出 | Model構築 | 拒否 |
|---|---:|---:|---|
| positioned_complete | 1 | 1 | False |
| missing_context | 0 | 1 | False |
| missing_citing_position | 0 | 1 | False |
| unsupported_rule | 0 | 1 | False |
| validator_rejection | 1 | 0 | True |
| partial | 0 | 1 | False |

## 非認証Modelと検証関数の境界

- 未登録GIVENを直接Modelへ格納可能: `True`
- Model自身の信頼証明を確認できる: `False`
- 自作推論規則が汎用matcherを通過: `True`
- 人工Bridgeを渡してGIVENを検証可能: `True`
- 人工Bridgeの対象命題と結果の一致: `False`
- 人工Bridgeは正規のscreened bridgeを模した入力であって、公開Webの証明入力ではない。
- 自作規則テストは正規のBackward Searchによる規則生成を偽装していない。
- P13の関数は任意のルール集合についての独立した証明検証器ではない。

## Rendererに残る2つの防御

- Stable eta の形状チェック: `True`
- Proposition 4.2 完全性の形状チェック: `True`

## 設計上の判断

- Complete の検証適用条件は fail-closed（検証不能なら拒否）にする必要がある。
- partial と明示的な互換APIを今回の変更対象へ拡大しない。
- 公開Web経路のTrust Boundaryだけを改善しても、任意のModelの数学的健全性は保証しない。
- Rendererの2チェックは信頼境界が全経路で確立するまで維持する。
- 今回は監査のみ。次工程で既存API・表示を保つ最小改修を検討する。
- 全体pytestはPhase終了時まで実行しない。

**AUDIT_STATUS**: `BOUNDARY_GAPS_CONFIRMED`

**FULL_PYTEST_NOT_RUN**
