# Phase 175 R4R12R8 — Δ の生成元像 Source-first 監査

## 目的

以下の等式について採用 Toda TeX の明示性と既存の型付き規則との境界を監査する。

$$
\Delta:\pi_{10}^{9}\longrightarrow\pi_{8}^{4},\qquad
\Delta(\eta_9)=E\nu'\circ\eta_7.
$$

## 出典

- `sources/toda/Toda_05_2.tex`：Chapter V, Proposition 5.8 の証明。
- 同 (5.8)：$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$。
- 同 Proposition 2.5：合成と $\Delta$ の関係。適用には条件を監査する。
- 同 (5.11)：目的等式が明示されている。
- 原著印刷版の独立照合は未実施。

## 数学的監査

$$
\begin{aligned}
\Delta(\eta_9)
&=\Delta(\iota_9)\circ\eta_7\\
&=\pm(2\nu_4-E\nu')\circ\eta_7\\
&=\pm\left(\nu_4\circ(2\eta_7)-E\nu'\circ\eta_7\right)\\
&=E\nu'\circ\eta_7.
\end{aligned}
$$

最後の等号は、$2\eta_7=0$ と $E\nu'\circ\eta_7$ の位数が 2 以下であることを含む。符号の省略を無条件に許さない。$\eta_9=E^2\eta_7$ と Proposition 2.5 の適用条件も別途型付きで確認する。

## 実装境界

- 新規 GIVEN：0件。
- 新規数学規則：0件。
- 既存 Proof Search、DB、Narrative Renderer、Web：変更なし。
- 実行するのは採用 TeX の形式的マーカー、既存監査コード／規則の形、Git 履歴の確認のみ。
- 今回の PASS は型付き証明が完成したことを意味しない。

## 変更ファイル／関数

- 新規 `phase175_r4r12r8_delta_generator_source_audit/audit.py`：`git`、`verify_repository`、`normalized`、`single_segment`、`inspect_source`、`inspect_existing_rule`、`build_report`、`main`。
- 新規 `tests/test_audit.py`：4テスト関数。
- 新規 `__init__.py`、`run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

## 完了条件

限定テスト PASS、DryRun／本実行 PASS、採用 TeX で (5.8) と (5.11) を確認し、推論上の未解決義務を JSON に記録する。全体 pytest は Phase 終了時まで実行しない。
