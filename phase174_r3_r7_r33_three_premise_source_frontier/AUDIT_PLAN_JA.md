# Phase 174 R3-R7-R33 — 下側 Δ の三前提・公開接続監査

## 変更対象（最初に列挙）

既存ファイル・クラス・関数・メソッド・import は変更しない。新規追加位置はリポジトリ直下 `phase174_r3_r7_r33_three_premise_source_frontier/` のみ。

- 新規 `source_contract.py`: `SourceEvidence` クラス全文、`inspect_prior_three_clauses()` と `classify_three_premises()`。
- 新規 `audit.py`: `git()`, `git_blob_sha()`, `matches_blob_pin()`, `canonical_sha256()`, `verify_checkout()`, `inspect_registered_frontier()`, `report()`, `main()`。
- 新規 `tests/test_source_contract.py`: 出典の順序、文言・境界の改変拒否、3前提の欠落検出。
- 新規 `tests/test_audit.py`: 実 GitHub 整合性、実 Toda 文献、実 DB prior と公開葉の照合。
- 新規 `run.ps1`: DryRun / 通常監査 / 限定 pytest を分ける。
- 新規 `README.md`、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`IMPORTS_FULL.txt`、`CODE_FULL_JA.md`。

## 数学的な依存条件

$\Delta:\pi_{11}^{11}\longrightarrow\pi_9^5$ の核を計算するには、次を独立に立証する必要がある。

1. 一般の対角群 $\pi_{11}^{11}=\mathbb Z\{\iota_{11}\}$。
2. Toda Proposition 5.8 の $\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$。
3. Toda (5.10) の $\Delta(\iota_{11})=\nu_5\eta_8$。

この3つの**一致する型付き証明**があれば、一般的な準同型の核計算から $\ker\Delta=\langle2\iota_{11}\rangle$ が従う。しかし現状の R32 は条件の妥当性を確認しただけで、公開 Verified Proof Tree の証明ではない。

Toda Proposition 5.9 の証明中に現れる核の結論は、今回の前提として GIVEN 登録しない。

## 検査対象

- 文献: `sources/toda/Toda_05_2.tex` の一般対角式、Proposition 5.8、(5.10)、Proposition 5.9 の位置。
- 公開供給: `phase165_r52_r9_shared_math.py`、`phase169_r10e2_unpositioned_citation/source_first.py`。
- DB prior: `phase169_r10e4_ordered_db_prior/db_prior.py` の `exact_prior_database_result(5,4)` と `precedes_db_goal(5,4,7,5)`。DB prior は独立した文献出典ではない。
- 型検査: R32 `kernel_contract.py` で実 DB prior の**現物の生成元型**を受理できるか。生成元を架空の HomotopyElement にすり替えない。
- 否定検査: 下側の Δ の核や根 $\pi_{12}^{7}=0$ を直接 GIVEN として供給していないか。

GitHub `develop` の対象コードと関連テストを調査したうえで、対象の blob SHA および R31/R32 の実行済ファイル SHA256 を固定する。GitHub が R32/R32R1 の監査ファイルだけで進んだ場合は、変更経路と SHA の双方を照合する。未知の本番コード変更は拒否する。

## Gate と完了条件

- Source Guard=PASS、三前提の文献の掲載順序が一致。
- DB prior のグループ・位数・先行条件が正しく、型の差があればそのまま記録される。
- 公開の三前提証明葉の実数が記録され、直接核／根の GIVEN はゼロ。
- 限定 pytest PASS。全体 pytest は Phase 174 最終時のみ。
- `PASS_R33_INDEPENDENT_THREE_PREMISE_FRONTIER_AUDITED_SOURCE_WIRING_PENDING`。これは核や根の証明完成を示さない。

## 次工程との境界

R34 以降で、文献に位置づけられた一般・既知の構造を **source-checked** に型付き登録し、一般推論規則のみで証明連鎖へ接続できるか検討する。R33 で登録・実装を先取りしない。
