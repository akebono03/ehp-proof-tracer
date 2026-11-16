# EHP Proof Tracer — Phase 175 R3R9 引継ぎ（2026-11-16）

## 数学的な訂正（確定）

Toda Chapter V、Lemma 5.7 の採用転記には、一般条件のあとに「特に、$E(\eta_2\circ\nu')=0$」と明記されている。この特別結論を**定理の引用として**使う場合、Lemma 5.4 の $E^2\nu'=2E\nu_4$ を後続証明で再度示す必要はない。一般の $\alpha$ に関する Lemma 5.7 の仮定は別であり、無条件の一般化は禁止。

## 実証済みの到達点

Phase 175 R3R8R1R2 は user Windows 実行で限定 pytest 85 PASS、$\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}$ の Group query `complete`、Trust `True`、Web `generic-complete-proof`、Reference 8件となった。ただし当時の Proof Tree は Lemma 5.4 を経由している。

## R3R9 の目標・変更

R3R9 は、Lemma 5.7 の明示的結論を出典付き `GIVEN` ソース型から `GeneratorImage` へ抽出する推論として表現し、Lemma 5.4 に依存しない新しい公開経路を選ぶ。その他の EHP 群構造推論、Hopf lift、検証済み DB 先行結果、共通 Narrative は変更しない。

- 新規 `phase175_r3r9_lemma57_explicit_public/` 以下に出典検証、抽出推論、公開接続、インストーラー、限定テスト、監査を追加。
- 唯一の既存コード変更：`phase165_r52_r9_shared_math.py` の `search_shared_group_goal()` にある `(n,k)=(3,4)` の import 接続先を旧 R3R8R1 route から R3R9 route へ変更。
- ベースライン GitHub `develop` の production blob：`3426b223f94e839e77972801977d58a4ca182767`、確認 HEAD：`7171af968ba510291f87b8bb484d8718a3cef204`。
- プロジェクト採用出典 Manifest は Lemma 5.7 の ID `toda:tex:ch5:0015`、SHA256 `01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c`、順序9100を要求。原著印刷本は未照合。

## 実行と報告

まず `R3R9.zip` をリポジトリ root に解凍し、`phase175_r3r9_lemma57_explicit_public/run.ps1 -DryRun`、成功後に通常実行。先行 R3R8R1 の正常レポートを要求。実際の公開探索が失敗すれば単一ファイルをバイト単位でロールバックする。

成功 Gate：`PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE`。単に完成しているだけではなく、Lemma 5.7 特別結論の抽出推論、Lemma 5.4 の非使用、Trust と Web 完成表示を要求する。

## 境界とユーザー要望

- $\pi_9^5$ / $\pi_{10}^6$ は次回以降。今回は未着手。
- 全体 pytest は Phase 175 の最後のみ。
- 変更対象の関数・クラス・import・テストは省略せず全文。ZIP と PowerShell コマンドを必ず用意。
- 専用 Narrative や直接の最終結論 GIVEN を作らない。
- 回答は日本語、数式は短く、先に結論。PowerShell への貼り付けで `{` が壊れた事例があるため、貼り付け例は可能なら `if` 不使用。
- 他チャットでの完全自動引継ぎは保証されないため、この文書や実行ログを参照して再開。
