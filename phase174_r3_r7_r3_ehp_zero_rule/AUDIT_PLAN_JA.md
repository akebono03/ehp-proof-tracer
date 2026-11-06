# Phase 174 R3-R7-R3 実装・監査記録

## 前提の確認

- 前工程 R3-R7-R2 は DryRun と本実行で PASS、限定 pytest 50件 PASS。
- $\pi_{12}^{7}=0$ の既存 Root 候補は 0 件、$\Delta$ 全射性候補は 0 件。
- EHP 完全列の隣接する 2 つの型付き Window には、現行の逆向き推論候補が各 1 件存在する。
- $\pi_{12}^{13}=0$ には Toda (5.1) による候補が 1 件存在する。
- $\pi_{11}^{6}$ は `search_failed`、Open Goal 2 件。
- GitHub `develop` の監査基準 HEAD：`c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c`。

## 変更対象

新規ディレクトリ `phase174_r3_r7_r3_ehp_zero_rule/` のみ。

- `rule.py`：`ehp_zero_inputs`、`ehp_zero_from_delta_surjectivity_rule`、`expand_ehp_zero_from_delta_surjectivity` を新規追加。
- `audit.py`：Source Guard、前工程 JSON 検査、孤立した Root 候補の監査。
- `tests/test_rule.py`、`tests/test_audit.py`：専用の限定テスト。
- `run.ps1`：`--import-mode=prepend` で限定 pytest と DryRun／本監査を実行。
- `README.md` は英語。その他の本監査資料は日本語。

既存の `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` は変更しない。

## 一般推論規則

群の同型そのものを結論として仮定しない。次の条件からのみ零群を導く。

$$
A \xrightarrow{\Delta} B \xrightarrow{E} C \xrightarrow{H} D,
\quad \operatorname{im}(\Delta)=\ker(E),
\quad \operatorname{im}(E)=\ker(H).
$$

$\Delta$ が全射で $D=0$ のとき、$E=0$ かつ $E$ は全射なので $C=0$。

この規則は `TodaPrimaryGroupZeroStatement` の具体的な二つの整数次元から一般的に Window を生成する。対象群の添字、stem、生成元名による専用分岐はない。

## 認証境界

`GoalExpansion` は証明候補であり、Verified ProofStep ではない。
既存 `shared_expansion_provider` は変更しない。配備用 Provider や Web には接続しない。
$\Delta$ 全射性は前工程で候補 0 件のため、目標群の完成を宣言しない。

## 実行と合格条件

PowerShell の `run.ps1 -DryRun` と `run.ps1` を実行。前工程 JSON の Gate と候補数を検証し、Root 候補を1件提案して4つの子 Goal を確かめる。
限定 pytest のみ実行。全体 pytest は Phase 174 最終 Gate まで保留。

## 次工程との境界

R3-R7-R4 は $\Delta$ の全射性を出典優先で導く経路と、$\pi_{11}^{6}$ の型付き未解決 Goal を調査する。Isomorphism（同型性）が全射性に依存する場合、その同型性候補を全射性の独立根拠としない。
