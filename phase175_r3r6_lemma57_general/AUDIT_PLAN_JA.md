# Phase 175 R3R6 — Toda Lemma 5.7 の一般命題と型付き推論

## 経緯・範囲

R3R5 の実測は `EHP_EXACTNESS=INFERRED`、`LOWER_PI62_GROUP=INFERRED`、`ZERO_GENERATOR_IMAGE=UNRESOLVED`、`ZERO_SUSPENSION_IMAGE=UNRESOLVED`、`HOPF_INJECTIVITY=UNRESOLVED` であった。次に必要なのは `E(η₂◦ν′)=0` を出典のある一般規則から導くことである。

Toda Lemma 5.7 は一般的に、$\alpha\in\pi_i(S^3)$ に対し

$$
E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5)
\quad\Longrightarrow\quad E(\eta_2\circ\alpha)=0
$$

を述べる。今回の登録はこの **一般条件式** のみであり、特例 $E(\eta_2\nu')=0$ を新規 GIVEN として直接注入しない。

## 変更一覧（全て新規、リポジトリ直下）

- `phase175_r3r6_lemma57_general/source.py`：`TodaLemma57GeneralCriterion`、`verify_lemma57_manifest`、`build_isolated_lemma57_source`、`merge_isolated_cited_source`。
- `phase175_r3r6_lemma57_general/rule.py`：`TodaLemma57DoubleSuspensionMembership`、`lemma57_criterion_inputs`、`lemma57_zero_generator_rule`、`expand_cited_lemma57_zero_generator`。
- `phase175_r3r6_lemma57_general/audit.py`：`latest_r3r5_report`、`inspected_general_criterion`、`launch_worker`、`worker`、`write_report`、`run`、`main`。
- `phase175_r3r6_lemma57_general/tests/test_source.py`、`tests/test_rule.py`、`tests/test_audit.py`：各テスト関数全文。
- `run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`。

既存コード・既存クラス・既存関数・既存 import は変更しない。新規クラス・関数は上記それぞれのモジュールに新規追加する。一般規則は孤立監査でのみ有効となり、公開 Provider には先取りして接続しない。

## Source-first と安全条件

1. Toda 第 V 章の Git blob `579661138928499ba04a51327f686d9b971b5314` と Lemma 5.7 の一般条件を照合する。
2. Phase 163 の順序付き manifest を検証する。Lemma 5.7 は 9100、Proposition 5.8 は 9200、原文抜粋の SHA-256 は `01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c`。
3. R3R5 正常本実行の証拠を要求する。DryRun の記録、追加 GIVEN を含む記録、前提が変化した記録は拒否する。
4. R3R5 の Source Guard と R3R4 の Git 履歴・作業ツリー保護を再利用し、監査前後の状態を比較する。
5. 実際の既存 `π₆²` 生成元を使って `GeneratorImage` の型を検査する。`η₂` の同一性は型付きの登録済み ID を検証し、任意の別元素を同一視しない。
6. `TodaLemma57GeneralCriterion` の出典付き GIVEN に加え、`TodaLemma57DoubleSuspensionMembership(α)` の **INFERENCE** を必須とする。後者を登録済み事実・データベース結論・テスト用の模擬 Step で置き換えない。
7. 公開 Proof Search、Renderer、Web、既存推論規則、既存証明データベースは変更しない。既存プロジェクト全文 pytest は実行しない。

## 検証する実測事項

- `PHASE175_R3R6_GENERAL_SOURCE=PASS`：一般命題の出典、順序、引用を検証。
- `PHASE175_R3R6_DOUBLE_SUSPENSION_MEMBERSHIP=`：$E^2\nu'$ の包含条件を既存規則から導けるか。
- `PHASE175_R3R6_LEMMA57_ZERO_GENERATOR_IMAGE=`：一般規則と独立前提から $E(\eta_2\nu')=0$ を導けるか。

Source Guard や型の整合性違反を検出した場合、Gate は FAIL とし、報告を `%LOCALAPPDATA%` に残す。未完成の証明探索そのものは Open Goal として記録する。

## 完了条件と次工程

DryRun：`PASS_R3R6_READ_ONLY_DRYRUN`。本実行：`PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED`。後者は**証明完成を意味しない**。次の R3R7 では $E^2\nu'=2\iota_5\circ E\nu_4$ の出典付き導出を確認し、包含条件の推論を一般規則で接続する。全体 pytest は Phase 175 終了時のみ。

## R3R6R1：Windows UTF-8 読込エラーの限定修正

Windows Python 3.10 上の R3R6 初回 DryRun では、限定 pytest が `54 passed, 1 failed` で停止した。失敗箇所は**既存の** `phase175_r3r5_pi73_lemma57_frontier/tests/test_audit.py::test_report_written_outside_source_tree` である。出力された `report.md` は UTF-8 だが、テストは `Path.read_text()` を `encoding` 未指定で使用したため、Windows の既定文字コード `cp932` で復号し `UnicodeDecodeError` を起こした。

変更対象は次の2ファイルのみ（文書更新を除く）。

- `phase175_r3r6_lemma57_general/run.ps1`：`$ErrorActionPreference` 直後に `PYTHONUTF8=1` と `PYTHONIOENCODING=utf-8` を設定する。既存 pytest コマンド、監査起動、Git 検査と戻り値判定は変更しない。実行は子 PowerShell のためユーザーの親セッションには影響しない。
- `phase175_r3r6_lemma57_general/tests/test_powershell_utf8.py`：既存テストへ変更を加えず、設定順序と UTF-8 実読込を検証する新規テスト2件を追加する。

既存ファイル・既存テスト、Toda 出典、一般推論、GIVEN、共有 Provider、公開 Web、Phase 175 の他の監査コードは**変更しない**。再実行は R3R6 だけの限定 pytest と監査に限り、Phase 終了前の全体 pytest は行わない。

R3R6R1 の成功条件：既存 R3R5 回帰テストを含む限定 pytest PASS、Source Guard PASS、Lemma 5.7 出典検査 PASS、DryRun PASS、本実行が未解決 Goal を正直に報告すること。数学上の完了判定は元の R3R6 と同一である。

## R3R6R2（2026-11-16）— R2→HEAD の Git 監査履歴の追加許可

ユーザーの Windows 実行では、R3R6R1 の限定 pytest は **57 passed** となり、UTF-8 の不具合は解消した。一方、DryRun は `R3_R2_LINEAGE_NOT_AUDIT_ONLY` で停止した。原因は R3R6 が R3R5 の `scoped_preflight()` を通して R3R4 版の `verify_lineage()` を使用しており、後続 R3R5 パッケージの Git への追加を許可していないこと。

変更は R3R6 パッケージ内の `audit.py` と新規 `tests/test_lineage.py` のみ。旧 R3R5 の `scoped_preflight()` を直接再利用する代わりに R3R6 内で次を実行する。

1. 既存 R3 `preflight` により R1/R2/本番 Source Guard と作業ツリー監視を維持。
2. 既存 R3 `select_r2_report` と `validate_r2` で R2 の正常実行証拠を再検証。
3. R2 の記録 HEAD が現 HEAD の祖先であることを検査する。
4. 祖先から HEAD までの差分が追加（`A`）だけであり、R2 の監査ディレクトリ、R3・R3R5・R3R6 の**列挙済み監査ファイル**に限定されることを検査。その他は拒否。
5. 旧 R3 の許可リストと完全一致することを検査してポリシーのドリフトを拒否。
6. R3R5 の `verify_reviewed_toda_source()` を従来どおり実行し、実行後も同じ監査を再実施。

本番コード、数学的推論、既存の GIVEN、共有 Provider、Web Renderer、旧 R1/R2/R3/R3R5 パッケージは変更しない。`tests/test_lineage.py` は一時 Git リポジトリで、許可された新規監査ファイル、予期しないファイル、実装ファイル変更、削除、移動、HEAD 改変を検査する。

### 完了条件

- Windows DryRun：`PHASE175_R3R6_SOURCE_GUARD=PASS`、`PHASE175_R3R6_R2_LINEAGE=AUDIT_ONLY_DESCENDANT`、`PHASE175_R3R6_GATE=PASS_R3R6_READ_ONLY_DRYRUN`。
- Windows 本実行：`PHASE175_R3R6_DOUBLE_SUSPENSION_MEMBERSHIP` と `PHASE175_R3R6_LEMMA57_ZERO_GENERATOR_IMAGE` を個別に記録し、`PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED` に到達。
- `UNRESOLVED` なら証明未完成。次の R3R7 は必須前提 $E^2\nu'=2\iota_5\circ E\nu_4$ の一般規則・出典接続を検討するが、この R3R6R2 では先取りしない。
- Phase 175 全体 pytest は終了時のみ実施。
