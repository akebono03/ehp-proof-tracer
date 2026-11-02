# Phase 173 R1 監査仕様

## 目的

$n\ge3$ の登録済みホモトピー群 $\pi_{n+k}^{n}$ について、現行の Backward Search（後向き証明探索）と Web Trust Boundary（完成証明の公開前検証）を変更せず再実行し、証明能力の実測状況を記録する。

## 調査した既存実装

- `phase171_r1_n3_registered_audit/audit.py` と `tests/test_contract.py`：既存の $n=3$ 全34群監査と契約テスト。
- `phase170_r3_r8_n2_exhaustive_audit/audit.py`：独立 Worker（検査対象ごとの隔離実行）と群の重複排除。
- `phase165_r55_nk_only_goal.py`：登録済み証明目標と検索 API。
- `phase165_r52_partial_proof.py`：証明探索結果と `ProofSearchStatus`。
- `phase165_r52_r9_shared_math.py`：共有の型付き Bridge。
- `phase169_r10e4_ordered_db_prior/db_prior.py`：登録済み先行 DB 結果。
- `phase168_r3_4_link_bridge.py`：ProofStep に結び付いた文献引用のモデル。
- `web_group_proof.py`：標準 Web 完成証明経路。
- `data/sphere.csv`：明示された $n\ge3$ の登録群797件。

現行 GitHub `develop` の HEAD は `11ea331f322883e2f2cf34b9e865dea2134f5058`。Phase 172 の文書更新・終了処理用ディレクトリは GitHub 上に反映されている。ローカル HEAD は実行時に確認する。

## 今回の追加ファイル・変更単位

既存ファイル、クラス、関数、メソッドは変更しない。

- `phase173_r1_nge3_audit/audit.py`：新規監査モジュール。全 import、関数本体は `CODE_FULL_JA.md` に全文掲載。
- `phase173_r1_nge3_audit/run.ps1`：新規 PowerShell 実行スクリプト。全文掲載。
- `phase173_r1_nge3_audit/tests/test_audit.py`：新規限定契約テスト。全 import、テスト関数を全文掲載。
- `phase173_r1_nge3_audit/__init__.py`：新規パッケージ識別ファイル。
- `phase173_r1_nge3_audit/README.md`：新規英語 README。
- `phase173_r1_nge3_audit/AUDIT_PLAN_JA.md`：本仕様。
- `phase173_r1_nge3_audit/CODE_FULL_JA.md`：新規コードとテストの全文。

## 範囲

最初の `-Scope priority` は $(n,k)=(3,0),\ldots,(3,33)$ および $(4,3),(5,3),(6,3),(7,3)$ の38群を対象とする。後四者は $\pi_7^4,\pi_8^5,\pi_9^6,\pi_{10}^7$ に相当する。 `-Scope all` は `sphere.csv` に明示された797群すべてを対象とする。優先監査の未選択759群は未監査と明示する。

## 判定条件

完成・Web検証済みの条件は以下の論理積。

1. `exact_prior_database_result(n,k)` が型付き DB 群構造を返す。
2. `search_group_from_registered_goal` が `complete`、証明の根と DB Goal が一致する。
3. ProofStep が1件以上、Open Goal が0件。
4. 既存の検証対象 Bridge に結び付いた Narrative Model の Reference が生成可能である。
5. 標準 Web 経路が `generic-complete-proof`、`partial_result=False`、表示 Step と行数が正でエラーなし。

`search_failed` や `partial` は実測結果のまま保存し、完成へ昇格させない。証明未完成は監査の正常な観測結果であり、Worker 例外・タイムアウトと区別する。

## テストと完了条件

限定 pytest：

```powershell
python -B -m pytest -q --disable-warnings -p no:cacheprovider .\phase173_r1_nge3_audit\tests\test_audit.py
```

作成環境の独立したテストでは22 PASS。これは既存 GitHub リポジトリ全体および実際の証明検索を走らせた結果ではない。利用者の Windows 実行結果によって、証明状態・引用・Web 成否を確定する。

`-DryRun` の完了条件：限定 pytest PASS、対象 Git/DB の preflight PASS、tracked 変更なし。

通常監査の完了条件：選択範囲の全件が検査され、`audit.json`・`audit.md` が生成され、Worker 失敗ゼロ、tracked 変更なし。未完成群は R2 に引き継ぐ。

**Phase 173 R2 以降との境界：** 今回は Subgoal を収集するだけで、その解決規則・新規 GIVEN・新規 DB レコード・レンダラー変更を加えない。全体 pytest は Phase 173 の正式終了時のみ行う。
