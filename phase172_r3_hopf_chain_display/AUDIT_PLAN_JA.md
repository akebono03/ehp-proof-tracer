# Phase 172 R3 — 検証済み Hopf 導出の本文整理

## R3R1 監査結果と事前確認

2026-10-31、GitHub `akebono03/ehp-proof-tracer` の `develop` で、共通 Renderer、R2 型付き Projection、R3R1 監査コード、Phase 171 の実際の Web 証明と関連テストを確認した。

Windows 実行ログの `PASS_R3R1_AUDIT_ONLY` と `PASS_CORRECTED_R3R1_AUDIT` により、$\pi_6^3=\mathbb Z/4\{\nu'\}$ の実際の Backward Search は `complete`、`open_goals=0`、ProofStep 50件、Reference 8件、最終 Hopf 関係は Step 16 であることが確認された。

R1 の ProofStep 依存関係も再照合した。Step 5 の cited suspension から Step 6/7 が導かれ、R2 によって Step 6/7 は本文で非表示となった。Step 8・9・13・14・15 は、それぞれ独立の追加引用を持たない中間推論。Step 11 は Proposition 2.2 の出典を持つ Step 10 に直接依存し、Step 12 は引用付き Hopf generator の事実。Step 16 はこれらを組み合わせた最終 Hopf 像。Step 17 の全射性に利用される。

## 変更ファイル・関数・追加位置

1. 既存 `phase168_r3_5_model_renderer.py` の **`render_model_backed_narrative_markdown()` 全体の置換**。追加するローカル import は新設 Projection の `project_verified_hopf_chain` のみ。トップレベル import は変更しない。既存関数全文と Renderer 全文は `-DryRun` の出力に収録する。
2. 新規 `phase172_r3_hopf_chain_display/projection.py` をリポジトリ直下の同名パッケージ内に追加。新規 dataclass `VerifiedHopfDisplay` と新規関数 `project_verified_hopf_chain()`。
3. 新規 `phase172_r3_hopf_chain_display/tests/test_projection.py`。新規 fixture `verified_pi63()` とテスト関数6件。
4. 新規 `phase172_r3_hopf_chain_display/install.py`、`run.ps1`、`__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

既存の別クラス・別関数・推論規則・DB・文書5件・Reference 格納内容は変更しない。

## 表示整理の成立条件

- `ProofNarrativeModel.status` は COMPLETE、未解決 Goal は空、完成した根の祖先のみを対象とする。
- MapSurjective の実際の証明前提に、Hopf 像の型付き Relation が存在する。
- 合成に関する各推論 Step の前提関係を、型付き等式と ProofStep 同一性から追跡できる。
- R2 により直接懸垂等式と対称等式はすでに本文非表示だが、その元の `GeneratorSuspension` は表示を維持する。
- Proposition 2.2 の GIVEN と $H(\nu')=\eta_5$ に該当する GIVEN の引用が存在する。
- 省く中間 Step は引用を持たず、ほかの表示対象から独立に使用されない。
- 出典番号は ProofStep の実際の祖先 Citation のみから取得する。出典名の文字列判定や別の数学的推論は行わない。
- 認識に失敗した場合は従来どおり全て表示し、推論・証明探索は変更しない。

## 期待する表示（概念例）

```
[R3]より, $E(\eta_{5})=\eta_{6}$.
[R4]より, $H(\nu'E\eta_{5})=H(\nu')E\eta_{5}$.
[R5]より, $H(\nu')=\eta_{5}$.
[R3], [R4], [R5]より, $H(\nu'\eta_{6})=\eta_{5}^{2}$.
```

これは **数式書式を固定するテスト仕様ではない**。実際の表示数式は既存の型付き Renderer による出力を使い、Citation 番号も動的に ProofStep から取得する。

## 検証 Gate

DryRun で source identity / 変更後関数全文出力が PASS。実行後は新規 R3 テスト、R2、Phase 171 の η 統合と位数4文章、Phase 169 の $\pi_6^4$ を5つの独立 pytest プロセスで限定確認。実環境で `complete`、未解決0、Reference 8件、$H(\nu'\eta_6)=\eta_5^2$ の表示、$\pi_6^3=\mathbb Z/4\{\nu'\}$ の表示を維持。失敗した場合は Renderer の元バイトを復元する。

**全体 pytest は Phase 172 の最後 R6 でのみ実行する。**

## 次工程との境界

R3 は Hopf 導出の表示に限定する。R4 の全射性の重複、R5 の `DB prior` を含む Reference 表示には触れない。新しい数学的 Goal や未証明 GIVEN も追加しない。
