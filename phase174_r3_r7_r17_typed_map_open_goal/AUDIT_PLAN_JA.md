# Phase 174 R3-R7-R17 実装・監査計画

## 監査前に確認した現行 GitHub

- リポジトリ: `akebono03/ehp-proof-tracer`、ブランチ `develop`。
- R16 反映後 HEAD: `388f63797a6aba61418bb93e734b8ce5999dc7f6`。
- R16 実行時のユーザー手元 HEAD: `e7bcd34a526b3f885a8e3be81c4aac362d8834c7`。
- HEAD 差分: `phase165_r52_r9_shared_math.py` の4行と R16 パッケージ。`web_group_proof_common.py` は変更されていない。
- 既存テスト: R16 公開 Root、R3 の一般 EHP 規則、Phase 173 共通未解決 Goal 表示を確認。

## 今回変更する対象

1. 既存ファイル `web_group_proof_common.py`
   - 既存関数 `_group_proof_statement_latex` の内部だけを置換。
   - 共通の `MapSurjective`、`MapInjective`、`MapIsomorphism` を型付き EHP 写像の数式に変換。
   - in-function import 変更後全文は `MODIFIED_FUNCTION_FULL_JA.md` に出力。
2. 新規ディレクトリ `phase174_r3_r7_r17_typed_map_open_goal/`
   - `patch.py`（ソース検査後の最小置換）
   - `audit.py`（Root / Delta / 循環依存と公開描画の検査）
   - `tests/test_patch.py`、`tests/test_audit.py`、`tests/test_public.py`
   - `run.ps1`、`README.md`、本ファイル、`CODE_FULL_JA.md`。

トップレベルの import、既存クラス、ほかの関数、探索規則、GIVEN 台帳、Narrative Renderer、既存 API は変更しない。

## 数学的責任境界

証明の目標は $\pi_{12}^{7}=0$。Root の一般 EHP 候補は1件で、独立前提として

$$
\Delta:\pi_{13}^{13}\longrightarrow\pi_{11}^{6}
$$

の全射性が必要。R16 の観測ではこの `MapSurjective` の公開候補は0件。
既存 `expand_generic_iso_goal` における `MapIsomorphism` は
`MapInjective` と `MapSurjective` の両方を要するため、独立した同型の証明がない限り
「同型だから全射」は循環した前提になる。この R17 では採用しない。

## 完了条件

- GitHub とローカルの lineage を厳格確認し、未知の tracked 変更を拒否。
- 上記関数以外の本番ファイルを変更しない。
- 未解決 Goal に `$\Delta: \pi_{13}^{13} \twoheadrightarrow \pi_{11}^{6}$` を表示。
- Root 候補1件、Delta 全射候補0件、検索未完成を維持。
- 新規数学規則・GIVEN・ProofStep を追加しない。
- 限定 pytest のみ実施。全体 pytest は Phase 終了時だけ。

## 次の R18 との境界

$\Delta$ の全射性を証明するには、$\pi_{11}^{6}$ の群構造・生成元像、
$E\pi_{10}^{5}=0$ と EHP 完全性の出典付き証明連鎖を別途監査・導入する必要がある。
候補を ProofStep として流用することはしない。
