# Phase 169 R10EG — 1-stem の競合する探索提案を分離する

## 根拠

R10EE で $\pi_5^4$ と $\pi_6^5$ が `partial` へ回帰した。R10EF では両者について、同一の型付き Goal に対する相異なる **2つの有効な推論経路**が採用されていることを確認した。

- $\pi_5^4$：任意回数の安定巡回群輸送、または証明済みの $\eta$ 懸垂による生成元の正規化。
- $\pi_6^5$：任意回数の安定巡回群輸送、または引用済みの一般 $\eta$ 系列の特殊化。

`phase165_r3_recursive_search.py::reconstruct_registered_goal()` は異なる2経路を「同一証明」と断定せず、曖昧性として `partial` にする。既存の保守的な Proof Tree 同一性を緩和することは避ける。

## 最小変更

**変更対象：** `phase169_r10e1_general_group_transport/transport.py` の `expand_prior_general_group_transport()` だけ。

対象の型付き Goal が、$k=1$、巡回位数2、出典から既に定義されている $\eta_n$ の型付き表記に厳密一致するとき、後から追加した一般輸送経路を提案しない。既存の `proved generator suspension normalizes transported cyclic group` や `cited stable eta-family notation for iterated transport` の適用、すべての必要な既出 GIVEN と INFERENCE の再生を維持する。

- `k!=1` では既存の一般輸送規則を維持する。
- `k=1` でも型・次数・生成元が異なるケースにはこの特殊化を適用しない。
- 強制的な `complete` や、証明の同一性の偽装、推論規則・DB・Reference の変更は行わない。
- import の追加は変更した関数内に限定し、ファイル先頭の import 一覧は不変。

## 限定テストと監査

既存 R10E1 / R10EC / R10A の関連テストを含む限定 pytest を行う。$\pi_5^4$ の完成 ProofStep 数10を回復すること、$\pi_6^5$ を含む1-stemが complete であること、2・8・9-stem の既存完成証明を保持すること、すべての完成 Proof Tree を検証境界で再生できることを確認する。全体 pytest は Phase 169 最後のみ。

## Git 作業状態

R10EF の `tracked_status_before.txt` は監査自身が書き換えた追跡ファイルである。R10EG はこれに触れず、既存の追跡状態を前後比較で保持する。実行ログはタイムスタンプ付きの新規ディレクトリに保存し、追跡済み出力ファイルを再利用しない。

## 失敗時と次 Phase

実行した限定テストまたは監査が失敗した場合、変更対象の元バイト列を自動復元する。R10EG の成功は Phase 169 全体の完了を意味しない。終了前の文書更新および全体 pytest は別の作業とする。
