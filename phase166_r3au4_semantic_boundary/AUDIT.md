# Phase 166 R3-AU-4：DB の構造的意味に関する監査

## 確認済みの既存コード

`repository.py` の `SphereRepository` は `Element` と `gen_coe` をそれぞれ整数リストとして読み、`models.py` の `GroupComponent` に保持する。両者の各位置を同じ基底の添字として対応させる根拠はない。

## 今回の変更対象

新規 `audit.py` の `read_csv`, `locate`, `integers`, `inspect`, `write_csv`, `main`。新規 `test_r3au4.py` の限定テスト3件。`run.ps1`。既存コードは変更しない。

## 監査方針

`generator` は任意の参考文字列とし、空欄・不一致をエラーにしない。`Element` と `gen_coe` の個数および係数位置を記録するが、それだけから合成・懸垂・冪を導出しない。零ベクトルを不正と断定しない。全 DB 行と高次 stem を含める。

## 完了条件と次工程との境界

CSV の全行に係数分類・長さ・非零位置を付け、参考文字列とは独立した結果を出力する。数学的な型付き式・LaTeX 一致は認定しない。次工程は係数の各位置を解釈する既存 DB 仕様・実装の調査であり、本 Phase で変換規則を仮作成しない。全体 pytest は Phase 166 終了時だけ実施する。
