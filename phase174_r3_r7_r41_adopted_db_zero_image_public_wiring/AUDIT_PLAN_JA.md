# R41 監査計画

## GitHub 実装前確認

- GitHub `akebono03/ehp-proof-tracer` `develop` の HEAD: `df93c0516dff64cddfebdac69d9755058322cdec`（R39 を統合済み）。
- 既存 `phase165_r52_r9_shared_math.py` Git blob SHA: `6b965aa49db2ad8707c75dcc953d3c78cdd3e458`。
- 既存 R38 公開 Provider、R39 の ProofStep 検証、R40 の採用 DB 信頼境界と R40R1 の修正済み pytest、R6・R7・R9、`proof.py` の推論照合を確認。
- `merge_backward_expansions()` は規則の同一性と前提が両方一致する場合のみ重複削除。R6 と R41 の候補は別規則として共存。

## 変更対象

1. 既存 `phase165_r52_r9_shared_math.py`: `shared_expansion_provider()` 全体のうち、`# R4-4 stage4` の直前に11行の接続コードを挿入。関数の残部を変更しない。モジュールの先頭 import に変更なし。実行後、変更済み関数全文を `CHANGED_FUNCTION_FULL.py`、全 import と関数前までの既存ソースを `IMPORTS_FULL.txt` に出力。
2. 新規 `phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py`: `screened_general_law()`、`build_public_adopted_zero_image_provider()` を追加。
3. 新規同ディレクトリ `source_guard.py`: Git と関連ソースのハッシュ／系譜を検証。`install.py`: Source Guard 後に原子的に単一ファイルを書き換える。
4. 新規 `audit.py` と `tests/`: 出典、実公開候補、R40 の真正な隔離 ProofStep、逆条件の拒否を検証。

## 実装境界

- `R40` の本体、R6、R7、R9、`phase165_r3_recursive_search.py`、DB、共通 Renderer、Web を変更しない。
- Toda (5.9) の一般法則を出典付きの GIVEN として用いるのみ。DB prior は先行データとして元の GIVEN のまま検証。独立した Toda 引用だと表現しない。
- 新しい接続は `GoalExpansion` の候補のみ。直接 GIVEN・完成 ProofStep・根の結論を挿入しない。
- 全体 pytest は Phase の最後だけ実行。

## 次工程

R42 では通常の公開 Proof Search が `E\pi_{10}^{5}=0` という内部 Goal を `Verified ProofStep` として再構成できるかを実測する。R41 は最終証明・上側 Δ の全射性を認定しない。
