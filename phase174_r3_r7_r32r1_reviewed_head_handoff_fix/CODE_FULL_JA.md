# R32R1 全コード／置換単位

## 対象

- `replacement/audit.py` は **完全な R32 audit.py** であり、そのまま置換可能。
- `replacement/run.ps1` は **完全な R32 run.ps1** であり、そのまま置換可能。
- `CHANGED_FUNCTIONS_FULL.py` は追加定数と、置換対象 `verify_checkout()` 関数の全文。
- `IMPORTS_FULL.txt` は `audit.py` の変更後の import 全文（既存と同じ）。
- `install.py` は Source Guard／両ファイルの全 SHA256 照合と置換処理を行う新規スクリプト全文。
- `tests/test_patch.py` は追加テスト関数全文と import を収録。

## 数学的内容

既存 R32 の条件付き巡回群核監査を変更しない。Source Guard のレビュー済み R31 統合 HEAD だけを追加受理し、R31 の固定 HEAD に依存する2テストを R32 の実行セットから外す。それ以外の既存テストを維持する。

## 元／修正版の完全ファイル hash（改行 LF 正規化 SHA256）

| ファイル | 元 | 修正版 |
|---|---|---|
| `audit.py` | `bd2327bf8bf49d6a25cf099f915aa15afc2dc3815b1457d0eb03e95aef7ec5f7` | `c191d8a9c25007e1d42b4a7faa6898b1d118a3b60f021f2dbb5ec713f0aa7656` |
| `run.ps1` | `d4fa72731ae50770c402b2ea0dfe0fd459c6152ce91de2a4f0507bdc9a8e87eb` | `6e070729ce6c5ae809be0f564a87372df179ab49ce971f7a3af41efdd0044103` |
