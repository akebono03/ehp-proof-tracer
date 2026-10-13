# Phase 165 R41 — 欠落 TeX の配布修正

## 変更対象
- `phase165_r14_r39_toda51.tex`：R40 と同じ採用 TeX を同梱し、プロジェクト直下にコピー。
- `run.ps1`：上記ファイルを最初に配置。R41 分岐導入済みなら再インストールしない。
- `phase165_r14_r41_proof_transfer.py`、`install.py`、`audit.py`、対象テスト5件：前版と同じ全文を同梱（変更なし）。

## 原因
R41 コードは `Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")` を参照するが、R41 ZIP に TeX が含まれていなかった。テスト5件はすべて `FileNotFoundError` で、Renderer の検証まで達していない。

## テストと完了条件
対象 pytest 5件と監査の実行。全体 pytest は実行しない。

## 次工程との境界
今回修正するのは欠落ファイルの配布だけ。Reference 抽出や `GeneratorImage` 等の共通 Renderer 対応は変更しない。
