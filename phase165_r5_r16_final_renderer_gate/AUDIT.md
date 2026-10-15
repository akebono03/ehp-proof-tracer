# Phase 165 R5-R16 判定方針

R5-R14 で17関数、テスト契約6件、アプリケーション直接参照1件が報告された。R5-R15 で旧 EHP 入力構築の重複部分は削除済み。

この段階で旧 Renderer の公開関数を機械的に削除すると既存テストと互換 API が破損する。したがって R5-R16 は公開正規経路の検証と、旧実装の残存を分離して最終判定する。

- `PUBLIC_PATH_UNIFIED_LEGACY_REMAINS`: 公開経路は正規化されているが旧定義が存在する。完全撤去とは判定しない。
- `PRECONDITION_FAILED`: R5-R11/R5-R15 の前提、正規公開経路、構文などに問題がある。
- `STATIC_RETIREMENT_CANDIDATE_NEEDS_RUNTIME_VERIFICATION`: 静的には対象定義がない。動的利用・外部契約は別途確認。

旧 Phase 162 fixture の既知の6件の失敗は未解決。監査でテストを削除・skip しない。全体 pytest は Phase 165 終了時のみ。
