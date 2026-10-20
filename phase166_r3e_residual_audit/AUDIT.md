# Phase 166 R3-E 残課題監査

## 対象

- `phase165_r56_presentation_adapter.py`：完成済み証明の表示経路の選択
- `phase165_r57_r10_step_narrative.py`：ProofStep の祖先と懸垂移送の検出
- `phase165_r12_r34_narrative.py`：内部規則名の文章化処理
- `phase165_r12_r34_r2_semantic_narrative.py`：表示対象規則の取扱い
- `phase165_r57_r8_eta_specialization.py`：Proposition 5.1 の一般的な特殊化
- `phase165_r57_r11_proof_order_gate.py`：根に対する一般特殊化の取扱い
- `phase165_r55_nk_only_goal.py`：公開検索の入口
- `phase165_r4_golden_baseline/baselines/pi4_3.json`：過去の表示期待値

## 静的確認

1. `infinite cyclic quotient structure` は実際の推論規則名である。日本語化ヘルパーが存在する一方で、公開経路すべてに適用されてはいない。過去の Golden Baseline も英語を含む。
2. `pi_5^4` には Proposition 5.1 の一般命題からの特殊化経路があり、現在の公開証明はこの経路を採用している。
3. `phase165_r56_presentation_adapter.py` は、証明祖先に transport 推論が存在しない場合に、懸垂移送を含む既存表示を使用しないよう分岐する。
4. 懸垂を使う候補の未生成・候補の未選択・順序による除外のいずれかは、静的確認だけでは決定できない。

## 実行時監査

`audit.py` は `search_group_from_registered_goal` を使い、各完成証明の根の推論規則、祖先の推論規則名、GIVEN の引用元、transport 推論の有無、Narrative 本文、未解決 Goal を `audit_result.json` に出力する。書換えは監査ディレクトリだけ。

## 判定境界

本監査だけでは renderer の修正、推論経路の優先度変更、全体 pytest は行わない。
