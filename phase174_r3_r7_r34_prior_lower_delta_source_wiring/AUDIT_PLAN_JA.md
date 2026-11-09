# Phase 174 R3-R7-R34 — 前提2件の出典付き公開接続

## 変更対象（実装前に明示）

既存コードで置換するのは次の関数のみ。

- `phase165_r52_r9_shared_math.py`: `build_shared_typed_bridge` 内の source 登録部分のみ。`register_positioned_prop27` の直後へ `build_cited_lower_delta_sources` の import と sources 追記を追加する。

新規追加（リポジトリ直下の `phase174_r3_r7_r34_prior_lower_delta_source_wiring/`）：

- `source.py`: `git_blob_sha`、`pinned_source_text`、`reviewed_source_positions`、`checked_prior_statements`、`build_cited_lower_delta_sources`。
- `install.py`: `git`、`reviewed_remote_head`、`patch_source`、`expected_source_bytes`、`preflight`、`install`、`main`。
- `audit.py`: `screen_report`、`report`、`main`。
- `tests/test_source.py`、`tests/test_install.py`、`tests/test_public.py`、`tests/test_static_helpers.py` のテスト関数全体。
- `run.ps1`、この README、監査計画書、変更コード全文、import 全文、検査記録。

既存クラス、既存テスト、主要5文書、共通 Renderer、一般推論規則は変更しない。

## 証拠と数学的境界

出典優先で、Toda Proposition 5.8 の

$$\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$$

および、先行する式 (5.10) の

$$\Delta(\iota_{11})=\nu_5\eta_8$$

だけを、出典付きの独立した既知前提として登録する。これらは Proposition 5.9 の証明で導出する核や群の結論そのものではない。

源泉の検査は① `Toda_05_2.tex` の確認済み Git blob、② Proposition 5.8・(5.10)・Proposition 5.9 の原文上の順序、③ Manifest の文献ID・出典位置、④ `sphere.csv` と `HyoujiGen.csv` の実際の `Composition` の一致、の四層とする。DB prior は表示の検算に限り、文献の代替としない。

登録する型は、`Relation(TodaPrimaryGroup(9,5), FiniteCyclicGroup(2, Composition(...)))` と、`TodaDeltaImageUpToSignStatement`。後者は原文の正符号の等式より弱い主張であり、符号を捏造しない。

対角群 $$\pi_{11}^{11}=\mathbb Z\{\iota_{11}\}$$ の具体化は、既存の一般式 (5.1) からの INFERENCE で別途得る。R32 の `HomotopyElement` 限定契約は `Composition` を受け付けないため、核の一般推論は次工程で厳格な型検査のもと検討する。

## 実行／完了条件

- GitHub `develop` の確認済み履歴と、既存コードのハッシュ検査に PASS。
- 提示済み R30–R33 パッケージの実体を残す。
- 公開 Source-first 経路から新しい出典付き GIVEN 2件を確認。
- 下側核、Δ の全射性、根 $$\pi_{12}^{7}=0$$ を GIVEN として追加しない。
- 新規ルール追加0、共通Narrative変更0。
- 限定 pytest PASS。全体 pytest は Phase 174 の最後のみ。

予定 Gate: `PASS_R34_TWO_EARLIER_CITED_LEAVES_SCREENED_DOMAIN_AND_KERNEL_PENDING`。
