# Phase 168 R3-41P14 — Trust Boundary 監査（読み取り専用）

## 前提

- GitHub `akebono03/ehp-proof-tracer` の `develop`、R3-41P13 適用済み。
- 実装を上書きしない。既存テストも変更しない。
- 既存の2つの Renderer 数学的形状チェックは維持する。
- 全体 pytest は実行しない。

## 今回の監査対象

- `web_group_proof.py` / `build_standard_web_group_proof_view()`
- `phase168_r3_41p13_trust_boundary/verification.py` / `verify_proof_tree_for_narrative()`
- `phase168_r3_3_proof_narrative_model.py` / `build_proof_narrative_model()`
- `phase168_r3_4_link_bridge.py` / `build_linked_proof_narrative_model()`
- `phase168_r3_27_typed_statement_projection.py` / `project_stable_eta_notation_transition()` と `typed_sentence()`
- `phase168_r3_5_model_renderer.py` / `render_model_backed_narrative_markdown()`

### 監査で現時点までにわかったこと

現行 `web_group_proof.py` では、完全証明でも以下のとき検証を行わず Model に進む。

1. 探索コンテキストが渡されていない。
2. 証明対象の文献位置付き assertion ID が未確定。
3. GIVEN / INFERENCE 以外の規則を含む。

これは正規の `(n,k)` だけで悪用できることの立証ではない。監査では内部の引数・返り値をモックし、分岐の挙動を直接確かめる。

`ProofNarrativeModel` は不正 ProofStep も格納可能で、証明書ではない。汎用検証関数へ人工 Bridge を渡した場合も、正規探索の選別済み Bridge であるとの出所保証はない。また P13 の matcher 再実行は渡された推論規則自体の登録・出所を保証しない。したがって直接作成された Model の数学的健全性を主張しない。

## 解凍・実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p14_trust_boundary_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p14_trust_boundary_audit\run.ps1"
```

限定テストを省略し、読み取り専用の監査だけを行う場合は `-SkipTests` を付ける。

## 出力

`phase168_r3_41p14_trust_boundary_audit/output/` に以下を生成する。

- `audit.json`: 各分岐、3群の検証件数、全文一致、2つのチェックの有無
- `audit.md`: 日本語報告書
- `pi3_2_current.md` / `pi4_3_current.md` / `pi5_4_current.md`: 現在の全文
- `pytest_focused.log`: 限定 pytest のログ
- `review_bundle_YYYYMMDD_HHMMSS_mmm.zip`: 監査結果の提出用 ZIP

`AUDIT_STATUS BOUNDARY_GAPS_CONFIRMED` は**検証を迂回する構造が確認された**という意味であり、「安全性保証が完了した」という意味ではない。

## 次工程との境界

R3-41P14 は監査のみ。R3-41P15 では、今回確認された標準 Web の位置付き完全証明に限って fail-closed（検証不能なら拒否）への最小変更を検討する。partial や明示的な互換経路は引き続き表示できる必要がある。Renderer の2つの数学的チェック削除は対象外。
