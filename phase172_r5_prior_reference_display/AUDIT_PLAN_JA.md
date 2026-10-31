# Phase 172 R5：先行 DB 結果の Reference 表記

## 事前確認

2026年10月31日、GitHub `akebono03/ehp-proof-tracer` の `develop` の共通 Renderer、ProofNarrativeModel、先行 DB 前提の登録・検証経路、関連 pytest を確認した。Phase 172 R4 のユーザー実行結果は `PASS_R4_SURJECTIVITY_DISPLAY_ONLY`、限定 pytest 6セット PASS、既存ファイル変更は Renderer 9行のみ。現在のコミット `3f79cefb37ed56f66d42bfeecc995b7ab9052e76` は R3 の完了時点であり、R4 の変更は未コミット。

## 数学上の境界

`phase169_r10e4_ordered_db_prior/db_prior.py` の `DB prior: sphere.csv` は**採用済み先行データベース結果**を表す監査用出典識別子で、文献の独立した定理ではない。既存 `verified_db_step()` と Trust Boundary はこの識別子および `ADOPTED_DATABASE_PRIOR` の同一性に依拠するため、これらを変更しない。

Web Reference のみ、型付き群・座標・文献の参考注記を維持して以下のように表示する。

- `[R2] 先行データベース結果 $\pi_{7}^{5}$（sphere.csv, n=5, k=2）［参考: Proposition 5.3］`。
- `[R8] 先行データベース結果 $\pi_{6}^{5}$（sphere.csv, n=5, k=1）［参考: Proposition 5.1］`。

一般の DB 前提にも、同じ型付き検証条件を使う。特定の η/ν 元、群次元、文献番号のための専用分岐は設けない。

## 変更対象

| 対象 | 処理 |
|---|---|
| `phase168_r3_5_model_renderer.py` | `render_model_backed_narrative_markdown()` 内で完成証明の Reference 見出しに表示 Projection を適用 |
| 新規 `phase172_r5_prior_reference_display/projection.py` | `display_prior_reference_locator()`。認証済み引用付き DB GIVEN にのみ表示変換を適用 |
| 新規 `phase172_r5_prior_reference_display/tests/test_projection.py` | 実証明、出典保持、偽造した出典の fail-closed 検査7件 |
| 新規 `phase172_r5_prior_reference_display/install.py` と `run.ps1` | GitHub 監査済み内容との一致検査、DryRun、限定 pytest、失敗時の Renderer 復元 |
| 新規 `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `__init__.py` | 実行説明と変更コード全文 |

既存のクラス、推論規則、ProofStep、DB locator、文献引用の ID、出典メタデータ、トップレベル import は変更しない。変更後の既存関数・ファイルの全文を DryRun 時に `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r5_*` に出力する。今回のパッケージ以外の README.md など5つの基幹ドキュメントは変更しない。

## 完了条件

- `DryRun=PASS` と内容ガード PASS。
- 限定 pytest 6セットがすべて PASS。
- Web Reference 8件、ProofStep 50件、未解決 Goal 0、`generic-complete-proof`、完成証明を保持。
- 先行データベース結果の見出し2件のみ改善し、内部の `DB prior` locator は不変。
- 失敗時は Renderer を適用前に復元。

## 次 Phase との境界

R5 は Reference の人間向け見出しのみ。証明文章の数式整理は R2〜R4 に固定し、R6 で1-stem・2-stem・$\pi_6^3$ の回帰監査と Phase 172 全体 pytest を一度だけ実施する。
