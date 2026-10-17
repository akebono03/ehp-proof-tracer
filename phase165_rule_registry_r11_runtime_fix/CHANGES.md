# Phase 165 R11 再修正

- `audit.py`: `main()` の誤った「shared provider が R8 規則発見を直接呼び出す必須条件」を撤廃。共通 Provider → generic provider → R8 discovery の経路を確認する。
- `test_audit.py`: `test_r11_shared_provider_may_not_call_discovery_directly()` を追加。既存監査テストも全体提示。
- `run.ps1`: 修正版を起動。監査終了コードが異常なら停止。
- 本番ソースと既存テストは変更しない。Phase 最終の全体 pytest は実施しない。
- 有効な規則供給経路の接続だけを検証し、数学的証明の完了や登録規則全体の網羅性は主張しない。
