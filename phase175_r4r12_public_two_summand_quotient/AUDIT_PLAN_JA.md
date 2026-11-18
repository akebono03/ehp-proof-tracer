# Phase 175 R4R12 監査・実装計画

## 目的

R4R11 の出典付き (5.8)・Proposition 2.5・符号正規化を維持しつつ、R4R3 に既存の「階数2の基本 2-群の商」一般規則を共有 Proof Search に接続する。Toda (5.8) の再証明、直接の結論 GIVEN、専用 Narrative、追加の数学規則は行わない。

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` だけを、既存関数全文単位で更新する。import 変更なし。
- 新規 `phase175_r4r12_public_two_summand_quotient/provider.py`：`ordered_summand_inputs()`、`expand_public_two_summand_quotient()`、`build_public_two_summand_quotient_provider()` を新設。
- 新規 `installer.py`：`git()`、`git_blob_sha()`、`function_replacement()`、`plan()`、`install()` を新設。変更後の関数およびモジュール全文を監査出力する。
- 新規 `audit.py`：`git()`、`preflight()`、`validate_prior()`、`find_prior()`、`inspect_public_root()`、`report_folder()`、`run()`、`main()` を新設。
- 新規 `tests/test_provider.py`、`tests/test_installer.py`、`tests/test_audit.py`：各テスト関数全文を収録。
- 新規 `run.ps1`、本 README、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`。

## 数学的根拠と厳格な境界

R4R3 の既存一般推論規則の条件は次のとおり。

$$
C=\mathbb Z/2\{z\},\quad
A=\mathbb Z/2\{a\}\oplus\mathbb Z/2\{b\},
$$

$$
C\xrightarrow{\Delta}A\xrightarrow{E}B,
\qquad \operatorname{Im}\Delta=\ker E.
$$

別途、$E$ の全射性、$\Delta(z)$ が $A$ の一方の生成元であること、他方の生成元の $E$-像が $y$ であることが**証明された場合にだけ**、$B=\mathbb Z/2\{y\}$ を導出する。

`exact_prior_database_result()` は群の候補を読み出すが、`ProofStep` を返さない。R4R12 は $\Delta(z)$ の値を選ばず、両方の条件付き候補を残す。各候補の6つの `subgoals` は共通検索器が判定する。`(n,k)=(5,4)` は実環境の監査例であり、規則本体は特定の次元・文字列表記に依存しない。

## 出典・履歴監査

- GitHub `develop` のレビュー済み HEAD `abf619040d52aa9fd61c5bca60db81e28912e24d`、ブランチ、追跡ファイル変更範囲を照合。
- R4R3 ルール、共通 `CyclicStructureStatement`、DB prior、一般 map 型を Git blob で固定。
- 未コミットの先行 R4R11R2 数学・監査モジュールの内容を固定。
- 先行 R4R11 本実行 Gate と Source-first 証拠を厳格に要求。
- 前インストーラーで完全に検証した現在の `shared_expansion_provider()` だけを変更。
- 変更後の import は既存どおり。既存 API や共通 Renderer は変更しない。

## 検証・完了条件

新規テスト、既存 R4R3・R4R10・R4R11・R4R5 の関連限定 pytest が PASS。DryRun では本番コードを書き換えず、変更後全文を出力。本実行で R4R3 の一般規則名を持つ root candidate を共有 Provider が返すことを検証。

DryRun Gate：`PASS_R4R12_TWO_SUMMAND_QUOTIENT_DRYRUN`

本実行 Gate：`PASS_R4R12_TWO_SUMMAND_QUOTIENT_ROOT_CANDIDATE_PI95_PENDING`

これは root candidate の存在を認証する Gate であり、完成証明の Gate ではない。$\pi_9^5$ は未完成のまま。全体 pytest は Phase 175 最後まで実行しない。

## 次の境界

R4R13 以降：R4R11 が提案する無符号 $\Delta$ 関係（推論候補）から、必要な `GeneratorImage` を独立に導く一般規則、命名／構造正規化、$E$ 全射・生成元像の前提の証明経路を監査する。先行結果を再探索したり、結論を直接 GIVEN にしない。
