# Phase 165 R14-R15 — 対角群の型付き出典接続

変更対象は新規 `phase165_r14_r15_typed_diagonal.py`（`TypedPremiseBinding` クラス全文と `match_diagonal_toda51_claims()`、`audit_r15()` 関数全文）、`test_phase165_r14_r15_typed_diagonal.py`（関連テスト関数5件と全 import）、`audit.py`、`run.ps1`、本書。既存クラス・関数は変更しない。

既存の `instantiate_toda51_clause()` を使って `(5.1)` の対角群命題を `n` および `n+1` に特殊化し、R14-R14 の一般同型推論に必要な型付き部分目標へ結び付ける。既存 Toda TeX で使われた `ι_1` と正規化済 `ι₁` の文字列表記だけは異なるため、生成元の family/index と source/target/dimension の照合を必須にする。

`E(ι_n)=ι_(n+1)` は `(5.1)` の対角群構造からは導けないため独立の未認証前提とする。Proposition 4.2 は2つの候補のままで、本文・適用条件の認証が済んでいない。引用権限も ProofStep も追加しない。

完了条件：5件の局所テスト、2つの対角群命題の正確な対応、生成元像が未認証のままであること、Proposition 4.2 を誤選択しないこと。全体 pytest は実行しない。

次段階：Prop. 4.2 の一般命題の原文同定・量化範囲確認と、懸垂された恒等写像 `Eι_n=ι_(n+1)` の出典確認、適切な型付き固定命題の登録・独立認証。その後に共通 Backward Search へ証明リーフとして接続する。
