# Phase 165 R5-R14 監査範囲

対象：旧 Phase 162 Web Narrative、旧 R3 Narrative、Proof Chain Renderer、Concrete Transport Renderer。

本番コード・監査スクリプト・テスト・ファイル内部からの直接呼出を区別する。AST による静的検査のため、外部 API や動的 import の不在は証明しない。

R5-R11 の EHP 共通入力と互換 import を必須条件とする。旧 Phase 162 fixture の6件の失敗は解決しない。全体 pytest は Phase 165 の最後まで行わない。
