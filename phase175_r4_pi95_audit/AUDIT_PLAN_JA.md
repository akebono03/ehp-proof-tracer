# Phase 175 R4 — $\pi_9^5$ の Source-first 監査計画

## 1. 基点

- 対象：$\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$（$n=5,k=4$）。
- GitHub `akebono03/ehp-proof-tracer` `develop` の調査時 HEAD：`c77a26fdebe0eead67f1f7dad3a469aa446b134f`。
- 引き継ぎ時 HEAD：`a1ce1558be6bab647c5d23d26047b9cce45d4e2e`。GitHub 上では2コミット進み、変更は R3R12 関連8ファイル。
- ユーザーのローカル・未コミット状態は遠隔 GitHub の表示だけでは判断できない。`run.ps1` の監査で Git の HEAD、追跡変更、Source PIN を確認する。

Phase 175 R2 時点の $\pi_9^5$ には `CyclicStructureStatement` と双方向の `Relation` という3個の Open Goal が残った。R3 では $\pi_7^3$ が完成したが、$\pi_9^5$ への新たな独立した証明完成は未確認である。

## 2. Toda Proposition 5.8 の独立した証明経路

Toda の採用 Chapter V TeX は、結論を単に列挙するだけでなく、次の証明を記述する。

まず先行完成群：

$$
\pi_8^4 = \mathbb Z/2\{\nu_4\eta_7\}\oplus\mathbb Z/2\{E\nu'\eta_7\},
\qquad
\pi_7^4 = \mathbb Z\{\nu_4\}\oplus\mathbb Z/4\{E\nu'\}.
$$

EHP 完全列の該当部分は、型として次になる。

$$
\pi_{10}^{9}\xrightarrow{\Delta}\pi_8^4\xrightarrow{E}\pi_9^5
\xrightarrow{H}\pi_9^9\xrightarrow{\Delta}\pi_7^4.
$$

Toda (5.8) の

$$
\Delta(\iota_9)=\pm(2\nu_4-E\nu')
$$

は、$\pi_7^4$ の自由部分で係数 $\pm2$ を持つ。したがって $\pi_9^9\cong\mathbb Z\{\iota_9\}$ からの $\Delta$ は単射である。EHP 完全性から $H=0$、よって $E:\pi_8^4\to\pi_9^5$ は全射となる。

一方 $\pi_{10}^9\cong\mathbb Z/2\{\eta_9\}$ であり、Proposition 2.5 の $\Delta$ と合成の関係、および (5.8) と $2\eta_7=0$ から、符号を含め

$$
\Delta(\eta_9)=\pm E\nu'\eta_7
$$

が従う。したがって

$$
\ker(E)=\mathrm{im}(\Delta)=\langle E\nu'\eta_7\rangle.
$$

第1同型定理より

$$
\pi_9^5\cong\pi_8^4/\langle E\nu'\eta_7\rangle
\cong\mathbb Z/2\{E(\nu_4\eta_7)\}.
$$

安定族の一般的な懸垂関係 $E\nu_4=\nu_5$、$E\eta_7=\eta_8$ と合成との両立を型付きで確認できれば、記名生成元は $\nu_5\eta_8$ になる。

**注意：上記は文献に支持された数学的導出案であり、R4 時点の EHP Proof Tracer 内で INFERENCE ProofStep として完成したとは扱わない。** 対象結論を直接 GIVEN とすることも禁止する。

## 3. 原文の次元表記について

採用 TeX の Proposition 5.8 の証明にある EHP 列では、$\pi_8^4$ に当たる場所が `\pi^{9}_{8}`（$\pi_8^9$）と印字されている。これは $\pi_9^5=E\pi_8^4$ という直後の記述と整合せず、次元に関する転記・誤植の可能性が高い。本監査はこの問題を記録するが、原本確認なしに TeX を書き換えない。また、その不正な次元を持つ命題を証明木に登録しない。

Toda (5.9) の $\nu_n\eta_{n+3}=0$ は **$n\ge6$** が条件であり、$n=5$ の $\nu_5\eta_8$ には適用できない。$E(\nu_5\eta_8)=\nu_6\eta_9=0$ であっても、元の $\nu_5\eta_8$ が零とは結論できない。

## 4. 対象ファイル、関数、テスト（R4 初回パッケージ）

本番ソース・既存テスト・主要5文書の**変更なし**。新規 `phase175_r4_pi95_audit/` のみ追加。

- `audit.py`：`git`, `validate_dirty_paths`, `preflight`, `evidence_from_text`, `source_inventory`, `validate_observations`, `worker`, `decode_worker`, `launch_worker`, `make_report_path`, `write_report`, `run`, `main` の全関数を新規追加。`__main__` エントリを末尾に配置する。
- `tests/test_audit.py`：限定の監査契約テスト全体を新規追加。既存の R34 `tests/test_source.py` は**変更せず実行する**。
- `run.ps1`：限定 pytest と DryRun / 本実行を行う新規 PowerShell スクリプト。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md`、`__init__.py`：すべて新規ファイル全文。

## 5. 判定

DryRun は追跡変更・Source PIN・出典テキストと型付き構造を検査し、証明探索を実行しない。通常実行は R1 の本物の監査関数 `inspect_one_group` を隔離ワーカーから呼び、目標 $\pi_9^5$ と先行完成群 $\pi_8^4$ を確認する。

想定 Gate：`PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE`。これは**監査成功であり、証明完成ではない**。既存の Open Goal が変更されていた場合は、結果を捏造せずエラーとして報告する。

全体 `pytest` は実行しない。R4 の次段階は不足する一般命題・推論規則の接続を決める作業であり、本 ZIP はそれを先取りしない。

## 6. R4R1 — pytest が更新した Git 追跡済み cache の最小補正（2026-11-17）

### 発生した事象

ユーザー環境の R4 初回 DryRun では限定 pytest 23 passed の直後に `R4_UNREVIEWED_TRACKED_CHANGES: ['.pytest_cache/v/cache/nodeids']` が発生した。証明探索・数学的出典の前処理で停止しており、R4 の Source PIN や目標群の Proof Search の成否は未確認である。`nodeids` は pytest の実行済みテスト一覧であり、数学的な GIVEN や Source PIN のファイルではない。

### 変更対象（省略なし）

1. `phase175_r4_pi95_audit/audit.py`：定数 `TRACKED_PYTEST_CACHE_FILE` を `ALLOWED_DIRTY_PREFIX` の直後に追加。`validate_dirty_paths()` を関数全文置換。`preflight()` を関数全文置換（返却値の cache 別記）。import は変更なし。
2. `phase175_r4_pi95_audit/run.ps1`：PowerShell スクリプト全文置換。限定 pytest に `-p no:cacheprovider` を指定。
3. `phase175_r4_pi95_audit/tests/test_audit.py`：既存テストは維持し、`test_preexisting_tracked_pytest_nodeids_is_explicitly_allowed()` と `test_unreviewed_paths_remain_blocked_with_pytest_cache()`（5パターン）を、既存の dirty-path 契約テストの直後に追加。import 変更なし。
4. 同パッケージの `README.md`、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md` をすべて全文更新。

その他のファイル、本番 Proof Search、一般数学規則、既存 Web Narrative、Phase 175 R3 のコード、ルート主要5文書は変更しない。`CODE_FULL_JA.md` に audit.py、test_audit.py、run.ps1 の実体と同一のソースを全文掲載する。

### 守る安全条件

- 例外を許すのは `.pytest_cache/v/cache/nodeids` **完全一致**のみ。`.pytest_cache/v/cache/lastfailed`、`.pytest_cache/v/cache/nodeids.backup`、その他のファイルは拒否する。
- 既存の `phase175_r3r12_hopf_conclusion/` のみを従来どおり許容する。
- キャッシュの改変が観測された場合、`report.json` の `preflight.tracked_dirty_pytest_cache` に明記する。黙って追跡差分を復元・破棄しない。
- `git diff HEAD --name-only` による未コミット追跡変更チェック、ブランチ、祖先 HEAD、18件の Source PIN、文献の位置・型付きチェックは保持する。
- Source-first、First Successful Proof Search を維持する。目標 $\pi_9^5$ の直接 GIVEN や専用証明を追加しない。
- 本実行 Gate は従来どおり `PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE`。全体 pytest は Phase 175 終了時のみ実施。

### 検証

作成環境で R4 監査契約の限定 pytest は **22 passed**。Windows 側の既存 R34 出典テスト・実群検索は実行ログが揃うまで未確認とする。失敗を取り繕う自動 `git restore`、Git コミット、追跡コード改変は行わない。


## 7. R4R2 — R3 で更新された共有証明ソースの PIN 系譜補正（2026-11-17）

### 実測された不一致

ユーザーの R4R1 DryRun は限定 pytest **29 passed** の後、`R4_SOURCE_PIN_DRIFT: phase165_r52_r9_shared_math.py` で停止した。R1/R2 監査の18件の固定 Source PIN と現在の GitHub `develop` を全件照合した結果、違いはこの1件のみ。R1 の Phase 174 基準 `4f87fc5722e85f7365250c07e684e959b71ae8bb` では blob `9fa11b383812570fae1a26868c98992a5934a327`、R3 引き継ぎ HEAD `a1ce1558be6bab647c5d23d26047b9cce45d4e2e` では blob `ee1efa2d91df479168b7b964d24e814e0f516449`。GitHub の現行 HEAD `c77a26fdebe0eead67f1f7dad3a469aa446b134f` でも R3 と同じ blob だった。

### 変更対象と追加位置

1. `phase175_r4_pi95_audit/audit.py`：定数 `REVIEWED_R3_SOURCE_PATH`、`REVIEWED_R1_SOURCE_BLOB`、`REVIEWED_R3_SOURCE_BLOB` を既存の `TRACKED_PYTEST_CACHE_FILE` の直後に新規追加。`reviewed_source_pins()` を既存の `validate_dirty_paths()` の直後に新規追加。`preflight()` を関数全文置換し、この関数を呼び出したうえで、レポートに R1→R3 の移行情報を追加する。import は変更しない。クラス変更なし。
2. `phase175_r4_pi95_audit/tests/test_audit.py`：テストファイル末尾に `test_reviewed_r3_source_pin_transition_is_exact_and_nonmutating()` と `test_reviewed_r3_pin_rejects_drift_without_loosening_other_guards()` を新規追加。既存テスト・import は不変。
3. `README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md`（日本語）：今回の実測結果と補正方法を追記し、ファイル全体を再出力する。
4. `run.ps1`、`__init__.py` は変更しない。既存本番コード・既存テスト・ルート主要5文書も変更しない。

### fail-closed 条件

- R1 の本来の `SOURCE_BLOBS` で当該パスが旧 SHA と厳密一致すること。基点が改ざんされていれば停止。
- `git rev-parse a1ce1558be6bab647c5d23d26047b9cce45d4e2e:phase165_r52_r9_shared_math.py` が新 SHA と厳密一致すること。監査担当が作った期待値だけで現在の差分を無条件に認可しない。
- 既存の R3 HEAD 祖先条件、ブランチ `develop`、追跡ファイル差分、他17件の Source PIN、採用 TeX・型付き出典・実群検索をすべて維持する。
- R3 の更新を認めるのはこの1パスだけ。ローカルで別の内容に変更した場合、および追加の未レビューコミットによる差分は `HEAD:path` 検査で拒否する。
- 新規 GIVEN、一般数学規則、専用 ProofStep、Narrative、完全証明の宣言は0。全体 pytest は Phase 175 の最後のみ。

### 終了条件・境界

DryRun の期待 Gate は `PASS_R4_AUDIT_ONLY_DRYRUN`。本実行の期待 Gate は `PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE`。いずれも実際の Windows ログ確認前には PASS と断定しない。R4R2 は監査前の Source PIN 識別誤りを直すだけで、$\pi_9^5$ の数学的根拠や Proof Search を変更しない。
