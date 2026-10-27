# Phase 169 R9 — HyoujiGen stable-family 設計監査

- Git local HEAD: `06162bbc18d6330dfcfc77cdc0d001c9f156c41b`
- Git local branch: `develop`
- DB rows: 233
- kinds=0: 40
- kinds=0 かつ最小次元が安定範囲外: 40

## 次元境界

| 系列 | 元の次元 n | 回数 r | 系列表記の候補 | 懸垂同型の安定範囲 |
|---|---:|---:|---|---|
| η | 2 | 1 | True | False |
| η | 3 | 5 | True | True |
| ν | 4 | 1 | True | False |
| ν | 5 | 2 | True | True |
| σ | 8 | 1 | True | False |
| σ | 9 | 3 | True | True |
| ε | 3 | 7 | True | False |
| ε | 10 | 2 | True | True |

系列表記の候補は数学的な等式を証明しない。
DB の family ID と `n_min` は命名のための情報であり、
群同型には Freudenthal の `n >= k+2` と Toda (4.5) の先行出典が必要。

## 関連コード

| ファイル | 有り | 関数欠落 |
|---|---|---|
| `phase166_r3aj_structured_generator.py` | True | - |
| `phase169_r7_general_stable_transport/rule.py` | True | - |
| `phase168_r3_5_model_renderer.py` | True | - |
| `phase165_r12_r21_eta_generator_chain.py` | True | - |
| `phase165_r52_r9_shared_math.py` | True | - |

## 目標となる表示

`[R3]より, $E^4(\eta_4^2)=\eta_8^2$.`

これは実際の Proof Tree に全ての中間 GeneratorImage が証明済みのときのみ表示可能。

## 実装後の責務境界

1. 型付き家族の同定: DB ID/kinds/k/n_min による候補生成。
2. 命名の数学的根拠: 登録済みの定義・文献に結合。DB 行自体は GIVEN としない。
3. 群同型: Toda (4.5) に基づく stable-range 検査を独立に維持。
4. 合成元: 懸垂と合成の関係を型付き再帰規則から証明。
5. Narrative: Proof Tree は完全保存し、証明済み連鎖のみ一式に圧縮。
6. 基点 π_8^5 の incomplete は別問題として残す。

本 ZIP は監査専用。本番変更なし。全体 pytest なし。
