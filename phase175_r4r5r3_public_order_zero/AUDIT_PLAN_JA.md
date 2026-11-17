# Phase 175 R4R5R3R1 — 共有 Backward Search への一般零関係規則接続

## 目的と対象

先行 DB 群の証明を再実行せず、一般推論 `G = A ⊕ Z/m{a} ⊕ B ⇒ ma=0` を、すべての適切な型付き証明 Goal に適用できるようにする。直和は入れ子を含み、有限巡回成分だけが対象。単独の `Z/m{a}` も同じ経路で扱う。

### 変更対象

- 既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider` 関数全体（構造は維持し、1か所に Provider を追加）。トップレベル import は変更なし。
- 新規 `phase175_r4r5r3_public_order_zero/provider.py` の `eligible_order_zero_sources`、`build_public_order_zero_provider`。
- 新規 `installer.py` の `git_blob`、`function_replacement`、`plan`、`install`。
- 新規 `audit.py` の `latest_prior`、`validate_prior`、`source_guard`、`public_order_zero_evidence`、`run`、`main`。
- 新規テスト `tests/test_provider.py`、`tests/test_installer.py`、`tests/test_real_integration.py`。既存 R4R5R2 の一般規則・関連テストは変更しない。

## Source-first（出典優先）と型・証明条件

1. 証明ルート `proof_target` の `(n,k)` を、既存 DB prior の `(k,n)` 辞書式順序検査に使う。
2. 入力 `Relation(Multiple(m,g),Zero())` の型付き始域・終域を検査する。
3. 同じ群の既存の完了済み先行結果・screen 済み固定出典・厳密な `sphere.csv` DB prior から、群表示の候補のみ選択する。候補の存在を証明扱いしない。
4. DB の安定域補完、異なる添字・生成元・位数、直和の自由成分や型不明成分を排除。
5. 共有再帰探索が選んだ `Relation(G, ...)` の ProofStep を正しく取得した場合のみ、R4R5R2 の一般 `InferenceRule` で零関係を導く。
6. 最初の成功で終了し、唯一性は検査しない。新規 GIVEN 0件、新規数学規則 0件。専用 Narrative 追加なし。

## 実行順序

- DryRun: 既存限定 pytest → R4R5R2 本実行レポート検証 → Git HEAD・元ファイル blob・規則 SHA 検査 → 関数全体の置換結果を audit 領域に書き出し。追跡コード変更なし。
- 本実行: 既存限定 pytest → 同じ厳密ガード → `shared_expansion_provider` 関数全体のみ原子的置換 → DB prior 親からの3推論照合 → 実環境の追加限定 pytest を PASS Gate の直前に実行。失敗時には元ファイル bytes を自動復元。
- 本実行後は `git diff --check` と `git status -sb` を確認。変更予定の tracked ファイルは1件。

## PASS 条件と次 Phase 境界

`PHASE175_R4R5R3_VERIFIED_PUBLIC_PROVIDER_EXAMPLES=3`、共有 Provider 接続 True、先行群の証明再実行 False、新規 GIVEN 0、新規数学規則 0、限定 pytest PASS。根の `pi_9^5` 証明は未完成のまま維持する。次は Proposition 2.5・Toda (5.8) の接続状況監査であり、R4R5R3 では先取りしない。全体 pytest は Phase 175 最終時のみ。

## R4R5R3R1 HEAD 履歴修正

R4R5R3 DryRun は 210 passed 後 `R4R5R3_UNREVIEWED_HEAD` で停止した。調査時の GitHub `develop` HEAD は `bc1a9eff9c1d051764ff817bb1948f55a1479961`、元のレビュー済み HEAD は `2789fb6297efaa35962695b95300063feb6e2ea2`。`git compare` で間にある変更は R4R5R2 の監査パッケージ10ファイルのみ、共有の本番ファイル BLOB は変更されていなかった。

`reviewed_head_lineage` を新設し、祖先関係と対象パス `phase175_r4r5_eta7_annihilator_isolated/` への限定を検査する。未知のコミット、無関係の追跡ファイル、元の数学規則 SHA256 の変更は引き続き拒否する。`source_guard` は通過した現行 HEAD と追加ファイル一覧を記録する。既存の Installer の Git BLOB pin、追跡コードの変更拒否、失敗時自動復元を維持。追加限定テスト `tests/test_head_lineage.py` を実行する。

今回修正する既存ファイルは監査パッケージ `audit.py`、`run.ps1`、関連ドキュメントのみで、追加関数は `reviewed_head_lineage`、変更関数は `source_guard`。新規テストファイルを追加。本番数学規則と `shared_expansion_provider` の接続コードは R4R5R3 のまま変更しない。Phase 175 の全体 pytest は実行しない。
