# Phase 165 R6-2 R4-R10 監査仕様

- 対象: `pi_4^3` の共通 Backward Search の Root Candidate。
- 比較: 完全な文献 Bridge と、共有証明経路のスクリーニング後の Bridge。
- 計測: Provider が返す Rule と Subgoal、前提に対応する ProofStep、Forward Match 件数、解決/未解決の通知。
- 正規探索器の検証ロジックは改変しない。実行時に照合関数を観測用にラップし、`finally` で戻す。
- 本番コード、Reference、規則は変更しない。個別候補の限定は監査実行の中だけで用いる。
- 完了条件: 生成候補と採用失敗の段階を分類できる JSON を保存し、対象テストに合格すること。
- 次 Phase 境界: 原因に対応した本番修正は本監査に含めない。
- 全体 pytest は Phase 165 の最後に限る。
