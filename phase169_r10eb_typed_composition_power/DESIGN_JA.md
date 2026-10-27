# Phase 169 R10EB — 型付き連続合成の共通累乗表示

## 目的

R10EA 監査で証明と Trust Boundary が PASS であることを確認した。直和群の結論の `\nu_{30}\nu_{33}\nu_{36}` は、Proof Tree 上では型付き合成として扱われているものの、公開用表示では `\nu_{30}^{3}` に正規化されていなかった。

## 変更対象

- `phase168_r3_27_typed_statement_projection.py`：`element_tex()` 全体を置換。変更後の import は不変。
- `toda_human_readable_renderer.py`：`render_toda_expression_latex()` 全体を置換。変更後の import は不変。
- 新規 `phase169_r10eb_typed_composition_power/display.py`：`_composition_factors()`、`typed_stable_composition_power_latex()` を追加。
- 新規 `phase169_r10eb_typed_composition_power/patch.py`：安全な置換と完全関数出力。
- 新規 `phase169_r10eb_typed_composition_power/tests/test_r10eb_typed_composition_power.py`：表示互換性・型付き拒否・共通規則の検証。
- 新規 `phase169_r10eb_typed_composition_power/audit.py`：実証明を再探索し Trust Boundary と表示を監査。
- 新規 `run.ps1`：ブランチ／blob 照合、限定 pytest、監査、失敗時の原状復元。

## 数式表示の条件

同一 ID の `kinds=0` 系列の $r\ge 2$ 個の生成元を $\alpha_n,\alpha_{n+k},\ldots,\alpha_{n+(r-1)k}$ とする。各因子の型・始域・終域・添字・系列・無装飾性・正規登録名が `HyoujiGen.csv` の記録と一致し、$k>0$ かつ隣接次数が一致する場合に限り、$\alpha_n^r$ と表示する。

この関数は提示専用であり、$E(\alpha_n)=\alpha_{n+1}$ の証明、合成の性質、群の構造をデータから導出しない。

## 既存の表示との境界

- $\nu_n^2$、$\sigma_n^r$、$\eta_n^2$ の既存表示と、非正規表記の互換表示は維持する。
- 異系列の合成（例：$\eta_n\circ\varepsilon_{n+1}$）の一般表示、および長い逐次懸垂列の短縮・重複削除は次の表示 Phase に委ねる。
- `Proof Tree`、`Proof Narrative Model`、引用、検索、`Trust Boundary` に変更を加えない。

## 限定検証・完了条件

対象群 $\pi_{22}^{13}$、$\pi_{23}^{15}$、$\pi_{24}^{15}$、$\pi_{39}^{30}$ の既存完成証明を再探索し、Trust Boundary で全件 PASS を確認する。$\pi_{39}^{30}$ の公開群構造に `\nu_{30}^{3}` が現れること、限定 pytest の合格、既存 tracked 変更の保全を完了条件とする。

全体 pytest は Phase 169 の最後にのみ実施する。
