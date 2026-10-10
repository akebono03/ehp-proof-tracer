# Phase 163 R4-R27 — Toda 第1章 原本照合ページ台帳

基準資料：利用者提供の Toda 第1章 PDF（全11ページ、印刷5〜15ページ）。

本 Phase はページ単位の照合記録を整備する。原本と TeX の全文逐字比較はまだ終わっていない。
既存の9箇所の修正履歴は引き継ぐが、修正済み箇所があるだけでページ全体を照合済みとはしない。

## 照合の完了条件

- Definitions（定義）、Equations（式）、Named statements（名前付き主張）、Proofs/prose（証明・本文）、Notation/conditions（記号・条件）の5領域を原本画像と照合する。
- 各領域について確認後、review を true にし、reviewer と evidence_note に具体的な証跡を記録する。
- 相違が残る場合は CORRECTION_REQUIRED、未照合は UNVERIFIED。すべて満たした場合のみ VERIFIED。
- 全11ページが VERIFIED になった場合に限り章全体の照合完了とする。

## 現在の結果

- VERIFIED: 0ページ
- CORRECTION_REQUIRED: 0ページ（既知の修正9箇所は過去 Phase で適用済み）
- UNVERIFIED: 11ページ
- 新しい TeX 修正: 0件

この台帳は実際の原本読解を代替しない。印刷原典との一致を自動的に認定しない。
既存 Registry、Statement ID、Proof Search を変更せず、全体 pytest は実施しない。
