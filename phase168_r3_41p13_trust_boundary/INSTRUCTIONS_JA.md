# Phase 168 R3-41P13 — 検証済み Proof Tree の受け渡し

## 決定

方式B。既存 matcher を Model へ入る直前に再実行し、GIVEN は選別済み Bridge の型付き登録と `precedes_citing_assertion()` で照合する。検証済みフラグ・独立した数学的検証エンジンは追加しない。

## 変更ファイル・関数

- 新規 `phase168_r3_41p13_trust_boundary/verification.py`：`UnverifiedProofTree` クラス、`verify_proof_tree_for_narrative()` 関数。公開 import は同ディレクトリの `__init__.py` から行う。
- 変更 `web_group_proof.py`：`build_standard_web_group_proof_view()` 関数のみ。元の関数を丸ごと置換。変更後の関数全文は `full_functions/`、ファイル全文は実行後 `output/web_group_proof.py.FULL.py` に保存。
- 新規 `phase168_r3_41p13_trust_boundary/tests/test_phase168_r3_41p13_trust_boundary.py`：限定テスト。
- `ProofStep`、`PartialProofResult`、`ProofNarrativeModel`、Renderer、既存の関連テストとドキュメントは変更しない。

## 安全な適用

作業ブランチは `develop`。ZIP を作業ルートに展開し、下記を実行する。

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41p13_trust_boundary.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41p13_trust_boundary\run.ps1"
```

`run.ps1` は変更前の3群の全文・Citation を保存し、変更前の `web_group_proof.py` をバックアップして、限定 pytest・変更後の全文比較・P12 文献順監査を実行する。失敗時は変更した Web ファイルを元のバイト列へ復元する。

手動復元：

```powershell
python .\phase168_r3_41p13_trust_boundary\restore.py
```

## 完了条件

- 3群の INFERENCE 39件・GIVEN 14件が検証を通過。
- 偽造 stable eta、EHP 完全性、GIVEN が拒否される。
- 3群の証明本文・Reference・Citation が変更前と完全一致し、P12 固定基準も PASS。
- 未位置決定の partial と直接 Model API は互換経路として保持（検証済みを自称しない）。
- 全体 pytest は実行しない。

## 境界と留意点

この検証は標準公開 Web 経路で、既存の信頼済み推論規則・選別済み Bridge が使われることを前提とする。外部から任意の Rule や Bridge を持ち込む一般的な形式証明検証器ではない。直接作成した Model の健全性は保証しない。残る Renderer 2箇所の数学的再判定は今回削除しない。位置未解決の Model は認証しない。完全な一元化は以後の境界整理で検討する。
