# Phase 169 R3K2 — 実行手順

## 変更するファイル・関数

- `phase168_r3_27_typed_statement_projection.py`：`element_tex()` 全体を置換。モジュール先頭の import は変更しない。関数内に `from expression import Composition` を追加する。
- `phase168_r3_5_model_renderer.py`：`render_model_backed_narrative_markdown()` 全体を置換。モジュール先頭の import は変更しない。関数内に `from phase165_r14_r6_generic_iso import GeneratorImage` を追加する。
- `phase169_r3k2_eta_transport/tests/test_r3k2_eta_transport.py`：新規テスト5件。必要な import と各テスト関数は同ファイルに全文同梱する。

変更前のファイルは `output/*.before`、変更後のファイル全文は `output/*.full.py`、変更後の関数全文は `output/element_tex.full.py` と `output/render_model_backed_narrative_markdown.full.py` に出力される。手元の R3K 実装に正確に合わせるため、関数全文はインストーラー実行時に生成する。

## 実行

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3k2_eta_transport.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3k2_eta_transport\run.ps1"
```

事前検査では `develop` ブランチと R3K 完了監査の JSON、`phase169_r3k_narrative_projection.py` の存在、変更箇所の形状を確認する。変更対象の関数形状が期待と違う場合は変更前に中止する。

## 予定する限定検証

```powershell
python -m pytest -q .\phase169_r3k2_eta_transport\tests\test_r3k2_eta_transport.py .\phase169_r3j1_narrative_import_isolation\tests\test_r3j_narrative_boundary_audit.py
python -m pytest -q .\phase168_r3_41l_reasoned_prose\tests\test_phase168_r3_41l_reasoned_prose.py
python -m phase169_r3k2_eta_transport.audit
```

最初の2コマンドは、EHP adapter の同名モジュール衝突を避けるため異なる pytest プロセスで実行する。全体 pytest は Phase 169 終了時のみ実行する。

## 完了条件

- 実際の公開 Web Narrative に、ProofStep の `GeneratorImage` に対応した `E(\eta_2^2)=\eta_3^2` が1回表示される。
- 使用した2つの単独懸垂の表示は、安全な場合のみ省略される。
- R6 の引用は実際の文献の locator を保持する。
- Reference の各 R 番号は証明本文に存在する。
- 新規限定テスト・既存の1-stem関連回帰テストが通る。

## 次の工程との境界

証明探索、ProofStep、Registry、既存の推論規則、他のホモトピー群の探索機能は変更しない。本文のさらなる短縮や $\pi_6^4$ の探索は R3K2 の対象外とする。
