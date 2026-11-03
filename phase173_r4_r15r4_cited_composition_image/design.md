# Phase 173 R4-R15R4 — 出典付き生成元像の合成推論

## 目的と前段階

R15R3 は、$\pi_{34}^3$ の4生成元から4個の形式的懸垂像を構成し、まだ個別の記名等式が未証明であることを明示した（限定 pytest 36件 PASS）。R15R4 は記号の一致を証明に変換するのではなく、**既存の出典付き定義から個々の生成元像を確実に導出できた場合のみ**合成像を証明する共通規則を追加する。

今回の対象は $k=31$ 固有の規則ではない。一般の型付き合成 $f\circ g$ と $f'\circ g'$ に対し、双方の `GeneratorImage` の推論が既に成立するならば、懸垂の函手性によって

$$
E(f\circ g)=E(f)\circ E(g)=f'\circ g'
$$

を導く。**左右両方の `GeneratorImage` の証明を必須の前提**とし、未証明の因子が1個でもあれば導出しない。

## 文献と未証明部分

GitHub `develop` の `phase169_r10d2_general_family_definition/family_citation.py` は、出典付き系列の実例と `GeneratorImage` を別々の型付き推論として扱う。`phase169_r10e8_hyoujigen_generic_suspension/source_records.py` は Chapter VI の $\varepsilon_n$、$\bar\nu_n$、$\mu_n$ の出典位置を検証する。Chapter V には $\nu_n$、$\sigma_n$ の系列定義が登録されている。これらの源泉は本監査で再度照合し、`GIVEN` を新規作成しない。

$k=31$ の既存 CSV 候補では、$\pi_{34}^{3}$ 側に次の4個の生成元がある。

$$
\delta_3\sigma_{27},\quad
\varepsilon_3\nu_{11}\bar\kappa_{14},\quad
\nu'\varepsilon_6\bar\kappa_{14},\quad
\phi'\nu_{28}^{2}.
$$

$\pi_{35}^4$ にある対応候補は、それぞれ形式上 $\delta_4\sigma_{28}$、$\varepsilon_4\nu_{12}\bar\kappa_{15}$、$E\nu'\varepsilon_7\bar\kappa_{15}$、$E\phi'\nu_{29}^{2}$ である。$\delta$（HyoujiGen ID 88）と $\bar\kappa$（ID 56）の懸垂系列の定義は現状の引用済み定義として確立されていないため、CSV の同じ系列 ID だけでは証明しない。$\nu_{28}^{2}$ の合成像は、引用済み $\nu$ 系列の定義と形式的 $E\phi'$ を再帰的に組み合わせ、実際の ProofStep（証明ステップ）で検査する。

## 変更範囲

既存ファイル・クラス・メソッド・import の変更はない。新規ディレクトリ `phase173_r4_r15r4_cited_composition_image/` 内だけを追加する。

- `bridge.py`：`generator_image`、`factor_image_goals`、`expand_composed_generator_image` を新規定義。すべて型・次数を検査し、合成規則は `INFERENCE` 2前提を必須とする。
- `replay.py`：`cited_source_steps`、`replay_cited_image`、`replay_named_image`、`proof_tree_steps` を新規定義。文献の既存ビルダーに登録された `GIVEN` のみを取り込み、`find_inference_matches_for_rule` と `apply_inference_match` で実際に導出する。First Successful Proof Search に従い最初の成功を採用する。
- `audit.py`：`expression_atoms`、`atom_evidence`、`inspect_k`、`main` を新規定義。命名済み像を出典付きで再検証できた件数と、欠落した系列定義 ID を監査する。
- `preflight.py`：`git`、`verify_source_head`、`main` を新規定義。監査済み祖先 HEAD、更新許容範囲、レビュー済み Git blobs、先行段階のソース SHA-256 をチェックする。
- `tests/`：静的・独立の型付きテストと実リポジトリでの限定テストを新規追加する。
- `run.ps1`：ZIP 展開後、DryRun・通常実行で実施するスクリプト。

`SOURCE_CODE.md` は上記ソース・テスト・スクリプトの全文を含む。`README.md` は英語、その他のドキュメントは日本語である。

## 安全性と完了条件

- `run.ps1 -DryRun` で変更なしの Source Guard と独立テストが通る。
- 通常実行では限定 pytest のみ実行し、全体 pytest は Phase 173 終了時だけにする。
- $k=31$ の4個の左側生成元・4個の右側照合・4個の残差成分を維持する。
- 新しく認定する `GeneratorImage` は既存の文献引用または形式的像からの推論木を持つ。認定件数はログに実測出力し、予想値を事実として先取りしない。
- 新規 `GIVEN`、ターゲット群の結論の押し付け、公開 Provider・Renderer の変更、全群完成宣言をしない。

## 次工程との境界

R15R5 では R15R4 の監査レポートに残る $\delta$ と $\bar\kappa$ などの出典不足を検討する。出典を確認できない場合は、名称を推測せず未解決の Goal として保持する。群構造の完全証明と公開接続は、その後の段階で扱う。
