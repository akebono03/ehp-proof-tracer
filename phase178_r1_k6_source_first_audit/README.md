# Phase 178 R1 — 6-stem Source-first Audit

監査専用。現行 develop の HEAD `15c1efad5003002137243daef6e8771191f63579` を固定する。本番コード、公式文書、既存テスト、数学的 GIVEN は変更しない。

対象は `data/sphere.csv` の登録済み非安定6-stem 6群のみ。安定範囲の313群、その他の非安定512群は個別探索しない。対象群の内部探索に必要な先行結果の利用は許す。DryRun は探索・pytest を実施しない。本実行は各対象について公開 Web 経路を一度呼ぶ。探索の途中に実際に観測された候補を保存し、未到達と候補なしを区別する。partial の証明木は Web Trust Boundary による完全証明の認定ではない。complete は実際の Web verifier 通過、対象直接 GIVEN 不在、未解決 Goal 0 等を確認する。

Toda の採用 TeX `sources/toda/Toda_05_2.tex` の (5.12)、Lemma 5.10、Proposition 5.11、(5.13) の位置を記録する。原著の独立照合ではない。GIVEN の一覧は選択した locator の一致を記録するものであり、数学的な適用可能性の認定ではない。実際の探索候補は別に記録する。(5.13) は Prop 5.11 の証明途中に出現するため、同じ命題の証明に独立した先行 GIVEN として循環使用しない。

`%LOCALAPPDATA%/EHPProofTracerAudit/phase178_r1_k6_source_first_audit/attempt_*` に report.json、各群の詳細 JSON、限定 pytest ログを保存する。timeout は各対象180秒（`-Timeout` で変更可能）。失敗を未完成と混同しない。未完成候補の順序は n の昇順、最終対象は詳細と出典の監査後に決める。全体 pytest は実行しない。限定 pytest は既存の再帰探索および First Successful Proof Search の合成テストのみ。

実行：`powershell -NoProfile -ExecutionPolicy Bypass -File .\phase178_r1_k6_source_first_audit\run.ps1 -DryRun`、次に `-DryRun` を外して実行する。
