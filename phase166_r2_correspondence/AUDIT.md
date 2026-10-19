# Phase 166 R2 — 既存関係式と命題台帳の対応候補監査

## 変更対象

- 新規 `phase166_r2_correspondence/audit.py`: `read_csv`, `_meaningful`, `_kind`, `_locator_index`, `analyze`, `main`
- 新規 `phase166_r2_correspondence/test_audit.py`: 限定テスト4件
- 新規 `phase166_r2_correspondence/run.ps1`: Windows 用実行コード
- 新規 `phase166_r2_correspondence/AUDIT.md`: 本監査記録
- 既存の `repository.py`、`proof.py`、`unified_statement_registry.py`、証明探索コードは変更しない。

## 現行コード確認

GitHub の `repository.py`、`proof.py`、`unified_statement_registry.py`、`phase163_r4_registry_bridge.py`、`phase165_r2_registry_lookup.py` と関連テストを確認した。R1 の出典解析 `classify` を再利用する。

## R2 の境界

このパッケージは出典位置と型付き命題の存在を**候補**として検査する。`composition` と `rep_linear` は表示文字列としてのみ保持し、数学的等価性を証明したとは扱わない。関係式・生成元・位数の型付き同一性は未検証として明示する。`ProofStep` や引用権限の自動発行は行わない。

出力: `results/summary.json` および `results/correspondence.csv`。対象の命題台帳が見つからなければ監査は失敗する。R2 の実装完了を意味するものではなく、R2 の第一段階（対応候補の構造監査）である。

## 実行

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r2_correspondence.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r2_correspondence\run.ps1"
```

## 完了条件

- 関係式687件を読み取り、各行の locator、命題候補、内容の型を監査できる。
- 内容同一性が未検証であることを維持する。
- 限定 pytest 4件が PASS する。
- 全体 pytest は Phase 166 R10 のみ。

## 次との境界

R2 後半では型付き数学表現を確実に構成できるデータのみ対応づける。R3 は引用資格の独立検査を担当する。
