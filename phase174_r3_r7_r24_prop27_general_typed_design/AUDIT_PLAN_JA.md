# Phase 174 R3-R7-R24 型付き一般命題の設計監査

## 対象

新規 `phase174_r3_r7_r24_prop27_general_typed_design/` のみ。既存コード・テスト・ドキュメントを変更しない。

- `audit.py`：第2章 Proposition 2.7 原文・第5章との照合、偶数次元の型付き signature と Git Source Guard。
- `tests/test_audit.py`：一般偶数次元、n=6 特殊化、符号保持、誤った添字や前提を拒否する限定テスト。
- `run.ps1`：DryRun と限定 pytest を実行。
- `README.md`：英語の実行説明。
- `CODE_FULL_JA.md`：追加コード全文。

## 採用する一般命題

第2章 `sources/toda/Toda_02_2.tex`、Proposition 2.7：偶数 $n$ に対し

$$H(\Delta(\iota_{2n+1}))=\pm 2\iota_{2n-1}.$$

写像の型は

$$\pi_{2n+1}^{2n+1}\xrightarrow{\Delta}\pi_{2n-1}^{n}\xrightarrow{H}\pi_{2n-1}^{2n-1}.$$

$n=6$ は $\pi_{13}^{13}\to\pi_{11}^{6}\to\pi_{11}^{11}$。

第5章の欄外抜粋にある $\iota_{2m-1}$ は、上記原文と整合しない。第2章の原文を優先し、原稿自体は変更しない。

## 厳密な境界

これは `Prop27TypedDesign` という型設計の検査であり、`InferenceRule`、`ProofStep`、公開 provider の登録ではない。一般定理の型付き特殊化を本番の INFERENCE にする作業は次工程へ残す。未証明の群構造、Δ全射、最終結論を GIVEN として登録しない。

## 完了条件

Git Source Guard、原文検査と限定 pytest が PASS する。全体 pytest は Phase 完了時まで実施しない。根の証明は未完成のまま維持する。
